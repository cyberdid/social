"""Tests for Corpus & Source Watch Lineage Matrix and Manifest.

Milestone M4: Corpus & Source Watch Provenance Harmonization
Social Master Plan v2.0
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_manifest_schema_and_validity():
    """Verify that lineage_manifest_2026-11-09.json exists and conforms to schema requirements."""
    manifest_path = REPO_ROOT / "reports/provenance/lineage_manifest_2026-11-09.json"
    assert manifest_path.exists(), f"Manifest file missing at {manifest_path}"

    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data.get("schema_version") == "social_lineage_manifest_v1"
    assert data.get("manifest_id") == "corpus_and_sourcewatch_lineage_2026-11-09"
    assert data.get("milestone") == "M4"
    assert "generated_at_utc" in data
    assert "provenance_rule" in data
    assert "corpus_reconciliation" in data
    assert "sourcewatch_reconciliation" in data
    assert "lineage_matrix" in data
    assert "verified_artifact_checksums" in data


def test_strict_provenance_rule_invariants():
    """Verify formulation of the strict provenance rule and its four invariants."""
    manifest_path = REPO_ROOT / "reports/provenance/lineage_manifest_2026-11-09.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    rule = data["provenance_rule"]
    assert "rule_statement" in rule
    assert "(corpus_version, run_id, timestamp)" in rule["rule_statement"]

    invariant_names = {inv["name"] for inv in rule["invariants"]}
    expected_invariants = {
        "prohibition_of_denominator_bleed",
        "immutable_content_addressing",
        "separation_of_transport_error_from_factual_absence",
        "complete_delta_accounting",
    }
    assert expected_invariants.issubset(invariant_names)


def test_corpus_reconciliation_exact_math():
    """Verify exact numerical reconciliation between historical (1408) and merged (1438) corpora."""
    manifest_path = REPO_ROOT / "reports/provenance/lineage_manifest_2026-11-09.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    rec = data["corpus_reconciliation"]
    hist = rec["historical"]
    merged = rec["merged"]
    deltas = rec["deltas"]

    # Post count reconciliation
    assert hist["total_posts"] == 23350
    assert merged["total_posts"] == 23386
    assert deltas["total_posts_delta"] == 36

    assert hist["relevant_posts"] == 1408
    assert merged["relevant_posts"] == 1438
    assert deltas["relevant_posts_delta"] == 30

    # Channel count reconciliation
    assert hist["relevant_channels_count"] == 159
    assert merged["relevant_channels_count"] == 158
    assert deltas["relevant_channels_delta"] == -1
    assert deltas["excluded_channels"] == ["kiber_boroshno"]

    # kiber_boroshno post details
    kiber = deltas["channel_exclusion_details"]
    assert kiber["channel"] == "kiber_boroshno"
    assert kiber["msg_id"] == 13675
    assert kiber["url"] == "https://t.me/kiber_boroshno/13675"
    assert kiber["source_snapshot"] == "20261105T104050Z"
    assert "20261105T104050Z" in kiber["reason_for_exclusion"]

    # URL casing mutations
    assert deltas["raw_url_string_diff_hist_only"] == 475
    assert deltas["raw_url_string_diff_curr_only"] == 505
    assert deltas["direct_casing_mutations_common_count"] == 354
    assert deltas["normalized_url_diff_hist_only"] == 121
    assert deltas["normalized_url_diff_curr_only"] == 151
    assert deltas["normalized_url_diff_curr_only"] - deltas["normalized_url_diff_hist_only"] == 30

    # View count reconciliation
    assert hist["total_views_relevant"] == 115931014
    assert merged["total_views_relevant"] == 119515745
    assert deltas["total_views_relevant_delta"] == 3584731

    # Similarity edges
    assert hist["minhash_lsh_verified_pairs_ge_0_6"] == 367
    assert merged["exact_cross_channel_pairs_ge_0_6"] == 369


def test_sourcewatch_reconciliation_exact_breakdown():
    """Verify reconciliation of Source Watch runs (9/12 vs 10/12) and DBR TLS root cause."""
    manifest_path = REPO_ROOT / "reports/provenance/lineage_manifest_2026-11-09.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    sw = data["sourcewatch_reconciliation"]
    assert sw["watchlist_targets_total"] == 12
    assert sw["target_types"]["listing_targets"] == 4
    assert sw["target_types"]["article_targets"] == 8

    # Automated case run (9/12)
    auto = sw["runs"]["automated_case_run"]
    assert auto["ratio"] == "9/12"
    assert auto["reported_success"] == 9
    assert auto["reported_errors"] == 3
    assert auto["error_breakdown"]["dbr_tls_cert_failures"] == 2
    assert auto["error_breakdown"]["transient_network_timeouts"] == 1

    # Dedicated snapshot run (10/12)
    snap = sw["runs"]["dedicated_snapshot_run"]
    assert snap["ratio"] == "10/12"
    assert snap["reported_success"] == 10
    assert snap["reported_errors"] == 2
    assert snap["error_breakdown"]["dbr_tls_cert_failures"] == 2
    assert snap["error_breakdown"]["transient_network_timeouts"] == 0

    # Root cause analysis
    rca = sw["root_cause_analysis"]["dbr_tls_verification_failure"]
    assert rca["error_type"] == "SSLCertVerificationError"
    assert len(rca["affected_urls"]) == 2
    assert any("dbr.gov.ua/news" in u for u in rca["affected_urls"])
    assert "transport infrastructure failure" in rca["classification"].lower()


def test_lineage_matrix_entries_and_checksums():
    """Verify that every metric in lineage matrix links to an exact (corpus_version, run_id, timestamp) and valid hash."""
    manifest_path = REPO_ROOT / "reports/provenance/lineage_manifest_2026-11-09.json"
    with open(manifest_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    matrix = data["lineage_matrix"]
    assert len(matrix) >= 15

    for entry in matrix:
        assert entry["metric_id"], "Missing metric_id"
        assert entry["metric_name"], "Missing metric_name"
        assert entry["reported_value"] is not None, "Missing reported_value"
        assert entry["corpus_version"], "Missing corpus_version"
        assert entry["run_id"], "Missing run_id"
        assert entry["timestamp_utc"], "Missing timestamp_utc"
        assert entry["source_locator"], "Missing source_locator"
        sha = entry["sha256"]
        assert len(sha) == 64 and all(c in "0123456789abcdefABCDEF" for c in sha), f"Invalid sha256: {sha}"

    # Verify physical file checksums on disk
    for rel_path, expected_hash in data["verified_artifact_checksums"].items():
        if rel_path.startswith("external/"):
            continue
        p = REPO_ROOT / rel_path
        if p.exists():
            actual_hash = hashlib.sha256(p.read_bytes()).hexdigest()
            assert actual_hash == expected_hash, f"Hash mismatch for {rel_path}: expected {expected_hash}, got {actual_hash}"


def test_build_script_verify_cli():
    """Verify that build_lineage_matrix.py --verify executes cleanly with exit code 0."""
    script_path = REPO_ROOT / "scripts/provenance/build_lineage_matrix.py"
    res = subprocess.run(
        [sys.executable, str(script_path), "--verify"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    assert res.returncode == 0, f"Script verification failed: {res.stderr}\nOutput: {res.stdout}"
    assert "Verification PASSED" in res.stdout


def test_markdown_report_structure_and_completeness():
    """Verify that corpus_and_sourcewatch_lineage_matrix_2026-11-09.md is comprehensive and well-formed."""
    report_path = REPO_ROOT / "reports/provenance/corpus_and_sourcewatch_lineage_matrix_2026-11-09.md"
    assert report_path.exists(), f"Markdown report missing at {report_path}"

    content = report_path.read_text(encoding="utf-8")
    assert len(content) > 10000, f"Report too short: {len(content)} characters"

    required_headings = [
        "# Corpus & Source-Watch Lineage Matrix Report",
        "## 1. Executive Summary & Epistemological Stance",
        "## 2. Part 1: Telegram Corpus Reconciliation (1,408 vs 1,438 Posts)",
        "## 3. Part 2: Source Watch Run Reconciliation (10/12 vs 9/12)",
        "## 4. Part 3: The Strict Provenance Rule",
        "## 5. Part 4: Complete Lineage Matrix (Master Table)",
        "## 6. Part 5: Reproducibility & Audit Protocol",
    ]
    for heading in required_headings:
        assert heading in content, f"Missing heading: {heading}"

    assert "kiber_boroshno" in content
    assert "SSLCertVerificationError" in content
    assert "dbr.gov.ua" in content
    assert "475" in content
    assert "1,408" in content
    assert "1,438" in content
    assert "159" in content
    assert "158" in content
    assert "115,931,014" in content
    assert "119,515,745" in content
    assert "9/12" in content
    assert "10/12" in content
