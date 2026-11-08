# Telegram reaction serializer/API parity check — 8 November 2026

## Result

Performed a bounded read-only check through the existing authorized Telegram MTProto session. For 10 already-collected public comments across three linked discussion threads, Social fetched each current `Message.reactions` vector, serialized the vectors into private snapshot rows, then fetched current aggregate reactions once per discussion peer using `messages.getMessagesReactions` and the same comment message IDs.

| Check | Result |
|---|---:|
| Discussion threads sampled | 3 |
| Existing comments selected | 10 |
| Current typed snapshot rows saved locally | 10 |
| API refresh requests | 3 (one per linked discussion peer) |
| Collector reaction states | `available`: 10 |
| API reaction states | `available`: 10 |
| State and type/count vector identical | **Yes, 10/10** |
| Reactor list requested | No |
| Comment text or account ID written to receipt | No |

Each API vector matched the corresponding collector-serialized vector exactly after canonical ordering by reaction type and key. This convenience sample checks only the available state across three threads; it does not establish parity for empty or `min`-marked states, all groups, permission states, all reaction constructors, or the full 533-thread corpus.

## Historical scalar comparison

The selected 6 November source row belongs to the old 39,598-comment snapshot. None of its rows contains a typed `reaction_breakdown` or `reaction_state`; it stores only a scalar total. Its old scalar did not equal the new live aggregate total. The two values come from different observation times and different schemas, so this is **not** a serializer/API parity failure and cannot be used to infer why the count changed. The historical row cannot be decomposed into emoji types or reconstructed as a reaction time series.

## Privacy and reproducibility

- The exact 10-row comparison, including local IDs needed for replay, remains outside Git at `/home/cyberdid/Downloads/SocialIncidentAnalysis/audience-response/telegram-reaction-parity-10-2026-11-08/private_snapshots.jsonl`.
- Private output directory mode: `0700`; snapshot file mode: `0600`.
- Private snapshot SHA-256: `aca8d40e9e6fc306ee7f9830ac937b0d81916b3acf157cf0a5051b14e42945df`.
- Content-free execution receipt is stored beside the private row. No text, reactor identities, or peer identifiers were queried or written to the public report.
- The request was bounded to one comment and one aggregate API refresh; no retry, polling, or `messages.getMessageReactionsList` call was made.

## Conclusion

The live collector serializer and MTProto aggregate endpoint agreed on these 10 current typed snapshots across three threads. This closes the first bounded parity check, not full-corpus coverage or the broader W14 gate. Repeated reaction snapshots, semantic classification benchmarks, and the historical reaction series remain unavailable or unevaluated.
