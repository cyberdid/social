# Teamwork Evidence, Claims, and Lineage Review (2026-11-08)

**Author:** Worker M2 (Evidence, Claims, and Lineage Reviewer)  
**Date:** 2026-11-08  
**Scope:** Read-only empirical audit of Acceptance Gates **P0.2** (Source-to-Finding Trace & Lineage), **P0.3** (Relevance Sampling Audit & Coverage), and **P0.6** (Physical Event Reconstruction & Chronology Bounds).  
**Repository Working Directory:** `/home/cyberdid/Projects/Social/.worktrees/social-master-plan`  
**Compliance Mandate:** Zero fabrication, strict ontological separation of reported claims from physical ground truth, default to `unknown` on absent evidence.

---

## 1. Executive Summary & Acceptance Gate Matrix

This report provides the formal read-only audit of the evidence, claim-lineage, relevance-sampling, and event-reconstruction layers for the Social Master Plan v1.1 closeout. Every claim, count, digest, and gate evaluation in this document is derived from immutable receipts, versioned schemas, deterministic replay tools, and validated repository artifacts.

| Acceptance Gate | Previous Status | Audited Status | Core Empirical Findings & Residual Blockers |
|---|---|---|---|
| **P0.2 Source-to-Finding Trace & Lineage** | Partial | **PARTIAL (OPEN)** | The 30-passage candidate retrieval bundle evaluates 555 candidate claims against 30 passages (1,110 BM25 directions; 11,897 candidate hits); it yields **0 accepted VerificationResults**, **0 confirmed dependency edges**, and **0 independent roots** (`independent_roots_lower_bound = 0`). Five source-attributed quotes from five archived pages are validated textually within scope, but official communications (e.g. MVS 26 individuals, NPU 130 persons) are source statements, not proven physical ground truth. Semantic claim verification and independent roots remain unestablished. |
| **P0.3 Relevance Sampling Audit & Coverage** | OPEN | **OPEN** | Replay with seed `20261108` reproduces exact stratum allocations and all n=378 sampled record IDs from N=19,945 rejected records (out of 23,386 total; 2,003 out-of-window; 1,438 selected). Achieved planning half-width is 0.049976. Frame digest fails reproduction (`70155a55...` expected vs `ecdb98...` / `02ab55...` computed) due to unrecorded sampler input row transformation. **0 sample records have been adjudicated**; false-negative rate and overall recall remain `unknown`. |
| **P0.6 Physical Event Reconstruction** | OPEN | **OPEN** | The main case run preserves 574 event mentions, but records **0 physical timeline rows** and leaves all 574 mentions unresolved (`merge_status = "unresolved_event_mention"`). Publication timestamps (2026-11-02 to 2026-11-05) do not establish event or filming times. Bounded 2-event reconstruction run models 1 day-level source mention and 1 communication publication timestamp with 0 causal inferences. Physical ground-truth timeline is completely absent; defaults to `unknown`. |

---

## 2. Ontological Boundary: Reported Claims vs. Physical Ground Truth

A foundational requirement of rigorous open-source and social incident analysis is the strict demarcation between **what a source reports** and **what physically occurred in reality**. In official and mass-media communications surrounding the Petropavlivska Borshchahivka incident (2–8 November 2026), multiple institutional actors released quantified and categorical claims. This audit establishes their formal boundaries:

### 2.1 The Ministry of Internal Affairs (MVS) Briefing Statement (26 Individuals)
- **Source Citation:** MVS briefing regarding events in Kyiv region, published 3 November 2026 (`https://mvs.gov.ua/news/u-ministerstvi-vnutrisnix-sprav-ukrayini-vidbuvsia-brifing-shhodo-podii-na-kiyivshhini`). Captured 2026-11-08T08:05:55.795375Z. Artifact SHA-256: `3aaf8cb5f02ab6b1228635d3a49ab9699c97cde2d49db993c84e84f3caef4f49`. Passage SHA-256: `69c5d2e3d195be84dcdd4da81b85cec09849a6605987ba5dc1b9709e55de27e0`.
- **Reported Text:** Exact sentence at Unicode code points 3526–3566: *«Загалом у приміщенні перебували 26 осіб.»*, preceded at Unicode code points 3293–3373 by context: *«Командувач Національної гвардії України генерал-майор Олександр Півненко пояснив»*.
- **Assessment Scope:** Evaluated under `claim_mvs_statement_26_people_20261103` in the append-only ledger continuation. Status is **`supported_within_scope`**.
- **Ontological Boundary:** `supported_within_scope` certifies **only** that the captured MVS webpage contains this attribution to Commander Oleksandr Pivnenko. It does **not** establish:
  1. That 26 individuals were physically present in the premises;
  2. The actual roster, military status, injuries, or conduct of the individuals;
  3. Independent physical verification of the premises or conditions;
  4. The truth of any other assertions in the briefing.

### 2.2 The National Police of Ukraine (NPU) Statement (130 Persons)
- **Source Citation:** NPU press communication, 5 November 2026 (`https://npu.gov.ua/news/politseiski-natsionalnoi-politsii-ukrainy-razom-z-sbu-vzhe-vstanovyly-130-osib-iaki-mozhut-buty-prychetnymy-do-zavorushen-na-petropavlivskii-borshchahivtsi`).
- **Reported Text:** Statements indicating that police together with SBU have established 130 persons who may be involved in the unrest.
- **Ontological Boundary:** This is an operational press announcement of an ongoing police inquiry. It is **not** a judicial verdict, not an authenticated roster of charged defendants, and not established physical fact. It cannot be used to declare that 130 identifiable individuals committed physical acts at the site without primary court filings, charge sheets, and defense proceedings.

### 2.3 Additional Institutional Communications
- **National Guard of Ukraine (NGU) Injury Report:** An NGU-hosted statement alleging that 4 servicemembers were injured. This is an administrative institutional press release; it is not a primary hospital admission log, forensic medical examination (SME), or authenticated trauma record.
- **Ombudsman Office Announcements:** Requests for administrative review and inquiries directed to law enforcement. These document regulatory actions taken by an ombudsman, not physical reconstruction of the altercation.
- **State Bureau of Investigation (DBR) Announcements:** An announcement on 7 November 2026 regarding an upcoming video segment (`https://dbr.gov.ua/news/top-news-vid-dbr56`). Two DBR pages failed capture during Source Watch crawls due to TLS certificate verification errors; this is a technical transport failure, not proof that records do not exist. However, no substantive findings can be inferred from uncaptured or announced materials.

**Rule of Evidence:** Any report statement asserting physical crowd counts, participant identities, or physical injury must cite authenticated primary ground truth (e.g. certified medical records, court proceedings, unedited geo-located and time-stamped video forensics). When only official press releases are available, the claim must be reported strictly as `source_attributed` and never promoted to `documented_fact`.

---

## 3. P0.2 Source-to-Finding Trace & Lineage Audit

### 3.1 The 30-Passage Candidate Retrieval Bundle Verification
The candidate retrieval system links extracted claims to primary text passages using deterministic local BM25 scoring. The offline run `run-source-linked-20261108` executed an audit over private typed inputs:

- **Passage Corpus:** 30 passages total:
  - 23 historical baseline passages (predominantly social posts and legacy excerpts);
  - 7 newly locatable article passages from the 2026-11-08 Source Watch snapshot (MVS, NGU, Ombudsman, Suspilne, hromadske).
  - Merged passage input SHA-256: `e0d03b457cf3d962e75296c19e41dd815941cb08056e94412b8eb05c32cba401`.
- **Query Set:** 555 candidate claims extracted across the incident dataset.
- **Search Budget & Execution:** 2 search directions per claim (claim proposition wording and counterevidence cue), executing exactly **1,110 BM25 search directions**.
- **Retrieval Output:**
  - Total candidate passage hits returned: **11,897**.
  - Candidate hits originating from the 7 newly added source passages: **3,012**.
  - Claims matching at least one of the 7 new passages: **552 / 555** (99.46%).
- **Verification Results:** **0 accepted EvidenceAssessments** and **0 `VerificationResult` records emitted**.
- **Status:** **`partial_candidate_retrieval_only`**.

#### Critical Analysis of Retrieval Results:
1. **Low Specificity of Whole-Post BM25 Queries:** The fact that 552 of 555 candidate claims retrieved at least one hit among the 7 news articles reflects lexical overlap between broad vocabulary (e.g. "Київщина", "поліція", "військові", "конфлікт") and full-post query strings. It does **not** indicate evidence support or semantic relevance.
2. **Retrieval Hits are Not Corroboration:** Under `claim-verification-v1.md`, candidate retrieval hits are solely search leads for review. They do not constitute semantic entailment, factual corroboration, or contradiction.
3. **Invalidity of the Historical 9,769-Hit Run:** In earlier run telemetry (`run-post-fix`), 9,769 hits were reported. This occurred because a zero-budget configuration was bypassed by an old runner substituting `top_k=20`. This count is invalid execution telemetry and has been officially superseded by the compliant 11,897-hit run receipt (`retrieval-validity-addendum-2026-11-08.md`).

### 3.2 Source Lineage and Independent Roots Audit
The source lineage pipeline (`src/analysis/source_lineage.py`) computes directed dependency edges and connected component families based on explicit references and identical asset hashes.

#### Whole-Corpus Lineage Telemetry (`reports/channel-evidence/masterplan-run-2026-11-08/`):
- **Input File:** `source_lineage_input.jsonl` (SHA-256: `2c3a8485a303d51d34746298108d349b400ca367eb931fd3c52a7b55aba348b8`).
- **Input Records:** 23,386 total records.
  - Non-blank text and valid time: 22,942.
  - Excluded blank text: 444.
  - Excluded invalid/missing time: 0.
- **Observed Candidate Relations:**
  - Total candidate edges: **2,823**.
  - Same-text platform forward resolutions: **348**.
  - Unresolved forward references (pointing outside snapshot): **498**.
  - Resolved forwards with different exact text: **29**.
- **Root Status:** `independent_root_count_established: false`.

#### Scoped Bounded Input Audit (`source-lineage-input-audit-2026-11-08.json`):
An audit was conducted over the bounded inputs: the 30 archived passages (`e0d03b45...`, 304,082 bytes) and the 574 report bundle evidence records (`0308da3e...`, 1,830,069 bytes):
- **Confirmed Dependency Edges Emitted:** **0**.
- **Independent Source Roots Asserted:** **0** (`independent_roots_lower_bound: 0`).
- **Audit Findings:** Neither input contains `claim_id` fields or explicit dependency references (`derived_from_evidence_ids`, `forwarded_from_evidence_id`, `quoted_evidence_ids`, etc.). Unique identifiers in the metadata do not establish independent sources. Under `source_lineage.py`, the absence of an observed link does **not** establish independence.

### 3.3 Structural Separation: `source_refs` vs. `evidence_ids`
To prevent confusing source publishers with specific text extractions, the schema strictly enforces:
- `source_refs`: List of `source_id`s representing the publishing institution or channel (e.g. `source_57425990dc7315a1b617c61cbe596ec31d6c53e1add19fa8442a38e41578229f` for MVS).
- `evidence_ids`: List of `passage_id`s or `artifact_id`s representing the exact captured text span or byte container (e.g. `passage_b1befbee74f5d623e709a2c4c2b36f723c1d6bd107411b2884e94812acfa3374`).
- Confirmed by unit test `test_source_references_are_not_copied_from_passage_evidence_ids`, which validates that source entity IDs are never conflated with evidence extraction locators.

---

## 4. P0.3 Relevance Sampling Audit & Coverage

Acceptance Gate P0.3 evaluates whether posts rejected by the rule-based relevance filter contain missed incident-relevant posts (false negatives), thereby biasing downstream analysis.

### 4.1 Population, Frame, and Stratified Allocation
The sampling frame and SRSWOR allocation were verified using `src/analysis/relevance_sampling_replay.py` against the clean post corpus:
- **Source Corpus:** `20261105T101013Z+20261105T102914Z/posts_clean.jsonl`.
- **Source Digest:** SHA-256 `d229d8618021cf285f24c712eb9cd37ca85eb0e8bee2d8a7f74b6e7c574cda3f`.
- **Total Source Posts:** **23,386**.
- **Time-Window Exclusions:** **2,003** posts excluded by rule (tagged `outside_time_window`).
- **In-Scope Frame:** **21,383** posts.
- **Rule-Selected (Positive) Posts:** **1,438**.
- **Rejected Frame Eligible for Audit:** **19,945** posts.

#### Stratified Sampling Allocation (Seed `20261108`):
The audit design uses stratified simple random sampling without replacement (SRSWOR) partitioned across four disjoint strata:

| Stratum ID | Description | Population $N_h$ | Sample $n_h$ | Inclusion Prob $\pi_h$ |
|---|---|---:|---:|---:|
| `rejected__candidate_no_toponym_context` | Topic candidate keywords present, but no recognized place name | 5,519 | 104 | 0.018844 |
| `rejected__candidate_place_only` | Incident place name present, but no incident topic keyword | 124 | 4 | 0.032258 |
| `rejected__candidate_reference_context` | Reference or context markers (links, forwards, media mentions) | 8,770 | 165 | 0.018814 |
| `rejected__random_remainder` | Remaining posts in the rejected frame | 5,532 | 105 | 0.018980 |
| **Total** | | **19,945** | **378** | — |

- **Achieved Planning Half-Width:** **0.049976** (target $\le 0.05$ at 95% confidence using finite-population correction and worst-case binary variance 0.25).

### 4.2 Replay Execution and Frame Digest Mismatch Analysis
The deterministic replay execution (`replay-receipt-2026-11-08.json`) confirms:
1. **Source Hash Match:** `source_sha256_matches_reference: true`.
2. **Strata Allocations Match:** `strata_match: true` (all four strata counts match exactly).
3. **Sample Membership Match:** `sample_membership_match: true` (exact set of 378 record IDs reproduced identically).
4. **Frame Digest Mismatch:** `frame_digest_match: false`.
   - **Expected Frame Digest (from prior manifest):**  
     `70155a5510fe4467ada895bcc68ef337ab5596e2e56e99f1f63646cc50472256`
   - **Recomputed Frame Digest:**  
     `ecdb98...ccd027` (in design-2026-11-08.md) / `02ab555b74196500bfee5cc5eb07d972498c1110a1354161f2de35508f886cdc` (in replay receipt).

#### Technical Root Cause of Frame Digest Mismatch:
In `relevance_sampling_audit_v1.py`, `_validated_frame` computes `row_digest = hashlib.sha256(_canonical_json(source)).hexdigest()` for every row in the rejected frame, and then hashes the sorted array of row summaries to create `frame_sha256`. Because `source` contains the full dictionary of each row as passed into the sampler, any variation in auxiliary fields added during upstream data loading (such as temporary keys, type normalizations, or composite ID keys) alters the row serialization. The initial sampler invocation did not archive the exact byte stream of its pre-sampler transformed rows.  
**Audit Finding:** The sample selection algorithm and the 378 sampled units are 100% reproducible and verifiable, but the cryptographic frame digest cannot be verified against historical records without the exact intermediate row representations.

### 4.3 Adjudication Status and Gate Determination
- **Adjudicated Records:** **0 / 378**. None of the 378 sampled records have been reviewed by human annotators or validated on an independent gold standard.
- **False-Negative Rate:** **`unknown`**.
- **Recall:** **`unknown`**.
- **Gate Status:** **P0.3 remains strictly OPEN**. A sampling design receipt cannot be certified as an executed audit.

---

## 5. P0.6 Physical Event Reconstruction & Chronology Audit

Acceptance Gate P0.6 evaluates whether the system can reconstruct a verifiable timeline of physical events on the ground, distinguishing real-world actions from media publication times.

### 5.1 Main Case Run Audit (`event_reconstruction_summary.json`)
The telemetry from the full automated case run confirms:
- **Candidate Event Mentions:** **574**.
- **Candidate Merge Links:** **0**.
- **Merge Status:** All 574 mentions are classified as `unresolved_event_mention`.
- **Physical Timeline Rows:** **0**.
- **Communication Timeline Rows:** **574** (all anchored purely by `publication_time_utc`, spanning from `2026-11-02T10:41:03Z` to `2026-11-05T10:18:17Z`).
- **Physical Event Time Established:** **`false`**.
- **Filming Time Established:** **`false`**.

### 5.2 Bounded Event Reconstruction Run (`reported-event-reconstruction-2026-11-08`)
A targeted bounded run of `event_reconstruction_cli` was executed over the official MVS statement passage (`passage_78ef18c56c48abeed87014bae6c0b802886ac86e1d708398ae719d9141243896`):
- **Input File:** `source-reported-event-input-2026-11-08.jsonl` (SHA-256: `2ea6052f5ace348928726541ec2ab37c28fec590f52ccdb9bc3403fcfa4b3596`).
- **Event Candidates:** 2 event mentions.
  1. **Physical Mention:** `event:mention_mvs_reported_situation_date_20261104`  
     - Event time: `2026-11-01T22:00:00Z` to `2026-11-02T21:59:59.999999Z` (Europe/Kyiv calendar day interval for 2 November 2026).  
     - Status: `unresolved_event_mention`.
  2. **Communication Mention:** `event:mention_mvs_publication_date_statement_20261104`  
     - Publication time: `2026-11-04T10:35:00Z`.  
     - Status: `unresolved_event_mention`.
- **Candidate Links:** **0**.
- **Temporal Relations Inferred:** **0**.
- **Causal Relations Inferred:** **0**.

### 5.3 Chronological & Forensic Deficiencies
1. **Day-Level Dating is Not Physical Ground Truth:** An official communication stating that an event occurred on "2 November" provides only a 24-hour coarse boundary. It does not establish the minute of initial confrontation, the duration of the standoff, or the chronology of police intervention.
2. **Prohibition of Causal Inference from Temporal Order:** Under `event-reconstruction-v1.md`, temporal order does not establish causation (`post hoc ergo propter hoc`).
3. **Absence of Independent Time Anchors:** No metadata exists in the repository verifying bystander video recording times, CCTV camera synchronization, emergency dispatch logs, or medical triage timestamps.
4. **Gate Status:** **P0.6 remains strictly OPEN**.

---

## 6. Uncertainty & Epistemic Limitations Inventory

In accordance with the Integrity Mandate, all unverified empirical questions are explicitly classified as `unknown` or `insufficient_evidence`:

| Epistemic Dimension | Repository State | Permitted Statement | Prohibited Inferences |
|---|---|---|---|
| **Physical Count in Building** | 1 source statement (MVS) quoting NGU commander stating 26 persons. | MVS published a briefing quoting Commander Pivnenko stating 26 individuals were in the building. | "It was established that 26 people were inside." |
| **Suspect Roster / Detainees** | Police communications citing 130 persons; Suspilne court reporting on 2 custody hearings. | Police announced ongoing identification of up to 130 persons; court hearings were reported for 2 named suspects. | "130 perpetrators have been confirmed." |
| **Injuries & Casualties** | NGU press statement asserting 4 injured servicemen. | An NGU publication asserts 4 servicemen sustained injuries. | "Four servicemen were injured" (as proven physical fact). |
| **Relevance Classifier Recall** | 378 sampled rejected posts; 0 human adjudications. | Relevance sampling design achieved target half-width 0.05 on 19,945 records; recall is unknown. | "The relevance filter captures >95% of relevant discussion." |
| **Source Independence** | 2,823 candidate edges; 0 confirmed dependency roots. | Observed posts share exact normalized text or forward references; independent roots are 0. | "Multiple independent channels verified the incident." |
| **Physical Event Timing** | 574 unresolved event mentions; 0 physical timeline rows. | Available data records when posts were published, not when physical actions occurred. | Substituting post publication time for event occurrence time. |

---

## 7. Cross-Workstream Interface Contract Verification

- **M1 (Replay & Release Auditor):** Verified that `reports/case-release-manifest-2026-11-08.json` and `reports/automated-case-run-2026-11-08/replay-audit-2026-11-08.json` record the identical inputs (8/8) and outputs (16/16) for both runs. Verified that the 30-passage bundle byte size (304,082 bytes) and digest (`e0d03b45...`) align with M1 release inventory.
- **M3 (Video & Transcript Engineer):** Verified that 0 raw ASR files are modified, all transcript corrections require `quote_safe: false` until listened to against audio segments, and no video OCR/ASR text is promoted to verified physical timeline evidence without audio verification.
- **M4 (Audience & W14 Analyst):** Verified that Telegram Star reactions are decoupled from emoji reaction totals in `src/analysis/audience_aggregation.py`, no reactor IDs are retained, and emoji affect abstention is enforced.
- **M5 (Independent Red-Team Reviewer):** Verified that all denominator shifts (e.g. 158 vs 159 relevant channels due to snapshot membership), retrieval budget distinctions (9,769 telemetry hits vs 11,897 compliant hits), and frame digest mismatches are fully documented without omission.
- **M6 (Integrator & Lead Agent):** Provides unambiguous gate evaluations: P0.2 is Partial (Open), P0.3 is Open, P0.6 is Open. These evaluations must be carried forward into Master Plan v1.2 and the final closeout report.

---

## 8. Verification Receipts & Command Log

### 8.1 Automated Test Verification
The domain test suite for M2 modules was executed and confirmed 100% passing:

```bash
PYTHONPATH=. /home/cyberdid/Projects/Social/.venv/bin/pytest \
  tests/test_claim_verification.py \
  tests/test_source_lineage.py \
  tests/test_relevance_sampling_audit_v1.py \
  tests/test_relevance_sampling_replay.py \
  tests/test_event_reconstruction.py -v
```
**Output:** `138 passed in 0.31s`.

The full repository test suite was executed:
```bash
PYTHONPATH=. /home/cyberdid/Projects/Social/.venv/bin/pytest -q
```
**Output:** `671 passed, 16 subtests passed in 5.21s`.

### 8.2 Cryptographic Digest Summary

> **Note (Reconciled per Red-Team RT-FINDING-01):** Table 8.2 was updated during M6 closeout integration to reflect the verified final on-disk byte sizes and SHA-256 digests.

| Artifact Path | Description | Byte Size | SHA-256 Digest |
|---|---|---:|---|
| `data/processed/20261105T101013Z+20261105T102914Z/posts_clean.jsonl` | Source post corpus (N=23,386) | 55,105,209 | `d229d8618021cf285f24c712eb9cd37ca85eb0e8bee2d8a7f74b6e7c574cda3f` |
| `reports/relevance-audit/replay-receipt-2026-11-08.json` | Relevance sampling replay receipt | 1,888 | `033be55a51d453f2649a158a1eca1094b464edc343be7a02b8de6d3f07c059d2` |
| `reports/channel-evidence/masterplan-run-2026-11-08/source_lineage_input.jsonl` | Source lineage input records | 10,037,860 | `2c3a8485a303d51d34746298108d349b400ca367eb931fd3c52a7b55aba348b8` |
| `reports/automated-case-run-2026-11-08/source-lineage-input-audit-2026-11-08.json` | Bounded lineage input audit receipt | 3,627 | `fb8922519d99797764c027deb2962a0e002c8f4ae2f7f7aaaa74c49ffe18ed78` |
| `reports/automated-case-run-2026-11-08/event_reconstruction_summary.json` | Main case run event reconstruction summary | 718 | `e32bdcbd22536254123453989c8d7a6af05519cb976ca2bbfe251867ef07f5e5` |
| `reports/automated-case-run-2026-11-08/reported-event-reconstruction-2026-11-08/run_receipt.json` | Bounded event reconstruction run receipt | 2,127 | `451b3f2865ed46c43d6683b01e7aec63a2c80e936bf3e5e7a26e94edde9c6359` |
| `reports/automated-case-run-2026-11-08/claim_retrieval_summary.json` | BM25 candidate retrieval summary | 625 | `69827dbe4aff455ea3771ddf1974d6414b7fa4897c5917bf19c24fb4a9252ab9` |

---

## 9. Conclusion

This audit confirms that while the underlying deterministic modules, schemas, and test harnesses for P0.2, P0.3, and P0.6 are mathematically correct and fully operational, the empirical case-level evidence gates cannot be certified as closed. 

Official statements remain source-attributed claims rather than established physical facts. The 30-passage candidate retrieval bundle has generated zero accepted verification results. The relevance sampling frame exhibits an unrecorded transformation digest mismatch, and its 378 sampled units remain unadjudicated. The physical timeline remains ungrounded with 574 unresolved mentions.

Accordingly, in compliance with the Social Master Plan v1.1 standards and the Teamwork Integrity Mandate, **P0.2 remains Partial (Open), P0.3 remains OPEN, and P0.6 remains OPEN**.
