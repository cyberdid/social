# Measurement Uncertainty & Robustness v1

`src/analysis/uncertainty_scenarios.py` computes descriptive sensitivity scenarios and optional partial-identification bounds for a fixed, non-probability corpus. It does not create standard errors, confidence intervals, or population estimates.

## What it measures

The input is one row per unique post/evidence observation. Each row has:

| Field | Meaning |
|---|---|
| `post_id` | Stable unique record identifier |
| `channel_id` | Stable source/channel key; channel-level sensitivity samples/excludes this cluster as one unit |
| `target_label_state` | `target`, `other`, or `unknown`, after the upstream classifier has been mapped to the analysis target |
| `channel_group` | Current channel group, or null/`unknown`/`U` where unresolved |
| `views_snapshot` | Optional non-negative snapshot counter captured at an identified time |
| `source_family_id` | Optional dependency-family ID backed by explicit lineage evidence |
| `lineage_status` | `confirmed_dependency_family`, `candidate`, or `unknown` |

Unknown rows are not silently coerced. Every generated scenario records how unknown post labels and channel groups were treated. The command reports:

- share of posts in the observed input corpus;
- share of channels with at least one target post;
- target share of the sum of recorded view-counter snapshots, with missing-counter row counts;
- sensitivity after excluding the largest `k` channels by post count or counter sum;
- optional target-share bounds from caller-supplied missing-target/non-target record ranges;
- confirmed dependency-family counts and the number of unknown-lineage records.

The source-lineage summary is descriptive: a dependency family is not an independent observation or an independent source root. The module therefore leaves `independent_source_root_count` null.

## Scenario arithmetic

For target-label uncertainty, the lower scenario counts only explicit `target` rows as target; the upper scenario also treats every `unknown` label as target. Both retain the same observed-corpus denominator. For a target channel group, scenarios either exclude unknown-group channels or assign them to the target group; they do not assume a probabilistic distribution over groups.

Top-k sensitivity ranks channels by the selected basis, removes each selected channel's records, and recomputes the same measures. Channel records are not treated as independent rows in this exclusion scenario.

If an external coverage audit supplies integer ranges for missing target and non-target posts, the module computes:

\[
L = \frac{T_{obs,L}+T_{miss,min}}{N_{obs}+T_{miss,min}+N_{miss,max}},\qquad
U = \frac{T_{obs,U}+T_{miss,max}}{N_{obs}+T_{miss,max}+N_{miss,min}}.
\]

These are assumption-conditional partial-identification bounds, not confidence intervals. The module never infers missing-post counts from platform coverage or a classifier score.

No bootstrap is used: resampling a targeted Telegram panel cannot make it representative of Telegram users or the public. A future model-based Monte Carlo procedure would require separately validated, explicit error distributions; this v1 emits no probability distribution or pseudo-calibrated interval.

## CLI

```bash
python src/analysis/uncertainty_scenarios.py \
  --input reports/case/posts_with_uncertainty_fields.jsonl \
  --output reports/case/uncertainty_scenarios.json \
  --target-label N3 \
  --target-group C \
  --top-k 0 1 5 \
  --top-k-basis views_snapshot
```

Optional `--coverage-bounds` takes a JSON object with four non-negative integer fields: `missing_target_min`, `missing_target_max`, `missing_non_target_min`, `missing_non_target_max`. Those values must come from an independently documented coverage audit; supplying them is an explicit scenario assumption.

## Interpretation limits

1. Shares describe only the provided snapshot and its documented selection process.
2. A sum of Telegram `views` counters is not unique audience, unique viewers, exposure, or causal influence.
3. Missing labels and unknown channel groups are scenarios, not latent probabilities.
4. A counter's capture time matters; cross-platform or cross-time comparisons need aligned snapshots.
5. Unknown lineage is not independence. A unique family ID is not enough to claim independent corroboration.
6. Coverage bounds are only as defensible as their externally supplied missing-record assumptions.
7. Classifier confidence values are not consumed; they need calibration on independent validation data before a probabilistic model could use them.

## Output contract

The JSON output has `analysis_type=descriptive_sensitivity_and_partial_identification`, `sample_design=targeted_nonprobability_panel_unless_separately_documented`, a scenario list with recorded assumptions and excluded channel IDs, optional `coverage_partial_identification`, and fixed limitations. `interval_type` explicitly says that scenario ranges are not confidence intervals. Output is written atomically.

## Verification

```bash
PYTHONPATH=. pytest -q tests/test_uncertainty_scenarios.py
python -m py_compile src/analysis/uncertainty_scenarios.py
git diff --check
```
