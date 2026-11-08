# Telegram MTProto reactions: units, snapshots, and privacy review

**Checked:** 8 November 2026 against Telegram's official MTProto documentation and the current Social implementation.  
**Scope:** read-only methods/code review; no live Telegram request was made for this note.

## Verified API behavior

- `messages.getMessagesReactions(peer, ids)` is a user-only method returning `Updates`. A matching `updateMessageReactions` carries a `MessageReactions` object. Telegram documents invalid/private-channel and invalid-message errors. The method returns current reaction information; it does not provide a historical series. ([method reference](https://core.telegram.org/method/messages.getMessagesReactions), [reaction API](https://core.telegram.org/api/reactions))
- `MessageReactions.results` is a vector of `ReactionCount` entries. The object can also carry `recent_reactions` and `top_reactors`. Its `min` flag identifies a reduced observation that may omit the current user's own reaction; `messages.getMessagesReactions` can provide the full aggregate information. ([constructor reference](https://core.telegram.org/constructor/messageReactions))
- Telegram distinguishes aggregate retrieval from `messages.getMessageReactionsList`, whose response contains reacting peers and user/chat objects. The list method is a separate deanonymizing surface; Social's aggregate-only design correctly avoids it. ([list method](https://core.telegram.org/method/messages.getMessageReactionsList))
- Telegram documents paid Star reactions as a separate `reactionPaid` type. Sending a paid reaction with amount `count` increments the Star reaction counter by that `count`; therefore a paid count is a platform payment quantity, not necessarily a count of distinct people. ([reaction API, paid reactions](https://core.telegram.org/api/reactions))
- The API documentation mentions short polling every 15–30 seconds for visible messages in a client UI. That is a client freshness behavior, not a justified cadence for research collection. Social's one-shot, explicit snapshot approach should remain bounded and should not imitate UI polling at scale. ([reaction API](https://core.telegram.org/api/reactions))

## Consequence for Social's current aggregation

`src/tg_comments_collect.py::serialize_reaction_snapshot` preserves a typed `paid` entry and also sums all typed counts into the compatibility field `legacy_total`. Preserving this legacy sum is reasonable for compatibility only if every analytical consumer uses `reaction_state` plus the typed vector and does not interpret the scalar as unique people, votes, or approval.

`src/analysis/audience_aggregation.py` currently computes `largest_available_reaction_comments` by summing every count in an `available` vector. For Telegram, this adds paid Star quantities to ordinary/custom emoji reaction counts. That composite ranking mixes units. It can rank a comment highly because of Star amount even when it has fewer reacting users. It must not be described as the most-supported comment or as a user-count measure.

## Recommended measurement contract

1. Keep the raw per-type vector unchanged and keep the legacy total only for compatibility.
2. For descriptive Telegram reaction-count ranking, compute a clearly named `non_paid_reaction_count` from `emoji` and `custom_emoji` rows only; state that it counts platform reaction instances, not unique users or support for every claim in the comment.
3. Report `paid_star_amount` separately, in Stars/reaction-count units. Do not add it to non-paid reaction counts and do not use it as evidence of audience size or claim endorsement.
4. Keep unknown reaction constructors separate. If the type cannot be assigned a known unit, abstain from any combined ranking that would include it.
5. Keep `current_user_excluded`, `not_reported`, `empty`, `no_update`, and `request_failed` distinct; only a complete `available` snapshot can enter the non-paid ranking.
6. If the project needs a neutral all-types count for compatibility, label it as an API aggregate sum with mixed units and do not use it for ranking or substantive interpretation.

## Implementation impact (review finding, not yet changed)

- **P0 for report validity:** adjust `src/analysis/audience_aggregation.py` and the corresponding views/schema in `src/analysis/audience_response_reporting.py` so the Telegram ranking excludes paid counts and exposes Stars separately. Add regression tests mixing `emoji`, `custom_emoji`, `paid`, and `unknown` entries. Preserve other platforms' own ranking semantics; do not force cross-platform comparability.
- Update `docs/specs/audience-response-v1.md` so the documented “sum of latest selected reaction snapshot” is explicitly platform- and unit-aware, including Telegram's paid Stars distinction.
- The collector and refresh adapter currently ignore `recent_reactions` and `top_reactors` in the serialized output. Preserve that allowlist: do not serialize those identity-bearing objects even when an API response contains them.

This finding is about measurement units, not whether a commenter supports the comment's political claim. Even standard emoji reactions are an engagement signal whose meaning depends on platform/context; they are not universal stance labels.
