# Telegram comment reaction pilot — 8 November 2026

## Scope

One already-collected public Telegram linked discussion thread was inspected through the existing authorized Telethon user session. The request read at most 10 comments and asked for aggregate reactions on one comment message. No post text, comment text, channel/group identifier, message ID, user ID, pseudonym, or session detail is stored in this receipt. The collector did not request any reactor list.

## Result

| Check | Result |
|---|---:|
| Discussion threads inspected | 1 |
| Comment messages read (maximum) | 10 |
| `messages.getMessagesReactions` message IDs requested | 1 |
| API response | 1 `updateMessageReactions` update |
| Reaction object state | `available` (not `min`-marked) |
| Reaction types in returned aggregate | 1 standard-emoji type |
| Sum of API `ReactionCount.count` values | 1 |
| Reactor identity list requested or stored | No |
| Raw text or platform identifiers stored | No |

Observation timestamp: `2026-11-08T11:58:54Z` (UTC). The aggregate was obtained using the linked discussion peer and the comment message ID. No retry or additional polling was performed.

## Interpretation and limits

This bounded pilot confirms that the already-authorized MTProto user session can retrieve typed aggregate reactions for at least one message in a linked discussion group. It does not establish availability across all 533 collected threads, every reaction type, every privacy setting, or every message. The single returned count is an API snapshot, not a historical value or a population estimate. No conclusion about support for the comment's claims follows from the reaction.

The existing 6 November snapshot cannot be backfilled with emoji types or prior reaction history: it preserved only the summed integer. New collection runs can preserve the typed vector and observation time. Repeated, explicitly bounded snapshots are required for reaction dynamics.

## API references

- [Telegram message reactions](https://core.telegram.org/api/reactions)
- [`messages.getMessagesReactions`](https://core.telegram.org/method/messages.getMessagesReactions)
- [Telegram discussion groups](https://core.telegram.org/api/discussion)
