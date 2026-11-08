# Relevance Sampling Audit v1

## Purpose and scope

This utility creates a reproducible audit sample from records rejected by an existing relevance rule. It estimates false-negative relevance **only within the rejected records supplied from the observed panel**. It does not estimate all Telegram posts, all channels, all platforms, or the fraction of relevant material that was never collected. A large sample cannot repair a non-probability channel panel or access gaps.

Candidate strata are prioritization devices, not detectors with known sensitivity. The tool keeps a random remainder stratum so posts that do not match its lexical/reference cues still have a known, positive inclusion probability when sampled.

## Input record contract

The JSONL input contains both selected and rejected records. Required fields default to `post_id` (unique stable string ID) and `relevant` (strict boolean). `text_clean` is optional string text. `relevance_reason_code` is optional and must be a lowercase code matching `[a-z0-9][a-z0-9_-]{0,63}`. IDs are validated across the complete input, not only rejected records.

Strata use a fixed, ordered, mutually exclusive assignment:

1. `rejected__candidate_no_toponym_context`: rejected text contains broad incident-topic vocabulary but no recognized place-name stem.
2. `rejected__candidate_place_only`: rejected text contains a recognized place-name stem, whether or not a topic cue is present.
3. `rejected__candidate_reference_context`: no prior cue matched, but a URL or forward/reply/quote/context field is present. The native Social `posts_clean.jsonl` field `links` and a normalized `urls` field are both recognized; callers do not need to rename `links` to `urls`.
4. `rejected__random_remainder`: all remaining rejected records.

This hierarchy is intentionally transparent and deterministic. Lexical matching is broad and may include unrelated posts; it is not a semantic or ground-truth classification. A source or context signal cannot establish that the post concerns the incident.

## Sampling design

Within each non-empty stratum, the code selects a simple random sample without replacement. It ranks stable IDs by `SHA256(seed || stratum_id || record_id)` and takes the first `n_h`; this avoids dependence on Python's `random.sample` implementation. The inclusion probability is `pi_h = n_h / N_h`. The manifest records each `N_h`, `n_h`, `pi_h`, seed, ID/decision field names, and a SHA-256 digest of the canonically serialized rejected frame. It contains identifiers and reason codes but not post text.

The allocation must explicitly name every non-empty stratum and assign it at least one sampled record; a non-empty stratum with zero allocation is rejected because it would make the combined point estimate unidentified. The CLI supports either repeated `--sample-size STRATUM=N` or the convenience option `--sample-size-per-stratum N`. For a precision-driven design, choose allocation after seeing stratum counts; a uniform allocation is a convenience, not an optimal allocation. If adjudication cost differs by stratum, use an explicitly documented allocation and retain the per-stratum inclusion probabilities.

Example:

```bash
python -m src.analysis.relevance_sampling_audit_v1 \
  --input data/processed/SNAPSHOT/posts_clean.jsonl \
  --output reports/relevance-audit/sampling-manifest.json \
  --seed 20261108 --composite-id-keys channel,msg_id \
  --sample-size-per-stratum 40
```

Telegram post IDs are channel-scoped. For `posts_clean.jsonl`, pass `--composite-id-keys channel,msg_id`; the manifest ID is an unambiguous typed JSON-array string, so equal message numbers in different channels remain distinct. The input is not modified. For a source with a globally unique field, keep the default `post_id` or choose another unique key with `--id-key`.

The manifest is a sampling receipt, not an adjudication result. Add adjudications in a separate JSONL with one row per sampled `record_id` and a boolean `missed_relevant`. The adjudication should be based on a written relevance rule and contextual evidence; uncertain cases should be resolved by a separate reviewer or reported as unresolved, not silently treated as a negative.

For a saved Social `posts_clean.jsonl` sample, replay the source-frame transformation and compare membership without writing sampled IDs to the receipt:

```bash
python -m src.analysis.relevance_sampling_replay \
  --input data/processed/<snapshot>/posts_clean.jsonl \
  --manifest <private-sampling-manifest.json> \
  --output reports/relevance-audit/replay-receipt.json
```

The replay recomputes the current `prep.relevance_decision`, excludes rows whose reason is `outside_time_window`, creates channel-scoped `(channel,msg_id)` identifiers, retains native `links`, and compares source hash, stratum counts, sample membership, and frame digest. Its receipt contains no source text or sample identifiers. A sample-membership match is useful procedural evidence; it is not an adjudication or recall estimate. Any mismatch must remain explicit.

## Sample-size helpers

For a simple random sample from a finite stratum of size `N`, worst-case proportion `p = 0.5`, two-sided confidence quantile `z`, and desired half-width `e`, the initial binomial size is:

`n0 = z^2 * p * (1-p) / e^2`

With finite population correction:

`n = ceil(n0 / (1 + (n0 - 1)/N))`, capped at `N`.

This helper is for one SRS proportion under its assumptions. Applying it separately to multiple strata does not automatically yield a specified precision for the combined weighted estimate; allocation and variance must be evaluated for the intended estimand.

For a stratified binary proportion, the allocation helper reserves a minimum in each non-empty stratum, distributes the remaining sample proportionally to remaining stratum capacity with deterministic largest-remainder rounding, and finds the smallest total `n` meeting the requested planning half-width. It uses the conservative finite-population bound

`Var(p_hat) <= sum_h W_h^2 * (1 - n_h/N_h) * [N_h/(4(N_h-1))]/n_h`,

where `W_h=N_h/sum_h N_h`. The `N_h/(N_h-1)` factor bounds the finite-population binary variance; it matters most in small strata. This is a design calculation for the supplied finite frame, not an outcome estimate, and it does not correct panel-selection or source-coverage bias. The proportional allocation is transparent and deterministic, not a claim of cost-optimal Neyman allocation.

For a rare-miss detection design, the helper sets `K = ceil(N * p_min)` and finds the smallest `n` such that the exact hypergeometric probability of seeing zero positives is no more than `alpha`:

`P(X=0 | N,K,n) = C(N-K,n) / C(N,n) <= 1 - confidence_level`.

This answers “how large an SRS is needed to have this probability of observing at least one missed case if at least `p_min` of this finite frame are missed?” It does not estimate a rare prevalence precisely and does not solve coverage bias.

## Analysis of adjudications

For stratum `h`, with frame size `N_h`, sample size `n_h`, and adjudicated missed-relevant proportion `ybar_h`, the stratified estimate of missed records is:

`Mhat = sum_h N_h * ybar_h`.

The estimated share among rejected records is `Mhat / sum_h N_h`. With binary labels and `n_h >= 2`, the design-based variance uses the stratified SRS estimator and finite population correction:

`Var(Mhat) = sum_h N_h^2 * (1 - n_h/N_h) * s_h^2/n_h`,

where `s_h^2` is the ordinary sample variance of the binary labels. A two-sided Wald interval is reported only when every non-census sampled stratum has at least two adjudications; it is approximate and can be poor for sparse outcomes. The output separately includes a conservative one-sided exact hypergeometric upper bound on missed count, using Bonferroni allocation across strata. This avoids reporting a zero-width interval merely because no sampled record was positive.

This module audits rejected records only. It does **not** estimate classifier recall: that would also require an independent adjudication of the selected records to estimate their true-positive count. The manifest records the number of selected records only as frame context. If non-empty rejected strata are left unsampled, analysis rejects the manifest instead of treating those strata as zero misses.

An empty stratum is omitted. A non-empty stratum must have at least one sampled unit; the generator rejects zero allocation and the analyzer rejects manifests that violate this rule. A census stratum has zero sampling variance and does not itself suppress an interval. For any non-census stratum, if all sampled labels are identical (all zero or all one), its sample variance is zero even though the unobserved finite population may contain the other class. The module therefore suppresses the approximate stratified Wald interval whenever at least one such non-census stratum exists, including when other strata have the opposite label. It continues to report the familywise-adjusted exact one-sided hypergeometric upper bound. This avoids a zero-width or implausibly narrow interval caused by pooling strata before detecting boundary samples.

## Interpretation and limits

- Do not present this output as a recall estimate. It estimates missed-relevant records within the supplied rejected-record frame only.
- The audit measures the existing decision rule among records already collected. It cannot find posts absent from the source panel or inaccessible to the collector.
- Candidate cues do not have validated recall. The random remainder is necessary to check misses outside those cues.
- Reposts/near-duplicates are still record-level units unless the frame is explicitly deduplicated before sampling. If the estimand is unique claims or source families, define those clusters as the sampling unit first.
- A sample of rejected records assesses false negatives, not false positives among selected records. Audit selected records separately if precision is required.
- Estimating precision among selected records requires a separate selected-side audit; the present utility does not do that.
- The reported interval is sampling uncertainty conditional on this finite frame, not uncertainty about unobserved Telegram content or public opinion.

## Validation checks

Tests cover deterministic selection, positive stratum allocations, inclusion probabilities, frame hashing, text omission from the manifest, invalid/duplicate IDs, composite Telegram IDs, formula helpers, design-weighted estimation, finite population correction, sparse zero-positive bounds, malformed adjudications, and output no-overwrite behavior. The tool never modifies the input frame or source data.
