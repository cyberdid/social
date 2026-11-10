# Multimodal implementation and evidence audit

Baseline: f0e9d0d67422b0c286a2cb9e7d4e935a833a9533. Audit 2026-11-10. Code was read directly; the historical 607-asset decode and ASR jobs were not rerun during this publication audit. No model API calls were made by the current audit.

| Component | Concrete implementation | Input/output | Status and validation |
|---|---|---|---|
| Local technical index | `src/media_pipeline.py:42,75,105,375` (`sha256_file`, `probe_media`, `decode_media`, `index_manifest`) | Local manifest to hashes, ffprobe metadata, full ffmpeg decode receipts | Implemented, unit/integration tested; technical file readability only |
| Bounded media runner | `src/analysis/video_pipeline_runner.py:148,339,407,468,544` | Archive adapter to index, audio/frame derivatives, optional OCR/ASR | Implemented; local paths, nonoverwriting/atomic outputs, model/config/code fingerprints; not wired to general incident runner |
| Derivatives | `src/analysis/video_local_extract.py:166,312` | Video to sampled frames and audio with checksums | Implemented local extraction with verified cache; sampling may omit brief evidence |
| Candidate text | `src/analysis/video_text_extract.py` | Tesseract TSV word boxes and faster-whisper timestamped segments | Implemented optional local models; candidates, no assertion that words or content are true |
| Perceptual comparison | `src/analysis/media_fingerprints.py:45,59,80,156,199` | Sampled pHash63/dHash64 and crop/mirror variants to candidate overlap/offset | Implemented; Hamming thresholds10/12, shorter-window consistent coverage>=0.6, >=3distinctframes/hashes, >=2s span; explicitly uncalibrated |
| ASR correction | `schemas/transcript_correction.schema.json`; 7-asset correction receipt | Original/alternative/aligned candidate text and uncertainty | Implemented sidecars, 10lexical candidates all quote_safe=false; no contextual reconstruction of inaudible words |
| Gemini feasibility pilot | `reports/video-pipeline/gemini-keyframe-pilot-2026-11-08.md` | 3stillframes from one15.278s clip through user Agy CLI | Reported external feasibility run, not an automated runner integration or video/audio verification |

## Denominator and provenance reconciliation

* `telegram-full-decode-2026-11-08.md`:806archive rows,775downloaded-verified source-post rows,607uniqueSHA256assets,9,472,884,834bytes;607/607strictdecodechecks passed. This is a historical receipt, not a new rerun or 607validated scenes.
* `telegram-archive-2026-11-07.json` plus bulk receipt:8,679frames,602audioavailable,5withoutaudio,12.04hours summed containerduration. Do not repeat the earlier case-draft's14.2audiohours: the inspected bulk receipt does not support that value. Container time is not speech duration.
* `telegram-asr-bulk-2026-11-08.md`:607uniqueassets,10,872candidate segments;558complete,44no_segments_returned,5audio_not_available. CPU/int8 faster-whisper1.1.0 with Systran/faster-whisper-small revision536b0662742c02347bc0e980a01041f333bce120. This is coverage, not semantic accuracy.
* `asr-correction-review-2026-11-08.md`:7selectedassets,407firstpass versus344secondpasssegments; larger model mobiuslabsgmbh/faster-whisper-large-v3-turbo revision0a363e9161cbc7ed1431c9597a8ceaf0c4f78fcf.333alignmentcandidates,10lexicalcandidates+1punctuation. No independent listening record. Not a corpus-wide model comparison.
* `asr_calibration_benchmark_2026-11-09.json`:18supplied-referenceclips,415referencewords,185errors (micro44.58%,macro41.61%);2617referencechars,598errors (micro22.85%,macro20.72%). Reference strings, clip list and review flags are supplied in the builder. A worker label `human_acoustic_listening`/`worker_video_semantics` does not identify an independently verified human listener.10quote_safe flags are recorded, not independently demonstrated quotation safety.
* `gemini-keyframe-pilot-2026-11-08.md`:reported56,606tokens for blocked fullvideo attempt and36,703 for isolated3keyframe run;92,309reportedtotal. No monetary cost measured. No Gemini/Agy call exists in current src/scripts (`rg` inspected). Model observations are not independent evidence.
* `reports/automated-case-run-2026-11-08/media_index_summary.json` describes a separate12assetpilot, not the607assetarchive. Keep these scopes separate.

## Technical versus semantic assurance

SHA256 identifies byte equality; decode checks readability. Neither establishes authenticity, date, place, identity, allegation truth or causal linkage. OCR/ASR are candidate extraction. Frame offsets are relative media alignment, not recording/upload time or copy direction. Camera-visible content still needs contextual verification. No geolocation accuracy benchmark or multimodal event-truth benchmark is available.
