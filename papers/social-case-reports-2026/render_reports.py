#!/usr/bin/env python3
"""Typeset the Petropavlivska Borshchahivka case documents as an academic report series.

The content of the main report comes from scripts/reports/build_report.py, which is executed without
writing a PDF so its figures stay data-driven. The two dossiers come from their Markdown sources.
Figures are redrawn from the saved result tables. Raw data and earlier editions are not touched.
"""
from __future__ import annotations

import collections
import hashlib
import html
import json
import re
import runpy
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.ticker import PercentFormatter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE.parent / "social-framework-2026"))
from figure_fonts import register_cmu_serif  # noqa: E402

register_cmu_serif()
BUILD = HERE / "build"
FIG = HERE / "figures"
OUT = ROOT / "output/pdf"
EDITION = "2026-11-10"
BLUE, ORANGE, INK = "#25638B", "#C86B25", "#243442"
plt.rcParams.update({
    "font.family": "CMU Serif", "font.size": 9, "axes.labelsize": 9, "axes.titlesize": 9.5,
    "xtick.labelsize": 8.5, "ytick.labelsize": 8.5, "text.color": INK, "axes.labelcolor": INK,
    "axes.edgecolor": "#82909C", "xtick.color": INK, "ytick.color": INK, "axes.spines.top": False,
    "axes.spines.right": False, "axes.linewidth": .65, "pdf.fonttype": 42, "savefig.facecolor": "white",
    "axes.formatter.use_locale": False,
})


def capture_main_story():
    from reportlab.platypus import BaseDocTemplate, Paragraph

    original = Paragraph.__init__

    def init(self, text, style=None, *args, **kwargs):
        self._raw = text
        original(self, text, style, *args, **kwargs)

    Paragraph.__init__ = init
    captured = {}

    def build(self, flowables, *args, **kwargs):
        captured["story"] = list(flowables)
        raise SystemExit(0)

    BaseDocTemplate.build = build
    argv = sys.argv
    sys.argv = ["build_report.py", "--output", str(BUILD / "unused.pdf"), "--no-manifest"]
    try:
        runpy.run_path(str(ROOT / "scripts/reports/build_report.py"), run_name="__main__")
    except SystemExit:
        pass
    sys.argv = argv
    Paragraph.__init__ = original

    def walk(x):
        name = type(x).__name__
        if name == "Paragraph":
            return ("P", x.style.name, x._raw)
        if name in ("Table", "LongTable"):
            rows = [[walk(c) if not isinstance(c, (str, int, float, type(None))) else ("P", "S", str(c)) for c in r]
                    for r in x._cellvalues]
            return ("T", [float(w) if w else 0 for w in x._colWidths], rows)
        if name == "Image":
            return ("I", x.filename)
        if name == "HBars":
            return ("B", x.data, x.title, x.maxval, x.paired)
        if isinstance(x, list):
            return ("L", [walk(i) for i in x])
        return (name,)

    return [walk(x) for x in captured["story"]]


def esc(text: str) -> str:
    text = html.unescape(text)
    out = []
    for ch in text:
        out.append({"\\": r"\textbackslash{}", "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_\allowbreak{}",
                    "{": r"\{", "}": r"\}", "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
                    "/": r"/\allowbreak{}", "\u00a0": "~"}.get(ch, ch))
    return "".join(out)


URL = re.compile(r"https?://[^\s<>)\]]+")
HEX = re.compile(r"\b[0-9a-f]{20,}\b")


def plain(text: str) -> str:
    """Escape a run of text, turning bare URLs, hashes and backtick spans into breakable forms."""
    parts, pos = [], 0
    pattern = re.compile(r"`([^`]+)`|" + URL.pattern + "|" + HEX.pattern)
    for m in pattern.finditer(text):
        parts.append(esc(text[pos:m.start()]))
        token = m.group(0)
        if m.group(1):
            parts.append(r"\texttt{" + esc(m.group(1)) + "}")
        elif token.startswith("http"):
            parts.append(r"\url{" + token.replace("%", r"\%").replace("#", r"\#") + "}")
        else:
            parts.append(r"\texttt{" + r"\allowbreak{}".join(token[i:i + 8] for i in range(0, len(token), 8)) + "}")
        pos = m.end()
    parts.append(esc(text[pos:]))
    return "".join(parts)


def rl_inline(s: str) -> str:
    """Convert ReportLab mini-markup to LaTeX."""
    out, stack = [], []
    for token in re.split(r"(<[^>]+>)", s):
        if not token.startswith("<") or not re.match(r"</?(b|i|font|link|a|br|code|para|super)\b", token):
            out.append(plain(token))
            continue
        tag = re.match(r"</?([a-z]+)", token).group(1)
        closing = token.startswith("</")
        if tag == "br":
            out.append(r"\newline{}")
        elif tag == "a":
            m = re.search(r'name="([^"]+)"', token)
            if m:
                out.append(r"\hypertarget{" + m.group(1) + "}{}")
        elif closing:
            out.append(stack.pop())
        elif tag == "b":
            out.append(r"\textbf{"); stack.append("}")
        elif tag == "i":
            out.append(r"\textit{"); stack.append("}")
        elif tag == "code":
            out.append(r"\texttt{"); stack.append("}")
        elif tag == "link":
            href = re.search(r'href="([^"]+)"', token).group(1)
            if href.startswith("#"):
                out.append(r"\hyperlink{" + href[1:] + "}{"); stack.append("}")
            else:
                out.append(r"\href{" + href.replace("%", r"\%").replace("#", r"\#").replace("&amp;", r"\&").replace("&", r"\&") + "}{"); stack.append("}")
        else:
            out.append("{"); stack.append("}")
    return re.sub(r"\\hyperlink\{([^}]+)\}\{\\textbf\{([^}]*)\}\}", r"\\hyperlink{\1}{\2}", "".join(out))


def md_inline(s: str) -> str:
    out, pos = [], 0
    for m in re.finditer(r"\*\*(.+?)\*\*|\[([^\]]+)\]\(([^)\s]+)\)|(?<!\*)\*([^*]+)\*(?!\*)", s):
        out.append(plain(s[pos:m.start()]))
        if m.group(1) is not None:
            out.append(r"\textbf{" + md_inline(m.group(1)) + "}")
        elif m.group(2) is not None:
            if m.group(3).startswith("http"):
                out.append(r"\href{" + m.group(3).replace("%", r"\%").replace("#", r"\#").replace("&", r"\&") + "}{" + plain(m.group(2)) + "}")
            else:
                out.append(plain(m.group(2)))
        else:
            out.append(r"\textit{" + plain(m.group(4)) + "}")
        pos = m.end()
    out.append(plain(s[pos:]))
    return "".join(out)


def longtable(rows, ratios, caption, size=r"\footnotesize"):
    total = sum(ratios)
    avail = 1 - .0185 * (len(ratios) - 1)
    spec = "@{}" + "".join(r">{\raggedright\arraybackslash}p{%.3f\linewidth}" % (avail * r / total) for r in ratios) + "@{}"
    head = " & ".join(size + r" \textbf{" + c + "}" for c in rows[0]) + r"\\"
    lines = [r"\begin{longtable}{" + spec + "}"]
    if caption:
        lines.append(r"\caption{" + caption + r"}\\")
    lines += [r"\toprule", head, r"\midrule\endfirsthead", r"\toprule", head, r"\midrule\endhead", r"\bottomrule\endfoot"]
    for row in rows[1:]:
        lines.append(" & ".join(size + " " + c for c in row) + r"\\[1pt]")
    lines.append(r"\end{longtable}")
    return "\n".join(lines) + "\n"


def figure(path, caption, width=r"\linewidth"):
    return ("\\begin{figure}[H]\n\\centering\\includegraphics[width=" + width + "]{" + path + "}\n\\caption{" + caption +
            "}\n\\end{figure}\n")


def num(value):
    return f"{value:,.0f}".replace(",", "\u202f") if float(value).is_integer() else f"{value:.1f}".replace(".", ",")


def draw_bars(item, name):
    _, data, title, maxval, paired = item
    n = len(data)
    fig, ax = plt.subplots(figsize=(6.0, .34 * n + .55), layout="constrained")
    labels = [re.sub(r"<[^>]+>", "", str(d[0])) for d in data]
    y = list(range(n))[::-1]
    if paired:
        ax.barh([v + .19 for v in y], [d[1] for d in data], height=.36, color=BLUE, label="частка публікацій")
        ax.barh([v - .19 for v in y], [d[2] for d in data], height=.36, color=ORANGE, label="частка поточних переглядів")
        top = maxval or max(max(d[1:3]) for d in data)
        for v, d in zip(y, data):
            ax.text(d[1] + top * .01, v + .19, num(float(d[1])) + "%", va="center", fontsize=8)
            ax.text(d[2] + top * .01, v - .19, num(float(d[2])) + "%", va="center", fontsize=8)
        ax.legend(frameon=False, fontsize=8, loc="lower right")
        ax.set_xlim(0, top * 1.14)
    else:
        ax.barh(y, [d[1] for d in data], height=.62, color=BLUE)
        top = maxval or max(d[1] for d in data)
        for v, d in zip(y, data):
            text = str(d[2]) if len(d) > 2 else num(float(d[1]))
            ax.text(d[1] + top * .012, v, re.sub(r"(?<=\d) (?=\d)", "\u202f", text), va="center", fontsize=8.5)
        ax.set_xlim(0, top * 1.13)
    ax.set_yticks(y, labels)
    ax.tick_params(axis="y", length=0)
    ax.grid(axis="x", color="#DDE3E8", linewidth=.5)
    ax.set_axisbelow(True)
    fig.savefig(FIG / f"{name}.pdf")
    plt.close(fig)


def draw_timeseries():
    df = pd.read_csv(ROOT / "reports/continuation_20261105/timeseries_10min_posts.csv", index_col=0)
    df.index = pd.to_datetime(df.index, utc=True).tz_convert("Europe/Kyiv")
    names = {"B": "українські неофіційні", "C": "російські та проросійські", "A": "місцеві паблики",
             "D": "офіційні й редакційні", "E": "іноземні", "U": "не класифіковані"}
    colors = {"B": BLUE, "C": "#A63D2F", "A": ORANGE, "D": "#5B8C5A", "E": "#B8BEC4", "U": "#7A838B"}
    fig, ax = plt.subplots(figsize=(6.4, 2.75), layout="constrained")
    bottom = None
    for g in [c for c in "BCADEU" if c in df.columns]:
        ax.bar(df.index, df[g], width=1 / 144 * .9, bottom=bottom, color=colors[g], label=names[g], linewidth=0)
        bottom = df[g] if bottom is None else bottom + df[g]
    tz = df.index.tz
    ax.set_xlim(datetime(2026, 11, 2, 11).astimezone(tz), df.index.max() + pd.Timedelta(minutes=30))
    ax.set_ylim(0, 36)
    ax.xaxis.set_major_locator(mdates.HourLocator(byhour=[0, 12], tz=tz))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m\n%H:%M", tz=tz))
    ax.set_ylabel("Дописи за 10 хвилин")
    ax.legend(frameon=False, fontsize=7.8, ncol=3, loc="upper right")
    fig.savefig(FIG / "timeseries.pdf")
    plt.close(fig)


def draw_bridges():
    nodes = pd.read_csv(ROOT / "reports/telegram_network_dynamics_20261106/node_metrics.csv").head(10).iloc[::-1]
    fig, axes = plt.subplots(1, 2, figsize=(6.4, 3.1), gridspec_kw={"width_ratios": [1.4, 1]}, layout="constrained")
    axes[0].barh(nodes.channel, nodes.betweenness_directed_unweighted, color=BLUE)
    axes[0].set_xlabel("Нормована спрямована betweenness")
    axes[0].xaxis.set_major_formatter(PercentFormatter(1, decimals=1, symbol="%"))
    axes[0].xaxis.set_major_formatter(lambda v, _: f"{v * 100:.1f}%".replace(".", ","))
    y = list(range(len(nodes)))
    axes[1].barh([i - .19 for i in y], nodes.in_volume, height=.36, color=BLUE, label="вхідні")
    axes[1].barh([i + .19 for i in y], nodes.out_volume, height=.36, color=ORANGE, label="вихідні")
    axes[1].set_yticks(y, [""] * len(y))
    axes[1].set_xlabel("Видимі форварди, n")
    axes[1].legend(frameon=False, loc="lower right", fontsize=8)
    for ax in axes:
        ax.tick_params(axis="y", length=0)
    fig.savefig(FIG / "forward_bridges.pdf")
    plt.close(fig)


def draw_narratives():
    bins = pd.read_csv(ROOT / "reports/telegram_network_dynamics_20261106/narrative_shares_6h.csv")
    labels = ["N0_official", "N1_hostages", "N2_death_torture", "N3_tcc_camp", "N4_cover_up"]
    titles = ["N0: офіційне\nпояснення", "N1: заручники,\nпідвал", "N2: смерть,\nкатування", "N3: табір,\nв’язниця", "N4: приховування,\n«Хартія»"]
    base = bins[bins.label.eq(labels[0])].reset_index(drop=True)
    xs = list(range(len(base)))
    fig, axes = plt.subplots(6, 1, figsize=(6.4, 5.4), sharex=True, layout="constrained",
                             gridspec_kw={"height_ratios": [1.25, 1, 1, 1, 1, 1]})
    axes[0].bar(xs, base.messages, color="#6B7780", width=.8)
    for x, value in zip(xs, base.messages):
        axes[0].text(x, value + 8, str(value), ha="center", va="bottom", fontsize=7.8)
    axes[0].set_ylim(0, base.messages.max() * 1.22)
    axes[0].set_ylabel("Дописи, n", rotation=0, ha="right", va="center", fontsize=8.5)
    for ax, label, title in zip(axes[1:], labels, titles):
        sub = bins[bins.label.eq(label)]
        ax.bar(xs, sub.share, color=ORANGE if label in labels[1:3] else BLUE, width=.8)
        ax.set_ylim(0, 1.05)
        ax.set_yticks([0, .5, 1], ["0%", "50%", "100%"])
        ax.set_ylabel(title, rotation=0, ha="right", va="center", fontsize=8.5)
    for ax in axes:
        ax.axvspan(len(xs) - 1.5, len(xs) - .5, color="#EFE7DA", zorder=-2)
        ax.grid(axis="y", color="#DDE3E8", linewidth=.5)
        ax.set_axisbelow(True)
    ticks = list(range(0, len(xs), 2))
    if len(xs) - 1 not in ticks:
        ticks.append(len(xs) - 1)
    axes[-1].set_xticks(ticks, [pd.Timestamp(base.iloc[i].bin_start).strftime("%d.%m\n%H:%M") for i in ticks])
    axes[-1].set_xlabel("Час київський; виділено неповний останній інтервал", fontsize=8.5)
    fig.savefig(FIG / "narrative_shares_6h.pdf")
    plt.close(fig)


# Main report: captions, added because the source tables have none.
TABLE_CAPTIONS = {
    46: "Дослідницькі питання та межі висновків.", 51: "Реєстр ключових офіційних заяв.",
    64: "Елементи першого повідомлення та стан їх підтвердження.", 72: "Хронологія події та перевірок (час київський).",
    76: "Склад цифрового корпусу.", 101: "Розподіл релевантних дописів і лічильників за групами каналів.",
    114: "Лексичні наративні мітки та надійність.", 127: "Копії текстів і межі причинного тлумачення.",
    131: "Сигнали координації та автоматизації в коментарях Telegram.", 138: "Спостережені статистики й умовні нульові моделі.",
    159: "Позиції в коментарях до відео про пожежу.", 173: "Результати збору за 42 посиланнями TikTok.",
    184: "Часові поля публікацій TikTok.", 190: "Охоплення інших платформ.", 198: "Показники коментарів YouTube.",
    204: "Субтитри YouTube за датами публікації.", 206: "Приклади з таймкодами та їхній контекст.",
    212: "Стан щоденного моніторингу відкритих джерел.", 216: "Калібрування ASR за акустичними стратами.",
    220: "Алгоритм пошуку інформаційних інцидентів.", 232: "Осі оцінки російського впливу.", 240: "Матриця ключових тверджень.",
    243: "Ризики для висновків і способи їх врахування.", 267: "Повний перелік 42 посилань TikTok.",
    273: "Зведена телеметрія обробки 607 відео Telegram.", 329: "Контрольні суми локальних файлів.",
}
BAR_CAPTIONS = {
    95: "Релевантні дописи за годинами першої доби.", 102: "Частка публікацій і поточних переглядів за групами каналів.",
    115: "Кількість публікацій за наративними мітками.", 139: "Найбільший пул S7: спостережена кількість фраз і фон.",
    142: "Близькі копії в межах 10 хвилин: спостереження і фон.", 161: "Позиції в коментарях до відео про пожежу.",
    174: "Верхньорівневі коментарі TikTok: лічильник платформи й отримані ідентифікатори.",
    196: "YouTube: публікації лексичного відбору за датами.",
}
IMAGE = {
    "timeseries.png": ("timeseries", "Часовий профіль релевантної хвилі публікацій у Telegram, 2--5 листопада 2026 року."),
    "forward_bridges.png": ("forward_bridges", "Проміжні вузли спостереженого графа форвардів."),
    "narrative_shares_6h.png": ("narrative_shares_6h", "Шестигодинні інтервали: обсяг дописів і частки лексичних міток."),
}
REACTION_TABLE = r"""\begin{longtable}{@{}>{\raggedright\arraybackslash}p{0.22\linewidth}>{\raggedright\arraybackslash}p{0.72\linewidth}@{}}
\caption{Обмежена перевірка паритету реакцій Telegram; знімок не оцінює весь корпус.}\\
\toprule\footnotesize\textbf{Параметр} & \footnotesize\textbf{Значення}\\\midrule\endfirsthead
\toprule\footnotesize\textbf{Параметр} & \footnotesize\textbf{Значення}\\\midrule\endhead
\bottomrule\endfoot
\footnotesize Вибірка & \footnotesize 10 коментарів у 3 дискусійних гілках, обраних із уже зібраних публічних коментарів\\
\footnotesize Результат & \footnotesize Вектори реакцій збіглися в 10 із 10 випадків: серіалізатор збирача порівняно з агрегатним MTProto API\\
\footnotesize Межа висновку & \footnotesize Повний корпус не перевірено; паритет для всіх груп, типів стану чи всіх реакцій не встановлено\\
\end{longtable}
"""
GEO_TABLE = r"""\begin{longtable}{@{}>{\raggedright\arraybackslash}p{0.16\linewidth}>{\raggedright\arraybackslash}p{0.39\linewidth}>{\raggedright\arraybackslash}p{0.39\linewidth}@{}}
\caption{Дві окремо описані події. Це не карта й не геолокація відео; місце зйомки відео пожежі не встановлено.}\\
\toprule\footnotesize\textbf{Ознака} & \footnotesize\textbf{Події, описані у джерелах} & \footnotesize\textbf{Окреме повідомлення про пожежу}\\\midrule\endfirsthead
\toprule\footnotesize\textbf{Ознака} & \footnotesize\textbf{Події, описані у джерелах} & \footnotesize\textbf{Окреме повідомлення про пожежу}\\\midrule\endhead
\bottomrule\endfoot
\footnotesize Дата & \footnotesize 2 листопада 2026 року & \footnotesize Ніч 4--5 листопада 2026 року\\
\footnotesize Місце & \footnotesize Петропавлівська Борщагівка, вул. Сонячна & \footnotesize Софіївська Борщагівка, Бучанський район, складське приміщення\\
\footnotesize Зміст & \footnotesize Повідомлення про події біля орендованої будівлі & \footnotesize За повідомленнями, пожежа сталася після атаки БпЛА\\
\footnotesize Джерела & \footnotesize Поліція Київщини; Суспільне (судове висвітлення, 6 листопада) & \footnotesize Київська ОВА (4 листопада); Борщагівська сільрада (5 листопада)\\
\end{longtable}
"""


def edition_patches(story):
    v2 = ROOT / "reports/evidence-verification/core_claims_verification_2026-11-10_rule_v2.json"
    sha = hashlib.sha256(v2.read_bytes()).hexdigest()
    rel = str(v2.relative_to(ROOT))
    done = collections.Counter()

    def patch(text):
        pairs = [("19 підтримано в межах визначеного предмета доказування, 6 мають статус «недостатньо доказів»",
                  "18 підтримано в межах визначеного предмета доказування, 7 мають статус «недостатньо доказів»"),
                 ("reports/evidence-verification/core_claims_verification_2026-11-09.json", rel),
                 ("0dea87a77ea444d9ba40970826a89aea0a6f3470d9913043a934329047ef269c", sha)]
        for a, b in pairs:
            if a in text:
                done[a[:25]] += 1
                text = text.replace(a, b)
        return text

    def visit(x):
        if x[0] == "P":
            return ("P", x[1], patch(x[2]))
        if x[0] == "T":
            return ("T", x[1], [[visit(c) for c in r] for r in x[2]])
        return x

    out = [visit(x) for x in story]
    assert len(done) == 3, done
    return out


def render_main(story):
    story = edition_patches(story)
    body, bullets = [], []
    bar_no = 0

    def flush():
        if bullets:
            body.append("\\begin{itemize}\n" + "\n".join("\\item " + b for b in bullets) + "\n\\end{itemize}\n")
            bullets.clear()

    i = 33
    appendix = False
    while i < len(story):
        x = story[i]
        kind = x[0]
        next_x = story[i + 1] if i + 1 < len(story) else None
        if kind == "P":
            style, raw = x[1], x[2]
            text = re.sub(r"<[^>]+>", "", raw).strip()
            if style != "Bulletx":
                flush()
            if style == "H1x":
                m = re.match(r"(\d+)\.\s*(.+)", text)
                if text.startswith("Додаток"):
                    m2 = re.match(r"Додаток ([A-Z])\.\s*(.+)", text)
                    if not appendix:
                        body.append("\\input{../content/conclusion_main}\n")
                        appendix = True
                    body.append("\\repchapternew{}{Додаток " + m2.group(1) + ". " + plain(m2.group(2)) + "}\n")
                else:
                    body.append("\\repchapter{" + m.group(1) + "}{" + plain(m.group(2)) + "}\n")
            elif style == "H2x":
                m = re.match(r"([0-9A-Z]+\.\d+)\.\s*(.+)", text)
                body.append("\\repsection{" + m.group(1) + "}{" + plain(m.group(2)) + "}\n")
            elif style == "H3x":
                body.append("\\repsubsection{" + plain(text) + "}\n")
            elif style == "Bulletx":
                bullets.append(rl_inline(re.sub(r'^<font[^>]*><b>•</b></font>\s*', "", raw)))
            elif style == "Sourcex":
                body.append("\\sourceitem{" + rl_inline(raw) + "}\n")
            elif style == "Captionx":
                body.append("{\\small\\noindent\\textit{Примітка.} " + rl_inline(raw) + "\\par}\\medskip\n")
            else:
                body.append(rl_inline(raw) + "\n\n")
        elif kind == "T":
            flush()
            rows = [[rl_inline(c[2]) if c[0] == "P" else "" for c in r] for r in x[2]]
            size = r"\scriptsize" if len(rows[0]) >= 6 or i == 329 else r"\footnotesize"
            body.append(longtable(rows, x[1], TABLE_CAPTIONS[i], size))
        elif kind == "B":
            flush()
            bar_no += 1
            name = f"bars_{bar_no}"
            draw_bars(x, name)
            body.append(figure(name + ".pdf", BAR_CAPTIONS[i], r"0.94\linewidth"))
        elif kind == "I":
            flush()
            base = Path(x[1]).name
            if base == "reaction_distribution.png":
                body.append(REACTION_TABLE); i += 2; continue
            if base == "geospatial_map.png":
                body.append(GEO_TABLE); i += 2; continue
            name, caption = IMAGE[base]
            body.append(figure(name + ".pdf", caption))
            if next_x and next_x[0] == "P" and next_x[2].startswith("Рис."):
                i += 1
        i += 1
    flush()
    callout = rl_inline(story[7][2][1][0][2])
    summary = ("\\begin{keybox}{Ключовий доказовий підсумок}\n" + callout + "\n\\end{keybox}\n")
    title = (r"\reptitle{Серія аналітичних матеріалів Social \textperiodcentered{} Кейс 2026/1 \textperiodcentered{} Документ 1}{Аналітичний звіт}"
             r"{Інцидент у Петропавлівській Борщагівці та інформаційна хвиля довкола нього}"
             r"{Офіційні матеріали, цифровий слід, наративи, коментарі, координація та контекст відео}"
             r"{Редакція 3.2 \textperiodcentered{} 10 листопада 2026 року}"
             r"{Подія: & 2 листопада 2026 року\\ Цифровий зріз: & 2--5 листопада 2026 року\\ Часовий пояс: & київський\\ Статус: & доказовий аналітичний звіт}"
             r"{Документ не є процесуальним висновком чи вироком. Особи, яким повідомлено про підозру, вважаються невинуватими, доки їхню вину не встановить суд.}")
    return wrap("Інцидент у Петропавлівській Борщагівці: аналітичний звіт", "Петропавлівська Борщагівка: аналітичний звіт",
                title, "\\input{../content/summary_main}\n" + summary + "\\reptoc\n" + "".join(body))


def wrap(pdf_title, short, title, body):
    return (r"\documentclass[11pt,a4paper]{report}" "\n" r"\usepackage{social_report}" "\n" r"\graphicspath{{../figures/}}" "\n"
            r"\hypersetup{pdftitle={" + pdf_title + r"},pdfauthor={Олександр Пилипенко}}" "\n"
            r"\renewcommand{\DocShort}{" + short + "}\n" r"\begin{document}" "\n" + title + "\n" + body + "\n" r"\end{document}" "\n")


def render_markdown(source, title_tex, pdf_title, short):
    lines = source.read_text(encoding="utf-8").splitlines()
    head, i = [], 1
    while i < len(lines) and not lines[i].startswith("## "):
        if lines[i].strip() and lines[i].strip() != "---":
            head.append(md_inline(lines[i].strip()))
        i += 1
    body = ["\\begin{keybox}{Про документ}\n" + "\n\n".join(head) + "\n\\end{keybox}\n\\reptoc\n"]
    table_no, section_no = 0, ""
    while i < len(lines):
        line = lines[i].rstrip()
        s = line.strip()
        if not s or s == "---":
            i += 1
            continue
        if s.startswith("## "):
            title = s[3:]
            m = re.match(r"(\d+)\.\s*(.+)", title)
            section_no = m.group(2) if m else title
            body.append("\\repchapter{" + (m.group(1) if m else "") + "}{" + md_inline(m.group(2) if m else title) + "}\n")
        elif s.startswith("### "):
            body.append("\\repsection{}{" + md_inline(s[4:]) + "}\n")
        elif s.startswith("|"):
            block = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                block.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            rows = [block[0]] + block[2:]
            widths = [max(min(max(len(r[c]) for r in rows), 900) ** .5, 8.5) for c in range(len(rows[0]))]
            table_no += 1
            body.append(longtable([[md_inline(c) for c in r] for r in rows], widths, plain(section_no[:1].upper() + section_no[1:]) + "."))
            continue
        elif re.match(r"(\d+\.|-) ", s):
            items = []
            numbered = bool(re.match(r"\d+\.", s))
            while i < len(lines):
                t = lines[i].strip()
                if re.match(r"(\d+\.|-) ", t):
                    items.append(md_inline(re.sub(r"^(\d+\.|-) ", "", t)))
                elif t or not (i + 1 < len(lines) and re.match(r"(\d+\.|-) ", lines[i + 1].strip())):
                    break
                i += 1
            if numbered and section_no == "Джерела":
                start = int(re.match(r"\d+", s).group())
                body.append("".join("\\sourceitem{[%d]\\enspace %s}\n" % (start + n, t) for n, t in enumerate(items)))
            else:
                env = "enumerate" if numbered else "itemize"
                start = int(re.match(r"\d+", s).group()) if numbered else 1
                opt = "[start=%d]" % start if numbered and start != 1 else ""
                body.append("\\begin{" + env + "}" + opt + "\n" + "\n".join("\\item " + t for t in items) + "\n\\end{" + env + "}\n")
            continue
        else:
            para = [s]
            while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(r"(#|\||\d+\. |- |---)", lines[i + 1].strip()):
                i += 1
                para.append(lines[i].strip())
            body.append(md_inline(" ".join(para)) + "\n\n")
        i += 1
    return wrap(pdf_title, short, title_tex, "".join(body))


DOSSIER_TITLE = (r"\reptitle{Серія аналітичних матеріалів Social \textperiodcentered{} Кейс 2026/1 \textperiodcentered{} Документ 2}{Аналітична довідка}"
                 r"{Публічно названі фігуранти, процесуальний статус і відкриті питання}{Петропавлівська Борщагівка, 2 листопада 2026 року}"
                 r"{Редакція 10 листопада 2026 року}"
                 r"{Зріз джерел: & 6 листопада 2026 року, 15:40 за Києвом\\ Доповнення: & 8 листопада 2026 року\\ Статус: & огляд відкритих джерел}"
                 r"{Документ не є вироком, висновком слідства чи офіційним документом державного органу. Особи, яким повідомлено про підозру, вважаються невинуватими, доки їхню вину не встановить суд.}")
ATTR_TITLE = (r"\reptitle{Серія аналітичних матеріалів Social \textperiodcentered{} Кейс 2026/1 \textperiodcentered{} Документ 3}{Методичний протокол}"
              r"{Раннє попередження й оцінка можливого російського впливу}{Методика та її застосування до інформаційної хвилі довкола Петропавлівської Борщагівки}"
              r"{Редакція 10 листопада 2026 року}"
              r"{Об'єкт: & інформаційна хвиля 2--5 листопада 2026 року\\ Статус: & методичний протокол і застосування до кейсу}"
              r"{Протокол розмежовує аномалію поширення, координацію, зв'язок із російським інформаційним середовищем і державну відповідальність. Жоден із цих рівнів не випливає автоматично з іншого.}")


def compile_doc(name, tex, output):
    (BUILD / f"{name}.tex").write_text(tex, encoding="utf-8")
    run = subprocess.run(["tectonic", "-X", "compile", "--keep-logs", "-r", "2", "-o", ".", "-Z", "search-path=..", f"{name}.tex"],
                         cwd=BUILD, capture_output=True, text=True)
    if run.returncode:
        print(run.stdout[-1500:], run.stderr[-3000:])
        raise SystemExit(f"compile failed: {name}")
    log = (BUILD / f"{name}.log").read_text(errors="replace")
    pdf = BUILD / f"{name}.pdf"
    pages = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout).group(1))
    target = OUT / output
    target.write_bytes(pdf.read_bytes())
    print(name, "pages", pages, "overfull", log.count("Overfull \\hbox"), "missing", log.count("Missing character"),
          "undefined", log.count("undefined"))
    return {"name": name, "pdf": str(target.relative_to(ROOT)), "pages": pages,
            "pdf_sha256": hashlib.sha256(target.read_bytes()).hexdigest(), "tex_sha256": hashlib.sha256(tex.encode()).hexdigest()}


def main():
    BUILD.mkdir(exist_ok=True)
    FIG.mkdir(exist_ok=True)
    draw_timeseries(); draw_bridges(); draw_narratives()
    only = set(sys.argv[1:])
    records = []
    if not only or "main" in only:
        records.append(compile_doc("report_main", render_main(capture_main_story()), f"petropavlivska_borshchahivka_report_{EDITION}.pdf"))
    if not only or "dossier" in only:
        records.append(compile_doc("report_dossier", render_markdown(ROOT / "reports/figures-and-proceedings-2026-11-06.md", DOSSIER_TITLE,
                                   "Публічно названі фігуранти, процесуальний статус і відкриті питання", "Фігуранти й процесуальний статус"),
                                   f"petropavlivska_figures_and_proceedings_{EDITION}.pdf"))
    if not only or "attr" in only:
        records.append(compile_doc("report_attribution", render_markdown(ROOT / "wiki/methods/russian-influence-attribution-early-warning.md", ATTR_TITLE,
                                   "Раннє попередження й оцінка можливого російського впливу", "Раннє попередження й оцінка впливу"),
                                   f"russian_influence_attribution_early_warning_{EDITION}.pdf"))
    if not only:
        (OUT / f"manifest-{EDITION}.json").write_text(json.dumps({"edition": EDITION, "renderer": "papers/social-case-reports-2026/render_reports.py",
                                                                  "engine": "tectonic/XeTeX", "artifacts": records}, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
