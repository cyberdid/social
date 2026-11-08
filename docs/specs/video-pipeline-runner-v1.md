# Local Video Evidence Runner v1

## Purpose and limits

`src.analysis.video_pipeline_runner` is the repeatable local entry point for the existing technical video stages. It normalizes an acquisition manifest, indexes existing media with `ffprobe`, extracts periodic frames and audio with `ffmpeg`, and can optionally run OCR or ASR. It does not download media, decide whether a clip depicts the incident, verify recording time or location, identify speakers, or establish that a statement is true.

OCR and ASR output consists of candidate observations. It must be checked against the relevant original frame or audio before being quoted as evidence. Semantic validation is recorded as `not_performed` in the run receipt.

Raw media, run outputs, and derived assets must remain outside a Git checkout. The runner rejects output directories inside a checkout and rejects media paths inside a checkout. Checkout detection stops at filesystem boundaries, matching Git's default repository discovery behavior for mounted media and Downloads volumes. It does not move, rename, rewrite, or delete source media.

## Supported inputs

The first positional input is a JSONL manifest. Each non-empty line must be one JSON object.

### Telegram archive manifest

Use the existing archive schema and the default `telegram_archive` format. Only rows marked `downloaded_verified` by the archive adapter are forwarded to the technical indexer. The adapter validates the local file, declared size, digest format, and source URL. The media indexer independently hashes and probes the bytes, then the runner compares that verified digest with the archive's declared digest. A mismatch makes the index stage and overall run partial; it cannot be reported as a clean technical run.

```bash
python -m src.analysis.video_pipeline_runner \
  /data/social/case/archive.jsonl \
  /data/social/case/runs/video-run-01 \
  --derived-media-dir /data/social/derived/video
```

### Already-normalized local platform manifest

Use `--source-format local_media_manifest` for flat acquisition records such as TikTok and YouTube rows. Relevant fields are:

| Field | Requirement |
|---|---|
| `platform` | Platform label; optional, defaults to `unknown` in normalized rows. |
| `status` | `downloaded`, `downloaded_verified`, or `already_present` is eligible for local validation. Other statuses are retained in coverage totals and excluded from processing. |
| `url` or `source_locator` | Absolute HTTP(S) source URL. This is provenance only; it is never opened by the runner. |
| `local_file` or `local_path` | Existing local regular video file outside a Git checkout. Absolute paths are recommended. |
| `file_size_bytes` | Declared non-negative integer; must match the file. |
| `sha256` | Declared 64-character hexadecimal digest; must match the file. |
| `video_id`, `message_id`, or `id` | Optional external identifier used in a stable record key. |

Example:

```bash
python -m src.analysis.video_pipeline_runner \
  /data/social/case/public-platforms-manifest.jsonl \
  /data/social/case/runs/platform-video-run-01 \
  --source-format local_media_manifest \
  --derived-media-dir /data/social/derived/video
```

Failed or access-gated rows (including YouTube rows marked `download_failed`) remain visible in `source_coverage.platform_status_counts` and the normalization receipt's exclusion counts. The runner does not retry them, fetch them, or attempt to bypass a platform gate. Only locally present files whose size and SHA-256 match the manifest are sent to `ffprobe`.

The local adapter does not import captions, titles, or comments. It does not infer that a video is relevant to the incident. Unsupported file suffixes and malformed/missing metadata are recorded as exclusions.

## Stages and outputs

The runner writes these files under the external run directory:

| Stage | Output | Meaning |
|---|---|---|
| `source_normalization` | `index_input.jsonl`, `source_normalization.receipt.json` | Candidate local files with source provenance plus inclusion/exclusion accounting. `partial` means some input rows were excluded. |
| `index` | `media_index.jsonl` | Local file hashes, media type, `ffprobe` output, optional full decode checks, and comparison of declared versus verified source hashes. |
| `extraction` | `local_extraction.jsonl`, `local_extraction.jsonl.receipt.json` | Technical frame/audio derivatives and their hashes. |
| `text` | `text_observations.jsonl`, `text_observations.jsonl.receipt.json` | Optional OCR/ASR candidate observations. `skipped` by default. |
| Final run receipt | `run_manifest.json` | Deterministic run identity/configuration, code fingerprints, source coverage, per-stage state, artifact hashes, and limitations. |

The persistent derived-media directory stores content-addressed asset directories keyed by the source media SHA-256. Each directory contains the technical extraction receipt and generated frame/audio files. Matching valid derivatives are reused; conflicting or invalid existing asset directories are not overwritten.

## Run identity and safe resume

`run_id` is the first 20 hexadecimal characters of a SHA-256 over the canonicalized input manifest hash, source format, extraction options, first-line versions reported by `ffprobe`/`ffmpeg`/Tesseract, the OCR/ASR settings, local ASR model artifact fingerprints, configured Tesseract trained-data hashes, and source fingerprints for the Python pipeline components. Timestamps are excluded from the identity. A caller-declared revision is retained as provenance but never substitutes for the model-byte fingerprint. Changing the input snapshot, pipeline code, executable version, model bytes, trained data, or relevant options produces a different run ID. A run directory already bound to another ID is rejected.

Re-running with the same manifest and options is safe:

- The source normalization stage is deterministically regenerated.
- The media indexer reuses matching successful records and checkpoints unfinished records.
- The extractor verifies existing content-addressed derivatives and reuses them when source hashes and extraction parameters match. Per-record reuse flags are returned as runtime metadata but excluded from the canonical extraction JSONL; the receipt summary carries a reuse count so ordinary reruns retain the same extraction input identity for OCR/ASR.
- The OCR/ASR stage is skipped unless configured; when configured, output is reused only when its input/output hashes and complete recorded text-stage parameters match the active configuration. If an executable or model cannot be fingerprinted (for example, an unpinned remote ASR alias or unresolved system Tesseract data), the runner reruns text extraction instead of reusing a potentially stale result, including when an interrupted JSONL journal has no receipt.
- Stage state is checkpointed to `run_manifest.json`; an exception marks the active stage `failed` and later stages `not_run_after_failure`.
- Symlinked, hard-linked, or non-regular stage outputs are rejected before that stage runs, so indexer journaling cannot append through an unsafe pre-existing path.

Use a new run directory when changing the input snapshot, code, or pipeline parameters. Do not edit a manifest while the run is executing; the runner hashes it at the start and checks its bytes again before finalizing.

## Optional OCR and ASR

Both are disabled by default. OCR requires a local Tesseract executable and trained language data; ASR uses `faster-whisper` with the configured model. Enabling either is explicit and can require local model storage or a model download through that library. With the pinned `faster-whisper==1.1.0` environment, a remote model ID plus `--asr-model-revision` is rejected: that loader does not apply the requested revision. Supply an explicit local model snapshot directory instead; the pipeline fingerprints the actual files (including files reached through snapshot symlinks) and records the revision as provenance. Preloaded model objects cannot be byte-verified and are not cacheable. The runner itself makes no Gemini or other hosted API calls.

```bash
python -m src.analysis.video_pipeline_runner \
  /data/social/case/archive.jsonl \
  /data/social/case/runs/video-text-run-01 \
  --derived-media-dir /data/social/derived/video \
  --tesseract tesseract --languages ukr+rus+eng \
  --asr-model small --asr-model-revision '<pinned-model-revision>'
```

Configure only the stage(s) needed for a given run. An ASR model name without a pinned revision is recorded as an unpinned provider/model alias by the downstream text extractor; for repeatable research, supply a revision or use a local model artifact.

## Receipt statuses

- `completed_bounded`: all executed technical stages completed without row exclusions or partial statuses. This is not semantic verification.
- `completed_partial`: the pipeline ran, but some manifest rows were excluded, a declared media digest differed from verified bytes, or a technical stage returned partial results.
- `failed_with_receipt`: a stage raised an exception or the source manifest changed during the run. Inspect `run_manifest.json` and the failed stage's error.

Stage values include `running`, `completed`, `partial`, `reused`, `skipped`, `failed`, and `not_run_after_failure`. A `completed_partial` status is expected when an acquisition manifest contains both usable local files and unavailable/gated platform rows.

## Technical dependencies

- Python environment with the repository dependencies.
- `ffprobe` and `ffmpeg` available on `PATH`, or explicit `--ffprobe` and `--ffmpeg` executable paths.
- Optional `pytesseract`/Tesseract trained data for OCR as required by the existing text stage.
- Optional `faster-whisper` and a model for ASR. For the pinned `faster-whisper==1.1.0` environment, `requirements-video-local.txt` pins `av==18.1.0`; PyAV 19 removed an `av.open` argument still used by that faster-whisper release.

No model provider key, network search, or platform login is needed for the default local technical pipeline.

## Verification

The runner's unit tests cover stage ordering, optional text defaults, failure receipts, run snapshot binding, local-platform coverage handling, and a smoke path using tiny synthetic media and fake `ffprobe`/`ffmpeg` executables:

```bash
PYTHONPATH=. pytest -q tests/test_video_pipeline_runner.py
```

Passing these tests verifies stage orchestration and technical file handling. It does not validate the accuracy of OCR/ASR or the semantic relevance of any video.
