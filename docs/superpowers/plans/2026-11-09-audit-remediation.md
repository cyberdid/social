# Social Audit Remediation Implementation Plan

> **For agentic workers:** This plan is executed in the isolated worktree `$SOCIAL_REPO_ROOT`.

**Goal:** Remove unsupported quantitative and geographic claims, correct evidentiary scope and provenance, validate autonomous retrieval on held-out claims, and synchronize the published report artifacts.

**Architecture:** Keep source facts and generated reporting separate. Figure generation must consume verified data or clearly display limited coverage. Claim verification must search the captured evidence corpus without manually forcing a primary passage, preserve uncertainty for physical claims supported only by institutional denials, and keep source provenance explicit. Regenerate the report only after upstream data and wording are corrected.

**Tech Stack:** Python 3, existing deterministic retrieval and ReportLab/PDF build scripts, JSON/JSONL provenance artifacts, Poppler PDF inspection.

**Spec:** User-provided audit findings in the active conversation; supporting repository audit at `docs/audit-v2.0-feedback.md` and `reports/orchestrator/teamwork-red-team-2026-11-09.md`.

## Global Constraints

- Never present hardcoded illustrative values as measured results.
- Do not infer video geolocation from locality names or a schematic.
- Distinguish an official denial from independent refutation of a physical fact.
- Keep the verifier deterministic and scoped to its captured evidence corpus; describe that scope accurately.
- No absolute machine-specific paths in tracked outputs or reusable scripts.
- Run the requested held-out end-to-end verification and the relevant project checks.

---

### Task 1: Correct reaction and location figures

**Files:** `scripts/reports/generate_report_figures.py`, generated audience/map PNGs, and the related captions in `scripts/reports/build_report.py`.

- Replace unsupported 533-thread status and reaction totals with a visualization of the documented 10-comment/3-thread parity sample and explicit full-corpus unavailability, or remove the figure if it cannot be represented without implying population coverage.
- Replace the arbitrary coordinate grid with a clearly non-scale comparison of separately reported events. Remove the 4.2 km claim and any claim that the fire video is geolocated to either incident site.
- Keep event dates, locality names, source attribution, and uncertainty visible.

**Acceptance:** No unsourced reaction values, fake scale, unsupported distance, or categorical video-location conclusion remains in the generated images or report text.

### Task 2: Correct fire source provenance and physical-claim epistemics

**Files:** `data/raw/official_bulletins/kyiv_ova_fire_20261105.txt`, `scripts/analysis/build_core_claims_verification.py`, generated evidence-verification JSON/Markdown, and report source notes.

- Replace the untraceable “official bulletin” transcription with source-attributed, timestamped evidence whose saved artifact and source URL agree; preserve conflicting updates on casualties and locality.
- Keep the warehouse-fire occurrence distinct from claims about the specific TikTok video and from claims about casualties.
- Physical claims 01/02 may retain official denial as contradicting evidence, but cannot be labelled independently refuted without qualifying independent physical evidence.
- Preserve v2.1's existing insufficient-evidence treatment for injury causality, video location, and TCC presence.

**Acceptance:** Every fire-related passage resolves to a traceable source/version; official statements are represented as statements; no underlying physical claim is over-resolved.

### Task 3: Remove forced passage selection and validate held-out claims

**Files:** `src/analysis/claim_verification.py`, `scripts/analysis/build_core_claims_verification.py`, `tests/test_blind_claim_verification.py`, and focused verification tests.

- Remove runtime dependence on manually assigned `primary_passage_id` and `counter_passage_ids`; use ranked retrieval over the captured evidence corpus and infer relations only from retrieved candidates.
- Preserve `expected_relation` and `target_status` only in test fixtures/ground truth, never production inference.
- Add held-out claims absent from `build_core_claims_spec`, with no manually designated passage IDs; assert that retrieval finds relevant source passages and that insufficient/conflicting evidence abstains.
- Report the verifier accurately as retrieval and deterministic relation inference over the captured corpus; do not imply open-web source discovery.

**Acceptance:** The held-out end-to-end test passes without forced passage IDs, and all existing 25-claim outputs are regenerated from retrieval rather than seeded primary passages.

### Task 4: Calibrate timeline wording, remove local paths, synchronize closeout, rebuild and inspect PDFs

**Files:** `scripts/analysis/build_physical_event_timeline.py`, `scripts/analysis/build_asr_calibration_benchmark.py`, `scripts/provenance/build_lineage_matrix.py`, `reports/source-watch/latest.json`, generated benchmark/lineage/closeout reports, `scripts/reports/build_report.py`, `output/pdf/*` and the PDF manifest.

- Describe physical chronology as curated reconstruction from listed source mentions; replace uncalibrated probability-like confidence scores with qualitative evidence tiers or explicitly labelled analyst judgements.
- Make private ASR inputs configurable and replace absolute sample-machine command paths with repository-relative commands.
- Update the v2.0 closeout as an explicitly historical record and generate a v2.1 remediation status with current totals and remaining limitations.
- Rebuild report PDFs, check manifest hashes/page counts/text, and visually inspect changed pages.

**Acceptance:** No stale v2.0 totals are presented as current; tracked build inputs are portable; PDF figures and text agree with the machine-readable results and render without overlap.
