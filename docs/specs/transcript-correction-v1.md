# Transcript correction layer v1

## Purpose

Keep speech recognition useful for locating evidence while allowing clearly
mistaken wording to be repaired without rewriting the source transcript or
turning contextual inference into a verbatim quotation.

## Required layers

1. **Raw ASR** is immutable and identified by the media SHA-256, ASR model and
   model revision. Keep its original text, timestamps, language diagnostics and
   word-level diagnostics unchanged.
2. **Correction candidates** are separate records tied to an exact media hash
   and audio interval. Each record stores the raw span, proposed reading, basis,
   risk class and review status.
3. **Source-checked transcript** may be produced only after a person has checked
   the interval against the audio. It remains an edited transcript; it is not
   proof that the statement itself is true.

## Correction rules

- Correct an obvious orthographic or domain-term recognition error only as a
  separately labelled editorial candidate. Example classes include a common
  technical term whose phonetic ASR rendering is malformed.
- Use surrounding speech and independently captured copies to propose a
  reading, but do not use contextual plausibility alone to alter an alleged
  fact.
- Never silently normalize names, numbers, dates, locations, negation, speaker
  attribution, medical/legal claims, or contested allegations. Mark these for
  audio review; if they remain ambiguous, retain the raw text and abstain.
- Do not repair grammar in a way that changes who did what, certainty, tense,
  modality, or the force of a statement. Preserve disfluencies where they
  affect meaning.
- A correction made from external context is not “verified from audio.”
  Context may identify terminology but cannot establish what the speaker said.
- Model confidence and agreement are triage signals, not calibrated
  probabilities or independent evidence of truth.
- A corrected reading is quote-safe only after the audio interval is checked.
  Even then, the proposition requires separate factual verification.

## Status vocabulary

- `candidate_contextual`: plausible language/domain repair; not checked against
  audio; not quote-safe.
- `needs_audio_review`: competing readings or material content; do not choose a
  corrected wording.
- `verified_from_audio`: the cited audio interval was checked and the wording
  is sufficiently clear; this does not verify the claim's factual content.
- `formatting_only`: punctuation/spacing presentation change only; it remains
  `quote_safe: false` until the audio itself is reviewed. If the interval is
  reviewed and the wording is clear, use `verified_from_audio` instead.
- `rejected`: candidate was checked and not supported by the audio.

## Output contract

Use `schemas/transcript_correction.schema.json`. Store private transcript text
and media locators with the source evidence outside Git where required by the
project's data-handling policy. Public reports should contain aggregate
coverage, model details, hashes where safe, unresolved categories and explicit
limits; do not publish raw personal or medical allegations just to demonstrate
the pipeline.

## Validation

- Verify media SHA-256 and interval bounds before attaching a correction.
- Reject corrections for a different asset hash or an invalid/empty interval.
- `verified_from_audio` requires `review.method: audio_listening`, an
  `audio_review` basis, and `quote_safe: true`. An independent reference
  transcript alone cannot establish that the recorded audio contains the same
  wording.
- All other statuses require `quote_safe: false`; in particular,
  `formatting_only` is not evidence that the audio wording was checked.
- The JSON Schema checks field types and non-negative bounds; the semantic
  contract validator must additionally enforce `end_ms > start_ms` because
  JSON Schema cannot compare these sibling values with the current schema.
- Preserve raw transcript bytes and provide a diff for every proposed edit.
- Check that material fields (names, numbers, negation, locations, legal and
  medical claims) stay `needs_audio_review` unless an audio review record
  exists.
- Do not report WER/CER without an independently prepared reference transcript.
- Keep audio transcription review distinct from claim verification and event
  attribution.
