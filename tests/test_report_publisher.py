"""Tests for Analytical Report Publisher (Milestone M5 / GATE-05).

Verifies:
- Restored A4 dossier PDF exists and meets strict page budget: 25 <= pages <= 30.
- Extracted text contains 0 replacement characters (U+FFFD).
- All 4 high-resolution figures exist and have valid dimensions.
- Manifest output/pdf/manifest-2026-11-09.json conforms to schema and matches file hashes.
- Narrative synthesizes M1-M4 findings with Appendices A, B, and C.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent


def test_main_report_pdf_exists_and_page_budget():
    """Verify that main PDF exists and page count is strictly within [25, 30]."""
    pdf_path = REPO_ROOT / "output/pdf/petropavlivska_borshchahivka_report_2026-11-09.pdf"
    assert pdf_path.exists(), f"Missing main PDF: {pdf_path}"
    assert pdf_path.stat().st_size > 500_000, "PDF file size unexpectedly small"

    res = subprocess.run(["pdfinfo", str(pdf_path)], capture_output=True, text=True, check=True)
    pages = None
    page_size = None
    for line in res.stdout.splitlines():
        if line.startswith("Pages:"):
            pages = int(line.split(":")[1].strip())
        elif line.startswith("Page size:"):
            page_size = line.split(":")[1].strip()

    assert pages is not None, "Failed to parse page count from pdfinfo"
    assert 25 <= pages <= 30, f"Page budget violation: got {pages} pages, required [25, 30]"
    assert page_size is not None and "A4" in page_size, f"Expected A4 page size, got {page_size}"


def test_pdf_text_quality_and_zero_replacement_characters():
    """Verify that extracted text contains 0 replacement characters and substantial text content."""
    pdf_path = REPO_ROOT / "output/pdf/petropavlivska_borshchahivka_report_2026-11-09.pdf"
    res = subprocess.run(["pdftotext", str(pdf_path), "-"], capture_output=True, text=True, check=True)
    text = res.stdout

    assert len(text) > 50_000, f"Extracted text length {len(text)} is too short"
    replacement_count = text.count("\ufffd")
    assert replacement_count == 0, f"Found {replacement_count} replacement characters (U+FFFD) in PDF text"


def test_four_figures_exist_and_dimensions():
    """Verify that all 4 raster figures exist and meet resolution requirements."""
    figures = [
        ("Figure 1: Temporal wave", REPO_ROOT / "reports/continuation_20261105/timeseries.png", 1900, 700),
        ("Figure 2: Forward bridges", REPO_ROOT / "reports/telegram_network_dynamics_20261106/forward_bridges.png", 2000, 1000),
        ("Figure 3: Reaction distribution", REPO_ROOT / "reports/audience-response/reaction_distribution.png", 1900, 900),
        ("Figure 4: Geospatial map", REPO_ROOT / "reports/event-reconstruction/geospatial_map.png", 1900, 1000),
    ]

    for name, path, min_w, min_h in figures:
        assert path.exists(), f"Figure missing: {name} at {path}"
        with Image.open(path) as img:
            w, h = img.size
            assert w >= min_w, f"{name} width {w} < {min_w}"
            assert h >= min_h, f"{name} height {h} < {min_h}"


def test_manifest_schema_and_artifacts():
    """Verify manifest-2026-11-09.json integrity, hashes, and companion PDFs."""
    manifest_path = REPO_ROOT / "output/pdf/manifest-2026-11-09.json"
    assert manifest_path.exists(), f"Manifest missing: {manifest_path}"

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["edition_date"] == "09.11.2026"
    assert manifest["renderer"] == "ReportLab"
    assert manifest["visual_review"]["status"] == "passed"

    artifacts = {art["name"]: art for art in manifest["artifacts"]}
    assert "main" in artifacts, "Main artifact missing from manifest"
    assert "figures_and_proceedings" in artifacts, "figures_and_proceedings missing"
    assert "russian_influence_attribution" in artifacts, "russian_influence_attribution missing"

    for name, art in artifacts.items():
        pdf_file = REPO_ROOT / art["pdf"]
        assert pdf_file.exists(), f"PDF file does not exist: {pdf_file}"
        computed_sha = hashlib.sha256(pdf_file.read_bytes()).hexdigest()
        assert computed_sha == art["pdf_sha256"], f"SHA-256 mismatch for {name}: {computed_sha} != {art['pdf_sha256']}"
        assert pdf_file.stat().st_size == art["pdf_bytes"], f"Byte size mismatch for {name}"
        assert art["replacement_characters"] == 0, f"Replacement characters > 0 for {name}"
        assert art["text_extraction"] == "passed"


def test_synthesis_of_m1_to_m4_in_narrative():
    """Verify that extracted text includes key terms from M1, M2, M3, M4 syntheses and appendices."""
    pdf_path = REPO_ROOT / "output/pdf/petropavlivska_borshchahivka_report_2026-11-09.pdf"
    res = subprocess.run(["pdftotext", str(pdf_path), "-"], capture_output=True, text=True, check=True)
    text = res.stdout

    # M1 synthesis
    assert "claim_01" in text or "40" in text
    assert "Ладиц" in text
    assert "Паршонков" in text
    assert "426-1" in text

    # M2 synthesis & cannot_link
    assert "cannot_link" in text or "Софіївська Борщагівка" in text
    assert "4,2 км" in text

    # M3 synthesis & ASR benchmark
    assert "Whisper-large-v3" in text
    assert "41.6%" in text
    assert "607" in text

    # M4 synthesis & corpus reconciliation
    assert "1 408" in text
    assert "1 438" in text
    assert "kiber_boroshno" in text

    # Appendices
    assert "Додаток A" in text
    assert "Додаток B" in text
    assert "Додаток C" in text
