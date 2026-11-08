# Automated case-run aggregate receipt — 8 November 2026

- Run: `run-post-fix`; status: **partial**; as-of: `2026-11-08T01:14:07Z`.
- Observation window: `2026-11-02T09:00:00Z` to `2026-11-05T10:31:42.738963Z` (UTC).
- Processing was offline and deterministic on already collected snapshots; no new platform collection or model inference occurred.

> **Retrieval validity correction:** this Markdown is a superseding report. The 9,769-hit figure below is historical execution telemetry from a run whose configured zero query budget was bypassed by the old runner substituting `top_k=20`; it is invalid for compliant retrieval/analysis and is not a search-coverage measure. See the [retrieval-validity addendum](retrieval-validity-addendum-2026-11-08.md). A separate, budgeted source-linked run searched 555 candidate claims against 30 passages using 1,110 directions and returned 11,897 candidate matches; it accepted 0 evidence assessments and emitted 0 `VerificationResult`s ([receipt](source-linked-case-run-2026-11-08.md)).

## Integrated results

- **Historical claim-retrieval telemetry (invalid):** the old `run-post-fix` artifacts record 555 claim candidates, 23 archived passages, and 9,769 passage hits, with **0 claim verification results**. Because the zero query budget was bypassed, the hit count is not compliant retrieval or search coverage. This historical metric is retained only to describe the defective run.
- **Event reconstruction:** 574 communication/event-mention candidates preserved; 0 physical-event timeline rows; 574 unresolved mentions. No event time or filming time was established.
- **Conflict analysis:** 0 typed physical-event records and 0 position records supplied; 13 information-attention bins. Empty physical inputs are a coverage gap, not evidence of no physical action.
- **Telegram information dynamics:** 1,438 posts across 158 channels; snapshot counter sum 119,515,745 (not unique reach); 13 six-hour publication bins; peak 511 posts per bin.
- **Uncertainty:** 1,438 records have unknown narrative label and channel group; scenario bounds are [0, 1], not confidence intervals.
- **Evaluation:** structural hard gates passed with 0 failures; report files verified: 3; semantic accuracy remains not evaluated.

## Crosswalk and collection limits

- Legacy channel labels in the current relevant panel: A=8, B=19, C=87, D=26, E=5, U=13 (158 total). Within C, 26 manual and 61 auto-only. These labels do not establish origin, orientation, state control, or operation participation.
- Direct comparison of the historical and current positive-relevant channel sets gives 158 shared channels, 1 historical-only channel, and 0 current-only. The historical-only channel had 1 relevant post and is absent from the current merged file; this reconciles the denominator as a snapshot-membership difference, but the reason for its absence is unknown.
- Historical posts_clean SHA-256: `4e859d407aef52c72a8e690dc5716d7d92d11ff7d7a164760db5a4c0ad334350`; current merged posts_clean SHA-256: `d229d8618021cf285f24c712eb9cd37ca85eb0e8bee2d8a7f74b6e7c574cda3f`.
- Whole-corpus source-lineage registry has 2,823 candidate edges, but independent source roots are not established; these edges were not mapped to claims in this run.
- Source watch: 9 first-baseline pages and 3 access errors. A first baseline does not establish a new update.
- Local media index: 12 records; 12 unique indexed assets; 12 full technical decodes passed; no OCR/ASR observation or verification claim was added from this index.
- ASR pilot: 6 unique clips, 93 candidate segments; auto-language output was uk=3, ru=2, ko=1. No reference transcripts or adjudication exist; no accuracy metric is available. ASR was not run on the current 12-asset index.
- GPU check: RTX 4060 Laptop (compute 8.9), driver 610.57.04; system Python lacks CTranslate2 and resolves libcublas.so.13, while the prior large-v3 attempt failed on missing libcublas.so.12. GPU ASR remains blocked pending a compatible runtime.
- Gemini visual pilot: 1 clip and 3 sampled frames (0/5/10 s); candidate-only observation, not continuous review or an accuracy benchmark.
- TikTok metadata supplied 21 video `create_time/createTime` timestamps among 42 candidate links; 19 timestamped videos (18 accounts) fall inside the window, 2 outside, and 21 photo links lack a platform timestamp. Publication time is not filming time.
- YouTube and Instagram receipts were not supplied as typed evidence in this case run; platform coverage remains incomplete.

## Reproducibility and interpretation

- The retrieval addendum supersedes this report's prior retrieval interpretation. `run_receipt.json` records the historical `summary.md` digest `959834ba2d2900ce4d136d81418ff71c987e8dd8708bc241054711fbda885d2b`; a pre-correction check found the then-current Markdown digest was already different (`cd61ca5b2fdd8ee95c901c9e87fe2706f747d7d7e6f8c56e8842b5854c7ef0fa`). This revision changes the Markdown again, so the receipt does not authenticate the current Markdown bytes. The receipt's recorded `claim_retrieval_summary.json` digest remains unchanged and matched that file when checked; the receipt and hashed JSON are preserved.

- The machine-readable sanitized summaries and their hashes are in `run_receipt.json`. The private input manifest and full case artifacts remain outside Git because they contain source text and identifiers.
- Recorded runner commit is the base code revision; working tree was dirty at execution. The frozen structural control suite passed 6/6; this is not an independent semantic audit.
- No real-case historical report diff was run: no earlier machine-readable report receipt bundle was available. A synthetic replay/diff control passed separately.
- Synthetic replay control passed for two as-of snapshots, supersession/invalidation, and report diff; no earlier real-case report receipt existed for an incident-level diff. Distinguish the masterplan orchestrator receipt (`reports/orchestrator/masterplan-2026-11-08/`): it was a zero-target dry-run with no collection and downstream stages `not_run`. The separate typed-input integration run is documented in `reports/orchestrator/w00-integration-receipt-2026-11-08.md`; it ran local components but returned zero claim-verification results and does not establish incident facts.
- This run supports only descriptive statements about the supplied snapshot. It does not establish claim truth, physical-event chronology, unique reach, source independence, coordination, attribution, or causation.

## Semantic and primary-record gaps

- No independently adjudicated narrative labels or claim-scope spans; no semantic entailment, source authenticity, or claim verification evaluation.
- No primary medical records, court orders, docket documents, or independently checked event-time/filming-time evidence were ingested into this run.
- No independent source-root mapping for candidate posts; repeated reporting may share one origin.
- No typed primary physical-event or participant-position records; therefore the run does not reconstruct physical conflict, identify participants, infer motives, or establish causality.
- Official/press materials and media reports require separate source-specific attribution; absence from this input set does not disprove an event or proceeding.

## Post-run checks — 2026-11-08

- **Claim bookkeeping:** input hashes and counts were checked; 555 private follow-up projections now carry only `unverified` status because evidence search is incomplete. They accept no support or refutation. The original case-run's 0 verification results remains accurate; details and limits are in [claim_matrix.md](claim_matrix.md).
- **Real replay:** the private input manifest's 8/8 artifacts matched by hash and size; all 16 outputs were recreated, 9 byte-identical. Seven contain only new run/time metadata and dependent receipt digests. The 23 passages have no explicit URL/source locator and no populated source offset, so the replay does not prove a passage-to-primary-source locator. See [real replay receipt](real-replay-receipt-2026-11-08.md).
- **Telegram ASR:** separate CPU/int8 processing covered 607 unique archive assets, yielding 558 `complete`, 44 `no_segments_returned`, 5 `audio_not_available`, and 10,872 timestamped candidate segments. No reference transcript is available; accuracy and meaning remain unevaluated. See [ASR batch receipt](../video-pipeline/telegram-asr-bulk-2026-11-08.md).
- **Incremental operations:** a fixed allowlist dispatcher was exercised using synthetic correction data. No real claim or report was recomputed because no accepted typed correction evidence was available. See [Phase 10 receipt](../orchestrator/phase10-recomputation-dispatch-2026-11-08.md).
- **Cross-platform publication candidates:** a separate follow-up aligned three descriptive publication-time series: Telegram (1,438 posts/158 channels), YouTube (408 lexical metadata candidates/180 channels), and TikTok (19 timestamped videos/18 accounts). Selection methods differ; extractor timestamps are not independently adjudicated; the last bin is truncated at the IncidentSpec end. No source lineage, initiation, event time, or causal influence was established. See [aggregate report and input hashes](../cross-platform-publication-candidates-2026-11-08.md).
