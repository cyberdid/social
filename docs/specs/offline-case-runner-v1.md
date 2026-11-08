# Offline Case Runner v1

## Purpose

`src/analysis/offline_case_runner.py` composes compatible deterministic Social
analysis modules over artifacts that have already been collected. It does not
collect sources, call an LLM, assign truth, or infer missing roles or events.
The default mode is a dry run. `--execute` runs local processors only.

This is an integration boundary, not a claim that Social can autonomously
reconstruct every real incident. Missing, untyped, or incompatible inputs remain
`not_run`, `unverified`, or `unresolved`. Semantic accuracy remains
`not_evaluated` unless a separately adjudicated benchmark is supplied.

## Input names and contracts

`run_offline_case(incident_spec, run_dir, git_commit=..., inputs=..., execute=...)`
accepts only the following named local paths:

| Input name | File format | Component |
|---|---|---|
| `claims` | JSONL | Atomic claim rows for bounded retrieval |
| `passages` | JSONL | `passage_id`, `source_id`, `captured_at_utc`, `text`, optional lineage fields |
| `event_mentions` | JSONL | Existing event-reconstruction mention contract |
| `lineage_records` | JSONL | Claim-scoped evidence records consumed by `analyze_source_lineage` |
| `information_posts` | JSONL | Normalized post snapshots consumed by `summarize_information_dynamics` |
| `uncertainty_records` | JSONL | Normalized label/group records consumed by `analyze_uncertainty_scenarios` |
| `coverage` | JSON | Coverage object passed unchanged to information dynamics and report context |
| `conflict_input` | JSON | `episode_id`, `physical_event_records`, `position_records`, `information_attention_records` |
| `report_bundle` | JSON | Typed `findings`, `evidence_records`, and `verification_results` for the constrained renderer |

Inputs must be UTF-8 JSON/JSONL objects. Files are capped at 128 MiB each,
combined inputs at 512 MiB, each JSONL line at 4 MiB, and each JSONL file at
200,000 records. Symlink path components and path traversal are rejected.

`IncidentSpec` is validated against the existing v1 schema. The supplied
`git_commit` identifies the code revision that produced the run.

Before a component runs, recognized capture, publication, observation, query,
and view-snapshot timestamps are checked against `IncidentSpec.as_of_utc`.
In-scope publication/event times for information posts, event mentions, conflict
episodes, and uncertainty rows are checked against `IncidentSpec.time_window_utc`.
A malformed timestamp, post-cutoff record, or out-of-window in-scope record
fails that component closed with a `time_scope_contract_mismatch` receipt; it is
not silently removed from a historical run.

## Processing and status semantics

The runner writes a private, exclusive output directory (`0700`; files `0600`)
and refuses to overwrite an existing directory. It records input file hashes,
byte sizes and row counts in `input_manifest.json`, then emits
`task_receipts.jsonl`, `unresolved_queue.jsonl`, `case_summary.json`, and a
schema-validated `run_manifest.json`.

When claims and passages are supplied, `budgets.max_queries_per_claim` caps
BM25 queries per claim, independently of the candidate count. A zero budget
skips retrieval entirely: the stage receipt and unresolved queue record
`not_run` with reason `query_budget_zero`, and the candidate and verification
JSONL files contain no rows. The receipt also records `executed=false`; original
input counts and hashes remain in the input manifest, and other stages continue.
For a positive budget, the runner invokes the local retriever once per claim
and passes the cap through to its BM25 query schedule. The schedule deduplicates
variants in input order (statement first), then schedules the claim direction
followed by the counterevidence direction for each variant. Thus budget 1 runs
the statement claim query, budget 2 also runs its counterevidence query, and
larger budgets admit later supplied variants. The cap is applied before scoring;
queries omitted by the cap contribute neither scores nor executed query terms.

`search_receipt` records `planned_query_count`, `executed_query_count`,
`omitted_query_count`, `search_truncated`, and the schedule order. Its `directions`
and `query_terms` describe executed queries only. Candidate selection retains a
fixed `top_k=20` per executed direction. Budget beyond the finite schedule stays
unused; no additional variants or retries are generated. Direct retriever callers
that omit the optional `max_queries` cap retain the full existing search behavior.

The runner writes candidate passages and creates only `unverified` projections
with zero accepted assessments. Retrieval rank and repeated publication are never treated
as support. A missing claim scope blocks a verification projection.

Other components are invoked only when their own typed inputs are supplied:

- `event_mentions` → `reconstruct_timeline`, retaining separate physical and
  communication clocks;
- `lineage_records` → `analyze_source_lineage`, retaining candidate edges and
  zero independent roots unless established upstream;
- `information_posts` → descriptive information dynamics, with optional coverage
  and lineage inputs;
- `conflict_input` → conflict episode aggregation without inferring positions,
  motives, or physical escalation from communication counts;
- `uncertainty_records` → explicit observed-corpus sensitivity scenarios;
- `report_bundle` → constrained Markdown/JSONL report generator, followed by
  report output hash verification and structural evaluation gates.

No field mappings are guessed between modules. If the required upstream type is
not supplied, the stage is marked `not_run`. A component exception records the
exception class, not arbitrary input text or a traceback, and the run continues
to preserve other usable outputs.

Frozen-suite failures and evaluation exceptions are finalized as failed
evaluation receipts in both `task_receipts.jsonl` and `run_manifest.json`; they
do not leave an occupied run directory with a success-shaped interim status.

`analysis_status` is `complete` only when all registered stages were executed
successfully and the structural evaluation passed. A run with omitted optional
stages is `partial`; a failed component or hard gate is `failed`. The
RunManifest `state=completed_bounded` means only that the bounded controller
finished and is not a verdict about evidence completeness.

## Report and evaluation boundary

The renderer receives only the explicitly supplied typed report bundle. Its
checks validate cited evidence IDs, exact text or media locators, scope/status
consistency, and rendered output hashes. `evaluation.json` also invokes the
existing frozen synthetic control suite or structural run-bundle gates.

These checks do **not** independently verify the truth of cited statements or
recompute `artifact_sha256` from original source bytes: the report bundle has no
artifact registry/path contract. A formatted SHA-256 and exact quote locator
therefore establish structural consistency of the supplied record, not source
authenticity or semantic entailment. `unsupported_assertion_count` and semantic
accuracy remain `null` / `not_evaluated`.

## CLI

```bash
python -m src.analysis.offline_case_runner \
  --spec incident.json --run-dir runs/case-001 --git-commit abcdef0123456 \
  --event-mentions events.jsonl --claims claims.jsonl --passages passages.jsonl
```

The command above creates a dry-run plan. Add `--execute` to process supplied
files locally. Optional inputs use `--lineage-records`, `--information-posts`,
`--uncertainty-records`, `--coverage`, `--conflict-input`, and `--report-bundle`.
No collection, provider credentials, or platform API is accessed.

## Validation

Synthetic integration tests cover copy fan-out, unverified conflicting
passages, separate physical and communication timelines, source locator/output
hash preservation, and non-overwrite dry-run behavior. The frozen evaluation
suite is structural/adversarial and is not an incident-level semantic benchmark.
