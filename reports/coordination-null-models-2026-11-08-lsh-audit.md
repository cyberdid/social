# Addendum: exact Jaccard audit of the MinHash-LSH graph

**Document date:** 8 November 2026
**Status:** completed retrospective audit and exploratory conditional-null rerun
**Scope:** fixed continuation snapshot; not a probability sample of Telegram.

This addendum checks candidate recall of the legacy MinHash-LSH graph by exhaustive exact comparison and reruns the two channel-local timing nulls on the resulting exact graph. It refines the 6 November exploratory report; it does not establish organized activity, intent, inauthenticity, or attribution.

## Corpus and exact comparison

The continuation snapshot contains 23,350 collected posts and 1,408 selected relevant posts. The exact audit used full `text_clean` from `posts_clean.jsonl`, retaining the 1,384 relevant posts with text length at least 80 characters and the required channel and URL fields. It applied the existing 5-character shingle function and exact Jaccard scoring. As in the existing graph definition, same-channel pairs are excluded; 18 same-channel pairs met Jaccard ≥0.60 and were not graph edges. The exact sparse sweep uses int64 intersections.

| Jaccard threshold | Exact cross-channel pairs | Legacy LSH pairs retained | Missed exact pairs | Extra legacy pairs | Recall |
|---:|---:|---:|---:|---:|---:|
| ≥0.60 | 369 | 367 | 2 | 0 | 367/369 = 99.45799458% |
| ≥0.75 | 288 | 288 | 0 | 0 | 100% |
| ≥0.90 | 213 | 213 | 0 | 0 | 100% |

The only two missed exact edges were:

| Earlier post | Later post | Exact Jaccard | Absolute lag |
|---|---|---:|---:|
| [insiderukr/137711](https://t.me/insiderukr/137711) | [georgeivensiya/54028](https://t.me/georgeivensiya/54028) | 0.6657142857 | 184.60 min |
| [stranaua/253568](https://t.me/stranaua/253568) | [russia_news07/119614](https://t.me/russia_news07/119614) | 0.6226415094 | 33.083333 min |

All 367 legacy edges at Jaccard ≥0.60 were in the exact cross-channel set; no false-positive edge was found. The exact graph has 357 nodes across 113 channels. There were no missed exact edges at Jaccard ≥0.75 or ≥0.90 **within this eligible snapshot**. These are finite-corpus recall counts, not estimates for posts outside the snapshot, short texts, omitted material, or Telegram as a whole.

Both missed edges have publication lags above 30 minutes. Therefore, the observed counts of pairs within 10 and 30 minutes do not change. The Jaccard ≥0.60 denominator does change from 367 to 369, so its observed shares change slightly:

| Threshold / lag | Legacy graph | Exact graph |
|---|---:|---:|
| J≥0.60 / ≤10 min | 134/367 = 36.51% | 134/369 = 36.31% |
| J≥0.60 / ≤30 min | 198/367 = 53.95% | 198/369 = 53.66% |
| J≥0.75 / ≤10 min | 94/288 | 94/288 |
| J≥0.75 / ≤30 min | 141/288 | 141/288 |
| J≥0.90 / ≤10 min | 53/213 | 53/213 |
| J≥0.90 / ≤30 min | 88/213 | 88/213 |

## Conditional timing nulls on the exact graph

Both channel-local cyclic slot-rotation models were rerun with the 369 exact edges and the slots of all 23,350 collected posts. They preserve channel-local time blocks and rotate content labels cyclically within each block; each graph node receives one rotated time shared across all of its incident edges. The 24-hour model has 184 blocks containing copy nodes and 9,801 timeline slots. The 2-hour model has 291 such blocks and 2,501 slots; 22 are one-slot blocks. The graph has 357 nodes and 113 channels.

The run used `B=9,999`, seed `20261106`, NumPy PCG64 independent streams, an upper-inclusive tail, and the plus-one estimate `p=(k+1)/(B+1)`. The table reports the null mean and central 95% of the simulated counts; these intervals describe the specified randomization distributions, not a population or causal-effect interval.

| Jaccard / lag | Exact-edge denominator | Observed | 24h null mean [2.5–97.5%] | 2h null mean [2.5–97.5%] | Raw p (24h / 2h) |
|---|---:|---:|---:|---:|---:|
| ≥0.60 / ≤10 min | 369 | 134 | 7.131 [2–13] | 42.868 [32–55] | 0.0001 / 0.0001 |
| ≥0.60 / ≤30 min | 369 | 198 | 20.164 [12–30] | 108.786 [93–125] | 0.0001 / 0.0001 |
| ≥0.75 / ≤10 min | 288 | 94 | 5.642 [2–11] | 30.424 [21–41] | 0.0001 / 0.0001 |
| ≥0.75 / ≤30 min | 288 | 141 | 15.979 [9–24] | 79.158 [66–93] | 0.0001 / 0.0001 |
| ≥0.90 / ≤10 min | 213 | 53 | 4.193 [1–9] | 19.717 [12–28] | 0.0001 / 0.0001 |
| ≥0.90 / ≤30 min | 213 | 88 | 11.841 [6–19] | 50.937 [41–61] | 0.0001 / 0.0001 |

The saved `results.json` and `test_summary.csv` agree: all 16 tests in the declared family (four S7 statistics and twelve timing statistics) have zero exceedances, raw `p=0.0001`, and Holm-adjusted `p=0.0016`. This resolves the earlier note of `p=0.0002` for the 2-hour Jaccard ≥0.90 / ≤30-minute test; the saved run records `tail_count=0` and `p_raw=0.0001` for that row as well. At 9,999 draws, 0.0001 is the minimum plus-one estimate, not a zero probability. The result is evidence of departure from these specified conditional nulls only; it is not proof of organized activity or evidence identifying an organizer.

## Reproducibility record

The saved `results.json` is the source of the null-run statistics, model parameters, environment, and recorded input hashes. The exact-edge CSV contains the 369 exact cross-channel edges; the legacy candidates are in `verified_similarity_edges.csv`. `summary.json` consolidates the recall comparison and run metadata without asserting a runtime timestamp.

On 8 November, the null model was rerun in a fresh temporary directory with the exact edge CSV, the recorded seed (`20261106`), and all 9,999 replicates. All six generated outputs matched the saved files byte-for-byte. The machine-readable comparison, command, input hashes, script hash, and output hashes are in [`replay_receipt_2026-11-08.json`](coordination-null-models-2026-11-08-lsh-audit/replay_receipt_2026-11-08.json). This verifies computational reproducibility for this declared run and corpus; it does not validate collection completeness, the conditional null assumptions, or any attribution.

| Artifact or input | SHA-256 |
|---|---|
| `reports/coordination-null-models-2026-11-08-lsh-audit/results.json` | `5d6cd59bd5c31239eff595317a17ec4fd67f6a6329b1475cc10b9557e97a5d74` |
| `reports/coordination-null-models-2026-11-08-lsh-audit/test_summary.csv` | `5ee2eed22e257a10fafba3e6bee7b0ebae1bf01a006f6fe68226b451be35a59b` |
| `reports/coordination-null-models-2026-11-08-lsh-audit/exact_cross_channel_edges_ge_0.6.csv` | `9e1d07c77cba556d1da414ab1d7a8952f09f220c29a71a33066b5f3ccf340e2b` |
| `data/raw/telegram_comments/20261106T071956Z/comments.jsonl` | `a481d50305e50639c555b7a5866045c9b3d8156a5cf9b8cc16b313b2de1e6fb6` |
| `reports/telegram-comments/20261106T071956Z/copypasta_groups.csv` | `ee692e523200a4422a7ae31eebde2718dbd23b0693dc6f0e2c04024e977187bc` |
| `reports/telegram-comments/20261106T071956Z/signals.json` | `5f361a3affb47bb92a7f27880489fe020b1fb78828a5715068dd7d99aa4b4d77` |
| `data/processed/continuation_20261105/posts_clean.jsonl` | `4e859d407aef52c72a8e690dc5716d7d92d11ff7d7a164760db5a4c0ad334350` |
| `reports/continuation_20261105/relevant_posts.csv` | `8b69539801a385bee8f5ea05c5315d18a6d518f96393ff5bf5cd6f57529f8b37` |
| `reports/continuation_20261105/verified_similarity_edges.csv` | `6d559f3a1d553c6015e30e664f53d0d0d623fa88b6c72808d020908303578a58` |
| `reports/coordination-null-models-2026-11-06/results.json` | `9fd8eaa2a0aac2a461e8ca6044081bb99151b75dfd5166ad5e6b045819f0e07a` |
| `src/analysis/coordination_lsh_audit.py` | `fcc7d1df59b613bad5b6bf7dfc5bb585e1de7122442ffab1031f70df7f4bae08` |
| `src/analysis/coordination_null_models.py` | `1fc68af8f45c83f54ba6de705c13de5cf35b3da774bbc7a9386db513120d4f8e` |
| `src/analysis/analyze.py` (shingle implementation) | `a6a4246ff88a42ba8ebf0d67fcd60f17c0d714086f0396f0ed90301eefaa9d94` |

The null-run input hashes, including the exact-edge CSV, comment inputs, relevant-post subset, and full-text input, are also recorded in [results.json](coordination-null-models-2026-11-08-lsh-audit/results.json). Full draws are in [temporal_null_draws.csv](coordination-null-models-2026-11-08-lsh-audit/temporal_null_draws.csv) and [s7_null_draws.csv](coordination-null-models-2026-11-08-lsh-audit/s7_null_draws.csv); the per-test result table is [test_summary.csv](coordination-null-models-2026-11-08-lsh-audit/test_summary.csv), and the complete exact edge list is [exact_cross_channel_edges_ge_0.6.csv](coordination-null-models-2026-11-08-lsh-audit/exact_cross_channel_edges_ge_0.6.csv).
