# Phase 10: controlled recomputation dispatch

**Status:** synthetic adapter dispatch implemented and exercised; real-case recomputation remains unavailable.

## What changed

`src.analysis.incremental_dispatch` adds a deterministic code-owned adapter registry that turns an explicit snapshot invalidation plan into an ordered task list. It executes only fixed, in-process Python analysis functions. It rejects arbitrary module names, import paths, shell commands, stale bindings, duplicate bindings, malformed inputs, and dependency cycles. A canonical SHA-256 consistency fingerprint is checked before execution; each executed task records hashes of its supplied input and result. These unkeyed hashes detect accidental changes but are not signatures of authenticity.

The dispatcher does not alter the immutable snapshot or change its `planned_not_executed` status. Its receipt is separate. It does not fetch sources, call an LLM, write a report, mutate the EvidenceLedger, infer missing dependencies, or make results flow implicitly between tasks. Each adapter needs a refreshed, typed payload selected by an explicit `input_key`.

## Fixed adapter map

| Adapter ID | Python function | Required input payload |
|---|---|---|
| `claim_verification.aggregate.v1` | `src.analysis.claim_verification.aggregate_verification` | `claim`, `assessments`, `as_of_utc`, `search_complete`; optional minimum independent roots and superseded result ID |
| `source_lineage.v1` | `src.analysis.source_lineage.analyze_source_lineage` | `records` |
| `event_reconstruction.timeline.v1` | `src.analysis.event_reconstruction.reconstruct_timeline` | `event_mentions`; optional `run_context` |
| `conflict_analysis.episode.v1` | `src.analysis.conflict_analysis.analyze_conflict_episode` | episode ID, typed physical-event, position and information-attention arrays; optional context |
| `information_dynamics.summary.v1` | `src.analysis.information_dynamics.summarize_information_dynamics` | normalized `posts`; optional coverage, lineage and binning parameters |
| `uncertainty_scenarios.v1` | `src.analysis.uncertainty_scenarios.analyze_uncertainty_scenarios` | scenario records and target label; optional scenario parameters |

Bindings have exactly three fields: `node_id`, `adapter_id`, and `input_key`. Only nodes in `invalidation_plan.invalidated_node_ids` are eligible. Nodes without a binding are retained as `not_dispatched`; an invalidated descendant is blocked when one of its invalidated predecessors lacks a runnable binding. Tasks follow deterministic topological order with lexical tie-breaking.

## Synthetic correction control

A synthetic snapshot represented an appended correction that invalidated a claim node and a downstream report node. The claim node dispatched through `claim_verification.aggregate.v1` using two explicitly independent synthetic roots. The analysis returned `supported_within_scope` and linked the result to the superseded synthetic result ID. The report node remained `not_dispatched` because report generation is not in this adapter allowlist. Running the same plan and payload twice produced the same output digest.

The sanitized receipt is `reports/orchestrator/phase10-dispatch-synthetic-2026-11-08.json`. It contains identifiers and hashes only; no synthetic claim or evidence text is persisted. Regression coverage is in `tests/test_incremental_dispatch.py`.

## Real-case boundary

This synthetic run validates dispatch mechanics, not Social's real-case conclusions. The current real case has an invalidation plan but no accepted, typed correction assessment to feed into claim verification, and its retrieval hits are not accepted evidence. Consequently this run does **not** update any real claim status, event timeline, conflict episode, or report. No real-case module recomputation is claimed. A future real dispatch requires explicit invalidated-node-to-adapter bindings plus verified refreshed inputs and a controlled output receipt; absence of bindings stays visible as `not_dispatched`.

## Validation

- `tests/test_incremental_dispatch.py`: 11 passed (including parameterized smoke coverage for all six registered adapters).
- `tests/test_incident_ops.py` and `tests/test_report_diff.py` with the dispatcher tests: 43 passed.
- Covered: correction-triggered claim aggregation, deterministic hashes, topological ordering, explicit missing-binding state, missing-input failure, arbitrary-adapter rejection, stale-binding rejection, plan fingerprint mismatch, cycle rejection, and all registered adapter entry points on synthetic inputs.
- The environment emitted one third-party anyio/pytest deprecation warning; there were no test failures.

## Remaining limits

- The dispatcher is an execution primitive, not an automatic dependency-schema inference engine.
- Downstream modules receive their own supplied payloads; result-to-input wiring is not automatic.
- Report generation and `report_diff` are intentionally not registered as execution adapters because they write/read report bundles and need a separately designed output transaction contract.
- A matching SHA-256 establishes deterministic byte identity, not truth, source authenticity, or completeness.
- Missing dependency edges can still omit affected work; only supplied graph edges are traversed.
