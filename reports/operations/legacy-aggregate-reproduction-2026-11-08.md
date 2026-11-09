# Reproduction of frozen legacy aggregates — 8 November 2026

## Scope

The legacy analysis for `continuation_20261105` was rerun from the current branch code against the already processed snapshot held in the main checkout. Inputs were read only; generated files were written to a temporary directory and removed after comparison. The temporary run imported the current `src/analysis/analyze.py` and `continuation_audit.py`; it did not collect data or call a model. No row text, source URLs, channel names, or identifiers are included here.

This verifies computational repeatability against the saved outputs, not the correctness or representativeness of the source material.

## Aggregate results

| Metric | Reproduced value |
|---|---:|
| Publications in snapshot | 23,350 |
| Relevant publications | 1,408 |
| Channels with relevant publications | 159 |
| Sum of snapshot view counters | 115,931,014 |
| Multi-channel copy clusters in legacy output | 132 |
| Verified similarity edges in sensitivity audit | 367 at Jaccard ≥0.60; 288 at ≥0.75; 213 at ≥0.90 |

View counters are a sum of captured counters, not unique reach.

## Output comparison

The following regenerated outputs were byte-identical to the saved baseline:

| File | SHA-256 |
|---|---|
| `results.json` | `2255092f6a205346dfcafd3474a6c7c814ee563622ba284ecb692f8b40376ea5` |
| `relevant_posts.csv` | `8b69539801a385bee8f5ea05c5315d18a6d518f96393ff5bf5cd6f57529f8b37` |
| `forwards_edges.csv` | `a619bc9c9e33005b3c5259860ab5a3e863c0f15b2887e33f0212a8cb1ec3b4c0` |
| `narratives_by_group.csv` | `f986fcc580bd2e8edcd9953e05a83fd023a88239b63d8c19a84838f995588b46` |
| `timeseries_10min_posts.csv` | `54ade37fe311a2e0d9e16c23c54a689bee5a875adfd495c0a81a5cba4484934a` |
| Audit `audit_results.json` | `e9051b3ba98e3676f0589d33eae99e12ea4241e7e94cf9dd1dfc91c649975f8c` |
| Audit `verified_similarity_edges.csv` | `6d559f3a1d553c6015e30e664f53d0d0d623fa88b6c72808d020908303578a58` |

`copy_clusters.csv` had 132 rows in both runs and its row multiset was identical, but the serialized row order differed because the legacy export sorts by `channels` without a deterministic tie-breaker. The saved baseline SHA-256 is `33e32164801efd550b1189106955c0ea6b369fef311756b0b7a29656ada79324`; the temporary reproduction SHA-256 was `6f2f2ccbbeb17a2747379836e57aaffaa4594d42577b0f440ca07f2cf681c6a8`. This is an ordering difference, not a changed cluster membership or aggregate. The legacy export was left untouched to preserve its existing output contract.

The two saved plots were regenerated with the same analysis code and frozen input snapshot, with output redirected to a temporary directory so the saved files were not changed. Both decoded to 1950×720 RGBA pixels and were pixel-identical to their saved counterparts; their PNG byte streams were not identical:

| File | Saved PNG SHA-256 | Regenerated PNG SHA-256 | Decoded RGBA SHA-256 | Result |
|---|---|---|---|---|
| `timeseries.png` | `e625fd1cff4e2b9967e4615af0cfef3d4ede56bd0d2956221d42136a8a5e98ee` | `ac143f0f0bb7edfbdbb69f14c74294a06ffca942d71e78b5cffec874bd8d06a3` | `4b3d563452361cb4df836bed6df6738fd8544540dc54511d7c881f404594257a` | Pixel-identical; PNG bytes differ |
| `timeseries_day1.png` | `852166eaf4b1bffe3d90eb85f6fce1c178e14788fd49760f7a6ca8c29e1c1063` | `8887d0a5c506d32a21b83957435a2b3bc3a25772dc0ff2cf7d098e12f05e3cfa` | `4a42894bd4ab0857a101c34d9f7a31c6d882d10cfeb4a193328466ae7206f985` | Pixel-identical; PNG bytes differ |

## Interpretation

The checked CSV/JSON outputs are reproducible from the same processed snapshot, except for the documented copy-cluster row ordering. The saved plots reproduce at decoded-pixel level, not as identical PNG byte streams. These comparisons cover the listed outputs only; no reproducibility claim is made for other legacy outputs. This run does not validate legacy narrative labels, MinHash/LSH recall, channel attribution, source independence, or any real-world claim. The worktree itself does not contain the ignored raw/processed dataset; the read-only input snapshot came from `$SOCIAL_REPO_ROOT/data/processed/continuation_20261105`.
