# W14 — Audience Response Intelligence Engine v1

**Status:** Accepted component design; typed Telegram reaction capture, bounded MTProto refresh adapter, contracts, target/abstention validation, frame-conditional aggregation, and structured report gates are implemented in the 8 November 2026 worktree. **Semantic classifiers and their local accuracy remain unimplemented / not evaluated.**
**Scope:** Descriptive analysis of collected online comments and their platform feedback. This component does not estimate Ukrainian population opinion, verify incident facts, identify anonymous users, or infer private psychological states.

## Repository audit

The existing Telegram comment collector is `src/tg_comments_collect.py` and uses Telethon/MTProto. It reads each comment's `Message.reactions.results` but stores only their sum in the legacy numeric `reactions` field (zero when no reaction object was returned). The record already retains the observation time (`fetched_at`), source post and comment IDs, reply pointer, top-level indicator, a pseudonymized discussion-chat key, and an HMAC pseudonym for the author. Thread completion/capping is recorded separately in `threads.jsonl`.

The captured 6 November snapshot contains 39,598 comments in 533 targeted threads. It includes one reaction total per comment at collection time, but no reaction-type breakdown and no earlier reaction snapshots. The old breakdown cannot be recovered from those totals. The sampling frame is targeted and active threads were prioritized; it is not a platform-wide sample.

`src/tg_collect.py` already preserves per-type aggregate reactions for channel posts as `{r, n}` pairs. W14 should use an explicit typed schema for comment reactions while retaining the comment collector's legacy `reactions` integer for downstream compatibility.

## Verified MTProto behavior

- A `MessageReactions.results` vector contains `ReactionCount` objects with a reaction type and a count. Reaction types include standard emoji, custom emoji (document ID), and paid reactions. Preserve the raw type and platform count; do not interpret paid-reaction counts as people or votes. See [Telegram message reactions](https://core.telegram.org/api/reactions) and the [MessageReactions constructor](https://core.telegram.org/constructor/messageReactions).
- `messages.getMessagesReactions(peer, ids)` can fetch current aggregate reactions for one or more messages. Telegram marks it user-only and documents `CHANNEL_PRIVATE` and invalid-channel/message errors. The public method documentation does not specify an administrator requirement. This is a current snapshot endpoint, not a history endpoint. See [`messages.getMessagesReactions`](https://core.telegram.org/method/messages.getMessagesReactions).
- When `MessageReactions.min` is true, the received aggregate can omit the current user's own reaction; use `messages.getMessagesReactions` for full reaction information or mark the observation as `current_user_excluded`. Never silently treat this state as complete.
- `messages.getMessageReactionsList` returns reacting peers and is distinct from aggregate counts. Telegram documents `BROADCAST_FORBIDDEN` for channel-post reaction lists to prevent deanonymization. Social must not collect reaction identities; it stores aggregate counts only. See [`messages.getMessageReactionsList`](https://core.telegram.org/method/messages.getMessageReactionsList).
- Channel comments are messages in the linked discussion supergroup. A request for a comment's reaction state must use the discussion peer and the comment message ID, not the source channel post ID. See [Telegram discussion groups](https://core.telegram.org/api/discussion).
- Reaction changes are exposed as updates/current state. Social must create its own timestamped snapshots to study change over time; historical values are not reconstructed by a later query. Respect flood-wait responses and do not poll at client UI intervals as a bulk research schedule.

## P0 comment reaction contract

Keep `reactions` as the existing integer sum for legacy readers. Add:

```json
{
  "reaction_breakdown": [
    {"kind": "emoji", "key": "👍", "count": 12},
    {"kind": "custom_emoji", "key": "document:123456789", "count": 3},
    {"kind": "paid", "key": "paid", "count": 5}
  ],
  "reaction_state": "available",
  "reaction_observed_at": "2026-11-08T12:00:00+00:00"
}
```

`reaction_state` is one of:

- `not_reported`: the MTProto `Message` had no `MessageReactions` object. This is not a new-schema zero.
- `empty`: an object was present, had an empty `results` vector, and was not marked `min`.
- `available`: a non-empty aggregate was present and not marked `min`.
- `current_user_excluded`: `MessageReactions.min` was set. The observed vector may be retained, but it is not represented as a complete aggregate.

The bounded `messages.getMessagesReactions` refresh adapter also returns a separate `request_status`. `ok` means a matching message update was returned; only then is a reaction observation timestamped. `no_update` means no matching update for the requested message ID was returned. `wrong_peer_update` means an update with that message ID was returned for a different peer. Both non-observation statuses carry `reaction_state=null` and `reaction_breakdown=null`; they are request outcomes, not reaction snapshots, and must not be converted to `not_reported` or zero. A matching update whose `reactions` field is absent remains `request_status=ok` with `reaction_state=not_reported`. Request failures carry `request_status=request_failed` and no reaction observation.

Audience aggregate output is schema `1.1` and records all four refresh outcomes (`ok`, `request_failed`, `no_update`, `wrong_peer_update`). The report validator continues to read schema `1.0` aggregates, where only `ok` and `request_failed` were recorded. It renders the two newer statuses as `not_recorded` for 1.0 input; an actual observed count of zero remains the numeric `0` in schema 1.1.
- `not_collected`: the field is absent in an older record.

`reaction_breakdown` is `null` for `not_reported`, an empty list for `empty`, and a list for `available` or `current_user_excluded`. `reaction_observed_at` records the time the collector observed the vector; for the initial collector it uses that row's `fetched_at`. Counts are non-negative integers. Custom emoji identifiers are serialized as decimal strings so JSON consumers do not lose 64-bit precision. Unknown future reaction constructors are preserved as `kind: "unknown"` with their constructor name and raw count.

An `available` snapshot must have a non-empty vector. A `current_user_excluded` snapshot may have an explicitly empty vector because a min-marked response can omit the current account's reaction while reporting no aggregate entries.

The compatibility total must equal the sum of the typed counts for observed vectors. In `current_user_excluded`, it remains the sum of the observed partial vector and must not be presented as a complete total. The legacy zero on `not_reported` is retained solely for compatibility; W14 analytics use `reaction_state` and `reaction_breakdown`.

### Unit independence: Telegram Stars vs emoji reactions

Telegram MTProto provides distinct reaction constructors: standard emoji (`reactionEmoji`), custom document emoji (`reactionCustomEmoji`), and paid Telegram Stars (`reactionPaid`). These represent fundamentally different measurement units and must maintain strict unit independence:

1. **Measurement unit separation**: Paid Star reactions count financial platform currency units, not distinct individuals or consensus votes. A single user can send multiple Stars in one interaction (e.g. 50 or 500 Stars), incrementing the counter by that currency amount. In contrast, standard and custom emoji reactions count non-paid reaction instances.
2. **Comment ranking segregation**: In `largest_available_reaction_comments`, rankings within each platform frame are computed strictly from `non_paid_reaction_count` (the sum of `emoji` and `custom_emoji` instances). Paid Star reactions (`kind == "paid"` or `reaction_type == "paid"`) are decoupled and segregated. They must never mix into or inflate non-paid emoji reaction counts, preventing financial payments from distorting descriptive comment rankings.
3. **Unknown reaction types**: Any unrecognized future reaction constructor (`kind == "unknown"` or `reaction_type == "unknown"`) is segregated from non-paid emoji rankings and preserved separately.
4. **No endorsement or population inference**: Neither emoji reaction counts nor paid Star quantities may be interpreted as unique people, endorsements of claims contained in a comment, or proxies for Ukrainian or general public opinion. Exposure is unavailable, and reaction behavior is highly non-random and platform-conditioned.

## Analytical dimensions and invariants

Each comment may have multiple topics, claims, stance targets, sentiment targets, and expressed emotions. `target_id` must resolve to a versioned Social `Claim`, `Entity`, `Event`, or explicitly registered action/statement. A broad target such as “police” is not interchangeable with a specific action or statement.

Sentiment, expressed emotion, stance, discussion interaction, hostility, and engagement remain separate outputs. A positive reaction count or reply count is not evidence that all reactors support every claim in the comment. Emoji reaction semantics are contextual and platform-specific. Do not infer the user's inner emotion or political belief.

Emoji-only comments must abstain for sentiment and emotion even when a parent/context text span is supplied: text written by someone else does not establish the emoji commenter's internal affect. A text-bearing context span whose offsets and text match caller-supplied context may support a separately justified topic, claim, stance, or hostility label; the comment's emoji alone cannot support those labels, and an emoji-only context span does not qualify. The report validator rejects known lexical forms of unqualified population-level language in English, Ukrainian, and Russian. This is a lexical check, not a semantic guarantee; it may miss paraphrases or other population claims, so report labels still need review.

Aggregate reports must state their unit and denominator: comment-weighted, author-weighted, thread-weighted, or channel-weighted. They describe the observed collected frame. They must not be phrased as population estimates. Platform-specific reaction fields are not compared as though they had the same semantics.

The structured report includes three compact platform-specific views. Target-by-stance rows count the selected aggregate unit by stance label, with a denominator of units that have at least one stance output for the same target; cells are marked as potentially overlapping. Topic/emotion cells count comments with both non-abstained outputs for the same target and platform, with a denominator of comments that have both dimensions for that target; multilabel cells are marked as overlapping. The top-reaction view ranks at most ten comments per platform by the sum of non-paid emoji and custom emoji reactions (`non_paid_reaction_count`) in the latest selected reaction snapshot when that snapshot is `available`, strictly decoupling paid Star currency payments and unknown types; its denominator is comments whose latest selected snapshot is `available` in that platform frame. A latest `current_user_excluded` snapshot does not enter this ranking. It includes no comment text, comment IDs, or user identifiers, and it is not exposure-adjusted engagement or population support. Platforms are presented in separate sections and are not compared as equivalent reaction measures.

Observed hostility labels are shown as their own dimension beside stance labels. Hostility is not a proxy for stance disagreement, and no scalar polarization score is emitted without a validated measure.

## Implementation boundary

P0 preserves Telegram's currently available typed aggregates in newly collected comments, without collecting reactor identities or changing old snapshots. The collector serializer, one-request `messages.getMessagesReactions` adapter, versioned snapshot schema, deterministic normalization/abstention contract, frame-conditional aggregates, and structured report validator/renderer are implemented. The bounded availability pilot queried one linked-discussion comment; it established availability for that single sample only. The API adapter does not poll automatically, and a single snapshot cannot reconstruct reaction history. Repeated future snapshots require an explicit bounded runner with flood-wait handling and per-item receipts.

The implementation is plumbing for future inference, not a validated audience-classification engine. It does not infer topic, claim, stance, sentiment, emotion, or hostility from raw comment text. No frozen local gold set or model benchmark has been run; all semantic quality remains `not_evaluated`. Target identifiers are validated against caller-supplied Social targets; this does not itself create or verify those claims/entities/events. The 6 November 39,598-comment corpus retains scalar legacy reaction totals only; it cannot be backfilled with emoji breakdowns or reaction history. New analytical views preserve `semantic_quality_status: not_evaluated` and do not claim classifier accuracy.

P1 now covers integration of a real, versioned classifier provider; the target graph already offers the intended interface. Before quantitative semantic claims, compare candidate models on a fixed Ukrainian/Russian/mixed-language benchmark with abstention, class-level precision/recall/F1, source-context coverage, and model/version provenance. Repeated reaction snapshots, platform-specific collection adapters, richer conversation/polarization analysis, and cross-platform normalization remain open. P2 adds deeper polarization and cross-platform comparisons after platform-specific coverage and semantics are independently documented.

No classifier is accepted from benchmark scores alone. Quality reports must identify model/version, language and context availability, abstention rate, test frame, per-class precision/recall/F1 where gold labels exist, and out-of-domain limitations. Without independent local adjudication, Social labels are candidate analyses and semantic accuracy remains `not_evaluated`.
