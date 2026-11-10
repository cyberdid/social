# Evidence, events, audience response, attribution, and bounded autonomy audit

Audit date: 2026-11-10. Read-only implementation inspection at baseline `f0e9d0d67422b0c286a2cb9e7d4e935a833a9533`, plus explicitly identified historical Git versions. No collection, platform requests, model downloads, or costly inference. Only this audit file was authored by this auditor. Line references below refer to this baseline unless prefixed by a historical commit. Paths are repository-relative.

## Findings that should constrain the system paper

1. **The implementation supports evidence accounting and bounded deterministic processing; it does not establish incident truth or independently measured semantic accuracy.** The ledger, exact citation checks, temporal separation, source-lineage labels, receipts, and report gates are substantial implemented mechanisms. These mechanisms should be described separately from semantic entailment, physical-event validation, source authenticity, and operator attribution.
2. **The original verification package was a curated execution with labels injected into assessment construction.** At `5812b67`, `build_core_claims_spec` supplied `primary_passage_id`, `expected_relation`, `target_status`, and preselected counter-passages (`scripts/analysis/build_core_claims_verification.py:427–442`). `build_verification_package` selected the primary passage, synthesized a candidate when retrieval missed it (`797–820`), passed `expected_relation` to assessment construction (`828–840`), and asserted the generated result equaled `target_status` (`911–913`). Thus retrieval ran, but the final labels were not a blind inference result. The script labeled those assessments `human_adjudication` and roots `confirmed_independent`; these field values alone do not demonstrate that an independent human adjudication study occurred.
3. **Current verification removes that direct label/passage injection, but remains corpus- and case-conditioned.** `build_core_claims_spec` is a hardcoded list of 25 analyst-selected claims, scopes, numeric values, queries, and interpretive rationales (`468–705`); `build_passages_bundle` selects fixed source artifacts, source IDs, lineage IDs, and literal passage strings (`90–460`). The current builder passes only statement/scope/key values/queries into retrieval and inference (`749–767`) and assesses retrieved candidates only (`765–797`). No `expected_relation`, `target_status`, or `primary_passage_id` is consumed in this current path. This is meaningful remediation, not a held-out benchmark.
4. **Current `validated_rule` acceptance is not demonstrated semantic validation.** `create_evidence_assessment` checks a recognized acceptance-basis string, nonempty rule ID and assessor, exact quoted character span, scope equality, and numeric consistency (`src/analysis/claim_verification.py:681–739`). It does not consult a rule-validation registry, gold set, or semantic judge. The caller supplies `validated_rule` and the same rule identifier for all accepted outputs (`scripts/analysis/build_core_claims_verification.py:774–789`). Report the field as rule acceptance provenance; do not paraphrase it as externally validated entailment.
5. **A current rule can accept the right number with the wrong predicate, and ordinary negation is not reliably handled.** The matcher accepts exact numeric support **or** three overlapping stems and a 0.30 stem ratio (`src/analysis/claim_verification.py:600–649`). Two bounded probes below reproduce false support at fixed confidence 0.92. The stored artifact also accepts injury/walking passages as support for “four deserters.” This is a concrete failure mode, not an estimated error rate.
6. **The general offline pipeline does not invoke the dedicated core-claim inference path.** `run_offline_case` retrieves candidates and calls `aggregate_verification(claim, [], search_complete=False)` (`src/analysis/offline_case_runner.py:407–430`); its policy explicitly says `retrieval_candidates_only_no_automatic_acceptance` (`583–587`). A paper must not transfer the dedicated curated builder's 36 accepted assessments to every orchestrated run.
7. **The event subsystem organizes supplied typed mentions; it does not discover or verify physical events.** The 574-event historical offline artifact and the later 10-mention curated timeline are different workloads. The latter contains five physical and five communication mentions, all 10 unresolved, and zero candidate links. The five physical mentions were supplied by an analyst. These counts are output inventory, not event extraction precision or recall.
8. **Audience topic/claim/stance/sentiment/emotion/hostility infrastructure is implemented as contracts, normalization and aggregation.** The inspected adapter receives labels rather than producing them. Its documentation explicitly excludes semantic validation (`src/analysis/audience_response.py:76–90`); aggregates require `semantic_quality_status: not_evaluated`. Local Ukrainian/Russian/mixed classifier benchmarking remains open in the tracked audience closeout (`reports/orchestrator/teamwork-audience-2026-11-08.md:198`).
9. **Channel infrastructure screening is not operational attribution.** The record builder emits marker/domain observations, default unknown attribution axes, `operational_attribution.status: unverified`, and `confidence: not_assessed` (`src/analysis/channel_evidence.py:144–180`). The two tracked snapshots contain 246 records/239 distinct channels, 137 infrastructure candidates, and 246 unknown origin/content-orientation records. Neither legacy groups nor those 137 candidates establish Russian ownership, state control, coordination, or an influence operation.

## Component inventory

“Implemented” means executable code exists and targeted checks below passed. It does not imply a validated scientific inference.

| Component and concrete entry point | Inputs | Outputs | Actual status / autonomy | Validation and boundary |
|---|---|---|---|---|
| `EvidenceLedger` (`src/evidence_ledger.py:79`) | Caller-authored source, artifact metadata, passages, claims, assessments/results | Immutable SQLite JSON rows; JSONL export/import | Implemented local evidence accounting; level 1 | Append-only triggers (`104–115`), idempotent same-ID insertion and conflict rejection (`288–297`), typed references/status checks (`306–448`). Artifact SHA is format-checked (`335–342`), not read and rehashed by the ledger; passage locator is generic JSON (`344–348`). It is not a content-addressed archive verifier or semantic fact checker. |
| `retrieve_evidence_candidates` (`src/analysis/claim_verification.py:201`) | Supplied claim/query variants and passage list; cutoff; query/top-k budgets | Ranked BM25 candidates, exact spans, search receipt; relation `unassessed` / status `unverified` | Implemented local retrieval; level 1–2 | Capture-time cutoff and direction-specific lineage deduplication (`210–218`); returned labels remain candidates (`372–373`). Search completeness means the supplied search schedule, not complete public-web coverage. |
| `infer_claim_passage_relation` (`449`) | Claim text/key values, entire supplied passage, optional candidate | Heuristic relation, acceptance decision, fixed confidence, rule ID, asserted values | Implemented deterministic case-aware heuristics; level 2 in dedicated builder | Topic-anchor denial guards (`483–519`); TCK, geographic-commentary and injury-causality special cases (`521–558`); numeric/lexical support (`584–649`). No independent semantic accuracy estimate. Candidate argument does not ground inference to its quote. |
| `create_evidence_assessment` (`663`) | Candidate, passage, caller relation/decision/scope/basis | Cited assessment, provenance, numeric/scope downgrade when applicable | Implemented structural acceptance gate; level 1 | Exact Unicode span comparison (`691–697`); caller-defined validated rule ID accepted (`704–710`); declared root is not audited independence (`768–770`). |
| `aggregate_verification` (`779`) | Accepted assessments, scope, cutoff, root threshold, search-complete flag | Scoped seven-state result, used/excluded assessment audit, lineage counts, official-position field | Implemented rule aggregation; level 2 | Excludes unaccepted/mismatched/uncited inputs (`820–859`). Root verdict uses declared IDs (`862–874`); confirmed-independent counts are separate (`882–885`). Physical-fact guard (`886–892`) prevents institutional denials alone from refuting physical facts. |
| `build_verification_package` (`scripts/analysis/build_core_claims_verification.py:708`) | Hardcoded 25 claims + 25 curated passages and supplied timestamps | Dedicated JSON/Markdown case package | Implemented curated end-to-end computation; level 2 | All current assessment passages must be retrieved (`759–797`); threshold one declared lineage root (`799–805`). Current counts are regression output, not measured accuracy. |
| `reconstruct_timeline` (`src/analysis/event_reconstruction.py:117`) | Already typed mentions with actors/predicate/place, time interval/publication time, evidence IDs and cannot-link constraints | Unmerged event candidates, possible-same links, two partial-order timelines, noncausal relations | Implemented typed event organization; level 2 | Exact attributes plus temporal overlap generate reviewable links (`219–242`); no merges. Every mention remains unresolved (`295–302`). Schema and reference checks do not validate whether events happened. |
| `resolve_entity_alias` (`src/analysis/event_reconstruction.py:307`) | Alias and supplied entity registry | Exact-normalized resolved / ambiguous / unresolved match | Implemented registry lookup; level 1 | No fuzzy identity discovery or identity-proof mechanism (`307–336`). No independent `event_resolution` implementation was found in inspected `src` files; event resolution here means candidate-link organization. |
| Physical timeline builder (`scripts/analysis/build_physical_event_timeline.py:26`) | Literal curated mention list, manually supplied intervals, entity IDs, cannot-links, evidence notes | Five physical + five communication mentions in tracked timeline | Implemented curated artifact builder; level 1–2 | Header explicitly says no raw-text/media event discovery (`1–5`); first event's interval and tier are literal inputs (`29–69`). |
| `run_offline_case` (`src/analysis/offline_case_runner.py:303`) | IncidentSpec + explicitly supplied typed files/snapshots | Stage receipts, candidate retrieval, timelines, conflict/information/uncertainty processing, report, manifests and unresolved queue | Implemented fixed offline pipeline; level 2 | Scope/time guards, bounded input loading, non-overwriting run output, structural release gates. General retrieval never creates accepted assessments (`407–430`); semantic status always `not_evaluated` (`583–587`, `630–631`). |
| `run_incident` (`src/analysis/incident_orchestrator.py:406`) | IncidentSpec, fixed watchlist audit, optional typed local input manifest, resource budgets and execute flag | Bounded collection/local run, per-stage receipts and manifest | Implemented bounded controller; level 2 | Only code-owned `web` source-watch adapter (`25–39`); no inferred seed routing, raw extraction, incident-specific relevance, or autonomous model selection. Target/resource limits (`411–428`, `504–522`), models disabled (`443`), and final state denotes controller completion (`695–703`). |
| `evaluate_run_bundle` / frozen suite (`src/analysis/evaluation_harness.py`) | Run artifacts and six checked-in synthetic scenario kinds | Hard-gate outcomes; frozen-control pass/fail; semantic fields `not_evaluated` | Implemented structural QA; level 1–2 | Hash/reference/time/contract checks; semantic exclusion explicit (`571–578`). `run_frozen_suite` labels itself synthetic regression (`645–664`). These are useful controls, not six blind incident evaluations. |
| `normalize_interpretations` (`src/analysis/audience_response.py:76`) | Supplied audience-label rows, comment/context text and registered targets | Stable ID rows for six dimensions, provenance, abstentions, exact spans | Implemented adapter/contract; level 1 | Requires known target/context IDs and provenance; refuses empty-text labels and unsupported emoji-only affect (`110–161`). No label-generation or semantic accuracy validation occurs here. |
| `aggregate_audience` (`src/analysis/audience_aggregation.py:301`) and renderer (`src/analysis/audience_response_reporting.py:315`) | Comment frame, supplied interpretation rows, reaction snapshots, unit/time bins/sensitivity settings | Descriptive target-linked proportions, explicit denominators, reaction availability, per-platform views | Implemented descriptive aggregation; level 2 | Abstentions remain denominator; overlapping labels disclosed (`462–490`). Frame provenance and semantic status emitted (`495–514`). Independent gold set absent; report validator enforces `not_evaluated` (`audience_response_reporting.py:114–115`). No population inference or exposure-adjusted endorsement. |
| `build_channel_evidence` (`src/analysis/channel_evidence.py:119`) | Profiles, public links, source refs, optional manually evidenced attribution axes | Infrastructure features, review candidate flag, unknown axes, unverified operational attribution | Implemented screening/contracts; level 1–2 | Rule: any profile marker or >=5 links with >=30% infrastructure links (`144–151`). Positive supplied axes need refs/scope/validity interval (`94–115`), but that gate does not adjudicate cited evidence. |

## Versioned verification counts and what changed

All rows refer to the same path, `reports/evidence-verification/core_claims_verification_2026-11-09.json`, obtained with `git show <revision>:<path>`. The filename date is not a unique run/version identifier. SHA-256 identifies exact tracked bytes. Counts were parsed from each version's `summary` and checked against per-claim assessment lists; these are not success rates.

| Revision | Package schema | Supported | Refuted | Insufficient | Accepted assessments | Relations supports/contradicts/rebuts/contextualizes | Exact artifact SHA-256 |
|---|---:|---:|---:|---:|---:|---|---|
| `5812b67` | 2.0 | 21 | 4 | 0* | 31 | 21 / 4 / 2 / 4 | `0f55adba5fc426489755c92ebe3d7cf2792c0f66e859eff6d884007441392c34` |
| `e1f66f9` | 2.1 | 19 | 2 | 4 | 27 | 20 / 2 / 1 / 4 | `67e62df6da3ab151230b1265b5bd6e4a33ad4f2bcdfe61b002ddd9f07d686e58` |
| `5d83c46` | 2.2 | 19 | 0 | 6 | 36 | 22 / 2 / 1 / 11 | `2181929db4ff06fea2df0a4d4d250f6d1457faa36cff8d92753353fa4b2dd491` |
| `4b70225`, unchanged at audit baseline | 2.3 | 19 | 0 | 6 | 36 | 22 / 2 / 1 / 11 | `0dea87a77ea444d9ba40970826a89aea0a6f3470d9913043a934329047ef269c` |

*Schema 2.0 summary omitted an insufficient-evidence field; none of its 25 per-claim results had that status. Every version has 25 claims and zero unverified results. The six unresolved current claims are 01 hostages, 02 death, 03 broken spine, 04 incident-caused injuries, 23 fire-video location, and 24 TCK presence.

The following transitions matter substantively:

| Claim | 2.0 | 2.1 | 2.2 / 2.3 | Interpretation |
|---|---|---|---|---|
| 01 hostages / 02 death | refuted | refuted | insufficient | Institutional denials are now separately retained as `officially_disputed`, not physical refutation. |
| 03 broken spine | refuted | insufficient | insufficient | Spokesperson rebuttal is not a clinical diagnosis or forensic record. |
| 04 injury timing/causality | supported | insufficient | insufficient | Injury acknowledgment does not establish when/how injuries occurred. |
| 23 fire-video location | supported | insufficient | insufficient | Geographic correction comments do not establish frame-level geolocation. |
| 24 TCK presence | refuted | insufficient | insufficient | NGU occupancy does not prove absence of TCK personnel. |

The increased 36 accepted assessments in 2.2/2.3 do not indicate improved accuracy. Some are broad contextualizations; three support assessments for claim 07 include two wrong-predicate passages. “Accepted” is a state in this program.

Schema 2.3 explicitly separates generation and evaluation at `2026-11-09T12:58:00Z` from latest eligible evidence capture at `2026-11-09T12:00:00Z` (artifact fields and builder `717–742`). Schema 2.2 reported generation `13:30:00Z`; 2.0/2.1 reported `08:00:00Z`. The earlier labels should not be interpreted as equivalent historical cutoff experiments. Capture filtering enforces timestamp inputs, not independent correctness of manually assigned capture metadata.

## Semantic failure probes and reproducibility boundary

On 2026-11-10, imported only `infer_claim_passage_relation` at the audit baseline and passed the following dictionaries; no files or external services were accessed by the calls. These two deliberately constructed adversarial probes are narrow demonstrations, not a representative test set, and were not added to or used to tune core code. Exact inputs, returned inference records, reproduction command, baseline commit, and the three existing claim-07 assessment/citation records are persisted in `papers/social-framework-2026/data/evidence_counterexamples.json`; both saved probe outputs were reproduced exactly from that artifact.

```python
from src.analysis.claim_verification import infer_claim_passage_relation

infer_claim_passage_relation(
    {"statement": "У будівлі перебували 26 військовослужбовців",
     "key_values": {"total_occupants_count": {"value": 26, "operator": "eq"}}},
    {"text": "26 дерев ростуть у саду."},
)
# Observed: relation='supports', decision='accepted', confidence=0.92,
# asserted_values={'total_occupants_count': {'value': 26, 'operator': 'eq'}},
# rationale says 0 matching root concepts.

infer_claim_passage_relation(
    {"statement": "Поліція прибула на місце події", "key_values": {}},
    {"text": "Поліція не прибула на місце події."},
)
# Observed: relation='supports', decision='accepted', confidence=0.92,
# rationale says 4 matching root concepts.
```

The first is explained by numeric-match `or` lexical-match logic (`640–649`); the second by lack of general predicate-polarity treatment outside specific denial cue rules. Fixed branch confidences (`0.85`, `0.88`, `0.90`, `0.92`) are not calibrated probabilities. The inference confidence is not propagated into assessment construction by the dedicated builder (`774–789`).

An existing artifact example is stronger evidence of operational relevance: for `claim_core_07_building_4_szch`, accepted `supports` assessments cite `psg_mvs_4_szch`, **and** `psg_ngu_4_injured`, **and** `psg_ngu_walked_independently`. Only the first states desertion; the other two concern injury and walking. Thus the artifact's asserted-values structure preserves the claim's count key without establishing its predicate. Further, inference sees full passage text (`463–464`), while `create_evidence_assessment` stores the retrieval candidate quote (`691–697`, `760–765`). Exact substring correctness therefore does not guarantee the quoted span is the evidence that motivated the label. Current contextualizations for claim 04 include a quote consisting of `України`; they remain structurally valid but semantically weak citations.

`tests/test_core_claims_verification.py:48–68` fixes expected case totals and minimum relation counts; `127–145` checks selected known case judgments; `207–221` checks repeatability. These are known-output regression tests and provenance checks. They do not establish independent blind performance. No held-out relation benchmark or independent local gold-set evaluation was located in the audited modules/artifacts.

## State vocabulary and evidence semantics

There is no single universal “verified” bit. The paper should preserve these distinct record layers:

| Layer | Vocabulary / guarantee | Evidence anchor |
|---|---|---|
| Ledger claim type | `published_claim` is source-attributed; `research_finding` requires references | `src/evidence_ledger.py:350–364` |
| Ledger assessment/result status | `unverified`, `supported_within_scope`, `refuted_within_scope`, `conflicting_evidence`, `insufficient_evidence`, `not_verifiable`, `superseded` | `src/evidence_ledger.py:20–31`; reference/supersession checks `381–448` |
| Passage relation | supports, contradicts, rebuts, contextualizes, insufficient_context and other module relation states; separate `candidate`/`accepted` decision | `src/analysis/claim_verification.py:698–708`, `727–758` |
| Report finding kind | documented_fact, source_attributed, supported_within_scope, refuted_within_scope, conflicting, hypothesis, unresolved, methodological_limit | `schemas/analytical_finding.schema.json:5–15`; schema explicitly excludes entailment |
| Event status | `unresolved_event_mention`; candidate link `possible_same`; time bounded/partially_bounded/unresolved | `schemas/event_reconstruction.schema.json:42–88` |
| Execution receipt | complete, partial, blocked, not_found, failed; detailed planned/not_run states may be projected to blocked | `src/analysis/incident_orchestrator.py:28`, `32–39` |
| Audience semantic quality | `not_evaluated`; availability/empty/not-collected states describe observation, not stance | `src/analysis/audience_aggregation.py:12`, `514`; reporting `114–115` |
| Attribution | Axis unknown/default, operational attribution unverified, confidence not_assessed | `src/analysis/channel_evidence.py:94–115`, `167–180` |

Declared source-lineage IDs are not independently established sources. The current aggregate status uses sets of root IDs irrespective of `independence_status`; confirmed independent roots are separately counted (`claim_verification.py:862–885`). In the core package every assessment has `independence_status: candidate`, and the builder threshold is one declared lineage root. Consequently the 19 supported results cannot be described as confirmed by 19 independent investigations or as independently corroborated facts. The physical guard currently applies only when scope type is literally `physical_fact` (`891`); claims whose scope is `official_statement` can receive support for reports of physical events. This is an ontology/scope boundary that must remain visible in prose.

## Events, QA, and autonomy

The tracked November 8 run's `case_summary.json` declares `analysis_status: partial`, `semantic_accuracy: not_evaluated`, and a dirty execution state with recorded base commit `bb8e019c69597448428bfd0fb2c313c66f4cea31`. Its `evaluation_summary.json` reports 574 events and evidence records, six frozen controls passed, zero verification results, and no incident-truth/citation-entailment/authenticity evaluation. These run receipts are evidence of bounded execution with structural checks. They are not a clean-revision experiment or 574 verified physical events.

The November 9 timeline has 10 mentions (5 physical, 5 communication), 10 unresolved items, and zero candidate links. `scripts/analysis/build_physical_event_timeline.py:26–69` shows actor, interval, source ID, evidence-tier and participant-position curation in the input itself. Evidence tiers (`corroborated_multi_source`, `official_proceedings`) are passed through as attributed relations (`event_reconstruction.py:174–195`); the module does not compute a calibrated confidence or independently establish corroboration. The tracked timeline Markdown explicitly defines these tiers as evidence-basis categories, not probabilities (`reports/event-reconstruction/physical_event_timeline_2026-11-09.md:17–23`).

`_timeline_bounds` uses publication time for communication mentions and requires both physical interval endpoints for physical ordering (`event_reconstruction.py:96–106`). Therefore missing or partially bounded physical time yields no physical timeline point, even if a publication time exists. All temporal edges have `causal: false` (`265–276`). Exact matching cannot-link constraints and unmerged possible-same links support cautious organization, not automatic event resolution or causal reconstruction.

The following **proposed descriptive scale is specific to this paper, not a standard or validated maturity model**. Rate a concrete execution path rather than assigning the entire repository one level.

| Level | Descriptive meaning | Repository evidence and limit |
|---:|---|---|
| 0 | Human performs substantive selection, interpretation and decision; software stores/exports it | Curated core claim/passage catalogue, physical mention list, supplied audience labels and attribution assertions. These are human/author inputs even when a script creates the final JSON. |
| 1 | Software executes one fixed transformation or check on supplied inputs | Ledger insertion, exact offset validation, exact alias lookup, infrastructure feature counts, audience normalization. No adaptive analytic judgment implied. |
| 2 | Software executes a bounded multi-step pipeline with predeclared rules, budgets, receipts and unresolved outcomes | Dedicated verification builder, offline runner, fixed source-watch orchestration and structural evaluation. This is the highest broadly supported characterization of the audited integrated paths. |
| 3 | Within a declared objective/budget, software chooses and revises analytic steps or evidence-gathering strategy from intermediate results, with explicit stopping/escalation | Not demonstrated by the audited controller: fixed adapter/watchlist; seed URLs not dispatched; typed inputs required; no raw extraction/model selection. The matcher chooses rule branches, but branching inside a fixed function is not evidence of this level. |
| 4 | Sustained autonomous investigation including independently validated semantic decisions and externally supported final conclusions, with robust oversight | Not demonstrated. No blind semantic evaluation, independent identity/operator attribution or validated physical-event adjudication in audited artifacts. A future design direction, not a current capability claim. |

The controller's state names are not evidence of completed analytic work: `normalized` and `extracting` receipts are explicitly `not_run` for pretyped inputs (`incident_orchestrator.py:670–671`); verifying is partial retrieval only (`672–679`); reconstructing is partial typed processing (`680–683`); reporting is structural (`684–687`). `completed_bounded` means controller processing finished, not that an incident investigation is complete.

## Audience and attribution statements safe for a paper

The implemented audience path can preserve target/context linkage, label provenance and exact text spans; refuse unsupported emoji-only affect; aggregate supplied labels by comment/author/thread/channel with explicit denominators, platform distinctions, abstentions and sensitivity settings; and report reaction availability. It cannot establish population attitudes, internal emotional state, exposure-adjusted support, classifier calibration, or causal persuasion from these contracts. The API reaction pilot is an existing collection receipt for one thread/one reaction request (`reports/audience-response/telegram-reaction-pilot-2026-11-08.md`), not a sentiment/stance/emotion benchmark. Excluding candidate-coordination flags is a descriptive sensitivity analysis; it does not by itself prove the retained comments are organic or the excluded ones are coordinated.

The tracked channel summary (`reports/channel-evidence/masterplan-run-2026-11-08/channel_evidence_summary.json`) records 2 snapshots, 246 channel records, 239 distinct handles, 137 infrastructure candidates and all 246 origins/orientations unknown. Avoid interpreting snapshot-record totals as unique actors. The code preserves legacy group A/B/C/D/E/U values separately (`channel_evidence.py:177`, `219–231`); manual mapping precedence is a data-source priority convention, not independent operational attribution. Separate origin, entity type, operator and content orientation axes are useful ontology design, but evidence-receipt requirements only enforce structure.

## Audit verification record

- Historical package summaries/claims were parsed directly from Git objects for `5812b67`, `e1f66f9`, `5d83c46`, `4b70225` and baseline HEAD; SHA-256 values above identify the objects' bytes. Baseline package has 25 curated passages, 89 retrieved candidate entries across claim receipts, and 36 accepted assessments.
- Two direct synthetic matcher calls above reproduced accepted false supports. Their result is a failure-mode demonstration with no population performance interpretation.
- The default `/usr/bin/python -m pytest` attempt failed because that interpreter lacks pytest. Retried with the existing project environment, without dependency installation:

```text
/home/cyberdid/Projects/Social/.venv/bin/python -m pytest -q \
  tests/test_evidence_ledger.py tests/test_claim_verification.py \
  tests/test_core_claims_verification.py tests/test_event_reconstruction.py \
  tests/test_audience_response.py tests/test_audience_aggregation.py \
  tests/test_channel_evidence.py tests/test_offline_case_runner.py \
  tests/test_incident_orchestrator.py
256 passed in 1.60s
```

These passing tests substantiate contract/regression behavior covered by the named suites. They coexist with the semantic counterexamples; no inference accuracy, extraction F1, independent corroboration rate, or autonomous investigation success rate is claimed.
