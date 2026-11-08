# Telegram video pipeline run — 2026-11-07

## Result

- Archive: **806** post records — 775 verified local video records, 29 non-video records, 2 metadata-only records.
- Deduplicated downloaded assets: **607** (9,472,884,834 bytes claimed by archive metadata).
- Technical index: **775/775** rows have `ffprobe` status `ok`; unique assets: **607**. Full decode was not requested for this 607-asset set.
- Local extraction: **775/775** rows complete across 607 unique assets; **8,679** periodic frames; audio status `{'extracted': 602, 'not_present': 5}`; aggregate video-container duration 12.04 hours.
- Controlled 12-video pilot: 12/12 strict full decodes passed; 12/12 extractions completed; OCR completed for 12/12, reading 117 sampled frames and emitting 3,661 candidate word spans.

## OCR observation

On the fire-video sample, OCR recovered visible overlay candidates: **05.11.26, Борщагівка, Софіївська**. These words are readable in-frame content only. They do not establish when or where the recording was made, nor prove that it depicts the incident under study. The OCR set also contains substantial noise, so none of its spans are accepted as quotations without checking the source frame.

## ASR and semantic model status

ASR was not run in the current 12-video pipeline pass. Earlier `small` model outputs were not reliable enough to cite; the one-clip `large-v3` GPU attempt failed because `libcublas.so.12` was unavailable. A previous single-video Gemini 3.8 Flash High run remains candidate-only and is not a measured accuracy benchmark. The reusable pipeline does not yet integrate a semantic video provider or independent VAD intervals.

## Reproducibility

- Run ID: `telegram-archive-20261107T2130Z`.
- Archive manifest SHA-256: `50ef4d23b5c5c064c62cbc9ffd82fdc44feeb7a2f459cd7d1bafae992769057f`.
- Technical index SHA-256: `09493c32cd040d3c0b1e37b63787bbf30c56661cd1a7f4ff726825f8756274b6`.
- Local extraction JSONL SHA-256: `9d988e67b1ee0d92afdc884aee0c6ae7e68342f8a287cdf2c0e41f202feefb4d`.
- Extraction receipt SHA-256: `03ea28e26f296e6cba0dcb0e167f139c513a00c8c810fa30c22045dc60d8d800`.
- Pilot OCR JSONL SHA-256: `408529941962d79e840ba120118395b977b2751d266afbd508843bfff6988f91`.
- Pilot OCR receipt SHA-256: `3e418cf9c942e8e735eef9d8bd9ca33c1cb12a8b43004f228726769e0756edde`.
- Raw media, frame/audio derivatives, and OCR/ASR JSONL remain outside the repository. This report contains aggregates and hashes only.

## Scope limits

This run establishes successful collection of a targeted Telegram archive, file/index integrity, and availability of periodic frame/audio derivatives. It does not establish completeness of Telegram coverage, scene identity, recording date, geolocation, speaker identity, truth of captions, or causation.

## Follow-up ASR batch — 2026-11-08

A separate local CPU/int8 pass subsequently processed all **607 unique assets** in this archive and emitted 10,872 candidate segments. It is not an ASR accuracy evaluation: reference transcripts are unavailable, the text was not independently adjudicated, and output must be checked against original audio. See the [aggregate ASR receipt](telegram-asr-bulk-2026-11-08.md); the transcript JSONL and per-asset records remain outside Git.
