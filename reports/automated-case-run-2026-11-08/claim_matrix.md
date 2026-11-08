# Claim verification matrix — bounded offline projection

**Run:** `run-post-fix`; as-of `2026-11-08T01:14:07Z`.

> **Retrieval validity correction:** the 9,769-hit value below is historical execution telemetry from a zero-budget run whose old runner bypassed `max_queries_per_claim=0` by substituting `top_k=20`. It is invalid for compliant retrieval/analysis and is not search coverage. The separate, budget-compliant source-linked run is reported in [its receipt](source-linked-case-run-2026-11-08.md) and the [retrieval-validity addendum](retrieval-validity-addendum-2026-11-08.md).

## Result

| Measure | Count |
|---|---:|
| Candidate claim records recovered and hash-verified | 555 |
| Archived passages in supplied search corpus | 23 |
| Historical BM25 hit telemetry from defective zero-budget run (not valid retrieval coverage) | 9,769 |
| Separate budget-compliant source-linked candidate matches (30 passages; 1,110 directions) | 11,897 |
| Accepted assessments / `VerificationResult`s in source-linked run | 0 / 0 |
| Per-claim projections emitted after this follow-up | 555 |
| `unverified` projections | 555 |
| Supported / refuted / conflicting verdicts | 0 |
| Independent accepted assessments | 0 |

Every emitted status is **unverified**. This is a bookkeeping projection for an incomplete evidence search, not a semantic review or finding about whether any proposition is true or false. Only the 11,897 matches from the separate source-linked run are candidate retrieval leads; the defective 9,769-hit zero-budget count is invalid telemetry and must not be used even as an evidence lead. The candidate leads were not converted to evidence assessments. The claims have no normalized substantive scope in the run input; the private records carry only `scope_status=not_parsed_in_case_run` as an explicit placeholder.

## Provenance and privacy

The claim and passage inputs were matched against the private-input hashes and record counts already recorded in `run_receipt.json`. Per-claim output was written outside Git to the private analysis directory, with 555 records. Output SHA-256: `7e33c6f693798e4671aebdcf2a955f147f1c9903d868c1021c9876511c474b9b`. This repository contains only this aggregate matrix: no claim text, claim IDs, source URLs, passage text, or per-claim rows.

The original case-run summary correctly recorded zero verification results because no VerificationResult projections were emitted in that run. This follow-up creates unverified projections only; it does not retroactively claim that the original run performed semantic verification.

## Limitations

- The 9,769 figure is invalid for compliant retrieval and must not be treated as search coverage. The separate source-linked run's 11,897 matches are candidate retrieval over its supplied 30 passages, not complete search, corroboration, or accepted evidence.
- Candidate claim spans and substantive scopes were not independently adjudicated.
- No supporting or contradicting assessments were accepted.
- Semantic accuracy, claim truth, source reliability, and coverage outside the supplied archive remain not evaluated.
