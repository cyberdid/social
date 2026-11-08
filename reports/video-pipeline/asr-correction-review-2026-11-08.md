# ASR correction review — 8 November 2026

## Scope and result

A second ASR hypothesis was generated for **7 of 607** Telegram video assets,
prioritized by incident-related vocabulary and low-confidence first-pass terms.
The comparison contains 407 first-pass segments and 344 second-pass segments.
It is a targeted lexical review, not a representative accuracy sample.

Two local ASR configurations were compared:

- First pass: `Systran/faster-whisper-small`, revision
  `536b0662742c02347bc0e980a01041f333bce120`, CPU/int8.
- Second pass: `mobiuslabsgmbh/faster-whisper-large-v3-turbo`, revision
  `0a363e9161cbc7ed1431c9597a8ceaf0c4f78fcf`, CPU/int8.

The second pass improved the *candidate wording* of several clear military
terms in the official-interview clip: `дислокації`, `Національної гвардії`,
and `навчальний центр`. These three are stored as contextual editorial
candidates, with the original ASR preserved. The military term `злагодження`
is plausible, but the phrase's case/number is unresolved and now requires audio
review. None is **quote-safe** because the audio was not independently
listened to in this run.

The 0–5.2 s opening fragment is **not** treated as a complete reconstructed
sentence. The longer first- and second-pass hypotheses contain additional
text after 5.2 s, while this correction record covers only 0–5.2 s. Because
the boundary has not been independently listened to, syntax and inflection
remain unsettled. The sidecar keeps a contextual editorial reading with an
ellipsis to mark an incomplete excerpt, plus the separate bounded word/term
candidates; it preserves the original ASR wording and marks every record
`quote_safe: false`. The ellipsis marks the excerpt boundary, not verified
continuity or spoken words. The two hypotheses disagree on a repeated `це` and
punctuation; omitting that disfluency is editorial smoothing, not a verified
word-level correction.

## Material disagreements

Most comparison spans differed substantially in wording or segmentation: 333
alignment candidates were marked for review, 10 as lexical candidates, and one
as punctuation-only. Those counts are alignment outcomes, **not an error rate**;
the two models segment speech differently and neither output is ground truth.

We left medical descriptions, alleged injuries, people counts, number ranges,
names/titles, negation, and legal claims unresolved where the hypotheses
disagreed or the words were materially consequential. In particular, a
possible reference to a spinal fracture is not repaired from context. The
transcript cannot establish that an injury occurred, when it occurred, or what
caused it. A phonetic rendering that may refer to “СЗЧ-шники” is held for
audio review because the label asserts a legally consequential status; it is
not evidence that the people had that status.

## Correction record and reproducibility

- Detailed correction candidates: private
  `/home/cyberdid/Downloads/SocialIncidentVideos/telegram/analysis/asr-correction-second-pass-20261108/correction_candidates.jsonl`
- File mode: `0600`; parent directory: `0700`.
- Correction records were schema-validated against
  `schemas/transcript_correction.schema.json`.
- First-pass ASR JSONL SHA-256:
  `987ee53ff56a477e86347509786ed5d1bc7f5e908bb18037c202bb023ff43912`.
- Second-pass output SHA-256:
  `a982735d47252b0dfe785b74f00df9f8beaf0f7fb068af7e61ad5046da76d91f`.
- Correction sidecar SHA-256:
  `cfcf8ec7bffc2585ff3545141c8d34b12ba7ef71b9709b2b0b6b66060594cad3`.
  The original sidecar digest was
  `8ec996bdd937d6f957a01ad5324470c8b7a724cb28d72fd58f7339a7460c5f87`;
  only the opening candidate's excerpt marker and limitation notes changed.
- Both ASR hypotheses in this review came from local CPU runs; no Gemini
  transcript or cloud ASR output contributed to them. A later interactive AGY
  terminal session authenticated Gemini 3.8 Flash High and supplied the 5.2 s
  opening clip for an independent transcription attempt. Gemini blocked both
  requested responses with its safety filter; no usable transcript or audio
  correction resulted, and no Gemini wording was added to the sidecar. The
  account's exact token charge was not independently verified. A separate
  visual keyframe pilot is documented in
  [the Gemini keyframe pilot report](gemini-keyframe-pilot-2026-11-08.md).
  A subsequent one-shot AGY request to Gemini 4 Argon High for the same
  5.2-second interval returned an individual-quota error before producing a
  response; no transcript was obtained and no further provider attempt was made.

Raw ASR was not overwritten. A correction becomes quote-safe only after a
reviewer checks the exact audio interval. Even then, that verifies wording,
not the truth of the utterance. No independent reference transcript exists,
so WER/CER and transcription accuracy were not evaluated. ASR token
probabilities are uncalibrated diagnostics, not probabilities that a word is
correct.

## Operational implication

The pipeline now has a versioned correction-record contract and a case-specific
candidate sidecar. It does **not** automatically “repair” all 607 transcripts.
The other 600 assets remain at first-pass status; uncertain spans should be
reported as unresolved rather than rewritten into plausible-sounding claims.
