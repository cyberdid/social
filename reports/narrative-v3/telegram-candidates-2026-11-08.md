# Telegram narrative-v3 candidates — 2026-11-08

## Scope and result

The deterministic `narrative_v3.classify` rules processed **23,386** rows in the merged local Telegram snapshot; **1,438** were already labeled relevant by the existing collection pipeline. The rules emitted 1,007 posts with a recognized topic mention and 555 claim-candidate records.

These are candidate counts from an intentionally narrow Ukrainian/Russian vocabulary. They do not estimate prevalence outside this target panel, prove stance or truth, or establish classifier accuracy. No independent gold set was available; `semantic_accuracy=not_evaluated`.

## Output counts

| Dimension | Counts |
|---|---|
| Commitment | attributed: 1; debunk: 1; direct_assertion: 9; none: 883; reports: 3; unclear: 541 |
| Stance to candidate claim | not_applicable: 883; oppose: 1; reports_no_stance: 3; support: 9; unclear: 542 |
| Source language label | ?: 17; ru: 749; uk: 672 |
| Recognized topic family (post counts, multi-label) | people: 670; medical/doctor: 419; ambulance: 280; police: 252; basement: 224; TCC: 107; NGU: 124; detention: 11 |

## Reproducibility and limitations

- Input: `/home/cyberdid/Projects/Social/data/processed/20261105T101013Z+20261105T102914Z/posts_clean.jsonl`; SHA-256 `d229d8618021cf285f24c712eb9cd37ca85eb0e8bee2d8a7f74b6e7c574cda3f`.
- Classifier: `src/analysis/narrative_v3.py`; SHA-256 `70eb8db12f3ee0a9d11bc519d712e44e20dfb584681eb692d54b9f9e02112757`.
- Candidate JSONL remains outside Git at `/home/cyberdid/Downloads/SocialIncidentAnalysis/narrative-v3-2026-11-08/narrative_candidates.jsonl`; SHA-256 `0f936c498b8e985a3f48660bbc2626c3f535bc19fbd9b16bdfbeba6d93bb4267`.
- Only posts marked relevant in the existing snapshot were counted. This does not validate that relevance label.
- One source row contributes at most one post-level classification. Multi-label topic mentions are not independent observations.
- `message_span` points to the full source message. The extracted proposition does not yet have a separately validated character-level offset.
- Quotes, reports, denials, and unclear cases are retained as separate rule outputs. A stance label is a rule-produced candidate, not a verified interpretation.
- Do not treat a mention, claim candidate, stance, or repeated claim as a fact or independent evidence.
