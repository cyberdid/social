"""Tests for Video & ASR Semantic Calibration Benchmark (Track 3 / GATE-03)."""

from __future__ import annotations

import json
from pathlib import Path
import pytest
import rapidfuzz.distance.Levenshtein as lev

from src.contracts import validate_document
from scripts.analysis.build_asr_calibration_benchmark import (
    normalize_text,
    compute_wer,
    compute_cer,
)

REPO_ROOT = Path(__file__).resolve().parents[1]
BENCHMARK_JSON_PATH = REPO_ROOT / "reports" / "video-pipeline" / "asr_calibration_benchmark_2026-11-09.json"
BENCHMARK_MD_PATH = REPO_ROOT / "reports" / "video-pipeline" / "asr_calibration_benchmark_2026-11-09.md"


@pytest.fixture(scope="module")
def benchmark_data():
    assert BENCHMARK_JSON_PATH.exists(), f"Benchmark JSON not found: {BENCHMARK_JSON_PATH}"
    with open(BENCHMARK_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def test_benchmark_files_exist():
    assert BENCHMARK_JSON_PATH.exists()
    assert BENCHMARK_MD_PATH.exists()
    assert BENCHMARK_JSON_PATH.stat().st_size > 5000
    assert BENCHMARK_MD_PATH.stat().st_size > 5000


def test_benchmark_metadata_invariants(benchmark_data):
    assert benchmark_data["schema_version"] == "1.0"
    assert benchmark_data["benchmark_id"] == "asr-calibration-benchmark-2026-11-09"
    assert benchmark_data["owner"] == "worker_video_semantics"
    assert "sampling_design" in benchmark_data
    assert benchmark_data["sampling_design"]["strata_count"] == 4


def test_stratified_sample_size_in_bounds(benchmark_data):
    clips = benchmark_data["clips"]
    total = len(clips)
    # Requirement R3: 15-20 representative audio clips
    assert 15 <= total <= 20
    assert benchmark_data["overall_metrics"]["total_clips"] == total


def test_all_four_strata_represented(benchmark_data):
    strata = benchmark_data["strata_summary"]
    required_strata = {"stratum_a", "stratum_b", "stratum_c", "stratum_d"}
    assert set(strata.keys()) == required_strata

    for sid in required_strata:
        assert strata[sid]["clip_count"] >= 3, f"Stratum {sid} under-represented"
        assert len(strata[sid]["clips"]) == strata[sid]["clip_count"]


def test_every_clip_has_positive_audio_interval(benchmark_data):
    for clip in benchmark_data["clips"]:
        cid = clip["clip_id"]
        interval = clip["audio_interval_ms"]
        assert "start_ms" in interval and "end_ms" in interval
        assert interval["start_ms"] >= 0
        assert interval["end_ms"] > interval["start_ms"], f"Non-positive interval in {cid}"
        assert clip["duration_ms"] == interval["end_ms"] - interval["start_ms"]
        assert clip["duration_ms"] > 0


def test_empirical_wer_cer_dynamic_programming_recalculation(benchmark_data):
    """Re-compute WER and CER from raw reference and hypothesis strings to verify integrity."""
    for clip in benchmark_data["clips"]:
        cid = clip["clip_id"]
        ref_text = clip["acoustic_reference"]["transcript"]
        raw_text = clip["first_pass_hypothesis"]["raw_text"]

        recomputed_wer = compute_wer(ref_text, raw_text)
        recomputed_cer = compute_cer(ref_text, raw_text)

        assert clip["first_pass_hypothesis"]["wer"] == recomputed_wer["wer"], f"WER mismatch in {cid}"
        assert clip["first_pass_hypothesis"]["cer"] == recomputed_cer["cer"], f"CER mismatch in {cid}"
        assert clip["first_pass_hypothesis"]["word_errors"] == recomputed_wer
        assert clip["first_pass_hypothesis"]["char_errors"] == recomputed_cer


def test_schema_validation_for_every_correction_document(benchmark_data):
    """Validate each clip's transcript correction schema against transcript_correction.schema.json."""
    for clip in benchmark_data["clips"]:
        doc = clip["schema_correction_doc"]
        validate_document(doc, "transcript_correction.schema.json")


def test_quote_safe_true_strictly_requires_audio_listening(benchmark_data):
    """Confirm quote_safe: true is ONLY granted if verified_from_audio with audio_listening."""
    quote_safe_count = 0
    for clip in benchmark_data["clips"]:
        cid = clip["clip_id"]
        if clip["quote_safe"]:
            quote_safe_count += 1
            assert clip["status"] == "verified_from_audio", f"{cid} quote_safe: true without verified_from_audio status"
            assert clip["review"] is not None, f"{cid} quote_safe: true without review metadata"
            assert clip["review"]["method"] == "audio_listening", f"{cid} review method must be audio_listening"
            assert "audio_review" in clip["basis"], f"{cid} basis must contain audio_review"
            assert clip["duration_ms"] > 0
        else:
            assert clip["status"] in ["candidate_contextual", "needs_audio_review", "formatting_only", "rejected"], (
                f"{cid} unexpected status for quote_safe: false"
            )

    assert quote_safe_count >= 8, f"Too few quote_safe: true clips ({quote_safe_count})"
    assert quote_safe_count == benchmark_data["overall_metrics"]["total_quote_safe_true"]


def test_sensitive_lexicon_quarantine_enforced(benchmark_data):
    """Verify that medical injury claims and criminal status assertions are held at quote_safe: false."""
    quarantined_clips = ["clip-09", "clip-10", "clip-13", "clip-17", "clip-18"]
    clips_by_id = {c["clip_id"]: c for c in benchmark_data["clips"]}

    for qid in quarantined_clips:
        assert qid in clips_by_id
        clip = clips_by_id[qid]
        assert clip["quote_safe"] is False, f"Sensitive clip {qid} illegally marked quote_safe: true"
        assert clip["status"] in ["needs_audio_review", "rejected", "candidate_contextual"]
        assert len(clip["limitations"]) >= 1


def test_macro_and_micro_aggregations_exactness(benchmark_data):
    overall = benchmark_data["overall_metrics"]
    clips = benchmark_data["clips"]

    calculated_macro_wer = round(sum(c["first_pass_hypothesis"]["wer"] for c in clips) / len(clips), 4)
    calculated_macro_cer = round(sum(c["first_pass_hypothesis"]["cer"] for c in clips) / len(clips), 4)

    total_ref_w = sum(c["first_pass_hypothesis"]["word_errors"]["ref_words"] for c in clips)
    total_err_w = sum(
        c["first_pass_hypothesis"]["word_errors"]["substitutions"]
        + c["first_pass_hypothesis"]["word_errors"]["deletions"]
        + c["first_pass_hypothesis"]["word_errors"]["insertions"]
        for c in clips
    )
    calculated_micro_wer = round(total_err_w / total_ref_w, 4)

    total_ref_c = sum(c["first_pass_hypothesis"]["char_errors"]["ref_chars"] for c in clips)
    total_err_c = sum(
        c["first_pass_hypothesis"]["char_errors"]["substitutions"]
        + c["first_pass_hypothesis"]["char_errors"]["deletions"]
        + c["first_pass_hypothesis"]["char_errors"]["insertions"]
        for c in clips
    )
    calculated_micro_cer = round(total_err_c / total_ref_c, 4)

    assert overall["macro_wer"] == calculated_macro_wer
    assert overall["micro_wer"] == calculated_micro_wer
    assert overall["macro_cer"] == calculated_macro_cer
    assert overall["micro_cer"] == calculated_micro_cer
