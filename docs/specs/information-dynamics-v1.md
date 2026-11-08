# Information Dynamics v1

Status: implementation contract for descriptive information-wave summaries. This is a candidate adapter for W09, not an attribution or causal inference engine.

## Scope

The module consumes normalized post snapshots and emits deterministic summaries for publication activity, collection activity, explicitly reported event-time references, source-dependency families, channel-group sensitivity, and top-k concentration. It does not replace the legacy Telegram network, coordination null-model, narrative, or channel-evidence modules. It has no implicit adapter from their files: callers must map fields into the contract below so that fields with different meanings are not silently merged.

## Input contract

Call `summarize_information_dynamics(posts, *, coverage=None, source_lineage=None, bin_hours=6, timezone_name="Europe/Kyiv", top_k=(1, 3, 5, 10))` from `src.analysis.information_dynamics`.

Each `posts` record requires:

| Field | Meaning |
|---|---|
| `post_id` | Stable identifier for one platform post in this run. |
| `platform` | Platform name; normalized to lowercase. |
| `channel_id` | Source/account/channel key used only for descriptive grouping. |
| `publication_time` | ISO-8601 timestamp with timezone, when platform content was published. |
| `observed_at` | Optional timezone-aware capture/collection time. |
| `reported_event_time_start`, `reported_event_time_end` | Optional source-attributed interval about the physical event. These fields do not validate that event time. |
| `view_count_snapshot` | Optional nonnegative integer counter snapshot, not a unique-person count. |
| `view_count_observed_at` | Optional timezone-aware time for the counter snapshot; falls back to `observed_at`. |
| `evidence_id` | Optional evidence ID for joining source-lineage edges; falls back to `post_id`. |
| `group_label`, `group_label_status` | Optional descriptive channel-group candidate and basis. Status supports `manual`, `evidence_supported`/`evidence_verified`, `automatic_candidate`/`auto_candidate`, or `unknown`. |

Repeated rows for a `post_id` are treated as snapshots of the same post. Immutable platform, channel, and publication-time fields must agree. The latest observed snapshot supplies the descriptive row; the latest counter snapshot is selected by `view_count_observed_at` (or `observed_at`). Conflicting counter values with the same snapshot timestamp are excluded from counter sums and counted as conflicts. No sampling weights are implied.

`coverage` may be a list of records (`platform`, `status`, optional `reason`, `queried_at`) or a mapping from platform to those fields. Missing coverage is `observed_coverage_unspecified`; a platform with no captured posts is not interpreted as having no relevant posts.

`source_lineage` accepts the `edges` collection produced by `analyze_source_lineage`. Only `confirmed_by_explicit_reference` and `identical_asset_bytes` edges connect records into confirmed dependency families. `candidate` edges are counted but do not merge families. Unknown or absent edges never become independent-root assertions.

## Output

The returned JSON-compatible object contains:

- `publication_series`: unique posts by platform and local-wall-clock bin, with UTC start/end boundaries.
- `observation_series`: unique posts by collection time, separately binned; records without `observed_at` are counted in `corpus` and omitted from these bins.
- `publication_to_observation_lag_seconds`: descriptive collection delay distribution, not platform latency.
- `reported_event_time_references`: per-post source-attributed intervals, kept distinct from publication and collection times.
- `coverage`: observed platforms plus explicit gaps and `does_not_establish_absence`.
- `source_lineage`: confirmed dependency components, candidate-edge count, unlinked-record count, and `independent_roots_lower_bound: 0`.
- `group_sensitivity`: `all_labels_as_recorded`, `automatic_candidates_unknown`, and `manual_and_evidence_supported_only` scenarios. The final scenario excludes non-manual/non-evidence-supported group assignments and reports its denominator.
- `top_k_concentration`: top-k shares of unique post counts and snapshot-counter sums by channel. Counter sums are named `snapshot_view_counter_sum` and never `reach` or audience.
- `limitations`: explicit prohibitions against reading descriptive activity as physical escalation, causality, bot classification, state direction, unique audience, or platform-wide prevalence.

Time bins are aligned to local wall-clock starts and advanced as fixed UTC durations. Timestamps are required to be timezone-aware; no naive timestamp is guessed into Kyiv time. Reported event-time intervals are preserved as intervals and are never used to claim a causal order.

## Interpretation and integration rules

1. Counts describe only the supplied corpus snapshot and its collection rules.
2. A dependency family records known relationships among evidence records. It does not identify the original source, prove coordination, or establish a root count.
3. `group_label` is descriptive input only. Automated labels are moved to `unknown` in one sensitivity scenario and excluded in another; none of these outputs attributes ownership or state direction.
4. View counters can overlap across posts, channels, and collection times. The latest available per-post counter snapshot is summed only for descriptive concentration; it is not unique reach.
5. Information activity and physical-conflict indicators are distinct. This module does not calculate physical escalation.
6. The output should be attached to a run manifest with input file hashes, coverage receipts, lineage output hash, software version, and `as_of` time by the calling orchestrator.

## Explicit gaps

- No statistical significance or event-conditioned null model is computed here; the existing coordination null-model workflow remains separate and requires its own DR2 review.
- No cross-platform identity resolution is attempted.
- No causal effect of information on participation, institutional action, or conflict outcomes is estimated.
- No population inference is valid for the targeted Telegram panel or partial multi-platform collection.
Native post and channel identifiers are platform-scoped. The output uses `platform:post_id` and `platform:channel_id` references where a cross-platform entity key is needed; equal numeric IDs on two platforms are not merged.

