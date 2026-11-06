from __future__ import annotations

import html
import re
import argparse
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    BaseDocTemplate,
    CondPageBreak,
    Frame,
    KeepTogether,
    LongTable,
    PageTemplate,
    PageBreak,
    Paragraph,
    Spacer,
    TableStyle,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE = ROOT / "reports/figures-and-proceedings-2026-11-06.md"
DEFAULT_OUTPUT = ROOT / "output/pdf/petropavlivska_figures_and_proceedings_2026-11-06.pdf"
parser = argparse.ArgumentParser()
parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
args = parser.parse_args()
SOURCE = args.source if args.source.is_absolute() else ROOT / args.source
OUTPUT = args.output if args.output.is_absolute() else ROOT / args.output
IS_ATTRIBUTION_REPORT = "russian-influence-attribution" in SOURCE.name

FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
ITALIC_FONT_DIR = Path("/usr/share/fonts/truetype/liberation")
pdfmetrics.registerFont(TTFont("DejaVu", str(FONT_DIR / "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", str(FONT_DIR / "DejaVuSans-Bold.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-Oblique", str(ITALIC_FONT_DIR / "LiberationSans-Italic.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-BoldOblique", str(ITALIC_FONT_DIR / "LiberationSans-BoldItalic.ttf")))
pdfmetrics.registerFontFamily(
    "DejaVu", normal="DejaVu", bold="DejaVu-Bold", italic="DejaVu-Oblique", boldItalic="DejaVu-BoldOblique"
)

NAVY = colors.HexColor("#14324A")
INK = colors.HexColor("#1F2F3D")
MUTED = colors.HexColor("#617386")
TEAL = colors.HexColor("#0C8582")
PALE = colors.HexColor("#EEF5F8")
PALE_GOLD = colors.HexColor("#FFF7E6")
GOLD = colors.HexColor("#E8AD3D")
RULE = colors.HexColor("#D6E0E8")
LINK = colors.HexColor("#176A9A")


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="ReportTitle", fontName="DejaVu-Bold", fontSize=21, leading=26,
    textColor=NAVY, spaceAfter=8, keepWithNext=True,
))
styles.add(ParagraphStyle(
    name="ReportKicker", fontName="DejaVu-Bold", fontSize=8.4, leading=11,
    textColor=TEAL, spaceAfter=7, uppercase=True, tracking=0.8,
))
styles.add(ParagraphStyle(
    name="ReportMeta", fontName="DejaVu", fontSize=8.2, leading=11.5,
    textColor=MUTED, spaceAfter=3,
))
styles.add(ParagraphStyle(
    name="ReportH2", fontName="DejaVu-Bold", fontSize=14.2, leading=18,
    textColor=NAVY, spaceBefore=11, spaceAfter=6, keepWithNext=True,
))
styles.add(ParagraphStyle(
    name="ReportH3", fontName="DejaVu-Bold", fontSize=10.5, leading=13.5,
    textColor=TEAL, spaceBefore=7, spaceAfter=3, keepWithNext=True,
))
styles.add(ParagraphStyle(
    name="ReportBody", fontName="DejaVu", fontSize=8.9, leading=13,
    textColor=INK, spaceAfter=6, alignment=TA_LEFT, splitLongWords=1,
))
styles.add(ParagraphStyle(
    name="ReportBodyTight", fontName="DejaVu", fontSize=8.2, leading=11.4,
    textColor=INK, spaceAfter=3, splitLongWords=1,
))
styles.add(ParagraphStyle(
    name="ReportList", fontName="DejaVu", fontSize=8.8, leading=12.3,
    textColor=INK, leftIndent=12, firstLineIndent=-8, spaceAfter=3,
))
styles.add(ParagraphStyle(
    name="ReportCallout", fontName="DejaVu", fontSize=9.0, leading=13.2,
    textColor=NAVY, borderColor=TEAL, borderWidth=0.8, borderPadding=9,
    backColor=PALE, spaceBefore=3, spaceAfter=9,
))
styles.add(ParagraphStyle(
    name="ReportTableHead", fontName="DejaVu-Bold", fontSize=7.8, leading=10,
    textColor=colors.white, spaceAfter=0,
))
styles.add(ParagraphStyle(
    name="ReportTable", fontName="DejaVu", fontSize=7.45, leading=10.1,
    textColor=INK, spaceAfter=0, splitLongWords=1,
))
styles.add(ParagraphStyle(
    name="ReportSource", fontName="DejaVu", fontSize=7.8, leading=10.8,
    textColor=INK, leftIndent=15, firstLineIndent=-15, spaceAfter=4, splitLongWords=1,
))
styles.add(ParagraphStyle(
    name="ReportSourceNote", fontName="DejaVu", fontSize=7.6, leading=10.2,
    textColor=INK, spaceAfter=3, splitLongWords=1,
))


def normalize(text: str) -> str:
    return (text.replace("—", "-").replace("–", "-").replace("−", "-")
            .replace("‑", "-").replace("‒", "-").replace("−", "-"))


def inline_markup(text: str) -> str:
    text = normalize(text)
    links: list[str] = []

    def stash_link(match: re.Match[str]) -> str:
        label = html.escape(match.group(1), quote=False)
        url = html.escape(match.group(2), quote=True)
        links.append(f'<link href="{url}" color="{LINK.hexval()}" underline="1">{label}</link>')
        return f"@@LINK{len(links) - 1}@@"

    text = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", stash_link, text)
    text = re.sub(r"\[([^\]]+)\]\((?!https?://)([^)]+)\)",
                  lambda m: f"{m.group(1)} (локальний файл: {m.group(2)})", text)
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<i>\1</i>", text)
    for i, link in enumerate(links):
        text = text.replace(f"@@LINK{i}@@", link)
    return text


def split_table_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


class ReportDoc(BaseDocTemplate):
    def __init__(self, filename: str, **kwargs):
        super().__init__(filename, **kwargs)
        frame = Frame(
            18 * mm, 17 * mm, A4[0] - 36 * mm, A4[1] - 34 * mm,
            leftPadding=0, rightPadding=0, topPadding=5 * mm, bottomPadding=3 * mm,
            id="normal",
        )
        self.addPageTemplates(PageTemplate(id="main", frames=[frame], onPage=self.draw_chrome))

    def draw_chrome(self, canvas, doc):
        canvas.saveState()
        width, height = A4
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.6)
        canvas.line(18 * mm, height - 13 * mm, width - 18 * mm, height - 13 * mm)
        canvas.setFont("DejaVu-Bold", 7)
        canvas.setFillColor(MUTED)
        canvas.drawString(18 * mm, height - 10.5 * mm, "ПЕТРОПАВЛІВСЬКА БОРЩАГІВКА")
        canvas.setFont("DejaVu", 7)
        header = "РАННЄ ПОПЕРЕДЖЕННЯ Й АТРИБУЦІЯ · 06.11.2026" if IS_ATTRIBUTION_REPORT else "ОГЛЯД ВІДКРИТИХ ДЖЕРЕЛ · 06.11.2026"
        canvas.drawRightString(width - 18 * mm, height - 10.5 * mm, header)
        canvas.line(18 * mm, 12 * mm, width - 18 * mm, 12 * mm)
        canvas.setFont("DejaVu", 7)
        canvas.setFillColor(MUTED)
        footer = "Методичний OSINT-протокол; не офіційна атрибуція" if IS_ATTRIBUTION_REPORT else "Самостійна аналітична довідка; не документ державного органу"
        canvas.drawString(18 * mm, 8 * mm, footer)
        canvas.drawRightString(width - 18 * mm, 8 * mm, f"{doc.page}")
        canvas.restoreState()


def table_flowable(rows: list[list[str]], widths: list[float]) -> LongTable:
    rendered = []
    for row_index, row in enumerate(rows):
        style = styles["ReportTableHead"] if row_index == 0 else styles["ReportTable"]
        rendered.append([Paragraph(inline_markup(cell), style) for cell in row])
    table = LongTable(rendered, colWidths=widths, repeatRows=1, hAlign="LEFT", splitByRow=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("GRID", (0, 0), (-1, -1), 0.35, RULE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, PALE]),
    ]))
    return table


def make_story() -> list:
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    story = []
    i = 0
    in_sources = False
    conclusion_first = True
    seen_title = False
    available_width = A4[0] - 36 * mm
    table_widths = [62 * mm, 69 * mm, available_width - 131 * mm]

    while i < len(lines):
        raw = lines[i].rstrip()
        line = raw.strip()
        if not line:
            i += 1
            continue
        if line == "---":
            story.append(Spacer(1, 3))
            i += 1
            continue

        if line.startswith("# "):
            if not seen_title:
                kicker = "РАННЄ ПОПЕРЕДЖЕННЯ Й АТРИБУЦІЯ ІНОЗЕМНОГО ВПЛИВУ" if IS_ATTRIBUTION_REPORT else "ОГЛЯД ФІГУРАНТІВ ТА ПРОЦЕСУАЛЬНОГО КОНТЕКСТУ"
                story.append(Paragraph(kicker, styles["ReportKicker"]))
                story.append(Paragraph(inline_markup(line[2:]), styles["ReportTitle"]))
                story.append(Spacer(1, 2))
                seen_title = True
            i += 1
            continue

        if line.startswith("**Аналітична довідка"):
            story.append(Paragraph("Аналітична довідка для подальшої перевірки", styles["ReportMeta"]))
            i += 1
            continue
        if line.startswith("**Зріз джерел:") or line.startswith("**Статус документа:"):
            story.append(Paragraph(inline_markup(line), styles["ReportMeta"]))
            i += 1
            continue

        if line.startswith("## "):
            heading = line[3:]
            if heading.startswith("Джерела"):
                if IS_ATTRIBUTION_REPORT:
                    story.append(CondPageBreak(45 * mm))
                else:
                    story.append(PageBreak())
                in_sources = True
            elif heading.startswith("7. Підсумкова оцінка"):
                story.append(PageBreak())
            story.append(Paragraph(inline_markup(heading), styles["ReportH2"]))
            conclusion_first = heading == "Короткий висновок"
            i += 1
            continue

        if line.startswith("### "):
            story.append(CondPageBreak(30 * mm))
            story.append(Paragraph(inline_markup(line[4:]), styles["ReportH3"]))
            i += 1
            continue

        if line.startswith("|"):
            raw_rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                raw_rows.append(split_table_row(lines[i]))
                i += 1
            rows = [raw_rows[0]]
            for row in raw_rows[1:]:
                if all(re.fullmatch(r":?-{2,}:?", cell.replace(" ", "")) for cell in row):
                    continue
                rows.append(row)
            story.append(CondPageBreak(42 * mm))
            widths = table_widths if len(rows[0]) == len(table_widths) else [available_width / len(rows[0])] * len(rows[0])
            story.append(table_flowable(rows, widths))
            story.append(Spacer(1, 7))
            continue

        if re.match(r"^[-*] ", line):
            content = re.sub(r"^[-*] ", "• ", line)
            story.append(Paragraph(inline_markup(content), styles["ReportList"]))
            i += 1
            continue

        if re.match(r"^\d+\. ", line):
            if in_sources:
                m = re.match(r"^(\d+)\.\s+(\[(?:ПЕРШОДЖЕРЕЛО|МЕДІА)\])\s+(.*)$", line)
                if m:
                    content = f'**{m.group(1)}. {m.group(2)}** {m.group(3)}'
                else:
                    content = line
                story.append(Paragraph(inline_markup(content), styles["ReportSource"]))
            else:
                story.append(Paragraph(inline_markup(line), styles["ReportList"]))
            i += 1
            continue

        if line.startswith("**Встановлено") or line.startswith("**Не встановлено"):
            story.append(Paragraph(inline_markup(line), styles["ReportCallout"]))
            i += 1
            continue

        if conclusion_first:
            story.append(Paragraph(inline_markup(line), styles["ReportCallout"]))
            conclusion_first = False
        elif line.startswith("**Класи джерел:"):
            story.append(Paragraph(inline_markup(line), styles["ReportSourceNote"]))
        elif in_sources:
            story.append(Paragraph(inline_markup(line), styles["ReportSourceNote"]))
        else:
            story.append(Paragraph(inline_markup(line), styles["ReportBody"]))
        i += 1

    return story


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = ReportDoc(
        str(OUTPUT), pagesize=A4,
        leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=19 * mm, bottomMargin=17 * mm,
        title=("Раннє попередження й атрибуція можливого російського впливу" if IS_ATTRIBUTION_REPORT else "Петропавлівська Борщагівка: публічно названі фігуранти та процесуальний статус"),
        author="Самостійний OSINT-огляд відкритих джерел",
        subject=("Методичний протокол і застосування до інформаційної хвилі 2 листопада 2026 року" if IS_ATTRIBUTION_REPORT else "Публічно названі фігуранти, процесуальні статуси та відкриті питання станом на 6 листопада 2026 року"),
    )
    doc.build(make_story())
    print(OUTPUT)


if __name__ == "__main__":
    main()
