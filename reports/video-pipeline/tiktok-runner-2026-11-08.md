# TikTok video pipeline run — 2026-11-08

## Scope

The runner processed the locally available items from the existing public-platform manifest. It performed source-manifest normalization, SHA-256 validation, `ffprobe` indexing, strict full decode, local frame/audio extraction, and OCR. It did not download media, use ASR, call a hosted model, or assess whether a clip depicts the incident.

Raw media, extracted frames/audio, OCR candidate output, and the run receipt remain under `/home/cyberdid/Downloads/SocialIncidentVideos`, outside this Git worktree. No OCR text is copied into this report.

## Results

| Measure | Result |
|---|---:|
| Input manifest rows | 75 |
| Locally available TikTok videos | 20 |
| Unique indexed assets | 20 |
| `ffprobe` status | 20/20 `ok` |
| Declared vs verified SHA-256 mismatches | 0 |
| Strict full decode | 20/20 completed |
| Local extraction | 20/20 completed |
| OCR | 20/20 completed; 296 sampled frames; 8,440 candidate spans |
| ASR | Not configured (20 records) |
| Not locally available | 55 rows: 54 YouTube and 1 TikTok `download_failed` |
| Overall runner status | `completed_partial` because 55 input rows had no local media |
| Runtime | About 4m 23s |

The 55 unavailable rows remain in the coverage receipt and were not retried. No access challenge or platform gate was bypassed. Every OCR result is candidate text and requires checking against the original frame before quotation or factual use.

## Reproducibility

- Runner: `src.analysis.video_pipeline_runner`
- Run ID: `4be4e4232de646765282`
- Source manifest SHA-256: `6a1a6b6a181056dc0f67b105b48f4e1adc66d4e7ac2f1320af4c62530c77e618`
- Run receipt: `/home/cyberdid/Downloads/SocialIncidentVideos/runs/tiktok-video-pipeline-2026-11-08/run_manifest.json`
- Media index: `/home/cyberdid/Downloads/SocialIncidentVideos/runs/tiktok-video-pipeline-2026-11-08/media_index.jsonl`
- Extraction manifest: `/home/cyberdid/Downloads/SocialIncidentVideos/runs/tiktok-video-pipeline-2026-11-08/local_extraction.jsonl`
- OCR candidate output: `/home/cyberdid/Downloads/SocialIncidentVideos/runs/tiktok-video-pipeline-2026-11-08/text_observations.jsonl`
- Tool versions, configuration, per-stage artifact hashes, source coverage, and code fingerprints are stored in the run receipt.

This run demonstrates repeatable local technical processing for the 20 available TikTok files. It does not establish event identity, filming date, location, speaker identity, claim truth, or completeness of TikTok/YouTube coverage.
