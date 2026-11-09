# AGY Gemini Teamwork Handoff: Master Plan v2.0
## Autonomous Execution of End-to-End Evidence Verification & Analytical Synthesis

**Для:** Власника проєкту для запуску Teamwork з Gemini 3.8 Flash.  
**Підготовлено:** 9 листопада 2026 року.  
**Цільовий план:** `docs/plans/social-master-plan-v2.0.md`.  
**Статус:** Готовий промпт для запуску.

---

## 📋 Промпт для запуску Teamwork (Готовий до копіювання)

```markdown
Autonomous execution of Social Master Plan v2.0 in the local repository, closing the five critical gaps identified in the external review of November 8, 2026: Evidence Verification (20–30 core claims), Physical Incident Reconstruction, Video/ASR Calibration, Corpus Versioning Lineage, and Full Analytical A4 PDF Dossier Restoration.

Working directory: $SOCIAL_REPO_ROOT
Integrity mode: development

## Reference Material
- Master Plan v2.0: `docs/plans/social-master-plan-v2.0.md`
- Master Plan v1.2: `docs/plans/social-master-plan-v1.2.md`
- Previous Closeout: `reports/orchestrator/masterplan-closeout-2026-11-08-final.md`
- Review Document: External evaluation of November 8, 2026 (score 87/100, 5 key bottlenecks)
- Core source modules: `src/analysis/claim_verification.py`, `src/analysis/event_reconstruction.py`, `scripts/reports/build_report.py`

## Requirements

### R1. Core Claims & Evidence Verification (Owner: worker_claims_evidence)
Extract a prioritized bundle of 20–30 core claims regarding the Petropavlivska Borshchahivka incident (injuries, 26 persons in building, 130 identified persons, 4 NGU injuries, fire timing, TCK presence, court arrest of 22-year-old woman). Process each claim through `claim_verification.py` against official passage bundles with exact character offsets. Establish deterministic relations (supports, contradicts, rebuts, contextualizes) and generate the first accepted VerificationResult records with counter-evidence checks. Output to `reports/evidence-verification/core_claims_verification_2026-11-09.{md,json}`.

### R2. Physical Incident Reconstruction (Owner: worker_event_reconstruction)
Construct a structured Physical Event Timeline strictly separated from communication mentions using `event_reconstruction.py`. Define at least 5 structured physical events (street confrontation, building confrontation, law enforcement arrival, fire ignition, detention) with temporal intervals, confidence, participant positions, and explicit unresolved constraints. Output to `reports/event-reconstruction/physical_event_timeline_2026-11-09.{md,json}`.

### R3. Video & ASR Semantic Calibration (Owner: worker_video_semantics)
Select a stratified calibration sample of 15–20 representative audio clips from the 607 Telegram videos. Produce verified acoustic reference transcripts, compute baseline Word Error Rate (WER) and Character Error Rate (CER), evaluate scene semantics, and transition validated records to `quote_safe: true`. Output to `reports/video-pipeline/asr_calibration_benchmark_2026-11-09.{md,json}`.

### R4. Corpus & Source-Watch Lineage Matrix (Owner: worker_corpus_provenance)
Harmonize corpus discrepancies between historical (1,408 posts, 159 channels) and merged (1,438 posts, 158 channels) datasets, and reconcile Source Watch runs (10/12 vs 9/12). Formulate a strict provenance rule where every metric and assertion in reports links to an exact `(corpus_version, run_id, timestamp)`. Output to `reports/provenance/corpus_and_sourcewatch_lineage_matrix_2026-11-09.{md,json}`.

### R5. Analytical Report Aesthetics & A4 Dossier Restoration (Owner: worker_report_publisher)
Upgrade report generation in `scripts/reports/build_report.py` to restore the comprehensive 25–30 page A4 analytical dossier. Embed high-resolution charts (temporal wave, coordination graph, reaction distribution, geospatial map), maintain an executive analytical narrative, and relegate technical execution logs and raw manifests to structured Appendices. Generate `output/pdf/petropavlivska_borshchahivka_report_2026-11-09.pdf` and update `output/pdf/manifest-2026-11-09.json`.

### R6. Independent Adversarial Red-Team Review (Owner: worker_red_team)
Conduct a read-only adversarial audit of the 20–30 claim verification results, physical timeline boundaries, citation offsets, and visual PDF rendering. Output findings with severity ratings and locators to `reports/orchestrator/teamwork-red-team-2026-11-09.md`.

### R7. Integration, Master Plan Synthesis & Test Suite Pass (Owner: worker_integrator_lead)
Integrate all workstream outputs, produce `reports/orchestrator/masterplan-closeout-2026-11-09-final.md`, update `log.md` and `README.md`. Verify that 100% of the repository test suite (745+ tests, plus new verification tests) passes cleanly.

## Acceptance Criteria
- [ ] At least 20 prioritized core claims have accepted `VerificationResult` records with exact passage locators.
- [ ] Physical event timeline contains at least 5 structured physical events with explicit temporal bounds.
- [ ] ASR calibration benchmark computes empirical WER/CER on 15+ reference clips.
- [ ] Corpus lineage matrix unifies all historical vs merged numbers with zero dangling citations.
- [ ] Restored A4 PDF report is 25+ pages with embedded charts and technical appendices.
- [ ] Red-team report completed with zero unaddressed critical findings.
- [ ] Full test suite (`pytest tests/`) passes 100% cleanly.
- [ ] Zero leaked credentials, private tokens, or reactor identities.
```
