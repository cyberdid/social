# W00 integration run — sanitized receipt

**Run:** `w00-integration-run-codex-20261108`  
**Incident:** `petropavlivska-borshchahivka-2026-11`  
**Time:** 8 November 2026, 07:07:54–07:08:00 UTC  
**Controller status:** `completed_bounded`; **local analysis:** `partial`  
**Machine-readable receipt:** [JSON](w00-integration-receipt-2026-11-08.json)

## What ran

The controller completed with a dry-run collection plan: zero targets dispatched, zero external source snapshots, and model inference disabled. It then ran local analysis over eight already supplied typed artifacts (4,108,777 aggregate bytes; record totals are listed below). This is an integration check of the orchestration and local-analysis path, not a new collection or a semantic case verification.

Local stages completed for event-mention reconstruction, conflict aggregation, information dynamics, uncertainty scenarios, report generation, and structural evaluation. Claim retrieval did not run because its query budget was zero. Source lineage did not run because lineage records were not supplied. The resulting local-analysis status is `partial` by design.

The structural evaluator passed with zero hard-gate failures. The generated three-file report bundle and its integrity checks both passed. Semantic accuracy, citation entailment, source authenticity, and independent source roots were not evaluated. The run returned zero verification results.

## Aggregate input and integrity counts

| Measurement | Count/status |
|---|---:|
| Typed input artifacts | 8 |
| Candidate claims | 555 |
| Event mentions | 574 |
| Information posts | 1,438 |
| Passages | 23 |
| Uncertainty records | 1,438 |
| Controller manifest output receipts | 20; 0 hash failures |
| Nested local-analysis output receipts | 16; 0 hash failures |
| Distinct report files checked | 3; bundle and integrity passed |

The 16 local-analysis output receipts are nested in the controller receipt set, so 20 and 16 are counts of manifest checks, not 36 distinct files. Input text, source URLs, post/account/channel identifiers, and private filesystem paths remain outside this receipt.

## What this run does not establish

- It does not establish the truth of any claim, the physical-event chronology, source independence, state attribution, or incident completeness.
- `completed_bounded` describes controller completion, not completion of case analysis.
- Retrieval results, if generated in a different run, remain candidates until separately assessed.
- No network collection or model inference occurred in this run.

Manifest fingerprints and the full limitation list are in the [JSON receipt](w00-integration-receipt-2026-11-08.json). The private run manifests and full run outputs are not copied into the repository.
