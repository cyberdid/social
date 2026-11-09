# TikTok OCR pilot — 2026-11-07

## Result

- Local TikTok assets processed: **20**; unique SHA-256 assets: **20**.
- Technical index: **20/20** successful; strict full decode: **20/20** passed.
- Local frame/audio extraction: **20/20** complete.
- OCR: **20/20** complete over **296** periodically sampled frames; **7,856** candidate spans were emitted.
- ASR: **not configured** for this run.

OCR output is noisy and is a candidate transcription only. Every span must be checked against its source frame before quotation or use in an event claim. Text seen in-frame does not establish recording time, location, scene identity, or the truth of a caption.

## Reproducibility

- Source manifest: `$SOCIAL_MEDIA_ROOT/public-platforms-manifest.jsonl`.
- Technical index SHA-256: `93dda8e8e9a33c5396b3acb04e5997ced237696de6f0c319943bfb08142913b1`.
- Local extraction SHA-256: `52250aa5f77c4944dca29b1a4f6ebd0bf7af49182feeb13919618d3deb64ba52`.
- OCR candidates SHA-256: `08e5085ceb144fa310afc139ab3f5b0ed93acda61f9cb0667813c3d869f278ac`.
- Raw media, frames, audio, and OCR JSONL remain outside the repository.

## Scope limits

The public-platform collection contained 21 TikTok source records: 20 local verified media files and one unavailable item. These results describe only those collected files and sampled frames; they are not a complete TikTok search or a semantic validation benchmark.
