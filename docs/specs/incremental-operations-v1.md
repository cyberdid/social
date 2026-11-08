# Incremental Incident Operations v1

## Scope

`src.analysis.incident_ops` is a local, append-only snapshot registry for multiple Social incidents. It validates the existing `IncidentSpec` and `RunManifest` contracts, applies a UTC knowledge-time cutoff to EvidenceLedger JSONL, creates a deterministic run ID, and records explicit downstream invalidation candidates. It does not collect data, rerun analyses, write to a ledger, or update upstream manifests.

`src.analysis.report_diff` compares two report bundles produced by `src.analysis.report_generator`. It reports changes in finding text, kind, verification result ID, and cited evidence IDs. It does not establish that a later finding is true or that a changed citation semantically supports it.

## Snapshot semantics

- `IncidentSpec.as_of_utc` is the default cutoff. `--as-of` can supply another UTC timestamp without editing the source IncidentSpec.
- Imported JSONL is validated through `src.evidence_ledger.EvidenceLedger` before snapshotting. The known-time field is `created_at` from that append-only ledger. Event time, publication time, and the date mentioned by a source are not treated as the time Social learned the record.
- Records with known time after the cutoff are omitted from the snapshot evidence set. The snapshot records only an exclusion count, not future record IDs or contents. This count is generated during retrospective filtering and is an audit statistic, not information available in the historical view.
- A run-manifest source snapshot is eligible only when its explicit `fetched_at_utc` is at or before the cutoff. Missing or later fetch time is recorded only in an exclusion count. Task receipts are similarly included only when `attempted_at_utc` is at or before the cutoff.
- Stable `run_id` is `run-` plus the first 24 hexadecimal characters of SHA-256 over canonical incident inputs, eligible ledger rows, dependency edges, and eligible source/task provenance. Run lifecycle fields (`started_at_utc`, `finished_at_utc`, upstream `run_id`, and ineligible future manifest entries) are not identity inputs. The historical `run_provenance` excludes run lifecycle state. Current snapshot time and the upstream run ID/state/timestamps/manifest digest appear only in `capture_metadata.temporal_scope=snapshot_capture_context_not_historical_evidence`; they describe snapshot creation context and must not be read as what was known at the cutoff.
- Repeating an identical snapshot returns `reused: true` and does not rewrite the stored JSON. A changed evidence set, spec, dependency graph, model/policy/source snapshot hash, eligible task receipt, or eligible source snapshot produces a different stable ID. RunManifest output receipts are outputs of a prior run, so they are not treated as inputs to the identity key.
- Each case is stored under `<store>/<incident_id>/snapshots/<run_id>/snapshot.json`. `incident_id` follows the existing schema and is also checked as a safe single directory component. Snapshots created from a current ledger are labeled `retrospective_as_of_filter`; they reconstruct ledger knowledge time and do not claim to be a contemporaneous archive made on that date.
- Snapshots carry both an input fingerprint (recomputed from the IncidentSpec, eligible provenance, ledger rows, and dependency edges) and a canonical content SHA-256 for accidental-edit detection. Reuse, parent selection, and listing validate both, and require top-level `as_of_utc` to match `IncidentSpec.as_of_utc`. These are consistency/integrity checks, not signatures against a malicious writer who can rewrite the file and recompute its digest.
- An explicit EvidenceLedger `supersedes` reference on an assessment or verification record is retained in `correction_history`. The tool does not infer correction from similar wording or a newer timestamp.

## Dependency invalidation

Optional dependency JSON uses only explicitly supplied directed edges:

```json
{"edges": [{"from": "evidence-42", "to": "claim-8"}, {"from": "claim-8", "to": "finding-3"}]}
```

For a snapshot relative to its selected parent, added ledger record IDs are changed nodes. Because the EvidenceLedger is append-only, snapshot creation fails if any record present in that parent is missing from the current export; it does not treat a truncated export as a deletion. If an added record explicitly supersedes an older record, both the new and superseded IDs seed downstream traversal. `invalidated_node_ids` is the transitive closure over supplied edges. The recorded status is always `planned_not_executed`; this module cannot safely infer module-specific recomputation commands or claim that results were refreshed. Missing edges mean that dependency is unknown, not that no dependency exists.

The latest parent used is the latest stored snapshot at or before the requested `as_of_utc`. If the same cutoff has a different evidence set, that prior snapshot may be the parent. A snapshot from a later cutoff is never selected as parent for a backdated view.

## Report comparison

Each report bundle must contain `run_receipt.json`, `findings.jsonl`, and `incident_report.md`. The receipt must include `incident_id`, `run_id`, UTC `as_of_utc`, and `output_sha256` entries for both output files. Every named output must exist as a regular non-symlink file and match its recorded SHA-256 before comparison. Receipt incident/run/as-of values are cross-checked against the corresponding metadata rows in the verified Markdown report. Findings bytes are parsed from the same in-memory bytes whose digest was checked. The before and after bundles must describe the same incident, and the after cutoff cannot precede the before cutoff.

Receipt output hashes detect accidental file/receipt mismatches; they are not a cryptographic signature. Because the receipt is local and unkeyed, a malicious editor who rewrites the receipt and report and recalculates hashes can forge a self-consistent bundle. Use a separately trusted signature or archived digest if adversarial authenticity is required.

Finding IDs are the join key. Added/removed entries mean added/absent in the supplied report bundle. They do not mean newly true/refuted. A changed item includes explicit field-level reasons. `explicit_correction` is emitted only when the later finding contains a correction/supersession reference. `reason_code` is passed through as metadata and is not treated as proof of correction.

## CLI

```bash
python -m src.analysis.incident_ops --help
python -m src.analysis.incident_ops snapshot --help
python -m src.analysis.incident_ops snapshot \
  --store reports/incident-snapshots \
  --spec config/incidents/example.json \
  --run-manifest reports/run_manifest.json \
  --ledger-jsonl reports/evidence-ledger.jsonl \
  --dependencies reports/dependencies.json \
  --as-of 2026-11-07T18:00:00Z
python -m src.analysis.incident_ops list --store reports/incident-snapshots
python -m src.analysis.incident_ops list --store reports/incident-snapshots --incident-id case_demo_2026

python -m src.analysis.report_diff --help
python -m src.analysis.report_diff \
  --before reports/run-then \
  --after reports/run-now \
  --output-dir reports/report-diff-then-now
```

The report-diff output directory must not already exist. Both commands reject path traversal and symlink components for input and output paths, and use exclusive file creation for immutable outputs. CLI exit status is `0` for success/help and `2` for invalid inputs or I/O failures.

## Validation and limits

- The operation tests cover no-op identity, new evidence, explicit corrections, append-only record retention, cutoff exclusion, lifecycle metadata labeling, receipt/report consistency, same-buffer hash-and-parse, symlink rejection, path traversal, and CLI help/output.
- Snapshot validation does not prove source authenticity, evidence entailment, independence, event-time correctness, completeness, or legal admissibility.
- The ledger cutoff uses EvidenceLedger `created_at`, which is caller-supplied/imported rather than a signed server-side observation timestamp. It cannot prove when a researcher first saw a source or prevent a backdated imported record; treat the output as a retrospective timestamp filter, not an independently authenticated historical archive.
- Deterministic snapshots are local records, not a distributed lock or database transaction. The directory layout is suitable for one local writer; concurrent writers should use a transactional registry before deployment.
- A changed node with no explicit edge has no inferred downstream invalidation. The output is a candidate plan only and must not be described as recomputation.
