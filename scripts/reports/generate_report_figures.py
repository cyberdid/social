"""Generate the bounded audience-reaction and reported-event figures."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch


ROOT = Path(__file__).resolve().parents[2]

FONT_FAMILY = "DejaVu Sans"
plt.rcParams["font.sans-serif"] = [FONT_FAMILY, "Liberation Sans", "Helvetica", "Arial"]
plt.rcParams["font.family"] = "sans-serif"

NAVY = "#172B4D"
BLUE = "#2B5F91"
ORANGE = "#B45309"
PALE_BLUE = "#F3F7FB"
PALE_ORANGE = "#FFF7ED"
PALE_GRAY = "#F8FAFC"
GRID = "#D8E0E8"
TEXT = "#1E2937"
MUTED = "#526174"


def _card(ax, xy, width, height, *, facecolor, edgecolor):
    card = FancyBboxPatch(
        xy,
        width,
        height,
        transform=ax.transAxes,
        boxstyle="round,pad=0.012,rounding_size=0.018",
        facecolor=facecolor,
        edgecolor=edgecolor,
        linewidth=1.2,
    )
    ax.add_patch(card)


def generate_figure_3_reactions():
    """Draw the documented sample parity result without implying corpus totals."""
    fig, ax = plt.subplots(figsize=(9.09, 4.25), dpi=220, facecolor="white")
    ax.set_axis_off()

    fig.text(
        0.065,
        0.925,
        "Рис. 3. Обмежена перевірка паритету реакцій Telegram",
        fontsize=13.0,
        fontweight="bold",
        color=NAVY,
    )
    fig.text(
        0.065,
        0.875,
        "Контрольний зразок: 10 коментарів у 3 пов’язаних дискусійних гілках; це не оцінка повного корпусу.",
        fontsize=9.1,
        color=MUTED,
    )

    # The receipt supports counts for the bounded sample only: it reports ten
    # selected comments across three threads and exact vector equality on 10/10.
    cards = [
        (0.065, 0.405, 0.255, 0.36, PALE_BLUE, BLUE),
        (0.372, 0.405, 0.255, 0.36, PALE_GRAY, NAVY),
        (0.679, 0.405, 0.255, 0.36, PALE_ORANGE, ORANGE),
    ]
    for x, y, width, height, face, edge in cards:
        _card(ax, (x, y), width, height, facecolor=face, edgecolor=edge)

    ax.text(0.085, 0.704, "ВИБІРКА", transform=ax.transAxes,
            fontsize=9.0, fontweight="bold", color=BLUE)
    ax.text(0.085, 0.607, "10 коментарів", transform=ax.transAxes,
            fontsize=13.2, fontweight="bold", color=NAVY)
    ax.text(0.085, 0.537, "у 3 дискусійних гілках", transform=ax.transAxes,
            fontsize=9.1, color=TEXT)
    ax.text(0.085, 0.455, "Вибрано з уже зібраних\nпублічних коментарів.", transform=ax.transAxes,
            fontsize=8.8, color=MUTED, linespacing=1.35)

    ax.text(0.392, 0.704, "РЕЗУЛЬТАТ ЗРАЗКА", transform=ax.transAxes,
            fontsize=9.0, fontweight="bold", color=NAVY)
    ax.text(0.392, 0.607, "10 із 10", transform=ax.transAxes,
            fontsize=15.0, fontweight="bold", color=NAVY)
    ax.text(0.392, 0.537, "векторів збіглися", transform=ax.transAxes,
            fontsize=9.1, color=TEXT)
    ax.text(0.392, 0.455, "Серіалізатор збирача ↔\nагрегатний MTProto API.", transform=ax.transAxes,
            fontsize=8.8, color=MUTED, linespacing=1.35)

    ax.text(0.699, 0.704, "МЕЖІ ВИСНОВКУ", transform=ax.transAxes,
            fontsize=9.0, fontweight="bold", color=ORANGE)
    ax.text(0.699, 0.613, "Лише зразок", transform=ax.transAxes,
            fontsize=11.0, fontweight="bold", color=TEXT)
    ax.text(0.699, 0.537, "Повний корпус не перевірено.", transform=ax.transAxes,
            fontsize=8.6, color=TEXT)
    ax.text(0.699, 0.455, "Загальні підсумки й статуси\nреакцій недоступні.", transform=ax.transAxes,
            fontsize=8.8, color=MUTED, linespacing=1.35)

    # The shaded notice prevents the sample-level result from being mistaken
    # for coverage of the wider Telegram corpus.
    _card(ax, (0.065, 0.155), 0.869, 0.16, facecolor="#F1F5F9", edgecolor=GRID)
    ax.text(0.085, 0.242, "НЕ Є ОЦІНКОЮ ПОПУЛЯЦІЇ", transform=ax.transAxes,
            fontsize=8.5, fontweight="bold", color=NAVY)
    ax.text(
        0.085,
        0.188,
        "Перевірка не встановлює паритет для всіх груп, типів стану чи всіх реакцій у корпусі.",
        transform=ax.transAxes,
        fontsize=8.5,
        color=TEXT,
    )

    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    output_paths = [
        ROOT / "reports/audience-response/reaction_distribution.png",
        ROOT / "reports/audience/reaction_distribution.png",
    ]
    for out_path in output_paths:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(out_path, dpi=220, facecolor="white", bbox_inches=None)
        print(f"Generated Figure 3: {out_path} ({out_path.stat().st_size} bytes)")
    plt.close(fig)
    return output_paths


def generate_figure_4_geospatial():
    """Compare two reported events without representing geographic scale."""
    fig, ax = plt.subplots(figsize=(9.09, 5.0), dpi=220, facecolor="white")
    ax.set_axis_off()

    fig.text(
        0.065,
        0.925,
        "Рис. 4. Дві окремо описані події — схематичне порівняння",
        fontsize=12.6,
        fontweight="bold",
        color=NAVY,
    )
    fig.text(
        0.065,
        0.878,
        "Картки зіставляють повідомлені дати, місця та джерела; їхнє розташування не має географічного значення.",
        fontsize=8.6,
        color=MUTED,
    )

    _card(ax, (0.065, 0.335), 0.415, 0.465, facecolor=PALE_BLUE, edgecolor=BLUE)
    _card(ax, (0.520, 0.335), 0.415, 0.465, facecolor=PALE_ORANGE, edgecolor=ORANGE)

    ax.text(0.088, 0.755, "ПОДІЇ, ОПИСАНІ У ДЖЕРЕЛАХ", transform=ax.transAxes,
            fontsize=8.4, fontweight="bold", color=BLUE)
    ax.text(0.088, 0.682, "2 листопада 2026 року", transform=ax.transAxes,
            fontsize=10.6, fontweight="bold", color=NAVY)
    ax.text(0.088, 0.615, "Петропавлівська Борщагівка", transform=ax.transAxes,
            fontsize=9.3, fontweight="bold", color=TEXT)
    ax.text(0.088, 0.565, "вул. Сонячна", transform=ax.transAxes,
            fontsize=9.0, color=TEXT)
    ax.text(0.088, 0.491, "Повідомлення про події біля орендованої будівлі.", transform=ax.transAxes,
            fontsize=8.5, color=TEXT)
    ax.text(0.088, 0.408, "Джерела: поліція Київщини; Суспільне\n(судове висвітлення, 6 листопада).",
            transform=ax.transAxes, fontsize=8.5, color=MUTED, linespacing=1.35)

    ax.text(0.543, 0.755, "ОКРЕМЕ ПОВІДОМЛЕННЯ ПРО ПОЖЕЖУ", transform=ax.transAxes,
            fontsize=8.4, fontweight="bold", color=ORANGE)
    ax.text(0.543, 0.682, "Ніч 4–5 листопада 2026 року", transform=ax.transAxes,
            fontsize=10.4, fontweight="bold", color=NAVY)
    ax.text(0.543, 0.615, "Софіївська Борщагівка", transform=ax.transAxes,
            fontsize=9.3, fontweight="bold", color=TEXT)
    ax.text(0.543, 0.565, "Бучанський район · складське приміщення", transform=ax.transAxes,
            fontsize=8.2, color=TEXT)
    ax.text(0.543, 0.491, "За повідомленнями, пожежа сталася після атаки БпЛА.", transform=ax.transAxes,
            fontsize=8.3, color=TEXT)
    ax.text(0.543, 0.408, "Джерела: Київська ОВА (4 листопада);\nБорщагівська сільрада (5 листопада).",
            transform=ax.transAxes, fontsize=8.5, color=MUTED, linespacing=1.35)

    _card(ax, (0.065, 0.190), 0.870, 0.095, facecolor=PALE_GRAY, edgecolor=GRID)
    ax.text(0.085, 0.236, "НЕМАЄ МАСШТАБУ · КООРДИНАТ · ВИМІРЯНОЇ ВІДСТАНІ",
            transform=ax.transAxes, fontsize=8.2, fontweight="bold", color=NAVY)

    ax.text(
        0.065,
        0.126,
        "Відео пожежі: місце зйомки не геолоковано й не встановлено.",
        fontsize=8.5,
        fontweight="bold",
        color=ORANGE,
    )
    ax.text(
        0.065,
        0.082,
        "Текстова позначка в публікації не є незалежною перевіркою і не прив’язує відео до жодного з цих місць.",
        fontsize=8.2,
        color=TEXT,
    )

    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)
    out_path = ROOT / "reports/event-reconstruction/geospatial_map.png"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=220, facecolor="white", bbox_inches=None)
    plt.close(fig)
    print(f"Generated Figure 4: {out_path} ({out_path.stat().st_size} bytes)")
    return out_path


if __name__ == "__main__":
    generate_figure_3_reactions()
    generate_figure_4_geospatial()
