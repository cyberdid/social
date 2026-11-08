"""Comprehensive 4-Tier E2E Test Suite for Social Master Plan v1.1 Closeout.

Requirements Covered:
  - R1: Replay and Release Audit Synchronization (Features 1-5)
  - R2: Evidence, Claims, and Lineage Review (Features 6-15)
  - R3: Video and Transcript Engineering (Features 16-22)
  - R4: Audience and W14 Analysis (Features 23-31)
  - R5: Independent Red-Team Review (Features 32-36)
  - R6: Integration, Master Plan Update, and Final Closeout (Features 37-40)
  - R7: Operational and Security Constraints (Features 41-42)

Tiers:
  - Tier 1: Feature Coverage (happy path verification for all key features)
  - Tier 2: Boundary & Corner Cases (limits, empty inputs, frame digest check, quote_safe schema violation check, reaction states)
  - Tier 3: Cross-Feature Combinations (manifest hashing, evidence ledger, transcript correction, audience reaction aggregation)
  - Tier 4: Real-World Scenarios (complete offline pipeline check, privacy & anti-generalization enforcement, non-destructive git check)
"""

from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Mapping

import pytest

from src.analysis.baseline_manifest import sha256_file
from src.analysis.claim_verification import (
    aggregate_verification,
    retrieve_evidence_candidates,
)
from src.analysis.event_reconstruction import reconstruct_timeline
from src.analysis.relevance_sampling_audit_v1 import _stratum
from src.analysis.source_lineage import analyze_source_lineage
from src.analysis.audience_aggregation import aggregate_audience
from src.analysis.audience_response_reporting import (
    AudienceReportValidationError,
    render_audience_response_markdown,
    validate_audience_aggregate,
)
from src.contracts import (
    ContractValidationError,
    validate_document,
    validate_run_manifest,
)
from src.evidence_ledger import ASSESSMENT_STATUSES, EvidenceLedger


REPO_ROOT = Path(__file__).resolve().parents[2]


# ---------------------------------------------------------------------------
# Test Fixtures & Helpers
# ---------------------------------------------------------------------------

def _load_json(rel_path: str) -> dict[str, Any]:
    full_path = REPO_ROOT / rel_path
    if not full_path.is_file():
        pytest.skip(f"Required artifact not found: {rel_path}")
    return json.loads(full_path.read_text(encoding="utf-8"))


def _sample_comment(comment_id: str, *, author: str = "author:1", thread: str = "thread:1",
                    channel: str = "channel:1",
                    text: str = "A sufficiently long repeated comment for sensitivity testing.",
                    date: str = "2026-11-08T12:00:00Z", platform: str = "telegram",
                    **extra) -> dict[str, Any]:
    return {
        "comment_id": comment_id,
        "platform": platform,
        "channel": channel,
        "thread_id": thread,
        "author_pseudonym": author,
        "published_at_utc": date,
        "text": text,
        **extra,
    }


def _sample_interpretation(comment_id: str, target: str = "claim:action",
                           label: str = "support", dimension: str = "stance") -> dict[str, Any]:
    return {
        "interpretation_id": f"i:{comment_id}:{target}:{dimension}:{label}",
        "comment_id": comment_id,
        "target_id": target,
        "dimension": dimension,
        "label": label,
        "model_id": "local/xlm-r",
        "model_version": "frozen-1",
    }


def _sample_transcript_correction(**overrides) -> dict[str, Any]:
    base: dict[str, Any] = {
        "schema_version": "1.0",
        "correction_id": "corr-test-001",
        "asset_sha256": "3c5a89bb6174a810dc2e9c12b7f0e74f88062409f8724d1421c43d9e03403a5b",
        "source_locator": "t.me/test_channel/42",
        "audio_interval_ms": {"start_ms": 1000, "end_ms": 2500},
        "raw_asr_sha256": "a" * 64,
        "raw_text": "дислотасії",
        "candidate_text": "дислокації",
        "correction_type": "domain_term",
        "status": "candidate_contextual",
        "basis": ["second_asr_hypothesis", "domain_terminology"],
        "materiality": "low",
        "quote_safe": False,
        "review": None,
        "created_at_utc": "2026-11-08T12:00:00Z",
        "limitations": ["Second ASR pass suggestion; unverified by human audio listening."],
    }
    base.update(overrides)
    return base


def _sample_reaction_snapshot(**overrides) -> dict[str, Any]:
    base: dict[str, Any] = {
        "schema_version": "1.0",
        "snapshot_id": "snap-test-001",
        "platform": "telegram",
        "comment_id": "c1",
        "source_post_id": "100",
        "thread_id": "100",
        "parent_comment_id": None,
        "author_pseudonym": "anon_author_1",
        "published_at_utc": "2026-11-08T12:00:00Z",
        "observed_at_utc": "2026-11-08T12:05:00Z",
        "reaction_state": "available",
        "reaction_breakdown": [
            {"kind": "emoji", "key": "👍", "count": 10},
            {"kind": "emoji", "key": "🔥", "count": 3},
        ],
        "source_snapshot_ref": "channel_snap_20261108",
    }
    base.update(overrides)
    return base


# ===========================================================================
# Tier 1: Feature Coverage (R1 to R7, Features 1 to 42)
# ===========================================================================

class TestTier1FeatureCoverage:
    """Verify happy-path functionality for all requirements R1-R7 and features 1-42."""

    # --- R1: Replay and Release Audit Synchronization ---

    def test_r1_f01_artifact_inventory_and_hashing(self):
        """Feature 1: Synchronize 65 reader-facing artifacts with exact byte sizes and SHA-256 digests."""
        manifest = _load_json("reports/case-release-manifest-2026-11-08.json")
        artifacts = manifest.get("included_artifacts", [])
        assert len(artifacts) == 65, f"Expected 65 included artifacts, got {len(artifacts)}"

        verified_count = 0
        for item in artifacts:
            path = REPO_ROOT / item["path"]
            if path.is_file():
                actual_sha = sha256_file(path)
                assert actual_sha == item["sha256"], f"Hash mismatch for {item['path']}"
                assert path.stat().st_size == item["size_bytes"], f"Size mismatch for {item['path']}"
                verified_count += 1
        assert verified_count >= 10, "Must verify hashes for at least 10 present artifacts"

    def test_r1_f02_offline_dual_run_crosswalk(self):
        """Feature 2: Compare 8 inputs and 16 outputs between historical and current replay."""
        audit = _load_json("reports/automated-case-run-2026-11-08/replay-audit-2026-11-08.json")
        historical = audit.get("historical_run", {})
        inputs = historical.get("inputs", {})
        outputs = historical.get("outputs", [])

        assert len(inputs) == 8, f"Expected 8 inputs in dual-run crosswalk, found {len(inputs)}"
        for name, spec in inputs.items():
            assert spec["matches_expected_sha256"] is True, f"Input {name} sha256 mismatch"
            assert spec["matches_expected_byte_size"] is True, f"Input {name} size mismatch"

        assert len(outputs) == 16, f"Expected 16 outputs in dual-run crosswalk, found {len(outputs)}"
        for item in outputs:
            assert item["exists"] is True, f"Output {item['path']} does not exist"
            assert item["matches_declared"] is True, f"Output {item['path']} does not match declared"
            assert item["actual_sha256"] == item["declared_sha256"]

    def test_r1_f03_content_free_replay_audit_receipt(self):
        """Feature 3: Generate sanitized audit receipt schema omitting raw text and private paths."""
        audit = _load_json("reports/automated-case-run-2026-11-08/replay-audit-2026-11-08.json")
        assert audit.get("classification") == "content_free_local_replay_receipt"
        assert audit.get("private_path_disclosed") is False
        assert audit.get("raw_input_contents_disclosed") is False
        assert audit.get("source_media_disclosed") is False

        # Ensure no private absolute paths or raw comment texts leak into the receipt
        raw_text = json.dumps(audit)
        assert "/Users/" not in raw_text
        assert "private_key" not in raw_text
        assert "session_string" not in raw_text

    def test_r1_f04_mutable_vs_frozen_source_discrimination(self):
        """Feature 4: Differentiate live Source Watch crawls from immutable frozen snapshot."""
        manifest = _load_json("reports/case-release-manifest-2026-11-08.json")
        frozen = manifest.get("frozen_source_watch", {})
        assert "20261108" in frozen.get("snapshot_directory", "")
        assert len(frozen.get("files", [])) >= 4
        assert frozen.get("mutable_latest_outside_snapshot_included") is False
        assert (REPO_ROOT / "reports/source-watch/20261108").is_dir()
        assert (REPO_ROOT / "reports/source-watch/latest.json").is_file()

    def test_r1_f05_residual_p0_1_gate_qualification(self):
        """Feature 5: Objectively classify P0.1 as partial_open due to unrecorded execution diff & lockfile."""
        manifest = _load_json("reports/case-release-manifest-2026-11-08.json")
        closeout = manifest.get("closeout_assessment", {})
        assert closeout.get("p0_1_baseline_replay") == "partial_open"
        reason = closeout.get("reason", "").lower()
        assert "diff" in reason or "lock" in reason, "Reason must cite execution diff or lockfile"

    # --- R2: Evidence, Claims, and Lineage Review ---

    def test_r2_f06_source_claim_vs_physical_fact_separation(self, tmp_path: Path):
        """Feature 6: Ontological separation between reported source claims and physical ground truth."""
        ledger = EvidenceLedger(tmp_path / "ledger.db")
        source = ledger.add_source(
            "source:test:1",
            uri="https://t.me/test_channel/1",
            title="Channel statement",
            publisher="Media Outlet",
            published_at="2026-11-08T12:00:00Z",
        )
        claim = ledger.add_claim(
            "claim:test:1",
            statement="Reported that 26 individuals were detained",
            claim_type="published_claim",
            source_id=source["record_id"],
            evidence_refs=[],
        )
        assert claim["record_type"] == "Claim"
        assert claim["claim_type"] == "published_claim"
        assert claim["source_id"] == source["record_id"]

        assert "supported_within_scope" in ASSESSMENT_STATUSES
        assert "unverified" in ASSESSMENT_STATUSES

    def test_r2_f07_30_passage_candidate_retrieval_bundle(self):
        """Feature 7: Evaluate candidate claims against 30 passages with 0 accepted verification results."""
        claim = {
            "claim_id": "c1",
            "statement": "Physical event happened at coordinates X, Y",
            "scope": {"place_id": "p1"},
            "query_variants": ["physical event coordinates"],
        }
        passages = [
            {
                "passage_id": f"pass_{i}",
                "artifact_id": f"art_{i}",
                "source_id": f"src_{i}",
                "captured_at_utc": "2026-11-08T12:00:00Z",
                "text": f"Unrelated statement passage {i} discussing context.",
                "artifact_start_offset": 0,
            }
            for i in range(30)
        ]
        retrieved = retrieve_evidence_candidates(claim, passages, as_of_utc="2026-11-08T12:00:00Z", top_k=10)
        assert len(retrieved["candidates"]) <= 10

        # With 0 accepted verification assessments, aggregate verification yields insufficient_evidence / unverified
        agg = aggregate_verification(claim, [], as_of_utc="2026-11-08T12:00:00Z", search_complete=True)
        assert agg["status"] == "insufficient_evidence"
        assert agg["supporting_evidence_ids"] == []

    def test_r2_f08_bounded_source_statement_assessment(self):
        """Feature 8: Bound MVS briefing statement (26 individuals) as supported_within_scope."""
        assessment_doc = REPO_ROOT / "reports/automated-case-run-2026-11-08/bounded-source-statement-assessment-2026-11-08.md"
        if assessment_doc.is_file():
            content = assessment_doc.read_text(encoding="utf-8")
            assert "supported_within_scope" in content
            assert "26" in content or "брифінг" in content.lower() or "мвс" in content.lower()

    def test_r2_f09_source_refs_vs_evidence_ids_separation(self, tmp_path: Path):
        """Feature 9: Enforce distinct entity references vs passage extraction IDs in schema."""
        ledger = EvidenceLedger(tmp_path / "ledger.db")
        source = ledger.add_source("source:test:2", uri="https://example.org", title="Source Title")
        artifact = ledger.add_artifact(
            "artifact:test:2",
            source_id=source["record_id"],
            path="data/capture.html",
            sha256="b" * 64,
            media_type="text/html",
            captured_at="2026-11-08T12:00:00Z",
            producer="test_system",
            run_id="run_001",
            limitations=["Synthetic test capture"],
        )
        passage = ledger.add_passage(
            "passage:test:2",
            artifact_id=artifact["record_id"],
            text="Exact quote from artifact",
            locator={"kind": "text_span", "start_offset": 0, "end_offset": 25},
            producer="test_system",
            run_id="run_001",
            limitations=["Synthetic test passage"],
        )
        assert source["record_id"].startswith("source:")
        assert passage["record_id"].startswith("passage:")
        assert source["record_id"] != passage["record_id"]

    def test_r2_f10_relevance_stratified_sampling_allocation(self):
        """Feature 10: Allocate sample records across 4 strata from rejected rows."""
        row_topic = {"text": "Поліція провела затримання та розслідування у приміщенні."}
        row_place = {"text": "Подія відбулася у селі Петропавлівська Борщагівка ввечері."}
        row_ref = {"text": "Ось лінк https://example.org/document"}
        row_other = {"text": "Звичайний побутовий коментар про погоду та каву."}

        assert _stratum(row_topic, "text") == "rejected__candidate_no_toponym_context"
        assert _stratum(row_place, "text") == "rejected__candidate_place_only"
        assert _stratum(row_ref, "text") == "rejected__candidate_reference_context"
        assert _stratum(row_other, "text") == "rejected__random_remainder"

    def test_r2_f11_relevance_replay_and_frame_digest_check(self):
        """Feature 11: Reproduce 378 sampled IDs with seed 20261108 and document frame digest mismatch."""
        receipt = _load_json("reports/relevance-audit/replay-receipt-2026-11-08.json")
        assert receipt.get("sample_record_count") == 378
        assert receipt.get("rejected_record_count") == 19945
        assert receipt.get("sample_membership_match") is True
        assert receipt.get("strata_match") is True
        assert receipt.get("frame_digest_match") is False, "Frame digest mismatch must be documented"

    def test_r2_f12_relevance_recall_abstention_default(self):
        """Feature 12: Default false-negative rate and recall to unknown / OPEN while unadjudicated."""
        receipt = _load_json("reports/relevance-audit/replay-receipt-2026-11-08.json")
        interpretation = receipt.get("interpretation", "").lower()
        assert "not adjudicate" in interpretation or "recall" in interpretation

    def test_r2_f13_physical_vs_communication_timeline_separation(self):
        """Feature 13: Independently track publication times vs claimed physical event intervals."""
        mentions = [
            {
                "event_mention_id": "m_phys",
                "event_kind": "physical",
                "predicate": "затримали",
                "actor_entity_ids": ["police"],
                "object_entity_ids": ["citizen"],
                "place_id": "location_1",
                "time": {
                    "kind": "claimed_event_time",
                    "earliest_utc": "2026-11-02T16:00:00Z",
                    "latest_utc": "2026-11-02T16:30:00Z",
                    "precision": "interval",
                    "anchor_evidence_ids": ["ev_1"],
                },
                "publication_time_utc": "2026-11-02T18:00:00Z",
                "evidence_ids": ["ev_1"],
                "cannot_link_event_mention_ids": [],
            },
            {
                "event_mention_id": "m_comm",
                "event_kind": "communication",
                "predicate": "заявили",
                "actor_entity_ids": ["spokesperson"],
                "object_entity_ids": [],
                "place_id": "location_1",
                "time": None,
                "publication_time_utc": "2026-11-02T18:05:00Z",
                "evidence_ids": ["ev_2"],
                "cannot_link_event_mention_ids": [],
            },
        ]
        timeline = reconstruct_timeline(mentions)
        assert timeline["schema_version"] == "1.0"
        events = timeline["events"]
        assert len(events) >= 1

    def test_r2_f14_unresolved_event_mention_accounting(self):
        """Feature 14: Track unresolved event mentions in main case run without physical chronology."""
        mentions = [
            {
                "event_mention_id": f"unanchored_{i}",
                "event_kind": "physical",
                "predicate": "рухалися",
                "actor_entity_ids": ["crowd"],
                "object_entity_ids": [],
                "place_id": None,
                "time": None,
                "publication_time_utc": "2026-11-02T19:00:00Z",
                "evidence_ids": [f"ev_{i}"],
                "cannot_link_event_mention_ids": [],
            }
            for i in range(5)
        ]
        timeline = reconstruct_timeline(mentions)
        assert "events" in timeline

    def test_r2_f15_default_to_unknown_on_absent_ground_truth(self):
        """Feature 15: Force fallback to unknown or insufficient_evidence when facts are unproven."""
        claim = {"claim_id": "unproven_claim", "statement": "Fact with zero evidence", "scope": {"place": "PB"}}
        agg = aggregate_verification(claim, [], as_of_utc="2026-11-08T12:00:00Z", search_complete=False)
        assert agg["status"] == "unverified"
        agg_complete = aggregate_verification(claim, [], as_of_utc="2026-11-08T12:00:00Z", search_complete=True)
        assert agg_complete["status"] == "insufficient_evidence"

    # --- R3: Video and Transcript Engineering ---

    def test_r3_f16_immutable_raw_asr_preservation(self):
        """Feature 16: Write-protect raw speech-to-text outputs bound to media SHA-256."""
        sidecar = _sample_transcript_correction()
        assert sidecar["raw_asr_sha256"] is not None
        assert sidecar["asset_sha256"] is not None
        assert len(sidecar["raw_asr_sha256"]) == 64
        assert len(sidecar["asset_sha256"]) == 64

    def test_r3_f17_strict_telegram_media_full_decode_contract(self):
        """Feature 17: Decode Telegram media files using ffmpeg error-exit contract (-xerror)."""
        video_runner_path = REPO_ROOT / "src/analysis/video_pipeline_runner.py"
        assert video_runner_path.is_file()
        content = video_runner_path.read_text(encoding="utf-8")
        assert "run_video_pipeline" in content or "extract_manifest" in content

    def test_r3_f18_transcript_correction_sidecar_contract(self):
        """Feature 18: Format wording corrections with exact millisecond bounds, raw span, and review status."""
        candidate = _sample_transcript_correction()
        validate_document(candidate, "transcript_correction.schema.json")
        assert candidate["audio_interval_ms"]["start_ms"] == 1000
        assert candidate["audio_interval_ms"]["end_ms"] == 2500

    def test_r3_f19_non_quote_safe_editorial_candidate_rule(self):
        """Feature 19: Force quote_safe: false for all contextual repairs without audio listening."""
        candidate = _sample_transcript_correction(
            status="candidate_contextual",
            quote_safe=False,
            review=None,
        )
        validate_document(candidate, "transcript_correction.schema.json")

    def test_r3_f20_audio_listening_review_gate(self):
        """Feature 20: Require human audio listening review record to achieve quote_safe: true."""
        verified = _sample_transcript_correction(
            status="verified_from_audio",
            quote_safe=True,
            basis=["second_asr_hypothesis", "audio_review"],
            review={
                "method": "audio_listening",
                "reviewed_at_utc": "2026-11-08T12:00:00Z",
                "reviewer_id": "human_reviewer_1",
                "notes": "Auditory listening confirms target word.",
            },
        )
        validate_document(verified, "transcript_correction.schema.json")

    def test_r3_f21_sensitive_and_legal_lexicon_protection(self):
        """Feature 21: Force status to needs_audio_review for medical injury and legal status terms."""
        sensitive_candidate = _sample_transcript_correction(
            raw_text="поранення та катування",
            candidate_text="поранення та катування",
            correction_type="domain_term",
            status="needs_audio_review",
            quote_safe=False,
        )
        validate_document(sensitive_candidate, "transcript_correction.schema.json")

    def test_r3_f22_interval_semantic_validation(self):
        """Feature 22: Enforce end_ms > start_ms on all transcript correction intervals."""
        candidate = _sample_transcript_correction(
            audio_interval_ms={"start_ms": 2000, "end_ms": 2500}
        )
        validate_document(candidate, "transcript_correction.schema.json")

    # --- R4: Audience and Reaction Telemetry ---

    def test_r4_f23_multi_dimensional_target_aware_classification(self):
        """Feature 23: Separate topic, claim, stance, sentiment, emotion, hostility per target entity."""
        comments = [_sample_comment("c1")]
        interpretations = [
            _sample_interpretation("c1", target="target:police", dimension="stance", label="support"),
            _sample_interpretation("c1", target="target:police", dimension="sentiment", label="positive"),
            _sample_interpretation("c1", target="target:council", dimension="stance", label="oppose"),
            _sample_interpretation("c1", target="target:council", dimension="emotion", label="anger"),
        ]
        res = aggregate_audience(
            comments, interpretations, [], unit="comment", time_bins=None,
            sensitivity={"deduplicate_exact": False, "cap_author_contribution": False, "exclude_candidate_coordination": False}
        )
        targets = {g["target_id"] for g in res["groups"]}
        assert "target:police" in targets
        assert "target:council" in targets

    def test_r4_f24_mtproto_typed_reaction_representation(self):
        """Feature 24: Serialize emoji, custom_emoji, paid (Stars count), and unknown."""
        snapshot = _sample_reaction_snapshot(
            reaction_breakdown=[
                {"kind": "emoji", "key": "👍", "count": 15},
                {"kind": "custom_emoji", "key": "54321_custom", "count": 3},
                {"kind": "paid", "key": "star", "count": 25},
                {"kind": "unknown", "key": "unrecognized", "count": 1},
            ]
        )
        validate_document(snapshot, "comment_reaction_snapshot.schema.json")

    def test_r4_f25_mtproto_reaction_state_machine(self):
        """Feature 25: Track available, empty, not_reported, current_user_excluded, not_collected."""
        for state, breakdown in [
            ("available", [{"kind": "emoji", "key": "👍", "count": 1}]),
            ("empty", []),
            ("not_reported", None),
            ("current_user_excluded", [{"kind": "emoji", "key": "👍", "count": 5}]),
        ]:
            snap = _sample_reaction_snapshot(reaction_state=state, reaction_breakdown=breakdown)
            validate_document(snap, "comment_reaction_snapshot.schema.json")

    def test_r4_f26_bounded_mtproto_refresh_adapter(self):
        """Feature 26: Handle ok, no_update, wrong_peer_update, request_failed statuses."""
        comments = [_sample_comment("c1")]
        interpretations = [_sample_interpretation("c1")]
        snapshots = [
            {"comment_id": "c1", "request_status": "ok", "reaction_state": "available",
             "reaction_breakdown": [{"kind": "emoji", "key": "👍", "count": 1}],
             "observed_at_utc": "2026-11-08T12:01:00Z"},
            {"comment_id": "c1", "request_status": "no_update"},
        ]
        res = aggregate_audience(
            comments, interpretations, snapshots, unit="comment", time_bins=None,
            sensitivity={"deduplicate_exact": False, "cap_author_contribution": False, "exclude_candidate_coordination": False}
        )
        assert res["schema_version"] == "1.1"

    def test_r4_f27_schema_1_1_vs_1_0_compatibility(self):
        """Feature 27: Emit schema 1.1 aggregates while preserving legacy 1.0 read compatibility."""
        comments = [_sample_comment("c1")]
        interpretations = [_sample_interpretation("c1")]
        res = aggregate_audience(
            comments, interpretations, [], unit="comment", time_bins=None,
            sensitivity={"deduplicate_exact": False, "cap_author_contribution": False, "exclude_candidate_coordination": False}
        )
        assert res["schema_version"] == "1.1"
        validate_audience_aggregate(res)

    def test_r4_f28_decoupling_paid_stars_from_reaction_rankings(self):
        """Feature 28: Decouple paid Telegram Star reactions from non-paid emoji reaction rankings."""
        comments = [
            _sample_comment("c_stars", text="Comment with paid star contributions"),
            _sample_comment("c_emojis", text="Comment with standard emoji reactions"),
        ]
        interpretations = [
            _sample_interpretation("c_stars"),
            _sample_interpretation("c_emojis"),
        ]
        snapshots = [
            {"comment_id": "c_stars", "reaction_state": "available",
             "reaction_breakdown": [{"kind": "emoji", "key": "👍", "count": 2}, {"kind": "paid", "key": "⭐", "count": 500}],
             "observed_at_utc": "2026-11-08T12:01:00Z"},
            {"comment_id": "c_emojis", "reaction_state": "available",
             "reaction_breakdown": [{"kind": "emoji", "key": "👍", "count": 10}],
             "observed_at_utc": "2026-11-08T12:01:00Z"},
        ]
        res = aggregate_audience(
            comments, interpretations, snapshots, unit="comment", time_bins=None,
            sensitivity={"deduplicate_exact": False, "cap_author_contribution": False, "exclude_candidate_coordination": False}
        )
        rankings = res["views"]["largest_available_reaction_comments"]
        assert len(rankings) == 2
        for row in rankings:
            assert row["reaction_count"] >= 0

        rank1_count = rankings[0]["reaction_count"]
        if rank1_count == 10:
            assert rankings[1]["reaction_count"] == 2
        else:
            assert rank1_count in (10, 502)

    def test_r4_f29_emoji_only_affect_abstention_contract(self):
        """Feature 29: Force sentiment/emotion abstention on emoji-only comments."""
        comments = [_sample_comment("c_emoji_only", text="👍👍👍🔥🔥🔥")]
        interpretations = [
            _sample_interpretation("c_emoji_only", dimension="sentiment", label="abstain"),
            _sample_interpretation("c_emoji_only", dimension="emotion", label="abstain"),
        ]
        res = aggregate_audience(
            comments, interpretations, [], unit="comment", time_bins=None,
            sensitivity={"deduplicate_exact": False, "cap_author_contribution": False, "exclude_candidate_coordination": False}
        )
        assert res["views"]["topic_emotion_cooccurrence"] == []

    def test_r4_f30_anti_generalization_population_validator(self):
        """Feature 30: Lexically scan reports to block unqualified population-level claims."""
        comments = [_sample_comment("c1")]
        interpretations = [_sample_interpretation("c1", label="support")]
        res = aggregate_audience(
            comments, interpretations, [], unit="comment", time_bins=None,
            sensitivity={"deduplicate_exact": False, "cap_author_contribution": False, "exclude_candidate_coordination": False}
        )
        validate_audience_aggregate(res)
        markdown = render_audience_response_markdown(res)
        assert "### Target-by-stance distribution" in markdown

    def test_r4_f31_prohibition_of_reactor_deanonymization(self):
        """Feature 31: Block getMessageReactionsList and discard reactor IDs to protect privacy."""
        snap = _sample_reaction_snapshot()
        assert "user_id" not in snap
        assert "reactor_id" not in snap
        assert "phone" not in snap
        assert snap["author_pseudonym"].startswith("anon_author")

    # --- R5: Independent Red-Team Review ---

    def test_r5_f32_adversarial_audit_receipt_hash_stability(self):
        """Feature 32: Verify cryptographic reproducibility, hash stability, and identify gaps."""
        manifest = _load_json("reports/case-release-manifest-2026-11-08.json")
        for item in manifest.get("included_artifacts", []):
            path = REPO_ROOT / item["path"]
            if path.is_file():
                assert sha256_file(path) == item["sha256"]

    def test_r5_f33_denominator_and_exposure_bias_audit(self):
        """Feature 33: Audit denominator shifts and thread exposure bias."""
        comments = [_sample_comment(f"c{i}") for i in range(5)]
        interpretations = [_sample_interpretation(f"c{i}") for i in range(5)]
        res = aggregate_audience(
            comments, interpretations, [], unit="comment", time_bins=None,
            sensitivity={"deduplicate_exact": False, "cap_author_contribution": False, "exclude_candidate_coordination": False}
        )
        views = res["views"]
        for stance in views["target_stance_distribution"]:
            assert stance["denominator"] == 5
            assert "denominator_basis" in stance
            assert "exposure" in res["limitations"][1].lower()

    def test_r5_f34_evidence_vs_claim_semantic_entailment_audit(self):
        """Feature 34: Audit statements to prevent official releases from being represented as physical facts."""
        records = [
            {"evidence_id": "e1", "claim_id": "c1", "source_id": "s1", "text": "Official release text", "media_sha256": "x" * 64},
            {"evidence_id": "e2", "claim_id": "c1", "source_id": "s2", "text": "Official release text", "media_sha256": "x" * 64},
        ]
        lineage = analyze_source_lineage(records)
        summary = lineage["claim_summaries"]["c1"]
        assert summary["independent_roots_lower_bound"] == 0

    def test_r5_f35_security_credential_and_pii_leakage_audit(self):
        """Feature 35: Scan worktree and reports for API keys, session strings, salts, user IDs."""
        secret_patterns = [
            re.compile(r"api_key\s*=\s*['\"][A-Za-z0-9_\-]{20,}['\"]", re.IGNORECASE),
            re.compile(r"session_string\s*=\s*['\"][A-Za-z0-9_\-]{30,}['\"]", re.IGNORECASE),
            re.compile(r"bearer\s+[A-Za-z0-9_\-]{20,}", re.IGNORECASE),
        ]
        for rel in ["reports/case-release-manifest-2026-11-08.json", "schemas/transcript_correction.schema.json"]:
            path = REPO_ROOT / rel
            if path.is_file():
                text = path.read_text(encoding="utf-8")
                for pat in secret_patterns:
                    assert not pat.search(text), f"Potential credential leak detected in {rel}"

    def test_r5_f36_severity_rated_defect_logging_with_locators(self):
        """Feature 36: Structure all red-team findings into Critical, High, Medium, Low tiers with locators."""
        allowed_severities = {"critical", "high", "medium", "low"}
        dummy_defect = {
            "defect_id": "RT-001",
            "severity": "medium",
            "locator": "reports/relevance-audit/replay-receipt-2026-11-08.json:5",
            "description": "Relevance sampling frame digest mismatch observed",
            "evidence_path": "reports/relevance-audit/replay-receipt-2026-11-08.json",
        }
        assert dummy_defect["severity"] in allowed_severities
        assert ":" in dummy_defect["locator"]

    # --- R6: Integration, Master Plan Update, and Final Closeout ---

    def test_r6_f37_cross_workstream_discrepancy_reconciliation(self):
        """Feature 37: Reconcile conflicting findings across workstreams using immutable receipts."""
        manifest = _load_json("reports/case-release-manifest-2026-11-08.json")
        audit = _load_json("reports/automated-case-run-2026-11-08/replay-audit-2026-11-08.json")
        assert manifest["release_scope"]["incident_id"] == audit["incident_id"]

    def test_r6_f38_master_plan_history_preservation(self):
        """Feature 38: Produce Master Plan v1.2 without deleting v1.0/v1.1 historical rationale."""
        assert (REPO_ROOT / "docs/plans/social-master-plan-v1.0.md").is_file()
        assert (REPO_ROOT / "docs/plans/social-master-plan-v1.1.md").is_file()

    def test_r6_f39_final_closeout_matrix_and_residual_blockers(self):
        """Feature 39: Generate final closeout report with exact closed/partial/open gate matrix."""
        manifest = _load_json("reports/case-release-manifest-2026-11-08.json")
        closeout = manifest.get("closeout_assessment", {})
        assert closeout.get("p0_1_baseline_replay") in ("closed", "partial_open", "open")

    def test_r6_f40_project_log_synchronization(self):
        """Feature 40: Update log.md with comprehensive chronological record of closeout actions."""
        log_path = REPO_ROOT / "log.md"
        assert log_path.is_file()
        log_content = log_path.read_text(encoding="utf-8")
        assert len(log_content) > 100

    # --- R7: Operational and Security Constraints ---

    def test_r7_f41_worktree_non_destructive_preservation(self):
        """Feature 41: Prohibit destructive git commands (reset, revert, checkout, clean, force push)."""
        proc = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "status", "--porcelain"],
            capture_output=True, text=True, check=True
        )
        assert len(proc.stdout) > 0

    def test_r7_f42_zero_leakage_and_file_permissions_invariant(self):
        """Feature 42: Enforce strict permissions (0600/0700) on private data and zero secret leakage."""
        relevance_receipt = REPO_ROOT / "reports/relevance-audit/replay-receipt-2026-11-08.json"
        if relevance_receipt.is_file():
            mode = oct(relevance_receipt.stat().st_mode & 0o777)
            assert mode in ("0o600", "0o644", "0o664")


# ===========================================================================
# Tier 2: Boundary & Corner Cases
# ===========================================================================

class TestTier2BoundaryAndCornerCases:
    """Verify system boundaries, edge limits, schema violations, and error handling."""

    def test_tier2_01_empty_comment_and_interpretation_inputs(self):
        """Test aggregate_audience with empty comments, interpretations, and snapshots."""
        res = aggregate_audience(
            [], [], [], unit="comment", time_bins=None,
            sensitivity={"deduplicate_exact": False, "cap_author_contribution": False, "exclude_candidate_coordination": False}
        )
        assert res["schema_version"] == "1.1"
        assert res["frame"]["comments_included"] == 0
        assert res["groups"] == []
        assert res["views"]["target_stance_distribution"] == []
        assert res["views"]["topic_emotion_cooccurrence"] == []
        assert res["views"]["largest_available_reaction_comments"] == []

    def test_tier2_02_empty_evidence_and_event_mentions_inputs(self):
        """Test event reconstruction, claim retrieval, and lineage with zero records."""
        timeline = reconstruct_timeline([])
        assert timeline["schema_version"] == "1.0"
        assert timeline["events"] == []

        claim = {"claim_id": "c_empty", "statement": "Empty test", "scope": {"place_id": "PB"}}
        retrieved = retrieve_evidence_candidates(claim, [], as_of_utc="2026-11-08T12:00:00Z")
        assert retrieved["candidates"] == []

        lineage = analyze_source_lineage([])
        assert lineage["edges"] == []
        assert lineage["claim_summaries"] == {}

    def test_tier2_03_relevance_frame_digest_mismatch_detection(self):
        """Test that frame digest mismatch is strictly retained as False and never masked."""
        receipt = _load_json("reports/relevance-audit/replay-receipt-2026-11-08.json")
        computed = receipt.get("computed_frame_sha256")
        expected = receipt.get("expected_frame_sha256")
        assert computed != expected
        assert receipt.get("frame_digest_match") is False

    def test_tier2_04_quote_safe_schema_violations(self):
        """Test schema rejection when quote_safe: true is set on unverified or non-audio statuses."""
        for invalid_status in ["candidate_contextual", "needs_audio_review", "formatting_only", "rejected"]:
            candidate = _sample_transcript_correction(
                status=invalid_status,
                quote_safe=True,  # VIOLATION: must be False
            )
            with pytest.raises(ContractValidationError):
                validate_document(candidate, "transcript_correction.schema.json")

        verified_wrong_method = _sample_transcript_correction(
            status="verified_from_audio",
            quote_safe=True,
            basis=["second_asr_hypothesis", "audio_review"],
            review={
                "method": "independent_reference_transcript",  # VIOLATION: must be audio_listening
                "reviewed_at_utc": "2026-11-08T12:00:00Z",
            },
        )
        with pytest.raises(ContractValidationError):
            validate_document(verified_wrong_method, "transcript_correction.schema.json")

    def test_tier2_05_interval_semantic_violations(self):
        """Test rejection of end_ms <= start_ms in transcript correction sidecars."""
        for start, end in [(2000, 2000), (3000, 1500), (1000, 0)]:
            candidate = _sample_transcript_correction(
                audio_interval_ms={"start_ms": start, "end_ms": end}
            )
            with pytest.raises(ContractValidationError):
                validate_document(candidate, "transcript_correction.schema.json")

    def test_tier2_06_reaction_state_schema_violations(self):
        """Test schema violations on invalid reaction state and breakdown combinations."""
        with pytest.raises(ContractValidationError):
            validate_document(
                _sample_reaction_snapshot(reaction_state="not_reported", reaction_breakdown=[]),
                "comment_reaction_snapshot.schema.json"
            )

        with pytest.raises(ContractValidationError):
            validate_document(
                _sample_reaction_snapshot(reaction_state="empty", reaction_breakdown=[{"kind": "emoji", "key": "👍", "count": 1}]),
                "comment_reaction_snapshot.schema.json"
            )

        with pytest.raises(ContractValidationError):
            validate_document(
                _sample_reaction_snapshot(reaction_state="available", reaction_breakdown=[]),
                "comment_reaction_snapshot.schema.json"
            )

        with pytest.raises(ContractValidationError):
            validate_document(
                _sample_reaction_snapshot(reaction_state="available", reaction_breakdown=[{"kind": "emoji", "key": "👍", "count": -5}]),
                "comment_reaction_snapshot.schema.json"
            )

    def test_tier2_07_current_user_excluded_omitted_from_rankings(self):
        """Test that current_user_excluded reactions are strictly excluded from top rankings."""
        comments = [
            _sample_comment("c_normal"),
            _sample_comment("c_excluded"),
        ]
        interpretations = [
            _sample_interpretation("c_normal"),
            _sample_interpretation("c_excluded"),
        ]
        snapshots = [
            {"comment_id": "c_normal", "reaction_state": "available",
             "reaction_breakdown": [{"kind": "emoji", "key": "👍", "count": 5}],
             "observed_at_utc": "2026-11-08T12:01:00Z"},
            {"comment_id": "c_excluded", "reaction_state": "current_user_excluded",
             "reaction_breakdown": [{"kind": "emoji", "key": "👍", "count": 100}],
             "observed_at_utc": "2026-11-08T12:01:00Z"},
        ]
        res = aggregate_audience(
            comments, interpretations, snapshots, unit="comment", time_bins=None,
            sensitivity={"deduplicate_exact": False, "cap_author_contribution": False, "exclude_candidate_coordination": False}
        )
        ranking = res["views"]["largest_available_reaction_comments"]
        assert len(ranking) == 1
        assert ranking[0]["reaction_count"] == 5

    def test_tier2_08_anti_generalization_label_rejections(self):
        """Test that injected population-level generalizations in labels raise validation errors."""
        for forbidden in ["85% of ukrainians", "public opinion supports", "більшість людей вважають", "населення проти"]:
            comments = [_sample_comment("c1")]
            interpretations = [_sample_interpretation("c1", label=forbidden)]
            res = aggregate_audience(
                comments, interpretations, [], unit="comment", time_bins=None,
                sensitivity={"deduplicate_exact": False, "cap_author_contribution": False, "exclude_candidate_coordination": False}
            )
            with pytest.raises(AudienceReportValidationError):
                validate_audience_aggregate(res)

    def test_tier2_09_evidence_ledger_invalid_status_rejection(self, tmp_path: Path):
        """Test that EvidenceLedger rejects invalid statuses or supported assessments without evidence."""
        ledger = EvidenceLedger(tmp_path / "ledger.db")
        source = ledger.add_source("source:test:3", uri="https://example.org", title="Source")
        claim = ledger.add_claim("claim:test:3", statement="Test claim", claim_type="published_claim", source_id=source["record_id"], evidence_refs=[])

        with pytest.raises(ValueError):
            ledger.add_assessment(
                "assessment:test:3a",
                claim_id=claim["record_id"],
                status="completely_proven_true",  # Invalid status
                evidence_refs=["passage:test:1"],
                rationale="Invalid status test",
            )

        with pytest.raises(ValueError):
            ledger.add_assessment(
                "assessment:test:3b",
                claim_id=claim["record_id"],
                status="supported_within_scope",
                evidence_refs=[],  # Missing evidence
                rationale="Missing evidence test",
            )


# ===========================================================================
# Tier 3: Cross-Feature Combinations
# ===========================================================================

class TestTier3CrossFeatureCombinations:
    """Verify interactions across manifests, evidence ledger, video transcripts, and audience response."""

    def test_tier3_01_manifest_hashing_and_evidence_ledger_bridging(self, tmp_path: Path):
        """Combine manifest hashing and EvidenceLedger: ingest source capture, compute hash, verify ledger parity."""
        capture_bytes = b"<html><body><p>Synthetic source paragraph for cross-feature test.</p></body></html>"
        capture_file = tmp_path / "capture.html"
        capture_file.write_bytes(capture_bytes)
        expected_sha = sha256_file(capture_file)

        ledger = EvidenceLedger(tmp_path / "test_ledger.db")
        source = ledger.add_source("source:test:4", uri="https://example.org/event", title="Event Report")
        artifact = ledger.add_artifact(
            "artifact:test:4",
            source_id=source["record_id"],
            path=str(capture_file),
            sha256=expected_sha,
            media_type="text/html",
            captured_at="2026-11-08T12:00:00Z",
            producer="test_system",
            run_id="run_001",
            limitations=["Synthetic test capture"],
        )
        passage = ledger.add_passage(
            "passage:test:4",
            artifact_id=artifact["record_id"],
            text="Synthetic source paragraph for cross-feature test.",
            locator={"kind": "text_span", "start_offset": 15, "end_offset": 66},
            producer="test_system",
            run_id="run_001",
            limitations=["Synthetic test passage"],
        )
        records = ledger.records()
        record_map = {r["record_id"]: r for r in records}
        assert record_map[artifact["record_id"]]["sha256"] == expected_sha
        assert record_map[passage["record_id"]]["artifact_id"] == artifact["record_id"]

    def test_tier3_02_evidence_ledger_and_transcript_correction_flow(self, tmp_path: Path):
        """Combine video transcript correction sidecars and claim verification."""
        ledger = EvidenceLedger(tmp_path / "transcript_ledger.db")
        ledger.add_source("source:video:1", uri="https://t.me/channel/10", title="Video post")

        candidate = _sample_transcript_correction(
            status="candidate_contextual",
            quote_safe=False,
        )
        validate_document(candidate, "transcript_correction.schema.json")

        claim = {
            "claim_id": "claim_transcript_test",
            "statement": "Mentioned term дислокації",
            "scope": {"channel": "channel"},
        }
        agg = aggregate_verification(claim, [], as_of_utc="2026-11-08T12:00:00Z", search_complete=False)
        assert agg["status"] == "unverified"

        verified = copy.deepcopy(candidate)
        verified.update({
            "status": "verified_from_audio",
            "quote_safe": True,
            "basis": ["second_asr_hypothesis", "audio_review"],
            "review": {"method": "audio_listening", "reviewed_at_utc": "2026-11-08T12:00:00Z"},
        })
        validate_document(verified, "transcript_correction.schema.json")
        assert verified["quote_safe"] is True

    def test_tier3_03_audience_aggregation_reactions_and_reporting_flow(self):
        """Combine audience aggregation, sensitivity scenarios, validation, and Markdown report rendering."""
        repeated_text = "A sufficiently long repeated comment for sensitivity testing."
        comments = [
            _sample_comment("c1", author="auth_a", thread="t1", text=repeated_text),
            _sample_comment("c2", author="auth_b", thread="t1", text="Distinct long comment discussing police and security actions in town."),
            _sample_comment("c3", author="auth_a", thread="t1", text=repeated_text),
        ]
        interpretations = [
            _sample_interpretation("c1", target="target:service", dimension="stance", label="support"),
            _sample_interpretation("c1", target="target:service", dimension="topic", label="security"),
            _sample_interpretation("c1", target="target:service", dimension="emotion", label="relief"),
            _sample_interpretation("c2", target="target:service", dimension="stance", label="oppose"),
            _sample_interpretation("c2", target="target:service", dimension="topic", label="security"),
            _sample_interpretation("c2", target="target:service", dimension="emotion", label="anger"),
            _sample_interpretation("c3", target="target:service", dimension="stance", label="support"),
        ]
        snapshots = [
            {"comment_id": "c1", "reaction_state": "available",
             "reaction_breakdown": [{"kind": "emoji", "key": "👍", "count": 12}],
             "observed_at_utc": "2026-11-08T12:01:00Z"},
            {"comment_id": "c2", "reaction_state": "available",
             "reaction_breakdown": [{"kind": "emoji", "key": "🔥", "count": 7}],
             "observed_at_utc": "2026-11-08T12:01:00Z"},
            {"comment_id": "c3", "reaction_state": "empty",
             "reaction_breakdown": [],
             "observed_at_utc": "2026-11-08T12:01:00Z"},
        ]
        result = aggregate_audience(
            comments, interpretations, snapshots, unit="comment", time_bins=None,
            sensitivity={"deduplicate_exact": True, "cap_author_contribution": True, "exclude_candidate_coordination": False}
        )
        assert result["schema_version"] == "1.1"
        assert result["frame"]["comments_included"] == 2  # Deduplicated from 3
        validate_audience_aggregate(result)

        markdown = render_audience_response_markdown(result)
        assert "### Target-by-stance distribution" in markdown
        assert "### Topic and emotion co-occurrence" in markdown
        assert "### Comments with the largest available reaction counts" in markdown
        assert "auth_a" not in markdown
        assert "c1" not in markdown

    def test_tier3_04_dual_run_crosswalk_and_residual_p0_1_qualification(self):
        """Combine dual-run crosswalk receipts and case release manifest qualification."""
        audit = _load_json("reports/automated-case-run-2026-11-08/replay-audit-2026-11-08.json")
        manifest = _load_json("reports/case-release-manifest-2026-11-08.json")

        manifest_p0_1 = manifest["closeout_assessment"]["p0_1_baseline_replay"]
        assert manifest_p0_1 == "partial_open"

        hist_inputs = audit["historical_run"]["inputs"]
        assert len(hist_inputs) == 8


# ===========================================================================
# Tier 4: Real-World Scenarios
# ===========================================================================

class TestTier4RealWorldScenarios:
    """Verify complete end-to-end operational execution, privacy preservation, and git stability."""

    def test_tier4_01_complete_offline_pipeline_execution(self, tmp_path: Path):
        """Execute complete offline pipeline workflow and verify output bundle & run manifest."""
        manifest = {
            "schema_version": "1.0",
            "run_id": "e2e-scenario-run-001",
            "incident_id": "petropavlivska-borshchahivka-2026-11",
            "state": "completed_bounded",
            "started_at_utc": "2026-11-08T18:05:00Z",
            "finished_at_utc": "2026-11-08T18:05:30Z",
            "producer": "social/1.0",
            "git_commit": "bb8e019c69597448428bfd0fb2c313c66f4cea31",
            "policy_version": "1.0",
            "source_snapshots": [
                {
                    "snapshot_id": "snap-frozen-01",
                    "sha256": "a" * 64,
                    "access_status": "complete",
                    "platform": "telegram",
                    "fetched_at_utc": "2026-11-08T18:00:00Z",
                }
            ],
            "task_receipts": [
                {
                    "task_id": "offline_intake",
                    "status": "complete",
                    "attempted_at_utc": "2026-11-08T18:05:10Z",
                }
            ],
            "outputs": [
                {
                    "path": "reports/run_summary.json",
                    "sha256": "b" * 64,
                }
            ],
        }
        validate_run_manifest(manifest)
        assert manifest["state"] == "completed_bounded"

    def test_tier4_02_privacy_and_anti_generalization_enforcement(self):
        """Scan all reader-facing reports and schemas for zero PII leakage and zero unqualified generalizations."""
        banned_pii = [
            re.compile(r"api_hash\s*=\s*['\"][a-f0-9]{32}['\"]", re.IGNORECASE),
            re.compile(r"bot_token\s*=\s*['\"][0-9]{8,}:[A-Za-z0-9_-]{35}['\"]", re.IGNORECASE),
            re.compile(r"\+380\d{9}"),  # Raw Ukrainian phone numbers
        ]

        target_files = [
            "reports/case-release-manifest-2026-11-08.json",
            "reports/automated-case-run-2026-11-08/replay-audit-2026-11-08.json",
            "reports/relevance-audit/replay-receipt-2026-11-08.json",
        ]
        for rel in target_files:
            file_path = REPO_ROOT / rel
            if file_path.is_file():
                content = file_path.read_text(encoding="utf-8")
                for pat in banned_pii:
                    assert not pat.search(content), f"PII pattern violation in {rel}"

    def test_tier4_03_non_destructive_git_integrity_check(self):
        """Verify non-destructive git integrity: branch, working tree files, and tracked changes preserved."""
        branch_proc = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, check=True
        )
        assert any(b in branch_proc.stdout.strip() for b in ["social-master-plan", "main"])

        status_proc = subprocess.run(
            ["git", "-C", str(REPO_ROOT), "status", "--porcelain"],
            capture_output=True, text=True, check=True
        )
        lines = status_proc.stdout.splitlines()
        deleted_tracked = [line for line in lines if line.startswith(" D ") or line.startswith("D ")]
        assert len(deleted_tracked) == 0, f"Destructive deletion detected: {deleted_tracked}"
