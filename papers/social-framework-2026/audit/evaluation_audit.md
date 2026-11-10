# Evaluation and statistical consistency audit

Audit date: 2026-11-10. Baseline: `f0e9d0d67422b0c286a2cb9e7d4e935a833a9533`. Only new-paper audit/data outputs were written. No collection, API inference, paid model call, or source-artifact regeneration was performed.

The authoritative machine-readable companion is [`audited_evaluation_metrics.json`](../data/audited_evaluation_metrics.json), abbreviated **M** below. Every reported measured count has its input file, SHA-256, denominator, and JSON path in M. `M.artifact_sha256` is the full hash registry; the source paths named below are relative to the repository root. Recomputed finite-corpus algorithmic agreement and structural tests do not establish semantic accuracy.

## Required corrections and provenance conflicts

**F-EVAL-01, major: missingness denominator was misreported.** The old article (`papers/social-case-study-2026/sections/article_en.tex:55` and Ukrainian counterpart) attributes 459 missing texts and 49 missing counters to the 1,408 relevant posts. Direct parsing finds **0 missing raw text, 0 blank cleaned text, and 0 missing counters among those 1,408 posts**. The 459 missing raw texts and 49 missing counters refer to **all 23,350 publications**, exactly as computed in `src/analysis/build_continuation.py:339-348`. After cleaning, 474 of all 23,350 texts are blank. Thus 1,384 long eligible relevant texts are consistent with 1,408 relevant posts: the other **24 relevant posts are shorter than 80 cleaned characters**, not missing. Values and definitions: `M.corpora.historical`; eligibility: `src/analysis/coordination_lsh_audit.py:31-37`.

**F-EVAL-02, major: the lineage document assigns the exact graph to the wrong corpus.** `reports/provenance/lineage_manifest_2026-11-09.json:40-50` stores 369 exact pairs under `corpus_reconciliation.merged`; its `lineage_matrix[metric_id=merged_exact_jaccard_pairs]` also calls the graph an audit of the merged 1,438 posts. The actual null run's `results.json.inputs_sha256`, its replay receipt, and the newly recomputed exact sweep all bind the graph to historical **1,408 relevant / 1,384 eligible** records. The exact-edge CSV hash is `9e1d07c77cba556d1da414ab1d7a8952f09f220c29a71a33066b5f3ccf340e2b`; its full-text input is `4e859d407aef52c72a8e690dc5716d7d92d11ff7d7a164760db5a4c0ad334350`, and relevant CSV input is `8b69539801a385bee8f5ea05c5315d18a6d518f96393ff5bf5cd6f57529f8b37`. The expanded full-text hash is different: `d229d8618021cf285f24c712eb9cd37ca85eb0e8bee2d8a7f74b6e7c574cda3f`. Hashing a mistaken lineage assertion does not validate the assertion. Preserve the source as historical evidence, but correct its scope in the new paper. Do not label 369 as an independently evaluated expanded-corpus result.

**F-EVAL-03, limitation: no independent semantic gold.** The saved label comparison is against Claude coding, not two independent human coders plus adjudication. Test counts, six synthetic controls, exact similarity retrieval recall, and report hashes cannot be used as semantic incident/report accuracy. The harness explicitly returns `not_evaluated` and a null unsupported-assertion rate (`src/analysis/evaluation_harness.py:366-379,571-578`).

**F-EVAL-04, limitation: inferential scope.** Conditional null departures are exploratory and finite-panel specific. The audit does not supply matched benign organic events, detector specificity, population prevalence, organizer identification, bot labels, causal transmission, or causal influence. Unknown labels and groups yield wide descriptive scenarios; their range is not a calibrated confidence interval.

## Versioned corpus ledger

| Quantity | Historical continuation | Expanded merged corpus | Denominator / M path |
|---|---:|---:|---|
| Publications in cleaned JSONL | 23,350 | 23,386 | All parsed rows; `corpora.*.records` |
| Relevant publications | 1,408 | 1,438 | Rows with `relevant == true`; `corpora.*.relevant_records` |
| Relevant channel identifiers | 159 | 158 | Distinct relevant `channel`; `corpora.*.relevant_channels` |
| Missing raw text | 459 | 444 | All publications; `all_missing_raw_text` |
| Blank cleaned text | 474 | 455 | All publications; `all_missing_clean_text` |
| Missing view counters | 49 | 49 | All publications; `all_missing_views` |
| Missing raw/clean text or views in relevant subset | 0 / 0 / 0 | 0 / 0 / 0 | Relevant subset; corresponding `relevant_missing_*` |
| Relevant cleaned texts of at least 80 characters | 1,384 | 1,416 | Relevant subset; `relevant_clean_text_ge80` |
| Sum of relevant snapshot view counters | 115,931,014 | 119,515,745 | Relevant posts with recorded counters; `relevant_view_counter_sum` |

Raw text missing means `not (row.get('text') or '').strip()`; cleaned missing substitutes `text_clean`; counter missing means `views is None`. No claim of unique audience follows from the counter sums. The expanded difference is a **net** 36 publications and 30 relevant records; it should not be described as 30 simply appended observations because canonicalization, removals, and relevance decisions differ. This audit verifies counts, not every source-lineage delta or the lineage document's inferred timestamps. Historical and expanded source hashes appear in `M.corpora` and the hash registry.

## Exact similarity and MinHash candidate recall

The historical relevant subset was reconstructed directly from full JSONL, not the exported `relevant_posts.csv.text`, which is truncated (`src/analysis/analyze.py:120`). Shingling uses lowercasing, punctuation removal, whitespace collapse, and sets of five-character substrings (`src/analysis/analyze.py:60-68`). The legacy candidate method uses 128 permutations and threshold 0.6 (`src/analysis/analyze.py:72-81`); scoring is exact on candidate shingle sets. The exhaustive implementation retains full `text_clean` of at least 80 characters with channel and URL, computes int64 sparse intersections, excludes same-channel pairs, and scores exact Jaccard (`src/analysis/coordination_lsh_audit.py:31-92`). The int64 regression control specifically exercises intersections exceeding an 8-bit range (`tests/test_coordination_lsh_audit.py:13-30`).

The bounded fresh exhaustive sweep reproduced the saved exact edge set and all scores to an absolute tolerance of `1e-14`. Same-channel checking independently reproduced **18** qualifying same-channel pairs; these are excluded by definition. See `M.exact_jaccard`, including eligible pair counts and exact denominator.

| Threshold | Exact cross-channel pairs | Legacy pairs retained | Misses | Extra legacy pairs | Conditional candidate recall |
|---|---:|---:|---:|---:|---:|
| J ≥ .60 | 369 | 367 | 2 | 0 | 367/369 = 99.45799458% |
| J ≥ .75 | 288 | 288 | 0 | 0 | 288/288 = 100% |
| J ≥ .90 | 213 | 213 | 0 | 0 | 213/213 = 100% |

These are exact finite-corpus retrieval proportions, not estimates of relevance recall, semantic classification, collection coverage, or performance outside this eligible historical snapshot. `summarize_candidate_recall` implements the numerator/denominator intersection (`src/analysis/coordination_lsh_audit.py:97-127`); values are in `M.exact_jaccard.recall_by_threshold`.

The exact graph has **357 posts and 113 channels** (`M.exact_jaccard.exact_graph_nodes`, `exact_graph_channels`). The two misses have lags **184.60** and **33.083333** minutes and Jaccard **0.6657142857** and **0.6226415094**, respectively (`M.exact_jaccard.missed_pairs`, exact URL pairs retained there). Both exceed 30 minutes. Hence observed counts remain **134/369** within 10 minutes and **198/369** within 30 minutes for J ≥ .60, replacing **134/367** and **198/367** in the legacy graph. Higher-threshold counts are **94/288, 141/288** and **53/213, 88/213**. Source: `M.null_model.tests[4:16]`, named `statistic` and `edge_denominator` fields, and saved `test_summary.csv` under the exact-audit directory. These denominators count edges sharing nodes; they are not independent observations.

## Null models and p-value audit

The saved source is `reports/coordination-null-models-2026-11-08-lsh-audit/results.json` (SHA-256 `5d6cd59bd5c31239eff595317a17ec4fd67f6a6329b1475cc10b9557e97a5d74`). It records **B=9,999**, seed **20261106**, and PCG64 streams derived from `[seed,family,model]`. `M.null_model` retains every test, graph denominator, mean, quantile, exceedance count, ratio, and p-value. The current script hash matches its saved recorded hash.

S7 uses **39,459 known-author comments from 39,598 raw comments**, **12,797 pseudonymous authors**, and **533 selected threads** (`results.json.comments`, mirrored at `M.null_model.bounded_prefix_replay.controls_comments`; filter and counts in `src/analysis/coordination_null_models.py:127-154,212-224`). The four-thread campaign reconciliation yields **126 phrases / 438 comments / 367 authors** (`src/analysis/coordination_null_models.py:153-174`). That last 367 counts authors and is unrelated to 367 graph edges. The S7 statistics are maximum eligible thread-signature pool size and total phrases in pools of size at least ten (`src/analysis/coordination_null_models.py:39-55`); observed values are **60** and **111**, not independent campaign counts. Model strata preserve author/day or day/activity/script structure. All phrase frequencies are checked every draw; full within-stratum dictionaries are checked on the first 25 (`:176-207`).

Timing randomization uses the fixed exact graph and all **23,350** collected timeline posts. One cyclic offset is sampled per channel-local time block; each node receives one new time used by all its incident edges (`src/analysis/coordination_null_models.py:73-83,227-265`). This preserves dependencies from shared nodes and avoids treating edges as independent. The **24h model has 184 occupied blocks / 9,801 slots**, and the **2h model has 291 occupied blocks / 2,501 slots**, of which **22 are one-slot blocks** (`M.null_model.bounded_prefix_replay.controls_timing.null_controls`; controls constructed at `:297-314`).

All saved S7 and timing draws were read afresh. Recalculation of means, central quantiles, maxima, effect ratios, inclusive tails, and plus-one p-values matched every saved test. All **16 tests** have **zero exceedances**, **p_raw=(0+1)/(9,999+1)=0.0001**, and **p_Holm=0.0016**. The family comprises two S7 models × two statistics plus two timing models × three thresholds × two lag windows (`src/analysis/coordination_null_models.py:208-210,261,268,303-309,335-344`). The upper inclusive rule and Holm implementation are `:86-108`. Never report p=0 or greater numerical resolution than this run supplies. `M.null_model.saved_draw_summary_checks` records each checked test's JSON index. The central 95% draw range is a randomization-distribution range, not a population confidence interval or causal-effect interval.

A fresh **25-draw prefix replay for each of all four models** exactly matched the corresponding first 25 saved rows, using the original seed and current code. This audit did not repeat the full 9,999 draws. The historical full replay receipt dated 2026-11-08 records six byte-identical outputs; its hash is verified, but that receipt is a historical claim, distinct from the fresh bounded checks. Current saved input and script hashes all matched. No independently labeled organic controls were added; thus empirical false-positive specificity remains unmeasured.

## Narrative reliability, temporal bins, and network

Narrative v2 is a multilabel regex codebook (`src/analysis/narratives.py:1-14,89-99`). The saved development/test distinction describes 50 development posts and a fresh 40-post test set. The test annotation file itself says Claude, seed 777, blind to rule labels (`reports/20261105T101013Z/validation/manual_labels_claude_test.csv:1-3`). This is model-to-rule comparison with model reference labels, not independent human reliability or semantic ground truth. Recomputed row-level confusion counts and unrounded values are in `M.reliability.labels`; all rows below have denominator **40 paired posts**.

| Label | TP / FP / FN / TN | κ against Claude | Precision / recall against Claude |
|---|---|---:|---:|
| N1 | 1 / 4 / 3 / 32 | .125 | .200 / .250 |
| N2 | 2 / 9 / 3 / 26 | .09434 | .18182 / .400 |
| N3 | 2 / 0 / 2 / 36 | .64286 | 1.000 / .500 |
| N4 | 0 / 2 / 4 / 34 | −.07143 | .000 / .000 |
| N0 | 7 / 2 / 4 / 27 | .60133 | .77778 / .63636 |
| medic_claim | 0 / 1 / 1 / 38 | −.02564 | .000 / .000 |
| debunk | 2 / 0 / 2 / 36 | .64286 | 1.000 / .500 |
| counter_debunk | 0 / 0 / 0 / 40 | undefined | undefined / undefined |

For counter_debunk, all-negative agreement is 1 but κ and positive precision/recall are undefined. Do not convert this into perfect class detection. The saved table rounds N1 raw agreement .825 to .82; M retains exact 33/40. Sampling and reference limitations preclude calibrated semantic accuracy or population CIs from these values. The later narrative_v3 unit tests check examples and abstention logic; their pass count is not a replacement independent benchmark.

Fresh computation reproduced the historical network statistics and entire six-hour bin table. The visible-forward graph has **69 endpoint nodes, 60 directed channel-pair edges, and 65 observed forward events**, with **20 cross-group edges / 24 cross-group events**. There are **53 two-step paths, 2 closed**, giving **2/53=.03773585** closure. Directed betweenness is **unweighted**; volume `n` is never interpreted as distance (`src/analysis/telegram_network_dynamics.py:29-72`). Scope excludes isolated channels and inherited channel groups are not independently validated attribution. Source/denominators: `M.network.metrics`, original `results.json`, and `M.network.input_sha256`.

Narrative bins cover **1,408 relevant posts, 15 bins, 2 empty bins**, and a final **0.17027778-hour partial bin**. Counts are N0 **307**, N1 **301**, N2 **505**, N3 **230**, N4 **81**; **557** posts have no label and **394** have multiple labels. The **1,424 assignments** exceed the number of labeled posts because labels overlap. Each label share divides by **all posts in its bin**, not label assignments; an empty bin explicitly stores zero plus `empty_bin=true`. Bins are left closed/right open in Kyiv time (`src/analysis/telegram_network_dynamics.py:75-103`). Counts and hashes: `M.network.metrics`. The saved script explicitly records Granger analysis as **not run** (`M.network.metrics.granger`). No change-point stability, fixed one-hour comparison, causal transmission, or operator test is measured.

The expanded `information_dynamics_summary.json` describes 1,438 posts using different UTC-aligned bins; it must not be silently combined with the historical Kyiv-aligned thematic table. Its lineage status is `not_run`, independent-root lower bound zero. These are different outputs with different bin origins and analysis eligibility.

## Uncertainty and evaluation harness

Uncertainty code implements deterministic unknown-label/group scenarios, top-k channel exclusion, and optional caller-supplied missing-record bounds (`src/analysis/uncertainty_scenarios.py:174-290`). It leaves independent source-root count null and does not bootstrap the targeted panel into a representative population. The archived expanded run reports **1,438 unknown labels and 1,438 unknown group row values**: its target post, channel, and counter-share scenario ranges are **[0,1]** (`M.uncertainty`). The group count is a count of observation rows carrying unknown group, not 1,438 distinct channels. The fresh algebra check reproduces the all-unknown post-share endpoints; private row-level channel mapping was not replayed (`M.uncertainty_recomputation`). No external coverage bounds were supplied; there is no calibrated joint error distribution, posterior, standard error, or confidence interval. Synthetic tests verify scenarios, top-k behavior, and explicit coverage assumptions (`tests/test_uncertainty_scenarios.py:25-73`).

The archived run has **6 findings, 574 evidence records and event records, 7 receipts, 15 listed outputs, 0 source snapshots, and 0 verification results** (`M.evaluation_harness.counts`). Its summary says **16 manifest files and 3 report-bundle files** verified; these are different recorded counters and must retain their names. The summary's structural pass is an archived result, not proof that zero verification results semantically support six findings. Its six frozen controls are synthetic, and real report diff is explicitly not run. Current `run_frozen_suite()` independently returned **6/6** (`M.current_frozen_suite`), covering microcase timeline, copy fanout, contradictions, correction cutoff, missing corpus, and old reused video. Each scenario is a deterministic invariant, not a sampled incident-truth observation (`src/analysis/evaluation_harness.py:583-664`).

The full existing offline suite passed using the repository interpreter: **783 passed, 16 subtests passed, 0 failed**, pytest time **7.41 s**, measured wall time **7.84 s**, maximum RSS **328,320 KiB**, exit **0**. Logs: [`pytest_offline.log`](../data/pytest_offline.log), [`pytest_timing.txt`](../data/pytest_timing.txt). This supersedes historical 745-test statements for the audited snapshot only; historical counts are not false merely because tests were later added. The full suite includes the E2E contracts. Neither the 58-test E2E count nor 783 passing cases is semantic accuracy. Provenance: `M.pytest_current`; exact start timestamp was not captured, so M records null rather than fabricating it. End time comes from the log's filesystem mtime.

## New system-paper experiments E1–E10

The system paper's experiment IDs differ from the DR1/DR4 research proposals. Current measurements are recorded in `M.experiment_status_system`; they are completed bounded evaluations with explicit limits, not promises of future validation.

| System ID | Experiment | Current evidence and limits |
|---|---|---|
| E1 | Reproducibility | Evaluated: current input/script hashes, all saved null summaries, four-model 25-draw prefixes, exact graph, bins, and full offline suite reproduce; no full recrawl or fresh full-null generation |
| E2 | Data collection | Evaluated saved-corpus counts, hashes and missingness; no independent collection-completeness or platform-recall benchmark |
| E3 | Duplicate detection | Evaluated historical 1,384-text exact candidate recall: 367/369, two misses, zero extra edges; no semantic duplicate gold or expanded-corpus score |
| E4 | Coordination detection | Evaluated conditional null statistics and bounded replay: 16 tests with B=9,999, raw .0001 and Holm .0016; organic-control specificity and attribution unmeasured |
| E5 | Evidence retrieval | Bounded captured-corpus regression controls included in current suite; curated retrieval measurements belong to the separate evidence audit; no independent open-web gold here |
| E6 | Claim verification | Deterministic abstention/verification controls included; separate evidence audit reports curated cases; independent semantic accuracy remains unmeasured |
| E7 | Event reconstruction | Synthetic timeline invariants and archived structure checked; no independently adjudicated incident-level event/argument accuracy |
| E8 | Video ASR | Existing offline contracts covered; recognition/media quality results delegated to media audit, not remeasured here |
| E9 | End-to-end workflow | Evaluated offline structural regression and six current frozen controls; archived report diff not run, no semantic report benchmark |
| E10 | Runtime/resources | Measured pytest wall/RSS and combined bounded-audit wall/RSS with interpreter/environment; no full production crawl/model/ASR throughput or cost claim |

## Supplemental DR proposal status

Identifiers are namespaced: DR1 §9 defines E1–E6; DR4 §13 defines a different E1–E11. The supplemental E1–E10 inventory below uses **DR4**, with source definitions at `docs/research/DR4-audience-response-2026-11-08.md:478-496`; machine-readable status is `M.experiment_status_DR4`.

| DR4 ID | Experiment | Evaluated status |
|---|---|---|
| E1 | Sentiment versus target stance | Not measured: no independent paired gold comparison |
| E2 | UA/RU/mixed emotion models | Not measured: no local labeled F1/calibration benchmark |
| E3 | Topic discovery versus NMF/LDA | Not measured: no held-out usefulness/stability comparison |
| E4 | Reaction semantics | Not measured: ingestion/schema tests do not validate reaction-to-stance association |
| E5 | Engagement age bias | Not measured: no repeated equal-age model comparison |
| E6 | Author concentration | Partial descriptive diagnostics; full balanced semantic aggregation/bootstrap absent |
| E7 | Coordination sensitivity | Partial: exact retrieval and conditional nulls checked; specificity and full semantic scenario comparison absent |
| E8 | Temporal robustness | Partial: six-hour thematic bins checked; bin/composition/change-point robustness absent |
| E9 | Sarcasm/context | Not measured: synthetic examples do not provide held-out slice scores |
| E10 | Cross-platform transfer | Not measured: no grouped leave-one-platform-out validation |

DR1 status (`M.experiment_status_DR1`): E1 independent human construct/codebook and E2 classifier comparisons remain unmeasured; E3 channel axes has structural artifacts without independent axis precision/recall; E4 joint error has deterministic scenarios without calibrated Monte Carlo; E5 null specificity has reproducible conditional nulls without matched benign events; E6 counter comparability has descriptive sums without equal-age/exposure validation. DR2's 378-item rejected-post relevance sample is a design/replay, with no adjudicated labels or measured relevance recall (`reports/relevance-audit/design-2026-11-08.md:17-47`). DR3's frozen/synthetic gates are implemented in part, while its independent incident chronology and joint evidence/verdict/report semantic metrics remain unmeasured. Recommendations in DR1–DR4 are not completed experiments simply because implementation scaffolding exists.

## Reproduction record and limits

Interpreter: `/home/cyberdid/Projects/Social/.venv/bin/python`; exact Python/package/OS/host/CPU values and UTC check timestamp are in `M.environment` and `M.checked_at_utc`. The combined bounded audit took **4.8317 s**, maximum RSS **1,032,620 KiB** (`M.audit_runtime`). That scope includes JSONL parsing, the full eligible exact sweep, saved-draw recomputation, four-model 25-draw replay, graph/bin reconstruction, and row-level label comparison. It excludes pytest and subsequent auxiliary same-channel/frozen/algebra checks. RSS measures the Python process including imported libraries and loaded artifacts, not an isolated production-stage memory budget.

Commands run from the worktree root:

```sh
/usr/bin/time -v -o papers/social-framework-2026/data/pytest_timing.txt \
  /home/cyberdid/Projects/Social/.venv/bin/python -m pytest -q \
  > papers/social-framework-2026/data/pytest_offline.log 2>&1
PYTHONPATH=. /home/cyberdid/Projects/Social/.venv/bin/python tests/check_telegram_network_dynamics.py
```

The bounded inline Python audit imported `coordination_lsh_audit`, `coordination_null_models`, and `telegram_network_dynamics` with `PYTHONPATH=src/analysis:.`. Reproduction recipe: parse historical JSONL; select `relevant`; call `exact_cross_channel_edges(rel)` and `summarize_candidate_recall` against saved legacy pair keys; compare exact pair keys and scores with saved CSV. Read each saved draw CSV by model, recompute `empirical_summary` for its named statistic, and apply `holm_adjust` to the 16 results. For fresh prefix checks, set `coordination_null_models.EDGES` to the exact-edge CSV and call `comment_analysis(25,20261106,tempdir)` and `temporal_analysis(25,20261106,tempdir)`; compare generated rows with saved rows whose `replicate<=25`. Run `compute_graph` and `narrative_bins` against historical input CSVs. Pair rule/manual rows by `i` for the exact confusion counts shown above. Temporary replay outputs were discarded; immutable source outputs were not overwritten. This recipe, M's per-file hashes/parameters, and production functions define the calculation; the original inline audit script was not added as a production module.

No collection completeness, independent source authenticity, real-world event truth, citation entailment, causal impact, independent attribution, local audience-label accuracy, or open-web retrieval recall was newly established. The new paper can defensibly claim deterministic controls and bounded computational reproducibility, with conditional finite-corpus retrieval measurements and clearly scoped descriptive statistics.
