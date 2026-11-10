#!/usr/bin/env python3
"""Render source-backed vector evaluation figure; no collection or model calls.

Run from any directory with the repository Python environment. Inputs are saved
finite-corpus audit metrics and their hash-verified original result artifacts.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


PAPER = Path(__file__).resolve().parent
ROOT = PAPER.parents[1]
BLUE = "#25638B"
ORANGE = "#C86B25"
INK = "#243442"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    metric_path = PAPER / "data/audited_evaluation_metrics.json"
    metrics = json.loads(metric_path.read_text())
    result_path = ROOT / metrics["null_model"]["source"]
    results = json.loads(result_path.read_text())
    assert sha256(result_path) == metrics["artifact_sha256"][str(result_path.relative_to(ROOT))]
    for path, expected in results["inputs_sha256"].items():
        assert sha256(ROOT / path) == expected, f"Source hash mismatch: {path}"

    recall = metrics["exact_jaccard"]["recall_by_threshold"]
    assert [r["exact_pairs_n"] for r in recall] == [369, 288, 213]
    assert [r["returned_pairs_n"] for r in recall] == [367, 288, 213]
    models = ["channel_2h_slot_rotation", "channel_24h_slot_rotation"]
    timing = [
        next(row for row in results["tests"]
             if row["model"] == model
             and row["statistic"] == "pairs_jaccard_ge0.6_lag_le10min")
        for model in models
    ]
    assert all(t["observed"] == 134 and t["edge_denominator"] == 369 for t in timing)

    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 9,
        "axes.labelsize": 9, "axes.titlesize": 9,
        "xtick.labelsize": 8.5, "ytick.labelsize": 8.5,
        "text.color": INK, "axes.labelcolor": INK,
        "axes.edgecolor": "#82909C", "xtick.color": INK, "ytick.color": INK,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.linewidth": 0.65, "pdf.fonttype": 42, "ps.fonttype": 42,
        "svg.fonttype": "none", "svg.hashsalt": "social-information-analysis-v1",
        "savefig.facecolor": "white",
    })
    fig, axes = plt.subplots(1, 2, figsize=(6.3, 2.7), gridspec_kw={"width_ratios": [1, 1]})
    fig.subplots_adjust(left=.082, right=.985, bottom=.275, top=.79, wspace=.50)
    left, right = axes

    x = np.arange(len(recall))
    width = .31
    bars = [
        left.bar(x - width/2, [r["exact_pairs_n"] for r in recall], width,
                 color=BLUE, label="Exact"),
        left.bar(x + width/2, [r["returned_pairs_n"] for r in recall], width,
                 facecolor="white", edgecolor=ORANGE, linewidth=1.2,
                 hatch="///", label="Legacy LSH"),
    ]
    for series in bars:
        for bar in series:
            left.text(bar.get_x()+bar.get_width()/2, bar.get_height()+7,
                      str(int(bar.get_height())), ha="center", va="bottom", fontsize=8.5)
    left.set_ylim(0, 450)
    left.set_yticks([0, 100, 200, 300, 400])
    left.set_xticks(x, [f"≥ {r['jaccard_threshold']:.2f}\n{100*r['recall']:.2f}%" for r in recall])
    left.set_xlabel("Jaccard threshold / candidate recall", labelpad=5)
    left.set_ylabel("Cross-channel pairs")
    left.set_title("(a) Exact and legacy pairs", loc="left", pad=27)
    left.legend(loc="upper left", bbox_to_anchor=(-.03, 1.12), frameon=False,
                fontsize=8.2, ncol=2, handlelength=1.15, columnspacing=.9)
    left.grid(axis="y", color="#DDE3E8", linewidth=.5)
    left.set_axisbelow(True)

    right.plot([134], [2], marker="D", markersize=5.5, color=ORANGE, linestyle="none")
    right.text(139, 2, "134", ha="left", va="center", fontsize=9)
    for y, row in zip([1, 0], timing):
        mean, lo, hi = row["null_mean"], row["null_q025"], row["null_q975"]
        right.errorbar(mean, y, xerr=np.array([[mean-lo], [hi-mean]]),
                       fmt="s", color=BLUE, markersize=4.5,
                       elinewidth=1.4, capsize=3, capthick=1.1)
        right.text(hi+5, y, f"{mean:.3f} [{lo:.0f}–{hi:.0f}]",
                   ha="left", va="center", fontsize=8.5)
    right.set_yticks([2, 1, 0], ["Observed", "2h null", "24h null"])
    right.set_ylim(-.52, 2.55)
    right.set_xlim(0, 165)
    right.set_xticks([0, 50, 100, 150])
    right.set_xlabel("Pairs within 10 minutes", labelpad=5)
    right.set_title("(b) Timing at Jaccard ≥ 0.60", loc="left", pad=27)
    right.text(0, 1.075, "Means and central 95% of null draws", transform=right.transAxes,
               fontsize=8.2, ha="left", va="bottom")
    right.grid(axis="x", color="#DDE3E8", linewidth=.5)
    right.set_axisbelow(True)
    right.tick_params(axis="y", length=0)
    fig.text(.082, .035, "Historical eligible texts: n = 1,384.", fontsize=8.2, ha="left")
    fig.text(.582, .035, "Null ranges are not confidence intervals.", fontsize=8.2, ha="left")

    out = PAPER / "figures"
    out.mkdir(exist_ok=True)
    fig.savefig(out / "information_analysis.pdf", metadata={
        "Title": "Finite-corpus copy recall and conditional timing nulls",
        "Creator": "Social source-backed evaluation figure generator",
        "CreationDate": None, "ModDate": None,
    })
    fig.savefig(out / "information_analysis.svg", metadata={
        "Title": "Finite-corpus copy recall and conditional timing nulls", "Date": None,
        "Description": "Historical n=1384; null bars show central 95% draw ranges, not confidence intervals.",
    })
    plt.close(fig)

    provenance = {
        "schema_version": "social_information_analysis_figure_v1",
        "dimensions_inches": [6.3, 2.7],
        "source_metric_json": str(metric_path.relative_to(ROOT)),
        "source_metric_sha256": sha256(metric_path),
        "generator_sha256": sha256(Path(__file__)),
        "source_sha256": {str(result_path.relative_to(ROOT)): sha256(result_path),
                          **results["inputs_sha256"]},
        "corpus": "historical continuation_20261105; relevant full text, length >=80; cross-channel pairs only",
        "eligible_text_count": metrics["exact_jaccard"]["eligible_records"],
        "left": {"rows": recall, "recall_denominator": "exact eligible cross-channel pairs at each threshold"},
        "right": {"jaccard_threshold": .6, "lag_minutes": 10,
                  "edge_denominator": 369, "observed": 134, "null_rows": timing,
                  "interval_semantics": "central 95% of saved randomization draws; not confidence intervals"},
        "null_replicates": results["B"], "null_seed": results["seed"],
        "limits": "Finite observed corpus; no attribution, organic-control specificity, or population inference.",
        "outputs_sha256": {str((out/name).relative_to(ROOT)): sha256(out/name)
                           for name in ["information_analysis.pdf", "information_analysis.svg"]},
    }
    metadata_dir = PAPER / "data/figure_data"
    metadata_dir.mkdir(exist_ok=True)
    (metadata_dir / "information_analysis.json").write_text(json.dumps(provenance, indent=2)+"\n")
    print(json.dumps({"outputs": list(provenance["outputs_sha256"]), "source_hashes_verified": True}))


if __name__ == "__main__":
    main()
