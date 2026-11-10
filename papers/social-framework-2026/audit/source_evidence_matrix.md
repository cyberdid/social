# Scientific claim–evidence matrix

Baseline f0e9d0d. New experimental outputs identify their own producer and baseline. No independent human adjudication claimed.

| Claim ID | Statement | File / artifact | Verification status | Limitation |
|---|---|---|---|---|
| S01 | Modular collectors, not universal ingestion | src/tg_collect.py; src/tg_comments_collect.py; src/source_watch_collect.py | Direct code; ingestion audit | Access-dependent, platform-specific |
| S02 | Append-only typed evidence accounting | src/evidence_ledger.py | Code/tests | Hash syntax does not rehash bytes; no semantic guarantee |
| S03 | Local BM25 retrieval with receipts | src/analysis/claim_verification.py | Code/tests | No independently labeled relevance gold |
| S04 | Numeric/lexical relation heuristics may false-support | papers/social-framework-2026/data/evidence_counterexamples.json | Fresh reproducible challenge | Hand-designed cases, not population error rate |
| S05 | Current25claim output19/0/6,36accepted | reports/evidence-verification/core_claims_verification_2026-11-09.json | Parsed versioned artifact | Curated claims/passages; no independent accuracy |
| S06 | 1384eligible historicaltexts,369exactpairs,367legacy | papers/social-framework-2026/data/audited_evaluation_metrics.json | Fresh exact recomputation | Finite eligible universe, not campaign truth |
| S07 | Saved16nullsummaries and25draw/modelprefix reproduce | papers/social-framework-2026/data/audited_evaluation_metrics.json | Fresh bounded replay | Full9999draws not rerun in this audit |
| S08 | 783tests+16subtests pass | papers/social-framework-2026/data/pytest_offline.log | Fresh execution | Software checks, not factual accuracy |
| S09 | Physicalmentions curated; event organizer no automatic merge | src/analysis/event_reconstruction.py; scripts/analysis/build_physical_event_timeline.py | Code/artifact | No physical event accuracy gold |
| S10 | 607unique media decode receipt | reports/video-pipeline/telegram-full-decode-2026-11-08.md | Historical receipt | No new decode, authenticity/locationunmeasured |
| S11 | 18suppliedreferenceclips microWER185/415 | reports/video-pipeline/asr_calibration_benchmark_2026-11-09.json | Artifact arithmetic | Reference/humanreviewprovenance not independently established |
| S12 | Gemini3keyframe feasibility only | reports/video-pipeline/gemini-keyframe-pilot-2026-11-08.md | Historical receipt/codeabsence | Not integrated continuous video analysis |
| S13 | Audience semantic labels supplied to aggregator | src/analysis/audience_response.py; src/analysis/audience_aggregation.py | Code/tests | No validated UA/RU classifier accuracy |
| S14 | Source dependency not independent truth corroboration | src/analysis/source_lineage.py | Code/tests | Unknown roots stayunknown |
| S15 | Fresh typed workflow partial;2candidates;1unverifiedclaim | papers/social-framework-2026/data/bounded_workflow_smoke.json | Fresh experiment | Synthetic, no reportpayload; no fullendtoendproof |
| S16 | Historical/expanded corpora have different countsandhashes | papers/social-framework-2026/data/audited_evaluation_metrics.json | Fresh parsing | Selectionnotrepresentative |
| S17 | Allsourcewatch failures retained as availabilitymissingness | src/source_watch_collect.py | Code/receipts | Historical reportlinkedrawsnapshot absent locally |
