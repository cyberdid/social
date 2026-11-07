# Channel Evidence v2: Candidate Export

`src/analysis/channel_evidence.py` exports per-channel observation records from a Telegram `channels.jsonl` snapshot and its posts snapshot. It is a candidate-feature exporter; it does not decide whether a channel is Russian, pro-Russian, state-controlled, or part of an operation.

## Independent axes

- `origin`, `entity_type`, `operator`, and `content_orientation` default to `unknown`.
- `infrastructure_features` records observed public-profile markers and counts of outbound domains.
- `infrastructure_candidate` is a routing flag only. A profile marker or a minimum-volume domain share can prompt review; neither is an attribution.
- `operational_attribution.status` remains `unverified` unless a separately sourced analysis writes a later assessment.
- `legacy_group` preserves an old A–U category as a distinct compatibility field; it does not fill the new axes.
- `source_refs` includes SHA-256 receipts for the input snapshots and a channel profile locator.

## Interpretation rules

1. Language, political content, copied narratives, and links do not establish operator identity.
2. Russian domains and Russian-platform markers remain infrastructure observations.
3. A non-unknown value for an attribution axis requires at least one evidence ID.
4. Absence of a marker is not evidence that a source is independent or non-state.
5. The export's counts describe the supplied panel and snapshot only.

## CLI

```bash
python src/analysis/channel_evidence.py \
  --channels data/raw/telegram_web/SNAPSHOT/channels.jsonl \
  --posts data/raw/telegram_web/SNAPSHOT/posts.jsonl \
  --groups config/channel_groups.csv \
  --groups config/channel_groups_auto.csv \
  --output reports/channel_evidence/SNAPSHOT/channel_evidence.jsonl
```

The manual group file should be passed first. The output path must differ from every input path. Export is atomic; raw snapshots and legacy config files are not modified.
