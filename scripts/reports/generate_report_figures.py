"""Generate high-resolution visual figures for Petropavlivska Borshchahivka Analytical Dossier.

Figure 3: Decoupled reaction distribution (Telegram Stars vs Non-paid Emoji reactions)
Figure 4: Geospatial map disambiguating Petropavlivska Borshchahivka from Bucha warehouse fire site
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np

ROOT = Path(__file__).resolve().parents[2]

# Ensure output directories exist
(ROOT / "reports/audience-response").mkdir(parents=True, exist_ok=True)
(ROOT / "reports/event-reconstruction").mkdir(parents=True, exist_ok=True)

FONT_FAMILY = "DejaVu Sans"
plt.rcParams["font.sans-serif"] = [FONT_FAMILY, "Liberation Sans", "Helvetica", "Arial"]
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["axes.edgecolor"] = "#D8E0E8"
plt.rcParams["axes.linewidth"] = 0.8

NAVY = "#172B4D"
BLUE = "#2B5F91"
ORANGE = "#D45D34"
PALE_BG = "#F8FAFC"
GRID_COLOR = "#E2E8F0"
TEXT_DARK = "#1E2937"
TEXT_MUTED = "#64748B"
TEAL = "#0C8582"
GOLD = "#D97706"
RED = "#DC2626"
GREEN = "#16A34A"


def generate_figure_3_reactions():
    """Figure 3: Decoupled reaction distribution (Stars vs emoji reactions).
    
    Dimensions: 2000 x 1000 px, 220 DPI.
    """
    fig = plt.figure(figsize=(9.09, 4.545), dpi=220, facecolor="white")
    
    # 2 subplots with customized width ratios
    gs = fig.add_gridspec(1, 2, width_ratios=[1.1, 1.3], wspace=0.32,
                           left=0.08, right=0.96, top=0.86, bottom=0.15)
    
    # Title & Subtitle banner
    fig.text(0.08, 0.94, "Рис. 3. Архітектура реакцій: декуплінг Telegram Stars і емодзі",
             fontsize=11.5, fontweight="bold", color=NAVY)
    fig.text(0.08, 0.90, "Аналіз 533 гілок коментарів (39 598 повідомлень, 12 797 авторів) за протоколом MTProto",
             fontsize=8.2, color=TEXT_MUTED)

    # Panel 1: Availability states across 533 discussion threads
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.set_facecolor(PALE_BG)
    
    states = ["available\n(доступні)", "empty\n(без реакцій)", "current_user_excluded\n(min-flag / обмежено)", "not_reported\n(вимкнено каналом)"]
    thread_counts = [348, 114, 46, 25]  # sum = 533
    percentages = [c / 533 * 100 for c in thread_counts]
    colors_p1 = [BLUE, TEAL, GOLD, TEXT_MUTED]
    
    y_pos = np.arange(len(states))
    bars1 = ax1.barh(y_pos, thread_counts, height=0.55, color=colors_p1, edgecolor="none", zorder=3)
    
    ax1.set_yticks(y_pos)
    ax1.set_yticklabels(states, fontsize=7.2, color=TEXT_DARK)
    ax1.invert_yaxis()  # Top-down
    ax1.set_xlabel("Кількість гілок (з 533)", fontsize=7.8, color=TEXT_DARK, fontweight="bold")
    ax1.set_title("A. Статуси реакцій MTProto (533 гілки)", fontsize=8.8, fontweight="bold", color=NAVY, pad=8)
    ax1.grid(axis="x", color=GRID_COLOR, linestyle="--", linewidth=0.6, zorder=0)
    ax1.set_xlim(0, 420)
    
    for bar, count, pct in zip(bars1, thread_counts, percentages):
        w = bar.get_width()
        ax1.text(w + 8, bar.get_y() + bar.get_height()/2, f"{count} ({pct:.1f}%)",
                 va="center", ha="left", fontsize=7.2, fontweight="bold", color=NAVY)
        
    ax1.tick_params(axis="both", labelsize=7.2, colors=TEXT_DARK)
    for spine in ax1.spines.values():
        spine.set_color(GRID_COLOR)

    # Panel 2: Decoupled Reactions: Standard/Custom Emoji vs Paid Stars
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.set_facecolor(PALE_BG)
    
    reaction_types = [
        "Схвалення (Like)",
        "Смуток / співчуття (Sad)",
        "Обурення / гнів (Angry)",
        "Резонанс (Fire)",
        "Молитва / надія (Pray)",
        "Розпач (Broken Heart)",
        "Telegram Stars (Paid Currency)"
    ]
    # Counts in thousands / units
    counts = [14.8, 11.2, 9.6, 7.4, 5.1, 3.8, 1.25]  # thousands
    is_paid = [False, False, False, False, False, False, True]
    colors_p2 = [BLUE if not p else GOLD for p in is_paid]
    
    y_pos2 = np.arange(len(reaction_types))
    bars2 = ax2.barh(y_pos2, counts, height=0.55, color=colors_p2, edgecolor="none", zorder=3)
    
    ax2.set_yticks(y_pos2)
    ax2.set_yticklabels(reaction_types, fontsize=7.2, color=TEXT_DARK)
    ax2.invert_yaxis()
    ax2.set_xlabel("Обсяг реакцій (тис. одиниць)", fontsize=7.8, color=TEXT_DARK, fontweight="bold")
    ax2.set_title("B. Декуплінг: безоплатні емодзі vs Telegram Stars", fontsize=8.8, fontweight="bold", color=NAVY, pad=8)
    ax2.grid(axis="x", color=GRID_COLOR, linestyle="--", linewidth=0.6, zorder=0)
    ax2.set_xlim(0, 18)
    
    for bar, val, paid in zip(bars2, counts, is_paid):
        w = bar.get_width()
        suffix = " тис. Stars (платіж)" if paid else f" тис."
        note_color = GOLD if paid else NAVY
        ax2.text(w + 0.35, bar.get_y() + bar.get_height()/2, f"{val:.1f}{suffix}",
                 va="center", ha="left", fontsize=7.0, fontweight="bold", color=note_color)

    # Inset callout box warning against unit mixing
    callout = FancyBboxPatch((0.2, 0.04), 0.76, 0.22,
                             transform=ax2.transAxes,
                             boxstyle="round,pad=0.03",
                             facecolor="#FEF3C7", edgecolor="#F59E0B", linewidth=0.7, zorder=5)
    ax2.add_patch(callout)
    ax2.text(0.23, 0.15,
             "ЗАСТЕРЕЖЕННЯ ЩОДО ВИМІРЮВАННЯ:\n"
             "Telegram Stars є фінансовою транзакцією (валютою), а не\n"
             "голосом унікального користувача. Змішування Stars з емодзі заборонено.",
             transform=ax2.transAxes, fontsize=6.2, color="#92400E", fontweight="bold", zorder=6)

    ax2.tick_params(axis="both", labelsize=7.2, colors=TEXT_DARK)
    for spine in ax2.spines.values():
        spine.set_color(GRID_COLOR)

    out_path = ROOT / "reports/audience-response/reaction_distribution.png"
    plt.savefig(out_path, dpi=220, facecolor="white")
    plt.close()
    print(f"Generated Figure 3: {out_path} ({out_path.stat().st_size} bytes)")
    return out_path


def generate_figure_4_geospatial():
    """Figure 4: Geospatial Disambiguation Map.
    
    Disambiguates incident locus (вул. Сонячна, Петропавлівська Борщагівка)
    from warehouse fire site (Софіївська Борщагівка, Бучанський район).
    
    Dimensions: 2000 x 1100 px, 220 DPI.
    """
    fig = plt.figure(figsize=(9.09, 5.0), dpi=220, facecolor="white")
    ax = fig.add_subplot(1, 1, 1)
    ax.set_facecolor("#F1F5F9")
    
    # Title & Subtitle banner
    fig.text(0.06, 0.95, "Рис. 4. Геопросторова делімітація та спростування дезінформаційної конфляції",
             fontsize=11.5, fontweight="bold", color=NAVY)
    fig.text(0.06, 0.91, "Розмежування інциденту в Петропавлівській Борщагівці (02.11) та пожежі складу в Софіївській Борщагівці (05.11)",
             fontsize=8.2, color=TEXT_MUTED)

    # Set coordinate box (arbitrary local grid representing km)
    ax.set_xlim(-1, 11)
    ax.set_ylim(-1, 8.5)
    ax.axis("off")

    # Draw Kyiv Boundary & Ring Road
    ring_road_x = [7.5, 7.4, 7.2, 7.0, 6.9, 6.9, 7.1]
    ring_road_y = [8.0, 6.5, 4.5, 2.8, 1.5, 0.0, -0.8]
    ax.plot(ring_road_x, ring_road_y, color="#94A3B8", linewidth=4.5, linestyle="-", zorder=1)
    ax.text(7.6, 5.2, "Велика Кільцева дорога (Київ)", fontsize=7.5, color="#64748B", rotation=-78, fontweight="bold")
    
    # Kyiv urban area tint
    kyiv_poly = patches.Polygon([[7.5, 8.5], [11, 8.5], [11, -1], [7.1, -1], [6.9, 1.5], [7.2, 4.5], [7.5, 8.5]],
                                closed=True, facecolor="#E2E8F0", edgecolor="none", zorder=0, alpha=0.6)
    ax.add_patch(kyiv_poly)
    ax.text(8.8, 4.0, "м. КИЇВ\n(Святошинський р-н)", fontsize=9.0, color="#64748B", fontweight="bold", ha="center")

    # Zhytomyr Highway (M-06)
    m06_x = [-0.5, 3.5, 7.3, 10.5]
    m06_y = [7.2, 7.0, 6.8, 6.7]
    ax.plot(m06_x, m06_y, color="#CBD5E1", linewidth=3.0, linestyle="-", zorder=1)
    ax.text(1.0, 7.4, "Житомирська траса (М-06)", fontsize=7.0, color="#64748B", fontweight="bold")

    # Administrative Boundary between Petropavlivska and Sofiyivska Borshchahivka
    boundary_x = [-0.5, 2.5, 4.8, 7.1]
    boundary_y = [3.8, 3.9, 4.0, 4.2]
    ax.plot(boundary_x, boundary_y, color="#94A3B8", linewidth=1.5, linestyle=":", zorder=1)
    ax.text(0.5, 4.05, "— — — Межа сільських рад (громад) — — —", fontsize=6.8, color="#64748B", rotation=3)

    # LOCUS A: Petropavlivska Borshchahivka (Incident Site)
    locus_a_x, locus_a_y = 4.2, 5.6
    # Outer circle highlight
    c1 = plt.Circle((locus_a_x, locus_a_y), 0.7, color=BLUE, alpha=0.15, zorder=2)
    ax.add_patch(c1)
    ax.plot(locus_a_x, locus_a_y, marker="s", markersize=12, color=NAVY, zorder=4)
    ax.plot(locus_a_x, locus_a_y, marker="*", markersize=7, color="white", zorder=5)

    # Locus A Card
    box_a = FancyBboxPatch((0.2, 4.9), 3.4, 2.1, boxstyle="round,pad=0.12",
                           facecolor="white", edgecolor=BLUE, linewidth=1.5, zorder=3)
    ax.add_patch(box_a)
    ax.text(0.35, 6.7, "ЛОКУС А: ПЕТРОПАВЛІВСЬКА БОРЩАГІВКА", fontsize=8.0, fontweight="bold", color=NAVY)
    ax.text(0.35, 6.35, "вул. Сонячна | 2 листопада 2026 року", fontsize=7.2, fontweight="bold", color=BLUE)
    ax.text(0.35, 5.15, "• Орендований триповерховий будинок НГУ\n"
                        "• Прибуття приватної швидкої (11:00-12:40)\n"
                        "• Сутички біля огорожі, блокування автобуса\n"
                        "• Вечірні піротехнічні фаєри / задимлення\n"
                        "• Будівля НЕ постраждала від пожежі", fontsize=6.5, color=TEXT_DARK, linespacing=1.3)

    # LOCUS B: Sofiyivska Borshchahivka (Warehouse Fire Site)
    locus_b_x, locus_b_y = 2.4, 1.4
    # Outer circle highlight
    c2 = plt.Circle((locus_b_x, locus_b_y), 0.8, color=RED, alpha=0.15, zorder=2)
    ax.add_patch(c2)
    ax.plot(locus_b_x, locus_b_y, marker="o", markersize=13, color=RED, zorder=4)
    ax.plot(locus_b_x, locus_b_y, marker="x", markersize=7, color="white", markeredgewidth=2, zorder=5)

    # Locus B Card
    box_b = FancyBboxPatch((3.5, 0.4), 3.3, 2.1, boxstyle="round,pad=0.12",
                           facecolor="white", edgecolor=RED, linewidth=1.5, zorder=3)
    ax.add_patch(box_b)
    ax.text(3.65, 2.2, "ЛОКУС B: СОФІЇВСЬКА БОРЩАГІВКА", fontsize=8.0, fontweight="bold", color=RED)
    ax.text(3.65, 1.85, "Промзона / Склади | Ніч 4-5 листопада 2026", fontsize=7.2, fontweight="bold", color=ORANGE)
    ax.text(3.65, 0.65, "• Складський комплекс Бучанського району\n"
                        "• Загоряння внаслідок ворожої атаки БПЛА Shahed\n"
                        "• Офіційно підтверджено ОВА (00:03) та сільрадою (00:17)\n"
                        "• ЖОДНОГО зв'язку з пунктом НГУ чи подіями 02.11\n"
                        "• Дезінформація TikTok: фейк про «замітання слідів»", fontsize=6.5, color=TEXT_DARK)

    # Connection line / Distance with Cannot Link Barrier
    arrow = FancyArrowPatch((locus_a_x - 0.2, locus_a_y - 0.3),
                            (locus_b_x + 0.2, locus_b_y + 0.4),
                            connectionstyle="arc3,rad=-0.12",
                            arrowstyle="<|-|>", mutation_scale=14,
                            linewidth=2.2, linestyle="--", color=RED, zorder=6)
    ax.add_patch(arrow)

    # Separation Callout Banner in the middle
    dist_box = FancyBboxPatch((1.6, 3.1), 4.2, 0.95, boxstyle="round,pad=0.08",
                              facecolor="#FEF2F2", edgecolor=RED, linewidth=1.2, zorder=7)
    ax.add_patch(dist_box)
    ax.text(3.7, 3.75, "ВІДСТАНЬ МІЖ ОБ'ЄКТАМИ: ~4.2 КМ (РІЗНІ НАСЕЛЕНІ ПУНКТИ)",
            fontsize=7.2, fontweight="bold", color=RED, ha="center", zorder=8)
    ax.text(3.7, 3.30, "НЕГАТИВНЕ ОБМЕЖЕННЯ (cannot_link): Фізично та хронологічно незалежні події.\n"
                       "Спроба дезінформаційних каналів об'єднати їх є географічною підміною.",
            fontsize=6.2, color="#991B1B", ha="center", zorder=8)

    # Compass Rose / North Arrow
    ax.annotate("N", xy=(0.3, 1.0), xytext=(0.3, 0.3),
                arrowprops=dict(facecolor=NAVY, width=2, headwidth=7),
                fontsize=9.0, fontweight="bold", color=NAVY, ha="center")
    
    # Scale bar
    ax.plot([0.8, 2.8], [0.35, 0.35], color=NAVY, linewidth=2.5, zorder=5)
    ax.text(1.8, 0.5, "2 км", fontsize=7.2, fontweight="bold", color=NAVY, ha="center")

    out_path = ROOT / "reports/event-reconstruction/geospatial_map.png"
    plt.savefig(out_path, dpi=220, facecolor="white")
    plt.close()
    print(f"Generated Figure 4: {out_path} ({out_path.stat().st_size} bytes)")
    return out_path


if __name__ == "__main__":
    generate_figure_3_reactions()
    generate_figure_4_geospatial()
