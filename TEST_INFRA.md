# Test Infrastructure Architecture: Social Master Plan v1.1

## 1. Overview & Testing Philosophy

The Social Master Plan v1.1 test infrastructure provides an independent, opaque-box, requirement-driven verification harness for the analytical and empirical components of the Social pipeline. Operating under strict forensic, privacy, and non-destructive git constraints, the test suite verifies structural contracts, byte-level hash integrity, schema validity, and analytical invariants without relying on facade implementations or hardcoded results.

### Core Testing Invariants:
1. **Requirement-Driven & Opaque-Box**: Tests are derived strictly from formal specifications (`PROJECT.md`, `ORIGINAL_REQUEST.md`, and versioned schemas under `schemas/`) rather than implementation internals.
2. **Genuine Cryptographic Verification**: File digests and byte sizes are verified using genuine SHA-256 algorithms (`hashlib.sha256`) against real filesystem artifacts.
3. **Strict Schema & Semantic Gate Enforcement**: Contracts are enforced through Draft 2020-12 JSON Schema validation augmented by semantic validators (e.g. interval order `end_ms > start_ms`, reaction state mutual exclusivity).
4. **Zero-Leakage & Privacy Compliance**: Automated adversarial regex scanners enforce zero leakage of API credentials, Telegram session strings, phone numbers, or private reactor identities.
5. **Anti-Generalization Population Invariant**: Audience telemetry and opinion distributions are validated to guarantee descriptive framing within observed comment boundaries, blocking unqualified population generalizations.

---

## 2. Test Suite Architecture: 4-Tier Hierarchy

The E2E test suite (`tests/e2e/test_social_masterplan_e2e.py`) is structured into four distinct verification tiers:

```
tests/e2e/
├── __init__.py
└── test_social_masterplan_e2e.py
    ├── TestTier1FeatureCoverage          (42 tests: Features 1–42, Requirements R1–R7)
    ├── TestTier2BoundaryAndCornerCases   (9 tests: Edge limits, empty frames, schema violations)
    ├── TestTier3CrossFeatureCombinations (4 tests: Multi-component pipelines & flows)
    └── TestTier4RealWorldScenarios       (3 tests: Offline pipeline, privacy scan, git preservation)
```

### Tier 1: Feature Coverage (Happy Path Verification)
Directly covers all 42 features identified in `PROJECT.md` across Requirements R1 through R7:
- **R1 (Features 1–5)**: Replay and Release Audit Synchronization (artifact hashing, dual-run crosswalk, content-free receipt, mutable vs frozen discrimination, residual P0.1 gate qualification).
- **R2 (Features 6–15)**: Evidence, Claims, and Lineage Review (source claim vs physical fact separation, 30-passage candidate bundle, bounded source assessment, source refs vs evidence IDs, stratified sampling allocation, frame digest check, recall abstention, timeline separation, unresolved event accounting, fallback to unknown).
- **R3 (Features 16–22)**: Video and Transcript Engineering (immutable raw ASR, ffmpeg `-xerror` decode contract, transcript correction sidecar schema, non-quote-safe candidate rule, audio listening review gate, sensitive lexicon protection, interval semantic validation).
- **R4 (Features 23–31)**: Audience and W14 Analysis (multi-target classification, MTProto typed reactions, state machine, refresh adapter, schema 1.1/1.0 compatibility, decoupling paid Stars from emoji rankings, emoji-only affect abstention, anti-generalization validator, reactor privacy protection).
- **R5 (Features 32–36)**: Independent Red-Team Review (receipt hash stability, denominator/exposure bias audit, semantic entailment audit, credential/PII leakage audit, severity-rated defect logging).
- **R6 (Features 37–40)**: Integration, Master Plan Update, and Final Closeout (cross-workstream reconciliation, history preservation for v1.0/v1.1, closeout matrix logging, project log synchronization).
- **R7 (Features 41–42)**: Operational and Security Constraints (worktree non-destructive preservation, file permissions and zero-leakage invariant).

### Tier 2: Boundary & Corner Cases
Verifies resilience against degenerate inputs, adversarial boundary conditions, and contract violations:
- Empty comment sets, empty interpretation matrices, and empty candidate passages.
- Frame digest mismatch detection ensuring discrepancies are never masked or coerced to `True`.
- Strict schema rejection when `quote_safe: true` is attached to non-audio-verified statuses.
- Interval semantic bounds rejecting reversed or zero-duration millisecond intervals (`end_ms <= start_ms`).
- Reaction state mutual exclusivity rules (`not_reported` with breakdown, `empty` with items, negative counts).
- Exclusion of `current_user_excluded` reactions from top reaction rankings.
- Rejection of injected population-level generalization claims (e.g., `"85% of ukrainians"`, `"public opinion"`).
- Rejection of unsupported statuses and unanchored claims in `EvidenceLedger`.

### Tier 3: Cross-Feature Combinations
Verifies end-to-end integration and data passing across analytical boundaries:
- **Manifest Hashing & Evidence Ledger**: Ingestion of source captures, deterministic SHA-256 calculation, and ledger record binding.
- **Evidence Ledger & Transcript Correction Sidecar**: Linking unverified transcript sidecars (`quote_safe: false`) into evidence assessments, ensuring claims remain unverified until human audio listening gate is satisfied (`quote_safe: true`).
- **Audience Telemetry & Report Rendering**: Ingesting multi-target comment frames with reaction snapshots, applying sensitivity controls (`cap_author_contribution`, `deduplicate_exact`), validating aggregate schemas, and rendering Markdown tables with PII masking.
- **Dual-Run Crosswalk & Gate Blocker Qualification**: Coupling crosswalk verification with release manifest assessments, objectively establishing `partial_open` residual gate status.

### Tier 4: Real-World Scenarios
Verifies system-level operational integrity in production-like contexts:
- **Complete Offline Pipeline Execution**: End-to-end execution of incident specification intake, run manifest generation, and stage receipts without network access.
- **Privacy & Anti-Generalization Automated Audit**: Systematic regex scan of all reader-facing reports and receipts for secret tokens, bot API keys, Ukrainian phone numbers, or reactor identities.
- **Non-Destructive Git Integrity Check**: Verification that worktree branch, tracked modifications, and untracked artifacts remain undamaged and fully preserved.

---

## 3. Feature Inventory Coverage Matrix

| Feature # | Feature Name | Requirement | Milestone | Test Function in `tests/e2e/test_social_masterplan_e2e.py` |
|---|---|---|---|---|
| 1 | Artifact Inventory & Byte Hashing | R1 | M1 | `test_r1_f01_artifact_inventory_and_hashing` |
| 2 | Offline Dual-Run Crosswalk | R1 | M1 | `test_r1_f02_offline_dual_run_crosswalk` |
| 3 | Content-Free Replay Audit Receipt | R1 | M1 | `test_r1_f03_content_free_replay_audit_receipt` |
| 4 | Mutable vs Frozen Source Discrimination | R1 | M1 | `test_r1_f04_mutable_vs_frozen_source_discrimination` |
| 5 | Residual P0.1 Gate Qualification | R1 | M1 | `test_r1_f05_residual_p0_1_gate_qualification` |
| 6 | Source Claim vs Physical Fact Separation | R2 | M2 | `test_r2_f06_source_claim_vs_physical_fact_separation` |
| 7 | 30-Passage Candidate Retrieval Bundle | R2 | M2 | `test_r2_f07_30_passage_candidate_retrieval_bundle` |
| 8 | Bounded Source-Statement Assessment | R2 | M2 | `test_r2_f08_bounded_source_statement_assessment` |
| 9 | Source Refs vs Evidence IDs Separation | R2 | M2 | `test_r2_f09_source_refs_vs_evidence_ids_separation` |
| 10 | Relevance Stratified Sampling Allocation | R2 | M2 | `test_r2_f10_relevance_stratified_sampling_allocation` |
| 11 | Relevance Replay & Frame Digest Check | R2 | M2 | `test_r2_f11_relevance_replay_and_frame_digest_check` |
| 12 | Relevance Recall Abstention Default | R2 | M2 | `test_r2_f12_relevance_recall_abstention_default` |
| 13 | Physical vs Communication Timeline Separation | R2 | M2 | `test_r2_f13_physical_vs_communication_timeline_separation` |
| 14 | Unresolved Event Mention Accounting | R2 | M2 | `test_r2_f14_unresolved_event_mention_accounting` |
| 15 | Default to `unknown` on Absent Ground Truth | R2 | M2 | `test_r2_f15_default_to_unknown_on_absent_ground_truth` |
| 16 | Immutable Raw ASR Preservation | R3 | M3 | `test_r3_f16_immutable_raw_asr_preservation` |
| 17 | Strict Telegram Media Full Decode Contract | R3 | M3 | `test_r3_f17_strict_telegram_media_full_decode_contract` |
| 18 | Transcript Correction Sidecar Contract | R3 | M3 | `test_r3_f18_transcript_correction_sidecar_contract` |
| 19 | Non-Quote-Safe Editorial Candidate Rule | R3 | M3 | `test_r3_f19_non_quote_safe_editorial_candidate_rule` |
| 20 | Audio-Listening Review Gate | R3 | M3 | `test_r3_f20_audio_listening_review_gate` |
| 21 | Sensitive & Legal Lexicon Protection | R3 | M3 | `test_r3_f21_sensitive_and_legal_lexicon_protection` |
| 22 | Interval Semantic Validation | R3 | M3 | `test_r3_f22_interval_semantic_validation` |
| 23 | Multi-Dimensional Target-Aware Classification | R4 | M4 | `test_r4_f23_multi_dimensional_target_aware_classification` |
| 24 | MTProto Typed Reaction Representation | R4 | M4 | `test_r4_f24_mtproto_typed_reaction_representation` |
| 25 | MTProto Reaction State Machine | R4 | M4 | `test_r4_f25_mtproto_reaction_state_machine` |
| 26 | Bounded MTProto Refresh Adapter | R4 | M4 | `test_r4_f26_bounded_mtproto_refresh_adapter` |
| 27 | Schema 1.1 vs 1.0 Compatibility | R4 | M4 | `test_r4_f27_schema_1_1_vs_1_0_compatibility` |
| 28 | Decoupling Paid Stars from Reaction Rankings | R4 | M4 | `test_r4_f28_decoupling_paid_stars_from_reaction_rankings` |
| 29 | Emoji-Only Affect Abstention Contract | R4 | M4 | `test_r4_f29_emoji_only_affect_abstention_contract` |
| 30 | Anti-Generalization Population Validator | R4 | M4 | `test_r4_f30_anti_generalization_population_validator` |
| 31 | Prohibition of Reactor De-anonymization | R4 | M4 | `test_r4_f31_prohibition_of_reactor_deanonymization` |
| 32 | Adversarial Audit of Receipts & Replays | R5 | M5 | `test_r5_f32_adversarial_audit_receipt_hash_stability` |
| 33 | Denominator & Exposure Bias Audit | R5 | M5 | `test_r5_f33_denominator_and_exposure_bias_audit` |
| 34 | Evidence vs Claim Semantic Entailment Audit | R5 | M5 | `test_r5_f34_evidence_vs_claim_semantic_entailment_audit` |
| 35 | Security, Credential & PII Leakage Audit | R5 | M5 | `test_r5_f35_security_credential_and_pii_leakage_audit` |
| 36 | Severity-Rated Defect Logging with Locators | R5 | M5 | `test_r5_f36_severity_rated_defect_logging_with_locators` |
| 37 | Cross-Workstream Discrepancy Reconciliation | R6 | M6 | `test_r6_f37_cross_workstream_discrepancy_reconciliation` |
| 38 | Master Plan v1.2 Release & History Preservation | R6 | M6 | `test_r6_f38_master_plan_history_preservation` |
| 39 | Final Closeout Matrix & Residual Blocker Logging | R6 | M6 | `test_r6_f39_final_closeout_matrix_and_residual_blockers` |
| 40 | Project Log Synchronization | R6 | M6 | `test_r6_f40_project_log_synchronization` |
| 41 | Worktree Non-Destructive Preservation | R7 | M1-M6 | `test_r7_f41_worktree_non_destructive_preservation` |
| 42 | Zero-Leakage & File Permissions Invariant | R7 | M1-M6 | `test_r7_f42_zero_leakage_and_file_permissions_invariant` |

---

## 4. Test Runner & Execution Guidelines

### Execution Commands

1. **Run the Full E2E Test Suite**:
   ```bash
   cd $SOCIAL_REPO_ROOT
   PYTHONPATH=. $SOCIAL_REPO_ROOT/.venv/bin/pytest tests/e2e/ -v
   ```

2. **Run by Specific Tier**:
   ```bash
   # Tier 1 (Feature Coverage)
   PYTHONPATH=. $SOCIAL_REPO_ROOT/.venv/bin/pytest tests/e2e/ -k "TestTier1FeatureCoverage"

   # Tier 2 (Boundary & Corner Cases)
   PYTHONPATH=. $SOCIAL_REPO_ROOT/.venv/bin/pytest tests/e2e/ -k "TestTier2BoundaryAndCornerCases"

   # Tier 3 (Cross-Feature Combinations)
   PYTHONPATH=. $SOCIAL_REPO_ROOT/.venv/bin/pytest tests/e2e/ -k "TestTier3CrossFeatureCombinations"

   # Tier 4 (Real-World Scenarios)
   PYTHONPATH=. $SOCIAL_REPO_ROOT/.venv/bin/pytest tests/e2e/ -k "TestTier4RealWorldScenarios"
   ```

3. **Run Full Repository Test Suite (Unit, Integration, and E2E)**:
   ```bash
   cd $SOCIAL_REPO_ROOT
   PYTHONPATH=. $SOCIAL_REPO_ROOT/.venv/bin/pytest
   ```

---

## 5. Coverage Thresholds & Acceptance Gates

| Metric | Target Threshold | Actual Status |
|---|---|---|
| E2E Test Pass Rate | 100% (58 / 58) | 100% PASS |
| Full Repository Pass Rate | 100% (745 / 745) | 100% PASS |
| E2E Execution Runtime | < 2.0 seconds | 0.17 seconds |
| Cryptographic Artifact Parity | 100% present artifacts | 100% MATCH |
| Schema Conformance | Draft 2020-12 strict pass | 100% PASS |
| PII / Credential Leakage | 0 occurrences | 0 DETECTED |
| Destructive Git Operations | 0 occurrences | 0 DETECTED |
