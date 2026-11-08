# Telegram OCR candidate batch — 2026-11-08

## Result

The local OCR pass completed for the Telegram video archive derivative set. The input contained **775 source-manifest rows representing 607 unique video assets**. OCR status was `complete` for all 607 unique assets; the batch recorded **zero skipped source rows**. ASR was not configured, so the receipt reports `asr:not_configured` for all 607 assets.

These counts describe processing coverage. They do not mean that every frame or every visible word was captured, and they do not establish what happened in the incident.

## Provenance and reproducibility

| Stage | Receipt / artifact | SHA-256 |
|---|---|---|
| Technical media index | `media_index.jsonl` | `09493c32cd040d3c0b1e37b63787bbf30c56661cd1a7f4ff726825f8756274b6` |
| Local frame/audio extraction | `local_extraction.jsonl` | `9d988e67b1ee0d92afdc884aee0c6ae7e68342f8a287cdf2c0e41f202feefb4d` |
| OCR candidate output | `ocr_candidates.jsonl` | `50f8db18d2b6c5fb124bc4d2396532d25ff5ecddd959d11ffe8724f98df6dfec` |

The OCR producer was `social.analysis.video_text_extract@1.0`. It used Tesseract 5.3.4 with `ukr+rus+eng`, CPU mode, and `int8` compute configuration. The archived input was processed from `/home/cyberdid/Downloads/SocialIncidentVideos/telegram/analysis/20261107T2130Z/local_extraction.jsonl`; the candidate output and receipt are under `/home/cyberdid/Downloads/SocialIncidentVideos/telegram/analysis/20261108T0000Z/`. The raw videos and derived OCR records remain outside the repository.

The output file's hash is recorded here without copying or quoting recognized text. The external receipt records the same input/output hashes and the software configuration.

## Interpretation limits

- OCR output is a **candidate text observation** tied to sampled frames. It may omit, misread, or mis-segment text; the engine's confidence values are not calibrated probabilities.
- OCR alone does not verify a caption, speaker, identity, event date, location, continuity, or whether a clip depicts the incident under study.
- No ASR transcript was produced. No standalone VAD interval output was configured.
- An OCR match is not independent corroboration when the same text is copied across posts or overlaid onto derivative videos.
- No claim-level semantic review or external accuracy benchmark was performed in this batch.
- The archive is a targeted set of collected public Telegram posts, not a census of Telegram or all incident-related video.

For evidentiary use, resolve a candidate back to its original media hash and frame/time locator, inspect the relevant source segment, preserve its provenance, and assess it against independent evidence. The OCR batch itself supports only the technical statement that OCR processing completed for the listed unique assets.
