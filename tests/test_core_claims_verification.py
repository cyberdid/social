"""Tests for core claims verification package (Milestone M1 / GATE-01).

Validates schema compliance, accepted VerificationResult counts (20-30 claims),
exact Unicode character offsets in primary artifacts, and deterministic relations.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts.analysis.build_core_claims_verification import (
    REPO_ROOT,
    build_verification_package,
    render_markdown_report,
)

OUTPUT_DIR = REPO_ROOT / "reports" / "evidence-verification"
JSON_REPORT = OUTPUT_DIR / "core_claims_verification_2026-11-09.json"
MD_REPORT = OUTPUT_DIR / "core_claims_verification_2026-11-09.md"


def test_core_claims_verification_files_exist():
    assert JSON_REPORT.exists(), f"Missing required file: {JSON_REPORT}"
    assert MD_REPORT.exists(), f"Missing required file: {MD_REPORT}"
    assert JSON_REPORT.stat().st_size > 100_000
    assert MD_REPORT.stat().st_size > 10_000


def test_core_claims_verification_schema_and_quantities():
    with open(JSON_REPORT, encoding="utf-8") as f:
        data = json.load(f)

    assert data["schema_version"] == "2.0"
    assert data["track"] == "Track 1: Core Claims & Evidence Verification"
    assert data["milestone"] == "M1"

    summary = data["summary"]
    # Requirement: 20-30 claims
    assert 20 <= summary["total_claims"] <= 30
    assert summary["total_claims"] == 25
    assert summary["supported_within_scope"] == 21
    assert summary["refuted_within_scope"] == 4
    assert summary["unverified"] == 0
    assert summary["total_accepted_assessments"] >= 25
    assert summary["exact_character_offsets_verified"] is True

    # 4 distinct deterministic relations present
    relations = summary["relations_distribution"]
    assert relations["supports"] >= 20
    assert relations["contradicts"] >= 4
    assert relations["rebuts"] >= 1
    assert relations["contextualizes"] >= 1


def test_core_claims_locators_and_exact_passage_offsets():
    with open(JSON_REPORT, encoding="utf-8") as f:
        data = json.load(f)

    passages = {p["passage_id"]: p for p in data["passages"]}

    for item in data["verification_bundle"]:
        claim = item["claim"]
        cid = claim["claim_id"]
        vr = item["verification_result"]

        assert vr["status"] in {"supported_within_scope", "refuted_within_scope"}
        assert vr["search_complete"] is True
        assert vr["minimum_independent_roots"] == 1
        assert len(vr["assessment_ids"]) >= 1

        for ass in item["assessments"]:
            assert ass["decision"] == "accepted"
            assert ass["assessor_id"] == "worker_claims_evidence"
            assert ass["assessment_source"] == "human_adjudication"
            assert ass["independence_status"] == "confirmed_independent"

            cit = ass["citation"]
            pid = cit["passage_id"]
            assert pid in passages, f"Passage {pid} not found in bundle for {cid}"
            passage = passages[pid]

            start = cit["start_offset"]
            end = cit["end_offset"]
            quote = cit["quote"]
            assert passage["text"][start:end] == quote, f"Quote mismatch for {cid}"

            art_start = cit["artifact_start_offset"]
            art_end = cit["artifact_end_offset"]
            assert art_start == passage["artifact_start_offset"] + start
            assert art_end == passage["artifact_start_offset"] + end
            assert cit["offset_unit"] == "unicode_codepoint"


def test_core_claims_numeric_consistency():
    with open(JSON_REPORT, encoding="utf-8") as f:
        data = json.load(f)

    claims_by_id = {item["claim"]["claim_id"]: item["claim"] for item in data["verification_bundle"]}

    # Verify key numeric claims are represented and exact
    # 26 occupants
    assert claims_by_id["claim_core_06_building_26_persons"]["key_values"] == {
        "total_occupants_count": {"value": 26, "operator": "eq"}
    }
    # 4 SZCh
    assert claims_by_id["claim_core_07_building_4_szch"]["key_values"] == {
        "szch_count": {"value": 4, "operator": "eq"}
    }
    # 4 NGU injured
    assert claims_by_id["claim_core_04_ngu_four_injured"]["key_values"] == {
        "injured_ngu_count": {"value": 4, "operator": "eq"}
    }
    # 130 identified
    assert claims_by_id["claim_core_09_npu_130_identified"]["key_values"] == {
        "identified_persons_count": {"value": 130, "operator": "eq"}
    }
    # 27 active participants
    assert claims_by_id["claim_core_10_npu_27_active"]["key_values"] == {
        "active_participants_count": {"value": 27, "operator": "eq"}
    }
    # Ladyka 59 days custody, 22 years old
    assert claims_by_id["claim_core_11_court_ladyka_custody"]["key_values"] == {
        "custody_days_count": {"value": 59, "operator": "eq"},
        "person_age_years": {"value": 22, "operator": "eq"},
    }
    # Ladyka 66560 bail
    assert claims_by_id["claim_core_12_court_ladyka_bail"]["key_values"] == {
        "bail_amount_uah": {"value": 66560, "operator": "eq"}
    }
    # Yena 60 days
    assert claims_by_id["claim_core_16_court_yena_custody_60"]["key_values"] == {
        "custody_days_count": {"value": 60, "operator": "eq"}
    }


def test_markdown_report_matches_json():
    with open(JSON_REPORT, encoding="utf-8") as f:
        data = json.load(f)

    md_content = MD_REPORT.read_text(encoding="utf-8")
    assert "# Доказова верифікація ядерних тверджень: Петропавлівська Борщагівка" in md_content
    assert "claim_core_01_hostages_40" in md_content
    assert "claim_core_06_building_26_persons" in md_content
    assert "claim_core_11_court_ladyka_custody" in md_content
    assert "claim_core_18_dbr_proceedings_426_1" in md_content
    assert "claim_core_22_fire_bucha_warehouse" in md_content

    # Every claim_id from JSON should appear in markdown table
    for item in data["verification_bundle"]:
        assert item["claim"]["claim_id"] in md_content


def test_build_core_claims_verification_deterministic():
    pkg1 = build_verification_package()
    pkg2 = build_verification_package()
    # Ensure exact match
    dump1 = json.dumps(pkg1, sort_keys=True)
    dump2 = json.dumps(pkg2, sort_keys=True)
    assert dump1 == dump2
