# Retrieval validity corrigendum — 8 November 2026

## Correction

The `run-post-fix` retrieval output (`2026-11-08T01:14:07Z`) was configured with `max_queries_per_claim=0`, but the old runner bypassed that zero budget by substituting `top_k=20`; the retriever then searched claim variants in both directions. Its 9,769 candidate-hit count is historical execution telemetry only. It is **invalid for compliant retrieval or analysis** and must not be described as search coverage, a completed search, corroboration, or evidence.

The separate `run-source-linked-20261108` used a budget of two directions per claim. It searched 555 candidate claims against 30 passages, executed 1,110 directions, and returned 11,897 candidate matches, including 3,012 from seven newly locatable passages. It accepted **0 evidence assessments** and emitted **0 `VerificationResult`s**. These are candidate-only retrieval results over the supplied corpus; they do not establish claim truth, complete source coverage, or semantic accuracy. See the [source-linked run receipt](source-linked-case-run-2026-11-08.md).

Current code behavior was verified by inspection, not by running tests for this corrigendum: `src/analysis/offline_case_runner.py` writes empty candidate/result outputs and records `not_run` with reason `query_budget_zero` when the configured budget is zero. For positive budgets it passes the value as `max_queries`; `src/analysis/claim_verification.py` limits the executed variant/direction schedule to that cap. `top_k` remains a separate candidate-count limit.

## Receipt and hash scope

`run_receipt.json` is preserved unchanged. It records `summary.md` SHA-256 `959834ba2d2900ce4d136d81418ff71c987e8dd8708bc241054711fbda885d2b`, while the current Markdown digest immediately before this corrigendum was `cd61ca5b2fdd8ee95c901c9e87fe2706f747d7d7e6f8c56e8842b5854c7ef0fa`. The edited Markdown is a superseding report; the historical receipt does not authenticate its present bytes. The receipt's recorded digest for `claim_retrieval_summary.json` is `69827dbe4aff455ea3771ddf1974d6414b7fa4897c5917bf19c24fb4a9252ab9`, which matched the preserved JSON when checked. Neither the receipt nor that JSON was edited.

This corrigendum is reflected in the [case-run summary](summary.md), [claim matrix](claim_matrix.md), [masterplan status](../orchestrator/masterplan-status-2026-11-08.md), and [main case report](../borshchahivka-report.md).
