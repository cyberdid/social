# Project: Social Master Plan v2.0
## Autonomous Execution of End-to-End Evidence Verification & Analytical Synthesis

## Architecture
The Social Master Plan v2.0 establishes an end-to-end evidence verification and analytical reconstruction system:
```
[Corpus & Source Watch Snapshots] ─────────┐
                                          │
[Video Assets & ASR Segments] ───────────┼─► M4: Corpus & Source-Watch Lineage Matrix (DONE)
                                          │     (reports/provenance/)
[Official Government / Legal Sources] ────┤
                                          ├─► M1: Core Claims Verification (DONE)
                                          │     (reports/evidence-verification/)
                                          │
                                          ├─► M2: Physical Incident Reconstruction (DONE)
                                          │     (reports/event-reconstruction/)
                                          │
                                          └─► M3: Video & ASR Semantic Calibration (DONE)
                                                (reports/video-pipeline/)
                                                      │
                                                      ▼
                                              M5: Analytical A4 Dossier Restoration (DONE)
                                                (output/pdf/, scripts/reports/build_report.py)
                                                      │
                                                      ▼
                                              M6: Adversarial Red-Team Audit (DONE)
                                                (reports/orchestrator/teamwork-red-team-2026-11-09.md)
                                                      │
                                                      ▼
                                              M7: Integration & Master Plan Synthesis (DONE)
                                                (reports/orchestrator/masterplan-closeout-2026-11-09-final.md,
                                                 clean test suite 774+ tests, log.md, README.md)
```

## Feature Inventory
Every feature from user requirements and survey phase is assigned to a milestone:
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | F1: Core Claims & Evidence Verification | 20–30 prioritized claims processed via `claim_verification.py` against official passage bundles with exact character offsets, counter-evidence checks, and accepted `VerificationResult` records | M1 | R1 / GATE-01 |
| 2 | F2: Physical Incident Reconstruction | Structured Physical Event Timeline strictly decoupled from communication timeline using `event_reconstruction.py`, with 5+ physical events, temporal intervals, participant positions, and negative constraints | M2 | R2 / GATE-02 |
| 3 | F3: Video & ASR Semantic Calibration | Stratified calibration sample of 15–20 audio clips across 4 strata, empirical WER and CER calculation, semantic evaluation, transition to `quote_safe: true` | M3 | R3 / GATE-03 |
| 4 | F4: Corpus & Source-Watch Lineage Matrix | Harmonize historical (1408 posts, 159 channels) vs merged (1438 posts, 158 channels) datasets (`kiber_boroshno`), reconcile Source Watch runs (10/12 vs 9/12, DBR TLS errors), strict provenance rule `(corpus_version, run_id, timestamp)` | M4 | R4 / GATE-04 |
| 5 | F5: Analytical A4 Dossier Restoration | Upgrade `scripts/reports/build_report.py` to restore 25–30 page A4 dossier with 4 embedded high-resolution raster charts (timeseries, network bridges, reactions, geospatial map), executive narrative, and Appendices A–C for raw logs/manifests | M5 | R5 / GATE-05 |
| 6 | F6: Independent Adversarial Red-Team Review | Read-only 6-vector audit of claims verification, physical timeline boundaries, citation offsets, ASR metrics, lineage matrix, and PDF visual rendering | M6 | R6 |
| 7 | F7: Integration, Closeout & Full Test Suite Pass | Harmonize `test_r7_f41` clean git tree assertion, verify 100% test pass (774+ tests), generate masterplan closeout report, update `log.md` and `README.md`, verify zero secret/PII leaks | M7 | R7 / GATE-06, GATE-07 |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Core Claims & Evidence Verification | Generate accepted `VerificationResult` records for 20–30 claims with exact character offsets | none | DONE |
| M2 | Physical Incident Reconstruction | Construct Physical Event Timeline with 5+ structured events and temporal bounds | none | DONE |
| M3 | Video & ASR Semantic Calibration | Produce acoustic references, compute WER/CER, gate quote-safety on 15+ clips | none | DONE |
| M4 | Corpus & Source-Watch Lineage Matrix | Reconcile 1408 vs 1438 posts, 159 vs 158 channels, 10/12 vs 9/12 Source Watch runs | none | DONE |
| M5 | Analytical A4 Dossier Restoration | Rebuild ReportLab report generator to produce 25–30 page A4 PDF dossier with 4 raster charts | M1, M2, M3, M4 | DONE |
| M6 | Adversarial Red-Team Audit | Independent read-only verification of claims, timeline, citations, and PDF rendering | M1, M2, M3, M4, M5 | DONE |
| M7 | Integration & Master Plan Synthesis | Test suite 100% pass, closeout report, log.md, README.md, zero-leak verification | M1, M2, M3, M4, M5, M6 | DONE |

## Interface Contracts
### M1: Core Claims Verification
- Output paths: `reports/evidence-verification/core_claims_verification_2026-11-09.json` and `reports/evidence-verification/core_claims_verification_2026-11-09.md`.
- Status: COMPLETED. 25 claims verified (21 supported, 4 refuted, 0 unverified), 31 accepted assessments, 100% test pass.

### M2: Physical Incident Reconstruction
- Output paths: `reports/event-reconstruction/physical_event_timeline_2026-11-09.json` and `reports/event-reconstruction/physical_event_timeline_2026-11-09.md`.
- Status: COMPLETED. 5 physical events with temporal bounds, negative constraints isolating Bucha fire, 100% test pass.

### M3: Video & ASR Semantic Calibration
- Output paths: `reports/video-pipeline/asr_calibration_benchmark_2026-11-09.json` and `reports/video-pipeline/asr_calibration_benchmark_2026-11-09.md`.
- Status: COMPLETED. 18 clips across 4 strata, empirical WER/CER calculated, 10 clips quote_safe: true, 100% test pass.

### M4: Corpus & Source-Watch Lineage Matrix
- Output paths: `reports/provenance/corpus_and_sourcewatch_lineage_matrix_2026-11-09.md` and `reports/provenance/lineage_manifest_2026-11-09.json`.
- Status: COMPLETED. 1408 vs 1438 reconciled (`kiber_boroshno`), 10/12 vs 9/12 Source Watch reconciled (DBR TLS error), 100% test pass.

### M5: Analytical A4 Dossier Restoration
- Output paths: `output/pdf/petropavlivska_borshchahivka_report_2026-11-09.pdf` and `output/pdf/manifest-2026-11-09.json`.
- Status: COMPLETED. 28 pages A4 (within 25-30 budget), 4 raster charts embedded, 96,980 chars, 0 replacement characters, 100% test pass.

### M6: Adversarial Red-Team Audit
- Output path: `reports/orchestrator/teamwork-red-team-2026-11-09.md`.
- Status: COMPLETED. Verdict APPROVE. 0 Critical, 0 High defects. All 6 audit vectors verified.

### M7: Integration & Master Plan Synthesis
- Output path: `reports/orchestrator/masterplan-closeout-2026-11-09-final.md`.
- Status: COMPLETED. 774/774 tests pass (100%), closeout report produced, log.md and README.md updated, zero-leakage verified.

## Code Layout & Write Ownership
- M1 Owner: writes ONLY to `reports/evidence-verification/`, `scripts/analysis/build_core_claims_verification.py`, `tests/test_core_claims_verification.py`.
- M2 Owner: writes ONLY to `reports/event-reconstruction/`, `scripts/analysis/build_physical_event_timeline.py`.
- M3 Owner: writes ONLY to `reports/video-pipeline/`, `scripts/analysis/build_asr_calibration_benchmark.py`.
- M4 Owner: writes ONLY to `reports/provenance/`, `scripts/provenance/build_lineage_matrix.py`, `tests/test_provenance_lineage.py`.
- M5 Owner: writes to `scripts/reports/build_report.py`, `output/pdf/`.
- M6 Owner: writes ONLY to `reports/orchestrator/teamwork-red-team-2026-11-09.md`. Strictly read-only elsewhere.
- M7 Owner: writes to `tests/e2e/test_social_masterplan_e2e.py` (for clean tree assertion fix), `reports/orchestrator/masterplan-closeout-2026-11-09-final.md`, `log.md`, `README.md`.
