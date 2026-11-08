# Telegram ASR pilot — 2026-11-08

## Scope and result

A local ASR pilot processed **6 unique Telegram video assets** selected across three duration bands (two each: up to 30 seconds, 31–120 seconds, and 121–180 seconds). All six produced `asr:complete`; the output contains **93 timestamped transcript candidate segments**. OCR was not run in this pass.

Automatic language detection returned Ukrainian for 3 assets, Russian for 2, and Korean for 1. That out-of-domain label is an explicit signal that language detection requires review on this material. It does not establish the true spoken language, and the segment count is not a transcript-accuracy metric.

The purpose was to verify the local processing path on a small sample before considering a larger run. No word-error rate or content-accuracy result is claimed: the pilot has no independently prepared reference transcripts and was not manually adjudicated. ASR output remains an unverified candidate and must not be quoted as fact without checking the original audio.

## Reproducibility

- Model family: `Systran/faster-whisper-small`
- Model revision: `536b0662742c02347bc0e980a01041f333bce120`
- Runtime: `faster-whisper==1.1.0`, CPU, `int8`
- PyAV: `18.1.0`; the optional ASR requirements now pin this compatible version because PyAV 19 removed an argument still used by the pinned faster-whisper release. See the [faster-whisper decoder source](https://github.com/SYSTRAN/faster-whisper/blob/master/faster_whisper/audio.py) and [PyAV release notes](https://github.com/PyAV-Org/PyAV/releases).
- Input subset SHA-256: `c1928b5365c2013b0e08811e0de1dd0d3a9c2d530e433c317582c7d569ecafae`
- ASR output SHA-256: `fc0a0f49359f43a0846f96949acf5b346a2a1424e7af4b2985d6594a67f62de1`
- Local input, transcript candidates, failed compatibility attempt, and receipts remain under `/home/cyberdid/Downloads/SocialIncidentVideos/telegram/analysis/asr-small-pilot-20261108/`.

No transcript text is copied into this report or repository. The model output should be used only as a locator for listening to the corresponding original segment. The pilot does not justify ASR processing of all 607 Telegram assets until language/recognition quality is checked on a suitable reference sample.
