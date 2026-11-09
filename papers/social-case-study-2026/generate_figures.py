#!/usr/bin/env python3
"""Generate the bilingual, source-backed figures used by the Social preprint."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
FIGURES = HERE / "figures"
NAVY = "#242424"
BLUE = "#3366A3"
ORANGE = "#E86E2D"
PALE_BLUE = "#E9EEF3"
PALE_ORANGE = "#F6EBE4"
GRID = "#D8D8D8"
TEXT = "#242424"
MUTED = "#555555"
GRAY = "#888888"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "axes.titlesize": 9.5,
        "axes.titleweight": "normal",
        "axes.labelsize": 8.5,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "text.color": TEXT,
        "axes.labelcolor": TEXT,
        "xtick.color": TEXT,
        "ytick.color": TEXT,
        "axes.edgecolor": GRID,
        "axes.linewidth": 0.8,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": GRID,
        "grid.linewidth": 0.55,
        "grid.alpha": 0.85,
        "axes.axisbelow": True,
        "figure.facecolor": "white",
        "savefig.facecolor": "white",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
    }
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def save(fig: plt.Figure, stem: str) -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    fig.savefig(FIGURES / f"{stem}.pdf", bbox_inches="tight", metadata={"Creator": "Social case-study figure pipeline"})
    plt.close(fig)


def timeline(lang: str) -> None:
    rows = read_csv(ROOT / "reports/continuation_20261105/timeseries_10min_posts.csv")
    group_cols = ["A", "B", "C", "D", "E", "U"]
    per_hour: dict[datetime, int] = defaultdict(int)
    raw_total = 0
    for row in rows:
        ts = datetime.fromisoformat(row["bin"]).replace(tzinfo=None)
        count = sum(int(row[c]) for c in group_cols)
        per_hour[ts.replace(minute=0, second=0, microsecond=0)] += count
        raw_total += count
    if raw_total != 1408:
        raise ValueError(f"baseline time series sums to {raw_total}, expected 1,408")

    start = min(per_hour)
    end = max(per_hour)
    hours: list[datetime] = []
    current = start
    while current <= end:
        hours.append(current)
        current += timedelta(hours=1)
    counts = [per_hour.get(ts, 0) for ts in hours]
    if sum(counts) != raw_total:
        raise ValueError("hourly aggregation changed the baseline denominator")

    en = lang == "en"
    fig, ax = plt.subplots(figsize=(7.0, 3.1), constrained_layout=True)
    ax.bar(hours, counts, width=0.035, color=BLUE, edgecolor="none", zorder=3)
    ax.fill_between(hours, counts, color=PALE_BLUE, alpha=0.85, zorder=2)
    police_time = datetime(2026, 11, 2, 17, 27)
    ax.axvline(police_time, color=ORANGE, linewidth=1.25, linestyle=(0, (4, 3)), zorder=4)
    peak_time = datetime(2026, 11, 2, 21)
    peak_idx = hours.index(peak_time)
    ax.scatter([peak_time], [counts[peak_idx]], color=ORANGE, s=25, zorder=5)
    ax.annotate(
        ("Peak: 114 posts" if en else "Пік: 114 дописів"),
        xy=(peak_time, counts[peak_idx]),
        xytext=(70, 25),
        textcoords="offset points",
        color=NAVY,
        fontsize=8,
        fontweight="bold",
        arrowprops={"arrowstyle": "-", "color": MUTED, "lw": 0.7},
        bbox={"boxstyle": "round,pad=0.2", "fc": "white", "ec": GRID, "lw": 0.5, "alpha": 0.95},
    )
    ax.text(
        police_time,
        max(counts) * 1.22,
        ("Police statement\n17:27" if en else "Заява поліції\n17:27"),
        color=ORANGE,
        fontsize=7.3,
        ha="left",
        va="top",
        bbox={"boxstyle": "round,pad=0.25", "fc": "white", "ec": PALE_ORANGE, "lw": 0.7},
    )
    ax.set_title(
        "Relevant Telegram posts by hour" if en else "Релевантні дописи Telegram за годинами",
        loc="left",
        color=NAVY,
        pad=10,
    )
    ax.set_ylabel("Posts per hour" if en else "Дописів за годину")
    ax.set_xlabel("Kyiv local time (UTC+02:00)" if en else "Київський час (UTC+02:00)")
    ax.set_ylim(bottom=0, top=max(counts) * 1.38)
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=12))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d Nov\n%H:%M" if en else "%d лис.\n%H:%M"))
    for day in (datetime(2026, 11, 3), datetime(2026, 11, 4), datetime(2026, 11, 5)):
        ax.axvline(day, color=GRAY, linewidth=0.7, linestyle=(0, (2, 3)), alpha=0.8, zorder=1)
    ax.set_xlim(hours[0] - timedelta(minutes=30), hours[-1] + timedelta(minutes=45))
    ax.tick_params(axis="x", pad=5)
    ax.grid(axis="x", visible=False)
    ax.grid(axis="y", visible=True)
    fig.autofmt_xdate(rotation=0, ha="center")
    save(fig, f"fig1_telegram_timeline_{lang}")


def narrative_counts(lang: str) -> None:
    rows = read_csv(ROOT / "reports/continuation_20261105/narratives_by_group.csv")
    expected = {
        "N1_hostages": 301,
        "N2_death_torture": 505,
        "N3_tcc_camp": 230,
        "N4_cover_up": 81,
        "N0_official": 307,
    }
    actual = {row["narrative"]: int(row["posts"]) for row in rows}
    if actual != expected:
        raise ValueError(f"narrative counts changed: {actual}")
    labels_en = {
        "N2_death_torture": "Death / torture (N2)",
        "N0_official": "Official account / denial (N0)",
        "N1_hostages": "Unlawful detention / hostages (N1)",
        "N3_tcc_camp": "‘Concentration camp TCC’ (N3)",
        "N4_cover_up": "Concealment of evidence (N4)",
    }
    labels_uk = {
        "N2_death_torture": "Смерть / катування (N2)",
        "N0_official": "Офіційна версія / спростування (N0)",
        "N1_hostages": "Незаконне утримання / заручники (N1)",
        "N3_tcc_camp": "«Концтабір ТЦК» (N3)",
        "N4_cover_up": "Приховування доказів (N4)",
    }
    en = lang == "en"
    labels = labels_en if en else labels_uk
    order = ["N2_death_torture", "N0_official", "N1_hostages", "N3_tcc_camp", "N4_cover_up"]
    values = [actual[k] for k in order]
    ylabels = [labels[k] for k in order]
    colors = [ORANGE if key == "N0_official" else BLUE for key in order]
    fig, ax = plt.subplots(figsize=(7.0, 2.9), constrained_layout=True)
    y = np.arange(len(order))
    bars = ax.barh(y, values, color=colors, height=0.62, edgecolor="none", zorder=3)
    ax.set_yticks(y, ylabels)
    ax.invert_yaxis()
    ax.set_xlim(0, 570)
    ax.set_xlabel("Posts with a rule match" if en else "Дописів із правиловим збігом")
    ax.set_title("Exploratory rule-matched narrative mentions" if en else "Дослідницькі правила пошуку згадок наративів", loc="left", color=NAVY, pad=10)
    for bar, value in zip(bars, values):
        ax.text(value + 8, bar.get_y() + bar.get_height() / 2, f"{value:,}" if en else f"{value:,}".replace(",", " "), va="center", ha="left", fontsize=8, color=NAVY, fontweight="bold")
    ax.grid(axis="x", visible=True)
    ax.grid(axis="y", visible=False)
    save(fig, f"fig2_narrative_mentions_{lang}")


def claim_status(lang: str) -> None:
    data = json.loads((ROOT / "reports/evidence-verification/core_claims_verification_2026-11-09.json").read_text(encoding="utf-8"))
    summary = data["summary"]
    values = [summary["supported_within_scope"], summary["insufficient_evidence"], summary["refuted_within_scope"]]
    if values != [19, 6, 0] or summary["total_claims"] != 25:
        raise ValueError(f"claim status counts changed: {values}")
    en = lang == "en"
    labels = (
        ["Supported within scope", "Insufficient evidence", "Refuted within scope"]
        if en
        else ["Підтверджено в межах твердження", "Недостатньо доказів", "Спростовано в межах твердження"]
    )
    colors = [BLUE, ORANGE, GRAY]
    fig, ax = plt.subplots(figsize=(7.0, 2.2), constrained_layout=True)
    left = 0
    for value, label, color in zip(values, labels, colors):
        if value:
            ax.barh([0], [value], left=left, color=color, height=0.55, edgecolor="white", linewidth=1.0, label=f"{label}: {value}")
            ax.text(left + value / 2, 0, str(value), color="white", fontsize=9, fontweight="bold", ha="center", va="center")
        left += value
    ax.set_xlim(0, 25)
    ax.set_ylim(-0.65, 0.65)
    ax.set_yticks([])
    ax.set_xticks([0, 5, 10, 15, 20, 25])
    ax.set_xlabel("Number of claims (n = 25)" if en else "Кількість тверджень (n = 25)")
    ax.set_title("Scope-qualified status of the curated claim set" if en else "Статус курованого набору тверджень із визначеним обсягом", loc="left", color=NAVY, pad=10)
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.35), ncol=3, frameon=False, fontsize=7.5)
    ax.grid(axis="x", visible=True)
    ax.grid(axis="y", visible=False)
    ax.text(24.9, 0.35, f"0 — {labels[2]}" if en else f"0 — {labels[2]}", ha="right", va="bottom", color=MUTED, fontsize=7.3)
    save(fig, f"fig3_claim_status_{lang}")


def coordination_null(lang: str) -> None:
    path = ROOT / "reports/coordination-null-models-2026-11-08-lsh-audit/temporal_null_draws.csv"
    rows = [r for r in read_csv(path) if r["model"] == "channel_2h_slot_rotation"]
    draws = np.array([int(r["j0.6_w10"]) for r in rows])
    results = json.loads((ROOT / "reports/coordination-null-models-2026-11-08-lsh-audit/results.json").read_text(encoding="utf-8"))
    result = next(
        r
        for r in results["tests"]
        if r["family"] == "copy_timing"
        and r["model"] == "channel_2h_slot_rotation"
        and r["statistic"] == "pairs_jaccard_ge0.6_lag_le10min"
    )
    if len(draws) != 9999 or result["observed"] != 134 or abs(float(draws.mean()) - 42.86808680868087) > 1e-9:
        raise ValueError("copy-timing null distribution no longer matches its recorded result")
    en = lang == "en"
    fig, ax = plt.subplots(figsize=(7.0, 3.0), constrained_layout=True)
    bins = np.arange(draws.min() - 0.5, draws.max() + 1.5, 1)
    ax.hist(draws, bins=bins, color=BLUE, alpha=0.88, edgecolor="white", linewidth=0.3, zorder=3)
    q025, q975 = np.quantile(draws, [0.025, 0.975], method="inverted_cdf")
    ax.axvspan(q025, q975, color=PALE_BLUE, alpha=0.9, zorder=1, label=(f"Central 95% null interval: {q025:.0f}–{q975:.0f}" if en else f"Центральний 95% інтервал нуля: {q025:.0f}–{q975:.0f}"))
    ax.axvline(float(draws.mean()), color=NAVY, linewidth=1.2, linestyle=(0, (4, 3)), label=(f"Null mean: {draws.mean():.2f}" if en else f"Середнє нуля: {draws.mean():.2f}"))
    ax.axvline(result["observed"], color=ORANGE, linewidth=2.0, label=("Observed: 134" if en else "Спостережено: 134"))
    ax.set_xlim(0, 145)
    ax.set_xlabel("High-similarity pairs posted within 10 minutes" if en else "Пар із високою схожістю, опублікованих у межах 10 хвилин")
    ax.set_ylabel("Null draws" if en else "Кількість симуляцій")
    ax.set_title("Observed timing count exceeds all 9,999 two-hour null draws" if en else "Спостережена кількість перевищує всі 9 999 симуляцій двогодинної нульової моделі", loc="left", color=NAVY, pad=10)
    ax.legend(frameon=False, fontsize=7.3, loc="upper right")
    ax.grid(axis="x", visible=False)
    ax.grid(axis="y", visible=True)
    fig.text(
        0.01,
        -0.035,
        ("No simulated draw reached the observed value; plus-one p = 0.0001; Holm-adjusted p = 0.0016." if en else "Жодна симуляція не досягла спостереженого значення; p із поправкою +1 = 0,0001; p після поправки Holm = 0,0016."),
        fontsize=7.3,
        color=MUTED,
    )
    save(fig, f"fig4_coordination_null_{lang}")


def asr_strata(lang: str) -> None:
    data = json.loads((ROOT / "reports/video-pipeline/asr_calibration_benchmark_2026-11-09.json").read_text(encoding="utf-8"))
    strata = data["strata_summary"]
    keys = ["stratum_a", "stratum_b", "stratum_c", "stratum_d"]
    en = lang == "en"
    labels_en = ["Broadcast / clean", "Semi-confined / interview", "Outdoor / noisy dialogue", "High-noise / confrontation"]
    labels_uk = ["Ефір / чисте мовлення", "Приміщення / інтерв’ю", "Вулиця / шумний діалог", "Сильний шум / сутичка"]
    labels = labels_en if en else labels_uk
    counts = [strata[k]["clip_count"] for k in keys]
    safe = [strata[k]["quote_safe_count"] for k in keys]
    macro = [strata[k]["macro_wer"] * 100 for k in keys]
    micro = [strata[k]["micro_wer"] * 100 for k in keys]
    if sum(counts) != 18 or sum(safe) != 10:
        raise ValueError("ASR benchmark stratum totals changed")
    fig, ax = plt.subplots(figsize=(7.0, 3.1), constrained_layout=True)
    y = np.arange(len(keys))
    height = 0.32
    bars1 = ax.barh(y - height / 2, macro, height, color=BLUE, edgecolor="none", label=("Macro WER" if en else "Макро WER"), zorder=3)
    bars2 = ax.barh(y + height / 2, micro, height, color=ORANGE, edgecolor="none", label=("Micro WER" if en else "Мікро WER"), zorder=3)
    ax.set_yticks(y, [f"{label} (n={n}; flagged {q}/{n})" if en else f"{label} (n={n}; прапорці {q}/{n})" for label, n, q in zip(labels, counts, safe)])
    ax.invert_yaxis()
    ax.set_xlim(0, 70)
    ax.set_xlabel("Word error rate (%)" if en else "Частка помилок слів (%)")
    ax.set_title("Speech-recognition discrepancy against supplied references (18 clips)" if en else "Похибка ASR відносно наданих еталонів (18 кліпів)", loc="left", color=NAVY, pad=10)
    for bars in (bars1, bars2):
        for bar in bars:
            ax.text(bar.get_width() + 1.2, bar.get_y() + bar.get_height() / 2, f"{bar.get_width():.1f}%".replace(".", ",") if not en else f"{bar.get_width():.1f}%", va="center", ha="left", fontsize=7.3, color=NAVY)
    ax.legend(loc="lower right", frameon=False, fontsize=7.5)
    ax.grid(axis="x", visible=True)
    ax.grid(axis="y", visible=False)
    save(fig, f"fig5_asr_error_{lang}")


def main() -> None:
    for lang in ("en", "uk"):
        timeline(lang)
        narrative_counts(lang)
        claim_status(lang)
        coordination_null(lang)
        asr_strata(lang)
    print("Generated 10 bilingual, source-backed vector figures.")


if __name__ == "__main__":
    main()
