# Video and Transcript Engineering Workstream Report (M3 / R3)

**Document ID:** `reports/orchestrator/teamwork-video-2026-11-08.md`  
**Milestone:** M3 (Video and Transcript Engineering) / Requirement R3  
**Working Directory:** `/home/cyberdid/Projects/Social/.worktrees/social-master-plan`  
**Execution Timestamp:** 2026-11-08T19:35:00Z  
**Branch:** `codex/social-master-plan`  
**Status:** COMPLETE (Technical decode & candidate sidecar verified; Quote safety strictly blocked pending acoustic listening)

---

## 1. Executive Summary

Milestone M3 (Requirement R3) of the Social Master Plan v1.1 closeout establishes strict engineering controls, cryptographic verification, and epistemological boundaries across the video analysis and automated speech recognition (ASR) pipelines.

### Key Outcomes:
1. **Immutable Raw ASR Preservation:** Confirmed that raw speech-to-text outputs for the entire Telegram corpus (607 unique video assets, 10,872 candidate segments, 10,462,222 bytes, SHA-256 `987ee53ff56a477e86347509786ed5d1bc7f5e908bb18037c202bb023ff43912`) remain **100% unmodified and write-protected**.
2. **Technical Decoding Completeness:** Verified strict technical full decoding (`ffmpeg -xerror` to null sink) across **607/607 unique Telegram assets** (9,472,884,834 bytes) and **20/20 local TikTok assets**, with zero stream errors and zero duplicate IDs.
3. **ASR Candidate Queue Processing:** Evaluated the second-pass candidate queue across 7 prioritized assets comparing `Systran/faster-whisper-small` and `mobiuslabsgmbh/faster-whisper-large-v3-turbo` (407 vs 344 segments; 333 review alignments, 10 lexical differences, 1 punctuation difference).
4. **Strict Schema & Quote-Safety Invariants:** Validated all 10 candidate correction records against `schemas/transcript_correction.schema.json`. Because human acoustic listening was not performed, **10/10 candidates strictly retain `quote_safe: false`**.
5. **Sensitive Medical & Legal Terms Safeguards:** All consequential phrases—including alleged spinal fractures ("перелом хребта") and legal labels ("СЗЧ-шники")—were strictly classified as `status: needs_audio_review` with `candidate_text` restrained or omitted, preventing unverified editorial smoothing.
6. **Semantic Interval Validation:** Verified that `end_ms > start_ms` is strictly enforced for 100% of candidate intervals (0 violations).
7. **Automated Verification:** Added comprehensive regression tests in `tests/test_video_transcript_correction.py`; verified that **77/77 video pipeline and contract tests pass** (`PYTHONPATH=. pytest tests/test_video_*.py tests/test_contracts.py`).

---

## 2. Technical Media Corpus Inventory and Extraction State

The local video evidence corpus consists of two authorized collections: Telegram source archives and TikTok public platform downloads.

### 2.1. Telegram Video Corpus
- **Manifest Source:** `/home/cyberdid/Downloads/SocialIncidentVideos/telegram/manifest.jsonl` (806 rows, SHA-256 `50ef4d23b5c5c064c62cbc9ffd82fdc44feeb7a2f459cd7d1bafae992769057f`).
- **Archive Categorization:** 775 publication records with verified local files, 29 non-video attachments, and 2 metadata-only rows.
- **Deduplication:** The 775 publication rows resolve to **607 unique media assets** by byte SHA-256, totaling 9,472,884,834 bytes.
- **Strict Full Decode:** `reports/video-pipeline/telegram-full-decode-2026-11-08.md` documents complete stream decoding of all 607 unique assets:
  - `media_index.status == ok`: 607/607
  - `decode_check.status == passed`: 607/607
  - Byte size & SHA-256 match input manifest: 607/607
  - Duplicate asset IDs in final index: 0
- **Derivative Extractions:**
  - Keyframes: 8,679 periodic visual keyframes extracted across 607 assets.
  - Audio streams: 602 extracted WAV streams; 5 assets contained no audio stream.
  - Optical Character Recognition (OCR): 245,289 candidate spans extracted across 607 assets (`reports/video-pipeline/telegram-ocr-candidate-batch-2026-11-08.md`).

### 2.2. TikTok Corpus & Runner Status
- **Public Platform Manifest:** 75 source rows (SHA-256 `6a1a6b6a181056dc0f67b105b48f4e1adc66d4e7ac2f1320af4c62530c77e618`).
- **Local Coverage:** 20 unique local TikTok videos; 55 platform rows (54 YouTube, 1 TikTok) were not locally available.
- **Runner State:** `completed_partial`. No external re-scraping or access bypassing was attempted.
- **Extraction:** 20/20 assets achieved `ffprobe == ok`, full decode passed, 296 frames analyzed, 8,440 OCR candidate spans extracted (`reports/video-pipeline/tiktok-runner-2026-11-08.md`).
- **Excluded Desktop Media:** 10 unmapped video files identified in `Telegram Desktop` without verifiable provenance links or manifest rows were formally excluded from processing.

---

## 3. ASR Architecture and Raw Data Immutability

### 3.1. Raw First-Pass Speech-to-Text
The first-pass baseline ASR extraction ran locally on CPU using int8 quantization:
- **Model:** `Systran/faster-whisper-small` (revision `536b0662742c02347bc0e980a01041f333bce120`).
- **Runtime Fingerprint:** `d57a3446f178e1eafdd82b9b63cd298f48f61fdfdafaaa3e6adbb0ee462afde7`.
- **Processing Coverage:** 607 unique assets evaluated:
  - `complete` (>= 1 segment returned): 558 assets
  - `no_segments_returned`: 44 assets (does not prove acoustic silence)
  - `audio_not_available`: 5 assets (no audio track)
  - Total candidate segments: 10,872 timestamped segments
- **Container Duration:** 12.04 aggregate video container hours (not audio or speech duration).

### 3.2. Absolute Raw Immutability Guarantee
In accordance with Rule R3 and PROJECT.md Feature 16:
- **File Location:** `/home/cyberdid/Downloads/SocialIncidentVideos/telegram/analysis/asr-bulk-20261108/telegram_text_observations.jsonl`.
- **File Permissions:** `0600` (directory `0700`).
- **File Byte Size:** `10,462,222 bytes`.
- **SHA-256 Digest:** `987ee53ff56a477e86347509786ed5d1bc7f5e908bb18037c202bb023ff43912`.
- **Audit Verification:** Verified on disk during this milestone; zero bytes modified, zero records overwritten.

---

## 4. Second-Pass ASR Candidate Queue & Sidecar Processing

To evaluate low-confidence incident-related terms without modifying baseline files, a targeted second-pass ASR was executed on **7 prioritized assets** using a larger model architecture:
- **Second-Pass Model:** `mobiuslabsgmbh/faster-whisper-large-v3-turbo` (revision `0a363e9161cbc7ed1431c9597a8ceaf0c4f78fcf`, CPU/int8).
- **Segment Volumes:** 407 first-pass segments vs 344 second-pass segments.
- **Alignment Disagreements:** 333 alignment spans flagged for review, 10 lexical candidates, 1 punctuation candidate. (These counts reflect segmentation differences between models, not an error rate).

### 4.1. Correction Candidate Queue Invariants
The sidecar contains 10 structured correction records stored at:
- **Sidecar Path:** `/home/cyberdid/Downloads/SocialIncidentVideos/telegram/analysis/asr-correction-second-pass-20261108/correction_candidates.jsonl`
- **Sidecar SHA-256:** `cfcf8ec7bffc2585ff3545141c8d34b12ba7ef71b9709b2b0b6b66060594cad3`
- **File Mode:** `0600`

| # | Correction ID | Interval (ms) | Status | Quote-Safe | Raw Wording | Candidate Wording | Rationale & Invariant Enforcement |
|---|---|---|---|:---:|---|---|---|
| 1 | `corr-3c5-opening-editorial-reading` | 0 – 5200 | `candidate_contextual` | **false** | `Дивіться, це будинок – це тимчасовий пункт дислотасії підрозділ на Ціннамі Гвардії,` | `Дивіться, це будинок — тимчасовий пункт дислокації підрозділу Національної гвардії…` | Truncated fragment; ellipsis marks boundary; disfluency ("це") smoothed editorially. Not a verbatim quotation. |
| 2 | `corr-3c5-dislokatsii` | 2920 – 3520 | `candidate_contextual` | **false** | `дислотасії` | `дислокації` | Lexical normalization based on second ASR pass; acoustic audio not listened. |
| 3 | `corr-3c5-national-guard` | 4040 – 5240 | `candidate_contextual` | **false** | `Ціннамі Гвардії` | `Національної гвардії` | Institutional entity repair supported by second model pass; unverified by audio. |
| 4 | `corr-3c5-training-center` | 20800 – 27700 | `candidate_contextual` | **false** | `начальний центр` | `навчальний центр` | Orthographic domain repair; acoustic listening pending. |
| 5 | `corr-3c5-unit-cohesion` | 31500 – 37000 | `needs_audio_review` | **false** | `злагочення підрозділ` | `злагодження підрозділів` | Term "злагодження" plausible, but case/number unresolved. Held for review. |
| 6 | `corr-3c5-pd-location` | 61600 – 65400 | `needs_audio_review` | **false** | `офіційні пути постійно десь локація` | `офіційні пункти постійної дислокації` | Abbreviation "ППД" context suggests term, but exact speaker wording unknown. |
| 7 | `corr-3c5-spinal-fracture` | 65900 – 68940 | `needs_audio_review` | **false** | `перелуманим грифтом дати` | `з переломаним хребтом, те, що кажуть лікарі` | **Medical injury claim.** Models disagree sharply. Held strictly for acoustic and factual verification. |
| 8 | `corr-ece68-medical-wording` | 169600 – 179600 | `needs_audio_review` | **false** | `15 фонів; три сича/свища; некротизована тканина` | *None* | Inconsistent/unnatural medical text in ASR. Candidate text suppressed. |
| 9 | `corr-ece68-quantity-allegations` | 144000 – 178000 | `needs_audio_review` | **false** | `Уривок із сумами, строками перебування та медичними твердженнями` | *None* | Numbers, periods of stay, and medical allegations. Suppressed to prevent editorial hallucination. |
| 10 | `corr-3c5-szch-label` | 132200 – 142100 | `needs_audio_review` | **false** | `ці сазачешники` | `ці СЗЧ-шники` | **Legal status label.** Imposes criminal/disciplinary attribution. Audio review and legal ground truth required. |

---

## 5. Contractual and Schema Integrity Validation

### 5.1. JSON Schema Invariants (`schemas/transcript_correction.schema.json`)
The transcript correction contract enforces two strict `allOf` rules:
1. `status == "verified_from_audio"` requires:
   - `quote_safe: true`
   - `review.method: "audio_listening"` (independent reference transcripts are disqualified from certifying audio verification)
   - `basis` must contain `"audio_review"`
2. `status in ["candidate_contextual", "needs_audio_review", "formatting_only", "rejected"]` requires:
   - `quote_safe: false`

### 5.2. Semantic Interval Duration Rule
The schema validator in `src/contracts.py:37-43` programmatically enforces that `end_ms > start_ms`. All 10 sidecar candidate intervals satisfy this constraint:
- 0 to 5,200 ms (+5,200 ms)
- 2,920 to 3,520 ms (+600 ms)
- 4,040 to 5,240 ms (+1,200 ms)
- 20,800 to 27,700 ms (+6,900 ms)
- 31,500 to 37,000 ms (+5,500 ms)
- 61,600 to 65,400 ms (+3,800 ms)
- 65,900 to 68,940 ms (+3,040 ms)
- 169,600 to 179,600 ms (+10,000 ms)
- 144,000 to 178,000 ms (+34,000 ms)
- 132,200 to 142,100 ms (+9,900 ms)
Zero intervals are inverted, zero-length, or negative.

### 5.3. External Cloud Provider Fallback Audit
- **Gemini 3.8 Flash High:** Interactive attempt to transcribe the 5.2s audio clip returned Google safety filter blocks on both attempts.
- **Gemini 4 Argon High:** One-shot request returned individual quota exhaustion.
- **Result:** 0 words, 0 characters, and 0 tokens from external AI models were incorporated into the sidecar or repository.

---

## 6. Verification and Regression Testing

A dedicated test suite was implemented in `tests/test_video_transcript_correction.py` covering:
- Schema validation of valid contextual candidates.
- Rejection of inverted or empty intervals (`end_ms <= start_ms`).
- Strict enforcement of `quote_safe: false` for all unverified statuses.
- Rejection of `quote_safe: true` without `audio_listening` method.
- Live file invariant auditing across all 10 records in `correction_candidates.jsonl`.
- Cryptographic hash checks of the sidecar and raw ASR files.
- Integrity verification of `reports/video-pipeline/asr-correction-receipt-2026-11-08.json`.

### Verification Command & Output
```bash
PYTHONPATH=. /home/cyberdid/Projects/Social/.venv/bin/pytest tests/test_video_*.py tests/test_contracts.py
```
```
============================= test session starts ==============================
platform linux -- Python 3.13.14, pytest-9.2.0, pluggy-1.7.0
rootdir: /home/cyberdid/Projects/Social/.worktrees/social-master-plan
collected 77 items

tests/test_video_archive_adapter.py .....                                [  6%]
tests/test_video_local_extract.py .............                          [ 23%]
tests/test_video_pipeline_runner.py .......................              [ 53%]
tests/test_video_text_extract.py ..............                          [ 71%]
tests/test_video_transcript_correction.py ............                   [ 87%]
tests/test_contracts.py ..........                                       [100%]

============================== 77 passed in 1.48s ==============================
```
Full repository test execution confirmed **683 passed in 5.24s** with zero regressions.

---

## 7. Epistemological and Evidentiary Boundaries

1. **ASR as Locator, Not Evidence:** Speech recognition segments are search locators for finding audio timestamps, not verbatim evidence of what was spoken or proof that an utterance is true.
2. **No WER / CER Gold Benchmarks:** Word Error Rate (WER) and Character Error Rate (CER) cannot be calculated because no independent human reference transcripts exist for the corpus.
3. **Uncalibrated Model Confidence:** Token log-probabilities and Whisper model confidence metrics are triage heuristics, not calibrated probabilities of lexical correctness.
4. **Editorial Smoothing vs Acoustic Reality:** Removing disfluencies (such as repeated "це") or inserting ellipses constitutes editorial structuring; it must never be represented as spoken dialogue.
5. **Medical and Legal Claims Independence:** Transcripts reporting that an individual had a broken spine or committed unauthorized absence (СЗЧ) are statements of claim, not physical evidence of injury or legal proof of military status.
6. **Corpus Coverage Limit:** The remaining 600 Telegram video assets remain at unverified first-pass ASR status.

---

## 8. Milestone M3 Closeout Status

| Gate / Requirement | Description | Status | Verification Receipt |
|---|---|:---:|---|
| **Raw ASR Protection** | Raw STT outputs write-protected and hash-verified | **CLOSED** | `987ee53ff56a477e86347509786ed5d1bc7f5e908bb18037c202bb023ff43912` |
| **Strict Technical Decode** | 607/607 Telegram media decoded to null sink | **CLOSED** | `reports/video-pipeline/telegram-full-decode-2026-11-08.md` |
| **Sidecar Schema Contract** | JSON Schema and interval validation enforced | **CLOSED** | `schemas/transcript_correction.schema.json` & `tests/test_contracts.py` |
| **Candidate Queue Review** | 7-asset queue processed with second-pass ASR | **CLOSED** | `reports/video-pipeline/asr-correction-receipt-2026-11-08.json` |
| **Sensitive Lexicon Defense** | Fracture & СЗЧ terms flagged `needs_audio_review` | **CLOSED** | `correction_candidates.jsonl` (records #7, #8, #9, #10) |
| **Quote-Safety Invariant** | `quote_safe: false` enforced for non-audio records | **CLOSED** | 10/10 candidates marked `quote_safe: false` |
| **Acoustic Audio Listening** | Human acoustic verification of audio tracks | **BLOCKED / NOT COMPLETE** | Requires human acoustic listening panel |
| **Media-to-Event Linking** | Visual/acoustic match to physical event chronology | **OPEN** | Requires independent geolocation/time-of-day proof |
