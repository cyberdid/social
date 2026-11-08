# Telegram ASR batch — 2026-11-08

## Coverage and outcome

The local CPU/int8 batch processed **607 unique video assets** from 775 Telegram source-post records. All 607 unique input asset hashes have exactly one output record; no output asset is missing or unexpected, and there are no duplicate output record IDs or analysis keys. The output contains **10,872 timestamped candidate segments**. All segment `start_ms`/`end_ms` values passed structural bounds checks.

| ASR status | Assets | Interpretation |
|---|---:|---|
| `complete` | 558 | The recognizer returned one or more candidate segments. This does not establish transcription accuracy. |
| `no_segments_returned` | 44 | No segments were returned; this is not evidence that the asset contains silence. |
| `audio_not_available` | 5 | The extraction did not provide an audio stream for ASR. |

This is a processing-coverage result only. No independent reference transcripts or human adjudication were available, so WER/CER, language-detection accuracy, speaker identity, and semantic truth were **not evaluated**. ASR output is a locator for reviewing the original audio; it must not be cited as verified speech or used alone to establish an event. Language labels are diagnostics only.

## Correction follow-up

A targeted second ASR pass compared 7 of these 607 files. The candidate-only
review and its handling of ambiguous wording are recorded in
[`asr-correction-review-2026-11-08.md`](asr-correction-review-2026-11-08.md).
Raw first-pass text remains unchanged. The second pass does not establish WER,
quote accuracy, medical facts, or event attribution.

## Reproducibility and privacy

- Model: `Systran/faster-whisper-small`, revision `536b0662742c02347bc0e980a01041f333bce120`.
- Runtime recorded by the batch: `faster-whisper==1.1.0`, CPU, `int8`; model fingerprint: `d57a3446f178e1eafdd82b9b63cd298f48f61fdfdafaaa3e6adbb0ee462afde7`.
- Input extraction JSONL SHA-256: `9d988e67b1ee0d92afdc884aee0c6ae7e68342f8a287cdf2c0e41f202feefb4d`.
- Output JSONL SHA-256: `987ee53ff56a477e86347509786ed5d1bc7f5e908bb18037c202bb023ff43912` (**10,462,222 bytes**).
- The 775 source-post links in the extraction resolve to the 607 deduplicated asset records; ASR was run once per unique asset.
- Aggregate video-container duration is 12.04 hours; this is not an audio-duration or speech-duration measure.
- Per-asset hashes, source identifiers, paths, audio, and transcript text remain outside the repository. This receipt contains aggregate results and corpus-level file hashes only.

