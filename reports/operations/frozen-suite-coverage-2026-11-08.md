# Frozen adversarial suite coverage — 8 November 2026

## Scope

This is a code-and-test inventory for master-plan scenarios F01–F16. It distinguishes the six controls executed by `src/analysis/evaluation_harness.py --frozen-suite` from unit/regression tests elsewhere. A passing deterministic test demonstrates the tested software invariant only; it does not validate a source, a real-world event, or semantic accuracy.

## Coverage matrix

| ID | Scenario | Current automated coverage | Remaining limit / status |
|---|---|---|---|
| F01 | Known incident | `tests/fixtures/evaluation_harness/known_microcase.json`; `tests/test_evaluation_harness.py::test_known_microcase_reconstructs_separate_physical_timeline`; interval tests in `tests/test_event_reconstruction.py`. | Synthetic microcase only. A real, independently verified event chronology and timing tolerance are unavailable; real-event accuracy is `not_evaluated`. |
| F02 | Conflicting witness accounts | `contradictory_testimony.json` checks both evidence sides and `conflicting_evidence`; aggregation regressions in `tests/test_claim_verification.py`. | Does not establish whether real statements were coded correctly or are independent. |
| F03 | Copy amplification | `mass_copy_fanout.json`, `tests/test_evaluation_harness.py::test_thousand_copies_cannot_claim_two_independent_roots`, and `tests/test_source_lineage.py`. | Verifies that supplied root IDs are not multiplied by fan-out. Discovery of the true first source in a real network remains unresolved. |
| F04 | Official correction / retraction | `corrected_statement_as_of.json`; as-of and supersession tests in `tests/test_claim_verification.py`. | Tests cutoff and explicit correction links, not the truth or legal effect of an actual correction. |
| F05 | Missing corpus | `missing_corpus.json` checks that unavailable sources and absent evidence do not produce a refutation. Parameterized regressions in `tests/test_claim_verification.py::test_incomplete_corpus_sensitivity_lowers_support_without_inventing_refutation` define ten synthetic source families, then remove 20%, 50% and 80% (retaining 8, 5 and 2 explicit independent roots). At a threshold of two roots, support remains within scope. `test_one_remaining_root_after_eighty_percent_loss_abstains` separately defines five families, removes four, and verifies that the single remaining root yields `unverified`. | This is a synthetic aggregation control, not evidence that the real source corpus is 20/50/80% complete. The frozen harness still has only one missingness case. |
| F06 | Miscontextualized video | `reused_video_mismatch.json`; CPU media fingerprint tests in `tests/test_media_fingerprints.py` cover different scenes and trimmed/resized/re-encoded shared footage. | Similar frames do not establish event, time or place. No independently verified real-video geolocation/recording-time benchmark exists. |
| F07 | Same-name actors | `tests/test_event_reconstruction.py::test_exact_alias_resolution_never_uses_fuzzy_names` retains ambiguous duplicate aliases. | No full-pipeline real-identity benchmark; identifiers and reference data are unavailable. |
| F08 | Nearby place names | `test_nearby_but_distinct_place_ids_do_not_produce_same_event_candidate`. | Tests distinct supplied IDs, not geocoding or correct extraction of ambiguous place names from text. |
| F09 | Quotation and stance | `tests/test_narrative_v3.py` covers quotation, reporting, denial, debunking, questions and abstention. | Sarcasm, nested quotes and cross-sentence stance have no independent gold evaluation. Candidate semantics remain `not_evaluated`. |
| F10 | Relative-time ambiguity | `test_unresolved_relative_time_is_preserved_but_not_placed_on_timeline`; separate publication/event time tests. | Relative phrases are kept unresolved; no validated resolver maps “yesterday” to a real event time or recording time. |
| F11 | Causal hallucination | `test_builds_interval_order_without_claiming_causality`, `tests/test_information_dynamics.py`, and `tests/test_report_generator.py::test_unsupported_causal_sentence_is_blocked`. | Guards against unsupported causal promotion; no causal effect is estimated for the incident. |
| F12 | Numeric quantifiers | `tests/test_claim_verification.py` checks natural-language operator matching for Ukrainian, Russian and English forms (`до 40`, `не меньше 40`, `понад 40`, `under 40`, `приблизно 40`) and symbolic forms (`<40`, `<=40`, `≤40`, `>40`, `>=40`, `≥40`, `≈40`). It rejects negated or conflicting bounds it does not interpret (`not up to 40`, `not ≤40`, `more than approximately 40`), checks `men` as a people-count role, and prevents `comment_count` from satisfying a people/participant count while accepting matching fields. | The parser handles a bounded explicit vocabulary only. It does not verify passage semantics or define a tolerance for approximate values; that assessment remains explicit and candidate-safe. |
| F13 | Edited media | `tests/test_media_fingerprints.py` exercises frame-level matching for trimmed, resized, re-encoded and horizontally mirrored clips; it finds a known segment inside a multi-scene montage and after a two-second title-card prelude, while rejecting clearly different footage. The v2 fingerprint records crop/mirror variants and matched frame times. | Only the deterministic title-card prelude is tested; overlay cards, arbitrary title insertion and exact segment-boundary correctness are not. Thresholds remain exploratory and uncalibrated; matches are candidates only. |
| F14 | Silence / poor ASR | `tests/test_video_text_extract.py::test_no_asr_segments_are_not_claimed_as_proof_of_no_speech`; time offsets and model provenance are tested. | No reference transcript means WER/CER, overlap-speaker accuracy and low-confidence calibration are unavailable. Batch transcript semantics are not validated. |
| F15 | Model/provider drift | `tests/test_video_text_extract.py` and `tests/test_video_pipeline_runner.py` cover model fingerprint, version and cache identity behavior. | No cross-provider/prompt semantic regression benchmark or automatic calibration revocation exists. There is no validated model-quality reference set. |
| F16 | Prompt injection in a source | `tests/test_report_generator.py::test_untrusted_finding_text_cannot_inject_markdown_link` tests output escaping only. | This is not an LLM prompt-injection test. The current deterministic workflow does not execute source text as agent instructions; a source-to-LLM tool boundary and dedicated adversarial controls are still required before adding autonomous browsing agents. |

## Result and release interpretation

- The standalone frozen harness remains **6/6 passed**; it covers selected structural invariants from F01–F06, not all 16 scenarios.
- Module regression tests extend coverage through F07–F15. This run added F05 synthetic 20/50/80% missingness aggregation checks over explicitly defined ten- and five-family denominators, F12 quantifier/operator and counted-entity checks, and F13 horizontal-mirror plus embedded-montage matching. They do not constitute one integrated end-to-end benchmark.
- F13's deterministic two-second title-card-prelude control passes; overlay cards and exact segment-boundary correctness remain untested.
- F16 is not an operational code path in the present system. A report escaping test cannot establish prompt-injection resistance.
- Real-case event truth, semantic claim/stance accuracy, source authenticity, physical chronology, recording geolocation, and real-world evidence independence remain `not_evaluated` because the necessary external references are absent.

## Source test paths

- `tests/test_evaluation_harness.py`
- `tests/test_claim_verification.py`
- `tests/test_source_lineage.py`
- `tests/test_event_reconstruction.py`
- `tests/test_narrative_v3.py`
- `tests/test_information_dynamics.py`
- `tests/test_report_generator.py`
- `tests/test_media_fingerprints.py`
- `tests/test_video_text_extract.py`
- `tests/test_video_pipeline_runner.py`
