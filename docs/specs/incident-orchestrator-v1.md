# Incident orchestrator v1: W00 and bounded W01 Source Watch bridge

`src.analysis.incident_orchestrator` creates one auditable run from an IncidentSpec.
It integrates exactly one collection adapter: the existing
`source_watch_collect.build_plan(audit_path)` and `source_watch_collect.run(...)`
callables. The code-owned registry maps `web` to that adapter. JSON cannot supply
commands, imports, callbacks, alternative registries, or host allowlists. A fresh
manifest returned by that exact collection call may be imported through the
existing `source_ingest_bridge` into a new run-local EvidenceLedger. Only the
collector's filtered `article_text` passages are made available to local
retrieval; the bridge does not create claims or assess evidence.

An independent opt-in mode invokes the code-owned `run_offline_case` adapter on
explicit pre-typed local inputs. When a fresh Source Watch manifest exists, its
bridge passages are merged with the caller's optional `passages` JSONL by
`passage_id` and passed through a copied input map. Caller input files remain
read-only. A duplicate ID with a different full record fails closed.

This is a fixed public source availability watch, not full autonomous incident
collection. Its existing official/media domain allowlist and watchlist logic are
unchanged. Incident seed URLs never expand that allowlist or become collection
targets. Watchlist results are not automatically incident-relevant and are not
filtered to the incident date window. Fetches describe present availability;
`as_of_utc` does not create historical web evidence.

## Running

Use the repository root as the working directory. Supply the producer's actual
Git revision explicitly; the runner does not run Git or any shell commands.

```bash
PYTHONPATH=. python -m src.analysis.incident_orchestrator \
  --spec tests/fixtures/incident_spec.valid.json \
  --run-dir data/runs/example-plan \
  --audit reports/source-refresh-url-audit-2026-11-06.json \
  --git-commit <actual-7-to-40-character-commit>
```

Default mode builds a local plan and records `source_watch` as `planned`, with
`executed: false`. It does not invoke the network collector. Add `--execute` to
perform read-only collection. Both the `web` platform and `public_web` access
method must be present. A zero `max_new_sources_per_run` budget prevents any
collection. Unsupported platforms remain explicit `not_run` coverage gaps,
including Telegram, YouTube, TikTok, Instagram, Facebook, Threads, X and local
files. An unused audit is not read when web collection is unavailable or blocked
by policy/budget.

To run deterministic local analysis, provide a separate JSON object and opt in:

```json
{
  "information_posts": "/absolute/path/to/typed-posts.jsonl",
  "claims": "/absolute/path/to/typed-claims.jsonl",
  "passages": "/absolute/path/to/typed-passages.jsonl"
}
```

```bash
PYTHONPATH=. python -m src.analysis.incident_orchestrator \
  --spec tests/fixtures/incident_spec.valid.json \
  --run-dir /absolute/path/to/private-run \
  --audit reports/source-refresh-url-audit-2026-11-06.json \
  --git-commit <actual-7-to-40-character-commit> \
  --run-local-analysis --typed-input-manifest /absolute/path/to/inputs.json
```

`--run-local-analysis` and `--execute` are independent: the first executes local
processors over the supplied inputs, while the second alone enables the public
watchlist network collector. Either, both, or neither may be selected. A typed
input manifest provided without `--run-local-analysis` is not opened. An opted-in
missing or invalid manifest yields `failed_with_receipt`; it does not fall back
to other paths or discover data. A bridge input is only the exact manifest path
in the collection call's returned `summary["manifest"]`, validated against that
summary's snapshot ID and the new run's
`raw/source_watch/<snapshot>/manifest.json` location. Dry-run, missing-manifest,
and failed-before-return paths do not inspect `latest.json` or prior captures. If
a separately requested collection fails and the passage merge has not failed
closed, the local run still processes independently supplied typed data, while
the outer run remains failed to preserve the collection failure.

Only the offline runner's existing input names are accepted: `claims`,
`passages`, `event_mentions`, `lineage_records`, `information_posts`,
`uncertainty_records`, `coverage`, `conflict_input`, and `report_bundle`.
Values must be nonempty path strings. Relative paths are interpreted against the
process working directory; absolute paths are recommended for reproducibility.
The nonempty manifest is bounded to 1 MB; duplicate keys, traversal and symlink
paths are rejected. Its byte hash is recorded in the local-analysis receipt.
The offline runner independently checks regular files and its
128 MiB per-file, 512 MiB total, 200,000-record and 4 MiB per-line limits.

When a fresh Source Watch manifest is returned, `source_ingest_bridge` imports
that exact file with `root=run_dir`; the orchestrator never searches for a
newest/latest file. Source, Artifact and Passage records are retained in the
run-local ledger. Only collector `article_text` extractions become passages;
artifact-only captures remain available in the ledger but do not become retrieval
passages. The merged JSONL uses the offline runner's required `passage_id`,
`source_id`, `text`, and `captured_at_utc` fields, plus relative artifact paths,
artifact hashes, source URIs, and the bridge locator metadata. This is a typed
input adapter, not raw-source normalization or claim extraction.
Filtered Source Watch passages carry `artifact_start_offset: null` because the
extractor does not map text positions back to the archived HTML; retrieval keeps
quote offsets relative to the filtered passage and preserves its locator.

An existing caller `passages` JSONL is read under the same 128 MiB, 200,000-row,
and 4 MiB-line limits. Records merge by exact `passage_id`: equal parsed records
are deduplicated, while a repeated ID with a different record fails the bridge
and local run. The orchestrator never writes to the caller's JSONL. The offline
adapter receives a copied input mapping whose `passages` value points to the
retained merged file. Other caller-provided input paths are preserved unchanged.

Every Source Watch row's `requested_at` must be a timezone-aware UTC timestamp
not later than IncidentSpec `as_of_utc`. A later or invalid capture time is an
explicit `time_scope_contract_mismatch` or timestamp failure. The merged passage
may be retained for audit, but local retrieval cannot report it as in-scope; the
run is failed. Search output remains a candidate list, and verification results
remain unverified until a separate evidence assessment is supplied.

Optional limits are `--timeout` (1–60 seconds per target, default 20), `--pause`
(0–60 seconds between targets, default 1), `--max-bytes` (1024–10,000,000 per
response body, default 2,000,000), and `--max-targets` (1–100, default 25). At most
`min(max_targets, IncidentSpec.budgets.max_new_sources_per_run)` plan targets are
selected in the collector's stable order. The remaining count becomes an
unresolved budget gap. Each target may involve the existing collector's bounded
redirect sequence; the target cap is not a cap on individual HTTP requests.
The collector checks elapsed time between reads/redirects; one blocking read may
exceed the target deadline by its read timeout. There are no automatic retries,
scheduling, recursion, model calls or paid services. The offline runner applies
`max_queries_per_claim` as a query-call budget: zero records
`not_run/query_budget_zero`, while a positive value caps local BM25 calls across
claim and counterevidence query variants. The candidate limit (`top_k=20` per
direction) is separate; a small query budget may leave a direction unsearched.
Other supplied local processors can run when claim retrieval is skipped.
Video/cost budgets do not enable additional work here.

Runtime dependencies are the existing collector dependencies (`requests` and
`beautifulsoup4`) and contract dependencies (`jsonschema` and `referencing`). Tests
also need `pytest`.

## Artifacts and states

The supplied run directory must not already exist, even for identical inputs.
There is no resume implementation. Path traversal and existing symlink components
in explicit inputs/output paths are rejected. Explicit JSON inputs are bounded
(1 MB IncidentSpec, 10 MB audit, 1 MB typed-input manifest); no token or session
file is discovered or read.
The runner creates no files outside the requested new run directory, apart from
creating its missing parent directories. Input documents are read-only.

The directory contains:

- `run_manifest.json`: validated by `validate_run_manifest`, with producer
  revision, state, limitations, source snapshot references and output hashes.
- `coverage_plan.json`: every requested platform, selected public watch targets,
  explicit policy/budget gaps and bounds. `seed_urls_not_dispatched` records the
  number of incident seed URLs left outside the fixed adapter scope.
- `task_receipts.jsonl`: local stage and per-target receipts, including
  `planned`, `not_run`, execution flags and failure outcomes.
- `unresolved_queue.jsonl`: non-complete tasks and their bounded reason codes.
- `raw/source_watch/<snapshot>/manifest.json` and immutable body files when
  collection executes. These are the original collector artifacts.
- `reports/source_watch/latest.json` and `latest.md`: the collector's manual
  review queue, scoped to this run so earlier run reports are preserved.
- `evidence_ledger.sqlite`: the append-only EvidenceLedger for the exact fresh
  Source Watch manifest, when one is returned by this run's collection call.
- `merged_passages.jsonl`: caller passages plus bridge passages, merged by ID;
  it is retained in the run root outside `analysis/` and supplied to the offline
  runner when local analysis is opted in.
- `source_ingest_receipt.json`: a content-free summary with bridge status,
  relative locators, hashes, and counts. It contains no source text or URL.
- `analysis/`: the offline runner's input manifest, stage receipts, unresolved
  queue, analysis artifacts, case summary, and nested run manifest when local
  analysis is requested and accepted. The outer manifest hashes every saved
  nested file, including `analysis/run_manifest.json`. These files may contain
  source text or identifiers; place the run in private storage outside Git.

RunManifest `source_snapshots` records the Source Watch manifest hash, relative
path and aggregate access status. The content-free bridge receipt records the
same manifest hash, ledger hash, merged-passage hash, bridge counts, and relative
paths. That collector manifest retains per-body hashes. RunManifest `outputs`
hashes all saved files other than the outer RunManifest itself, avoiding a
self-referential hash while including the ledger, merged passages, bridge
receipt, and any nested run manifest.
Unexpected collection exceptions preserve any partial raw files already written
and produce a bounded receipt containing the exception type, never the exception
message. Collector-authored raw receipts retain their existing diagnostic format.

The controller state path is:

```text
created → collecting → normalized → extracting → verifying → reconstructing
        → reporting → completed_bounded
```

The post-collection states are controller checkpoints. Without local opt-in they
receive `not_run`/`local_analysis_not_requested` (or `upstream_failed` if the
collection failed). With local opt-in, `normalized` and `extracting` remain
`not_run`: the local adapter accepts caller-typed records and collector-provided
filtered passage text, and does not claim to have normalized raw sources or
extracted claims. The outer `verifying` stage is
at most `partial` when claim retrieval ran, because the returned passages are
candidates requiring evidence assessment. The outer `reconstructing` stage is at
most `partial` when typed event or conflict records were processed; it does not
certify their truth. `reporting` may complete for an explicitly supplied,
preverified report bundle after structural citation checks. Semantic entailment
and source authenticity remain unevaluated.

Per-processor `local:<stage>` receipts preserve the nested execution flags and
attempt times and reasons and link to `analysis/task_receipts.jsonl`. The
`local_analysis` receipt links to `analysis/case_summary.json` and
`analysis/unresolved_queue.jsonl`. The adapter checks the nested aggregate
against the per-stage statuses: a failed stage cannot produce a successful outer
run, and a complete aggregate cannot hide a non-complete stage.
Unexecuted processors are `not_run`. At zero query budget the outer
`local:claim_retrieval` and `verifying` receipts preserve the nested runner's
`not_run/query_budget_zero` status and reason; the explicit input manifest still
records the supplied claims and passages. A malformed manifest, local runner
exception or inner failed status is receipted as failed, without recording
exception text; partial nested artifacts remain in place. A collection failure
yields a failed outer run; an independently requested local run still uses its
explicit inputs.
Unsupported platforms, deliberate dry-run and explicit zero budgets are bounded
coverage limitations and can finish `completed_bounded`. That state means the
controller finished its bounded work, not that the incident was fully collected
or analyzed.

Detailed receipt statuses include `complete`, `partial`, `blocked`, `not_found`,
`failed`, `planned` and `not_run`. Existing RunManifest v1 only accepts the first
five: the runner projects `planned`/`not_run` to `blocked` there, with `detail_ref`
pointing to the exact task in the detailed JSONL file. Consumers must consult the
detail receipt to distinguish a planned task from a blocked fetch. Schemas are
unchanged.

HTTP 401/403/429 and access challenges map to `blocked`, 404/410 to `not_found`,
truncated bodies to `partial`, and other failed HTTP/access/content outcomes to
`failed`. Different outcomes within a snapshot aggregate to `partial`; a uniform
snapshot retains its outcome. A collection-stage exception becomes `failed`.
Failure of the local filesystem itself can prevent receipt persistence; there is
no claim of crash recovery or protection against concurrent malicious filesystem
replacement. Existing directories are never silently overwritten.

CLI exit codes are 0 for `completed_bounded`, 1 for `failed_with_receipt`, and 2
for invalid inputs, unsafe/occupied paths or local setup errors.

## Safety and remaining scope

The adapter uses only credential-free HTTPS public requests on its fixed host
allowlist, verifies TLS, rejects cross-source redirects, and bypasses neither
platform gates nor access challenges. The orchestrator never imports
`src/archive_sources.py`, discovers credentials, posts, messages, mutates
external data, targets users, or invokes models. The local mode reads only the
explicit input paths supplied by its caller; it does not discover credentials or
private platform sources. Strings in the
IncidentSpec model fields are descriptive input only; model execution remains
disabled. Unknown command/import/allowlist configuration keys fail the existing
strict IncidentSpec schema.

Remaining work includes additional separately reviewed collection adapters,
automatic normalization and claim extraction, full passage-grounded evidence
assessment, historical filtering, relevance decisions, durable crash recovery
and validated no-op resume. The local adapter executes only the deterministic
offline stages for which compatible typed inputs were supplied.
