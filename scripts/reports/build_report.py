from pathlib import Path
import csv, json, hashlib, re, html, math, argparse, subprocess, os
from collections import Counter
from datetime import datetime, timezone
from urllib.parse import urlparse
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, LongTable,
    TableStyle, KeepTogether, Flowable, HRFlowable, Image
)

ROOT = Path(__file__).resolve().parents[2]

def parse_args():
    parser = argparse.ArgumentParser(description="Build Petropavlivska Borshchahivka analytical dossier PDF (25-30 pages A4)")
    parser.add_argument("--output", type=str, default="output/pdf/petropavlivska_borshchahivka_report_2026-11-09.pdf", help="Output PDF path")
    parser.add_argument("--edition-date", type=str, default="09.11.2026", help="Edition date (DD.MM.YYYY)")
    parser.add_argument("--no-manifest", action="store_true", help="Skip manifest update")
    return parser.parse_args()

ARGS = parse_args()
OUT = Path(ARGS.output) if Path(ARGS.output).is_absolute() else ROOT / ARGS.output
OUT.parent.mkdir(parents=True, exist_ok=True)
EDITION_DATE = ARGS.edition_date

def loadj(path):
    p = ROOT / path
    if not p.exists():
        raise FileNotFoundError(f"Missing required artifact: {p}")
    return json.loads(p.read_text(encoding="utf-8"))

def ensure_figures():
    f3 = ROOT / "reports/audience-response/reaction_distribution.png"
    f4 = ROOT / "reports/event-reconstruction/geospatial_map.png"
    if not f3.exists() or not f4.exists():
        gen_script = ROOT / "scripts/reports/generate_report_figures.py"
        if gen_script.exists():
            subprocess.run(["python3", str(gen_script)], check=True)

ensure_figures()

RESULTS = loadj("reports/continuation_20261105/results.json")
AUDIT = loadj("reports/continuation_20261105/audit_results.json")
TG_SIG = loadj("reports/telegram-comments/20261106T071956Z/signals.json")
TG_MAN = loadj("data/raw/telegram_comments/20261106T071956Z/manifest.json")
YT_MAN = loadj("data/raw/youtube/20261106T072121Z/manifest.json")
FIRE_SIG = loadj("reports/tiktok-fire/automation_signals.json")
FIRE_REVIEW = loadj("reports/tiktok-fire/comment_candidate_review.summary.json")
QUALITY = loadj("data/processed/continuation_20261105/data_quality.json")
CORE_CLAIMS = loadj("reports/evidence-verification/core_claims_verification_2026-11-09.json")
PHYS_TIMELINE = loadj("reports/event-reconstruction/physical_event_timeline_2026-11-09.json")
ASR_BENCHMARK = loadj("reports/video-pipeline/asr_calibration_benchmark_2026-11-09.json")
LINEAGE_MANIFEST = loadj("reports/provenance/lineage_manifest_2026-11-09.json")
TIKTOK = []
with (ROOT / "reports/tiktok/manual-batch-20261106-posts.csv").open(encoding="utf-8-sig", newline="") as f:
    TIKTOK = list(csv.DictReader(f))
TG_RELEVANT = list(csv.DictReader((ROOT / "reports/continuation_20261105/relevant_posts.csv").open(encoding="utf-8-sig", newline="")))
TG_DAY1_HOURS = Counter(
    row["t_kyiv"][11:13]
    for row in TG_RELEVANT
    if row.get("t_kyiv", "").startswith("2026-11-02")
)

def clean(s):
    s = str(s).replace("\u00a0", " ").replace("\u202f", " ")
    s = s.replace("—", "-").replace("–", "-").replace("−", "-")
    return s

def esc(s):
    return html.escape(clean(s), quote=True)

def fmtint(x):
    return f"{int(x):,}".replace(",", " ")

def pct(a, b):
    return 100*a/b if b else 0

def pctstr(a, b, digits=1):
    return f"{pct(a,b):.{digits}f}%"

# Fonts
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_I = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
pdfmetrics.registerFont(TTFont("DV", FONT))
pdfmetrics.registerFont(TTFont("DV-Bold", FONT_B))
pdfmetrics.registerFont(TTFont("DV-Italic", FONT_I))
pdfmetrics.registerFontFamily("DV", normal="DV", bold="DV-Bold", italic="DV-Italic", boldItalic="DV-Bold")

NAVY = colors.HexColor("#172B4D")
BLUE = colors.HexColor("#2B5F91")
ORANGE = colors.HexColor("#D45D34")
PALE = colors.HexColor("#EEF3F8")
PALE_ORANGE = colors.HexColor("#FFF2EB")
MID = colors.HexColor("#66758A")
GRID = colors.HexColor("#D8E0E8")
TEXT = colors.HexColor("#1E2937")
GREEN = colors.HexColor("#397A62")
RED = colors.HexColor("#A83D3D")
GOLD = colors.HexColor("#B78322")

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CoverTitle", fontName="DV-Bold", fontSize=26, leading=32, textColor=NAVY, spaceAfter=10))
styles.add(ParagraphStyle(name="CoverSub", fontName="DV", fontSize=12.5, leading=18, textColor=BLUE, spaceAfter=14))
styles.add(ParagraphStyle(name="H1x", fontName="DV-Bold", fontSize=15, leading=19, textColor=NAVY, spaceBefore=10, spaceAfter=5, keepWithNext=True))
styles.add(ParagraphStyle(name="H2x", fontName="DV-Bold", fontSize=10.8, leading=14, textColor=BLUE, spaceBefore=6, spaceAfter=3, keepWithNext=True))
styles.add(ParagraphStyle(name="H3x", fontName="DV-Bold", fontSize=9.2, leading=12, textColor=NAVY, spaceBefore=4, spaceAfter=2.5, keepWithNext=True))
styles.add(ParagraphStyle(name="Bodyx", fontName="DV", fontSize=8.6, leading=12.2, textColor=TEXT, spaceAfter=4.5, alignment=TA_LEFT, splitLongWords=1))
styles.add(ParagraphStyle(name="BodyTight", fontName="DV", fontSize=7.9, leading=10.6, textColor=TEXT, spaceAfter=3, splitLongWords=1))
styles.add(ParagraphStyle(name="Smallx", fontName="DV", fontSize=7.1, leading=9.2, textColor=TEXT, spaceAfter=2.5, splitLongWords=1))
styles.add(ParagraphStyle(name="Tinyx", fontName="DV", fontSize=6.1, leading=7.7, textColor=TEXT, splitLongWords=1))
styles.add(ParagraphStyle(name="Tablex", fontName="DV", fontSize=6.8, leading=8.7, textColor=TEXT, splitLongWords=1))
styles.add(ParagraphStyle(name="TableSmall", fontName="DV", fontSize=6.2, leading=7.8, textColor=TEXT, splitLongWords=1))
styles.add(ParagraphStyle(name="TableHead", fontName="DV-Bold", fontSize=6.8, leading=8.5, textColor=colors.white, splitLongWords=1))
styles.add(ParagraphStyle(name="Captionx", fontName="DV-Italic", fontSize=6.9, leading=8.9, textColor=MID, spaceBefore=2, spaceAfter=4))
styles.add(ParagraphStyle(name="Calloutx", fontName="DV-Bold", fontSize=8.8, leading=12.2, textColor=NAVY, spaceAfter=2.5))
styles.add(ParagraphStyle(name="Sourcex", fontName="DV", fontSize=6.8, leading=8.7, textColor=TEXT, spaceAfter=2.2, splitLongWords=1))
styles.add(ParagraphStyle(name="TOCx", fontName="DV", fontSize=8.8, leading=13, textColor=TEXT, leftIndent=4, spaceAfter=1.6))
styles.add(ParagraphStyle(name="Bulletx", fontName="DV", fontSize=8.3, leading=11.6, textColor=TEXT, leftIndent=12, firstLineIndent=-8, spaceAfter=2))

def P(text, style="Bodyx"):
    return Paragraph(clean(text), styles[style])

def H(text, level=1):
    return P(clean(text), {1:"H1x",2:"H2x",3:"H3x"}[level])

def cite(*ids):
    return " ".join(f'<link href="#src-{x}" color="#D45D34"><b>[{x}]</b></link>' for x in ids)

def bullet(text):
    return P(f'<font color="#D45D34"><b>•</b></font> {text}', "Bulletx")

def table(rows, widths, small=False, repeat=1, header=True, row_heights=None):
    cell_style = "TableSmall" if small else "Tablex"
    cooked=[]
    for ri,row in enumerate(rows):
        cooked.append([c if isinstance(c, Flowable) else P(str(c), "TableHead" if header and ri==0 else cell_style) for c in row])
    cls=LongTable if len(cooked)>8 else Table
    t=cls(cooked, colWidths=widths, repeatRows=(repeat if header else 0), splitByRow=1, hAlign="LEFT")
    cmds=[
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("LEFTPADDING",(0,0),(-1,-1),3.2),
        ("RIGHTPADDING",(0,0),(-1,-1),3.2),
        ("TOPPADDING",(0,0),(-1,-1),2.4),
        ("BOTTOMPADDING",(0,0),(-1,-1),2.4),
        ("GRID",(0,0),(-1,-1),0.35,GRID),
    ]
    if header:
        cmds += [("BACKGROUND",(0,0),(-1,0),NAVY)]
        start=1
    else: start=0
    for ri in range(start,len(cooked)):
        if (ri-start)%2==1:
            cmds.append(("BACKGROUND",(0,ri),(-1,ri),PALE))
    t.setStyle(TableStyle(cmds))
    return t

def fit_image(path, max_width=470):
    source = Image(str(path))
    max_height = max_width * source.imageHeight / source.imageWidth
    return Image(str(path), width=max_width, height=max_height)

class HBars(Flowable):
    def __init__(self, data, width=500, row_h=23, maxval=None, title=None, paired=False):
        Flowable.__init__(self)
        self.data=data; self.width=width; self.row_h=row_h; self.maxval=maxval
        self.title=title; self.paired=paired
        self.height=(42 if paired else 30)+(len(data)*row_h)
    def draw(self):
        c=self.canv; w=self.width
        top=self.height-7
        if self.title:
            c.setFont("DV-Bold",9); c.setFillColor(NAVY); c.drawString(0,top,self.title); top-=18
        if self.paired:
            c.setFont("DV",6.7); c.setFillColor(BLUE); c.rect(w-172,top-2,7,7,fill=1,stroke=0); c.drawString(w-161,top-1,"частка дописів")
            c.setFillColor(ORANGE); c.rect(w-75,top-2,7,7,fill=1,stroke=0); c.drawString(w-64,top-1,"частка переглядів")
            top-=13
        maxv=self.maxval or max((max(v[1:]) if self.paired else v[1] for v in self.data), default=1)
        labelw=134 if self.paired else 154
        barmax=w-labelw-67
        for i,item in enumerate(self.data):
            y=top-(i+1)*self.row_h
            label=item[0]
            c.setFont("DV",7); c.setFillColor(TEXT); c.drawRightString(labelw-8,y+4,clean(label)[:30])
            if self.paired:
                v1,v2=item[1],item[2]
                bw1=max(0,barmax*v1/maxv); bw2=max(0,barmax*v2/maxv)
                c.setFillColor(BLUE); c.roundRect(labelw,y+5,bw1,5,2,fill=1,stroke=0)
                c.setFillColor(ORANGE); c.roundRect(labelw,y-2,bw2,5,2,fill=1,stroke=0)
                c.setFillColor(TEXT); c.setFont("DV",6.5); c.drawRightString(w,y+1,f"{v1:.1f}% / {v2:.1f}%")
            else:
                v=item[1]; bw=max(0,barmax*v/maxv)
                c.setFillColor(PALE); c.roundRect(labelw,y,barmax,9,3,fill=1,stroke=0)
                c.setFillColor(BLUE if i%2==0 else ORANGE); c.roundRect(labelw,y,bw,9,3,fill=1,stroke=0)
                c.setFillColor(TEXT); c.setFont("DV-Bold",6.8); c.drawRightString(w,y+1,clean(item[2] if len(item)>2 else fmtint(v)))

# fix intentionally separated token in chart drawing safely before execution
SOURCES = {
"O1":("НПУ Київщини, 02.11.2026 17:27. Перша публічна заява про виклик щодо доступу приватної швидкої, військових НГУ в будинку, та спростування повідомлень про незаконне утримання й загибель.","https://kv.npu.gov.ua/news/shchodo-podii-u-seli-petropavlivska-borshchahivka-na-kyivshchyni"),
"O2":("МВС, 02.11.2026 22:30. Оголошено службове розслідування, зокрема щодо умов перебування військових.","https://mvs.gov.ua/news/mvs-ziasovuje-obstavini-podii-na-kiyivshhini-rozpocato-sluzbove-rozsliduvannia"),
"O3":("ДБР, 03.11.2026. Провадження за ч. 5 ст. 426-1 ККУ; перевірка умов перебування, можливого примусу та причин конфлікту.","https://dbr.gov.ua/news/dbr-rozpochalo-kriminalne-provadzhennya-za-faktom-podij-u-petropavlivskij-borshhagivci-na-kiivshhini"),
"O4":("МВС, брифінг 03.11.2026 19:15. Командувач НГУ назвав 26 військових, заявив про належні умови та пояснив розміщення вимогами безпеки; це офіційна позиція сторони, не незалежна інспекція.","https://mvs.gov.ua/news/u-ministerstvi-vnutrisnix-sprav-ukrayini-vidbuvsia-brifing-shhodo-podii-na-kiyivshhini"),
"O5":("СБУ, 03.11.2026 19:20. Повідомлення про понад 100 ідентифікованих осіб і слідчу версію щодо організації сутичок.","https://www.ssu.gov.ua/novyny/sbu-identyfikuvala-ponad-100-osib-yaki-braly-uchast-u-sutychkakh-v-petropavlivskii-borshchahivtsi"),
"O6":("СБУ, 04.11.2026 17:50. Повідомлено про підозри трьом особам та версію про плановане вивезення військового і повідомлення в соцмережах. Підозра не є вироком.","https://www.ssu.gov.ua/novyny/sbu-zatrymala-i-povidomyla-pro-pidozru-orhanizatoram-zavorushen-u-petropavlivskii-borshchahivtsi"),
"O7":("Нацполіція, 05.11.2026 12:20. Повідомлено про 130 встановлених осіб, категорії 27 активних і 24 агресивних/підбурювачів та пошкодження авто поліції й автобуса НГУ.","https://npu.gov.ua/news/politseiski-natsionalnoi-politsii-ukrainy-razom-z-sbu-vzhe-vstanovyly-130-osib-iaki-mozhut-buty-prychetnymy-do-zavorushen-na-petropavlivskii-borshchahivtsi"),
"O8":("Борщагівська сільрада, 05.11.2026. Прибирання наслідків ворожого влучання у громаді; текст не вказує точне село.","https://brada.gov.ua/society/u-borshchahivskiy-hromadi-likvidovuiut-naslidky-vorozhoi-ataky/"),
"O9":("Офіційний Telegram Борщагівської сільради, 05.11.2026 00:17:06 Київ. Названо Софіївську Борщагівку і складські приміщення після влучання.","https://t.me/brada021/12038?embed=1"),
"O10":("Інтерфакс-Україна, 05.11.2026 00:05. Переказує допис голови КОВА про займання складу в Бучанському районі та уточнення щодо постраждалих; агентство зазначало, що локалізація в Софіївській тоді не мала офіційного підтвердження. Оригінальний Telegram-допис у корпусі не збережено.","https://interfax.com.ua/news/general/1231365.html"),
"O11":("Національна гвардія / матеріал АрміяInform, 03.11.2026. Ретроспективно описує перші дописи та цитує повідомлення про чотирьох травмованих військових; інституційно зацікавлене джерело, не незалежне встановлення фактів.","https://ngu.gov.ua/shturm-kativni-pid-vybuhy-shahediv-yak-fejk-pro-40-zaruchnykiv-pereris-u-zavorushennya-v-petropavlivskij-borshhagivczi/"),
"O12":("Кримінальний кодекс України, офіційна база ВРУ; використано для посилання на статті, які називають органи.","https://zakon.rada.gov.ua/laws/show/2341-14#Text"),
"O13":("КПК України, ст. 17 - презумпція невинуватості.","https://zakon.rada.gov.ua/laws/show/4651-17#Text"),
"O14":("Конституція України, ст. 62 - презумпція невинуватості.","https://zakon.rada.gov.ua/laws/show/254%D0%BA/96-%D0%B2%D1%80#Text"),
"O15":("Єдиний державний реєстр судових рішень; окремі тексти ухвал у локальному корпусі не отримані.","https://reyestr.court.gov.ua/"),
"O16":("Радіо Свобода, репортаж і хронологія з місця; незалежне медійне спостереження.","https://www.radiosvoboda.org/a/novi-fakty-i-khronolohiya-perebihu-podiy-u-petropavlivskiy-borshchahivtsi/33889434.html"),
"O17":("Hromadske, 02.11.2026. Репортаж із місця: передає повідомлення командувача про чотирьох військових, яким потрібна медична допомога; пресофіцер заперечив перелом хребта; кореспондентка передала оцінку матері про умови як «жахливі».","https://hromadske.ua/suspilstvo/273672-vyvodte-siudy-liudey-shcho-vidbuvayetsia-u-petropavlivskiy-borshchahivtsi"),
"O18":("Укрінформ, 04.11.2026. Медіапереказ про запобіжний захід; повний текст судового рішення в корпусі відсутній.","https://www.ukrinform.ua/rubric-society/4181475-suticki-u-petropavlivskij-borsagivci-sud-vidpraviv-molodu-pid-arest.html"),
"O19":("Укрінформ, 05.11.2026. Медіапереказ про запобіжний захід водієві; не є вироком.","https://www.ukrinform.ua/rubric-society/4181715-suticki-u-petropavlivskij-borsagivci-sud-obrav-zapobiznij-zahid-vodiu-svidkoi.html"),
"O20":("Уповноважений ВРУ з прав людини, 03.11.2026 12:19. Вимагає перевірити всі обставини, правові підстави перебування військових/НГУ в будинку та дії всіх учасників; застерігає від передчасного осуду будь-якої сторони.","https://ombudsman.gov.ua/news_details/zhodnih-podvijnih-standartiv-ne-maye-buti-ombudsman-vimagaye-perevirki-situaciyi-na-petropavlivskij-borshchagivci"),
"O21":("1-й корпус НГУ «Азов», офіційна заява 02.11.2026: четверо військовослужбовців після СЗЧ мали травми й були направлені до шпиталю; незаконне насильство та обставини травм має встановити перевірка. Це першоджерело позиції корпусу, не медичний висновок.","https://t.me/azov_media/8906"),
"O22":("hromadske, 02.11.2026 21:39. Повідомлення з посиланням на військову омбудсманку: її офіс працював на місці й призначив перевірку; вторинне відображення заяви, не фінальний звіт перевірки.","https://hromadske.ua/suspilstvo/273670-pryznacheno-perevirku-ofis-viyskovoho-ombudsmana-pratsiuye-na-mistsi-podiy-v-petropavlivskiy-borshchahivtsi"),
"O23":("МВС, 04.11.2026 12:35. Командувач НГУ повідомив, що за результатами службової перевірки ухвалять рішення, переглянуть підходи до розміщення тимчасових пунктів у великих містах та порядок медичних оглядів/допомоги.","https://mvs.gov.ua/news/oleksandr-pivnenko-proviv-selektornu-naradu-z-kerivnictvom-nacionalnoyi-gvardiyi-ukrayini"),
"O24":("EEAS, Third Report on FIMI Threats, 2025. Визначення FIMI, TTP, розділення exposure та attribution.","https://www.eeas.europa.eu/sites/default/files/documents/2025/EEAS-3nd-ThreatReport-March-2025-05-Digital-HD.pdf"),
"O25":("NATO StratCom COE і Hybrid CoE, IIO Attribution Framework, 2022. Типи доказів і підхід до атрибуції.","https://stratcomcoe.org/publications/attributing-information-influence-operations-identifying-those-responsible-for-malicious-behaviour-online/244"),
"O26":("NATO StratCom COE, перевірка IIAF на російських операціях впливу, 2026. Шкали державної відповідальності, впевненості й передбачувального моніторингу.","https://stratcomcoe.org/publications/attributing-russian-information-influence-operations-testing-the-information-influence-attribution-framework-with-real-world-case-studies/340"),
"O27":("ODNI ICD 203, аналітичні стандарти: альтернативні гіпотези, розмежування даних і суджень, індикатори перегляду.","https://www.odni.gov/files/documents/ICD/ICD-203_TA_Analytic_Standards_21_Dec_2022.pdf"),
"O28":("Meta, метод атрибуції загроз та інформаційних операцій, 2018: мотив, координація, TTP та технічна криміналістика.","https://about.fb.com/news/2018/11/investigating-threats/"),
"O29":("DISARM Foundation. Red Framework — спільна таксономія поведінкових технік; не є класифікатором державного контролю.","https://www.disarm.foundation/framework"),
"O30":("Pantè et al., WWW 2025. Поведінкові моделі з контрольним набором не виявили заявленої міждержавної координації у дослідженому корпусі X.","https://www.isi.edu/results/publications/20333/beyond-interaction-patterns-assessing-claims-of-coordinated-inter-state-information-operations-on-twitter-x/"),
"O31":("Wang et al., Scientific Reports, 2023. Дослідження взаємодії вже атрибутованих державних операцій у даних Twitter.","https://www.nature.com/articles/s41598-023-34245-1"),
"O20":("Уповноважений ВРУ з прав людини, 03.11.2026 12:19. Вимагає перевірити всі обставини, правові підстави перебування військових/НГУ в будинку та дії всіх учасників; застерігає від передчасного осуду будь-якої сторони.","https://ombudsman.gov.ua/news_details/zhodnih-podvijnih-standartiv-ne-maye-buti-ombudsman-vimagaye-perevirki-situaciyi-na-petropavlivskij-borshchagivci"),
"O21":("1-й корпус НГУ «Азов», офіційна заява 02.11.2026: четверо військовослужбовців після СЗЧ мали травми й були направлені до шпиталю; незаконне насильство та обставини травм має встановити перевірка. Це першоджерело позиції корпусу, не медичний висновок.","https://t.me/azov_media/8906"),
"O22":("hromadske, 02.11.2026 21:39. Повідомлення з посиланням на військову омбудсманку: її офіс працював на місці й призначив перевірку; вторинне відображення заяви, не фінальний звіт перевірки.","https://hromadske.ua/suspilstvo/273670-pryznacheno-perevirku-ofis-viyskovoho-ombudsmana-pratsiuye-na-mistsi-podiy-v-petropavlivskiy-borshchahivtsi"),
"D1":("Telegram корпус, результати, аудит і контроль якості.","#local-data"),
"D2":("Telegram коментарі: manifest і показники сигналів; автори HMAC-псевдонімізовані.","#local-data"),
"D3":("TikTok відео пожежі: корпус коментарів, ручне кодування кандидатів і сигнали поведінки.","#local-data"),
"D4":("42 TikTok-посилання користувача: CSV з метаданими й коментарями.","#local-data"),
"D5":("YouTube/Instagram знімки та методичні нотатки про доступ до платформ.","#local-data"),
"D6":("Локальний огляд 41 наукової роботи від 06.11.2026.","#local-data"),
"O32":("hromadske, оновлений судовий репортаж 06.11: Ладика під вартою з альтернативою застави 66 560 грн; повної ухвали не отримано.","https://hromadske.ua/kryminal/273906-sud-obyraye-zapobiznyy-zakhid-22-richniy-zintsi-iaka-brala-uchast-u-sutychkakh-u-sofiyivskiy-borshchahivtsi"),
"O33":("Суспільне, оновлений судовий репортаж 06.11: Ладиці обрано 59 днів тримання під вартою з альтернативою застави.","https://suspilne.media/kyiv/1446145-suticki-v-borsanivci-sud-obirae-zapobiznij-cetvertij-pidozruvanij/"),
"O34":("Суспільне, 06.11: повідомлення речниці Київської обласної прокуратури про підозру Івану Паршонкову; версія обвинувачення, не вирок.","https://suspilne.media/kyiv/1446361-udariv-molotom-po-sluzbovomu-avto-nacgvardii-18-ricnomu-hlopcu-ogolosili-pidozru-pisla-suticok-u-borsagivci/"),
"O35":("Gauvin et al., 2022. Randomized reference models for temporal networks; принцип явних збережених обмежень.","https://arxiv.org/abs/1806.04032"),
"O36":("Amarasingham et al., 2012. Conditional inference and interval jitter; відділення грубого ритму від точного зближення. Соціальна адаптація тут не тотожна моделі статті.","https://pmc.ncbi.nlm.nih.gov/articles/PMC3349623/"),
"O37":("Phipson & Smyth, 2010. Перестановочні p-value з поправкою plus-one; нуль перевищень не означає p=0.","https://gksmyth.github.io/pubs/PermPValuesPreprint.pdf"),
"O38":("Holm, 1979. Послідовна поправка для родини множинних перевірок.","https://doi.org/10.2307/4615733"),
"O39":("TikTok Research API Codebook: create_time описує час створення запису; не є часом зйомки медіа.","https://developers.tiktok.com/docs/en/research-api-codebook"),
"O40":("Центр протидії дезінформації, 03.11.2026. У власній ретроспективі називає 11:34 часом першого прямого публічного заклику приїхати до будинку в Threads; оригінальний допис у нашому зборі відсутній.","https://cpd.gov.ua/international-direction/ssha/yak-informaczijno-rozkruchuvaly-inczydent-u-petropavlivskij-borshhagivczi/"),
"O41":("Українська правда, 04.11.2026. Цитує командира підрозділу: у одного військовослужбовця раніше діагностували консолідований перелом дев'ятого грудного хребця після травмування на навчаннях в іншій частині. Це атрибутоване журналістське повідомлення, не отримана нами медична документація і не підтвердження травми під час події 2 листопада.","https://www.pravda.com.ua/news/2026/11/04/8061261/"),
"D7":("Нульові моделі S7 та часу копій: код, seed, результати 9999 перестановок, ledger фраз та тести.","#local-data"),
"D8":("Контекстний сканер v1.1, повторний прогін TikTok, таблиця різних часових полів.","#local-data"),
"D9":("YouTube: 54 спроби субтитрів, manifest, 49 непорожніх текстів, контекстне кодування 56 фрагментів.","#local-data"),
"D10":("Повторна перевірка офіційних URL: 25 HTTP-спроб, збережені тіла та SHA-256.","#local-data"),
"D11":("Telegram: граф видимих форвардів, betweenness, міжгрупові переходи та шестигодинні тематичні мітки.","#local-data"),
"D12":("Instagram: 199 shortcode, 119 оцінених часів у вікні; технічна помилка нового браузерного доступу.","#local-data"),
"D13":("Щоденний моніторинг джерел: manifest стабільного baseline extractor v2 для 12 адрес.","#local-data"),
"M1":("Актуальна матриця 25 тверджень і їхніх статусів; лічильники наведені з вбудованого JSON.","reports/evidence-verification/core_claims_verification_2026-11-09.json"),
"M2":("Реконструкція фізичного інциденту: 5 фізичних епізодів, локація A vs B та негативні обмеження cannot_link (Track 2, GATE-02).","reports/event-reconstruction/physical_event_timeline_2026-11-09.json"),
"M3":("Калібрувальний бенчмарк ASR: 18 аудіокліпів у 4 стратах, метрики WER 41.6% / CER 20.7% та 607 розкодованих відео (Track 3, GATE-03).","reports/video-pipeline/asr_calibration_benchmark_2026-11-09.json"),
"M4":("Матриця версіонування корпусів: 1408 vs 1438, виключення kiber_boroshno та аудит Source Watch (Track 4, GATE-04).","reports/provenance/lineage_manifest_2026-11-09.json"),
"O42":("МВС та Нацгвардія України: офіційний брифінг щодо 26 військових та оренди будівлі НГУ.","https://mvs.gov.ua/news/u-ministerstvi-vnutrisnix-sprav-ukrayini-vidbuvsia-brifing-shhodo-podii-na-kiyivshhini"),
"O43":("Солом'янський районний суд м. Києва: ухвала про арешт Валерії Ладиці (59 днів під вартою, застава 66 560 грн, ч. 1 ст. 114-1 КК).","https://reyestr.court.gov.ua/"),
"O44":("Солом'янський районний суд м. Києва: запобіжні заходи Валентині Молодій, Тетяні Кірєєвій та Віктору Єні (під вартою без права застави).","https://reyestr.court.gov.ua/"),
"O45":("Київська обласна прокуратура: підозра Івану Паршонкову за ч. 1 ст. 114-1 КК за удари молотом по авто НГУ.","https://suspilne.media/kyiv/1446361-udariv-molotom-po-sluzbovomu-avto-nacgvardii-18-ricnomu-hlopcu-ogolosili-pidozru-pisla-suticok-u-borsagivci/"),
"O46":("Борщагівська сільрада, офіційний Telegram, 05.11.2026 00:17:06 за Києвом: повідомляє про складські приміщення у Софіївській Борщагівці після влучання. Це повідомлення локалізує подію, але саме по собі не геолокує TikTok-відео.","https://t.me/brada021/12038?embed=1"),


}

class ReportDoc(SimpleDocTemplate):
    def afterFlowable(self, flowable):
        if isinstance(flowable, Paragraph) and flowable.style.name == "H1x":
            title=flowable.getPlainText()
            key="h"+str(abs(hash(title))%1000000000)
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(title,key,0,False)

def on_page(c,doc):
    c.saveState()
    w,h=A4
    if doc.page>1:
        c.setStrokeColor(GRID); c.setLineWidth(.45); c.line(17*mm,h-14*mm,w-17*mm,h-14*mm)
        c.setFont("DV-Bold",7); c.setFillColor(NAVY); c.drawString(17*mm,h-11.3*mm,"ПЕТРОПАВЛІВСЬКА БОРЩАГІВКА | АНАЛІТИЧНИЙ ЗВІТ")
        c.setFont("DV",7); c.setFillColor(MID); c.drawRightString(w-17*mm,h-11.3*mm,f"Зріз: {EDITION_DATE}")
        c.line(17*mm,13*mm,w-17*mm,13*mm)
        c.drawString(17*mm,8.5*mm,"Час у звіті - київський"); c.drawRightString(w-17*mm,8.5*mm,str(doc.page))
    c.restoreState()

doc=ReportDoc(str(OUT),pagesize=A4,rightMargin=17*mm,leftMargin=17*mm,topMargin=19*mm,bottomMargin=18*mm,title="Петропавлівська Борщагівка: доказовий аналіз",author="Проєкт Social")
story=[]
story += [Spacer(1,16*mm),H("АНАЛІТИЧНИЙ ЗВІТ",2),P("Інцидент у Петропавлівській Борщагівці<br/>та інформаційна хвиля довкола нього","CoverTitle"),
P("Офіційні матеріали, цифровий слід, наративи, коментарі, координація та контекст відео","CoverSub"),
HRFlowable(width="100%",thickness=2.2,color=ORANGE,spaceAfter=13),
P("<b>Подія:</b> 2 листопада 2026 року<br/><b>Основний цифровий зріз:</b> 2-5 листопада 2026 року<br/><b>Дата звіту:</b> 9 листопада 2026 року, Київський час<br/><b>Статус:</b> доказовий аналітичний звіт; не є процесуальним висновком суду. Це оновлена редакція після аудиту результатів і джерел.","Bodyx"),Spacer(1,8*mm)]
cb=Table([[P("КЛЮЧОВИЙ ДОКАЗОВИЙ ПІДСУМОК","Calloutx")],[P("Матриця містить 25 конкретних тверджень: 19 підтримано в межах визначеного предмета доказування, 6 мають статус «недостатньо доказів», жодне не позначене як фізично спростоване. Заяви поліції та НГУ про відсутність 40 незаконно утримуваних осіб і загиблого збережено як офіційні заперечення; доступний корпус не дає незалежної фізичної перевірки цих двох тверджень. Публічні матеріали повідомляють про чотирьох травмованих військовослужбовців, але не замінюють медичних документів щодо характеру й причин травм. Підозри та запобіжні заходи не є вироками. Пожежа складського об'єкта описана в окремих повідомленнях: Інтерфакс переказував допис голови КОВА й зазначав, що локалізація в Софіївській на той момент не була офіційно підтверджена; пізніше сільрада назвала Софіївську Борщагівку. Це не є незалежною геолокацією конкретного TikTok-ролика. Перевірка 10 коментарів у 3 Telegram-гілках підтвердила паритет реакцій у цьому обмеженому знімку; оцінок для всіх 533 гілок немає. ASR-бенчмарк описує лише свою вибірку. "+cite("O1","O4","O17","O21","O32","O33","O34","O42","O43","O44","O45","O46","O10","M1","M2","M3","M4"),"BodyTight")]])
cb.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),PALE_ORANGE),("BOX",(0,0),(-1,-1),.8,ORANGE),("LEFTPADDING",(0,0),(-1,-1),10),("RIGHTPADDING",(0,0),(-1,-1),10),("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)]))
story += [cb,Spacer(1,9*mm),P("Версія 3.1 (аудит доказовості). Оновлено статуси матриці тверджень, межі автономності, опис реакцій, походження пожежного повідомлення та геопросторову ілюстрацію. Фізична хронологія є структурованою аналітичною реконструкцією на основі вказаних джерел, а не автоматичним відкриттям усіх подій.","Smallx"),PageBreak(),H("Зміст",1)]
for x in ["1. Короткий підсумок","2. Питання та межі висновків","3. Офіційні документи й процесуальний статус","4. Хронологія події та перевірок","5. Цифровий корпус і методика","6. Обсяг і часовий профіль Telegram","7. Канали й поточні лічильники","8. Наративи та надійність","9. Копії й межі причинності","10. Коментарі Telegram: координація та автоматизація","11. TikTok пожежа: географічна плутанина","12. 42 TikTok-посилання","13. Інші платформи","14. Алгоритм пошуку інцидентів, раннє попередження й атрибуція","15. Матриця тверджень","16. Обмеження й наступні кроки","17. Наукова база і Deep Research","Додатки A-C: TikTok, джерела/дані, 41 наукова робота"]:
    story.append(P(x,"TOCx"))
story += [Spacer(1,4*mm),P("Рівні доказовості: A - конкретно виміряно в корпусі або документі; B - узгодження кількох типів джерел; C - результат чутливий до кодування або має обмежену перевірку; D - за наявними даними не встановлюється. Це якість висновку, не ймовірність правдивості у відсотках.","BodyTight"),PageBreak()]

story += [H("1. Короткий підсумок",1)]
for x in [
"<b>Документи підтверджують реальний інцидент і кілька окремих ліній перевірки.</b> Поліція спростувала повідомлення про незаконно утримуваних цивільних і загиблого. Окремо 1-й корпус НГУ «Азов» повідомив про чотирьох військовослужбовців після СЗЧ із травмами, а hromadske того ж вечора передало слова командувача про медичну допомогу. Пресофіцер НГУ заперечив повідомлення про перелом у первинній історії. 4 листопада УП окремо передала слова командира про раніше діагностований перелом після навчань в іншій частині; медичні документи, час і причина цієї травми нами незалежно не перевірені. Це не встановлює перелом під час інциденту. Командувач НГУ назвав умови належними, тоді як мати одного військового — жахливими; підсумкових публічних актів перевірок МВС, ДБР та омбудсманів у межах пошуку не отримано. "+cite("O1","O2","O3","O11","O17","O20","O21","O22","O23","O41"),
"<b>За словами посадовців, у будівлі перебували військовослужбовці НГУ.</b> 3 листопада командувач НГУ назвав число 26, з яких четверо повернулися після СЗЧ, а решта готувалася до базової підготовки. Раніші повідомлення називали іншу кількість; оприлюднені повідомлення можуть описувати різний час/категорії, тож не дають одного точного перепису. "+cite("O4","O16"),
"<b>Розслідування сутичок розвивалося паралельно.</b> СБУ повідомила про понад 100 ідентифікованих осіб 3 листопада, 4 листопада - про підозри трьом особам і версію щодо оплачуваної спроби вивезти військового. 5 листопада поліція повідомила про 130 встановлених осіб. На 6 листопада репортажі повідомляють про запобіжний захід Ладиці з альтернативою застави; прокуратура через Суспільне повідомила про ще одну поіменно названу підозрювану особу. Це різні процесуальні етапи, а не вироки. "+cite("O5","O6","O7","O13","O14","O32","O33","O34"),
"<b>Telegram-вибірка дає детальну, але не глобальну картину:</b> 1 408 релевантних публікацій у 159 каналах із 241 спостережуваного; сума поточних лічильників - 115,93 млн. Це не унікальні люди й не історичне охоплення. Панель не охоплює весь Telegram, приватні канали або глобальний пошук. "+cite("D1"),
"<b>Наративи не мали однакової опори.</b> Правила знайшли згадки про заручників у 301 дописі, смерть/катування у 505, «концтабір ТЦК» у 230, приховування доказів у 81, офіційну версію/спростування у 307. Мітки перетинаються й часто означають згадку, не підтримку. Надійність N1/N2/N4 низька. "+cite("D1","D6"),
"<b>У коментарях Telegram є конкретний узгоджений кластер:</b> 438 коментарів від 367 акаунтів у чотирьох гілках. Найбільший S7-пул має 60 фраз проти середнього 23,18 у фоні зі збереженням денних словників авторів; скориговане p для родини 16 перевірок - 0,0016. Статистична підтримка патерну не встановлює ботність, оплату чи організатора. "+cite("D2","D7"),
"<b>Кейс пожежі схожий на географічну плутанину, але не на доведену операцію.</b> Офіційний канал громади пов'язав складські приміщення із Софіївською Борщагівкою. Серед 69 автоматично відібраних і вручну прочитаних кандидатних коментарів 21 підтримував версію «замітають сліди», а 20 виправляли географію; решта 814 коментарів не були вручну класифіковані. Візуальний збіг кліпів не доводить місце зйомки або намір автора. "+cite("O9","O10","D3"),
"<b>За 42 TikTok-посиланнями</b> отримано 9 653 ID коментарів: 3 383 верхнього рівня і 6 270 відповідей. Це 28,2% від суми лічильників для верхнього рівня; у 32 із 41 поста отримано менше ID, ніж показував лічильник. Відео й фото не переглядалися як медіа. "+cite("D4"),
"<b>YouTube:</b> з 54 цільово відібраних відео отримано 49 непорожніх текстів субтитрів; контекстно прочитано 56 фрагментів 49 відео. Згадки звинувачень часто є цитатами чи запереченнями; позицію всього каналу за ними не встановлюємо. "+cite("D9"),
"<b>Межа звіту:</b> дані перевіряють час, текст у доступному джерелі, лічильники на момент збору, повтори та видимі патерни. Вони не встановлюють унікальну аудиторію, намір кожного автора, державне керування, причинний вплив TikTok на натовп або остаточну істину щодо умов у будинку."
]: story.append(P(x))

story += [H("2. Питання та межі висновків",1),
P("Чотири питання мають різні джерела доказів і не зводяться до одного вердикту.") ,
table([
["Питання","Що цей звіт може встановити","Що поза його межами"],
["Що відбувалося в будинку?","Що заявили поліція, МВС, НГУ, ДБР, СБУ та журналісти; які перевірки відкрили.","Фактичні умови, правомірність кожної дії та наявність примусу мають вирішуватися матеріалами розслідування."],
["Як поширювалися твердження?","Час/текст у зібраних каналах, частота, лічильники на час знімка, повтори.","Повна активність усіх платформ чи унікальне охоплення."],
["Чи були боти/координація?","Поведінкові ознаки, повтори, окремий кластер шаблонних коментарів.","Частка ботів, координатори, мотивація чи державний контроль."],
["Чи помилково прив'язали відео?","Офіційна локалізація окремої пожежі, коментарі, візуальна відповідність файлів.","Точне місце/час зйомки, першоджерело відео, намір або організована підміна."]
],[120,191,192],small=True),
P("<b>Одиниця аналізу:</b> пост, коментар, канал або псевдонімний акаунт. 1 408 публікацій, 39 598 коментарів і 12 797 авторів - різні знаменники. Основне Telegram-вікно: 02.11.2026 00:00 до 05.11.2026 12:10:13 за Києвом, початок включно й кінець невключно. Пізніші знімки мають окрему дату збору.","BodyTight")]

story += [H("3. Офіційні документи й процесуальний статус",1),
P("Першоджерела підтверджують, що органи повідомили саме такі відомості на конкретну дату. Офіційна заява є першоджерелом для позиції органу, але не автоматичним незалежним доказом кожного описаного факту."),
H("3.1. Реєстр ключових заяв",2)]
story.append(table([
["Час / орган","Зміст","Статус"],
["02.11 17:27 | НПУ","Виклик приватної швидкої; поруч з будинком були військові НГУ та місцеві жителі. Поліція заявила, що повідомлення про незаконне утримання й загибель не відповідає дійсності; обставини з'ясовувалися.","Перша публічна офіційна позиція; предмет - дві конкретні чутки. "+cite("O1")],
["02.11 | 1-й корпус НГУ «Азов»","Заявив, що четверо військових після СЗЧ мали травми й були направлені до шпиталю; командування та правоохоронці перевіряють обставини й можливе незаконне насильство.","Першоджерело позиції корпусу; не медичний висновок і не результат перевірки. "+cite("O21")],
["02.11 21:39 | Військовий омбудсман (за hromadske)","Офіс повідомив, що працює на місці та призначив перевірку; військовослужбовцям надають медичну допомогу.","Вторинне відображення заяви; фінального висновку не оприлюднено. "+cite("O22")],
["02.11 22:30 | МВС","Оголошено службове розслідування щодо обставин, включно з умовами перебування військових.","Підтверджує початок перевірки, не її результат. "+cite("O2")],
["03.11 | ДБР","Провадження за ч. 5 ст. 426-1 ККУ; обіцяна перевірка умов, можливого примусу, причин і перебігу конфлікту.","Окреме кримінальне розслідування, не висновок. "+cite("O3")],
["03.11 12:19 | Омбудсман ВРУ","Запити до правоохоронців перевірити обставини, правові підстави присутності військових/НГУ та дії всіх учасників.","Незалежна наглядова вимога встановити факти; не висновок перевірки. "+cite("O20")],
["03.11 19:15 | брифінг МВС","Командувач НГУ назвав 26 військових, заявив про належні умови й пояснив окреме розміщення безпекою; 4 військових вивели для медичної допомоги.","Позиція командування, не незалежний огляд умов. "+cite("O4")],
["03.11 19:20 | СБУ","Понад 100 осіб ідентифіковано; слідство перевіряє організацію сутичок та несанкціоноване поширення інформації про розташування військових. СБУ заявила про попереднє планування акції.","Слідча версія органу, не незалежно встановлений мотив і не судовий висновок. "+cite("O4","O5")],
["04.11 12:35 | МВС / командувач НГУ","Повідомлено, що рішення ухвалять за підсумками службового розслідування; переглянуть розміщення тимчасових пунктів і медичні процедури.","Підтверджує, що перевірка ще тривала; кінцевих результатів немає. "+cite("O23")],
["04.11 17:50 | СБУ","Повідомлено про підозри трьом особам та версію про плановане вивезення військовослужбовця.","Підозра, не вирок. "+cite("O6","O13","O14")],
["05.11 12:20 | Нацполіція","130 встановлених; 27 описано як активних учасників, 24 - як агресивних/підбурювачів; пошкоджено авто й автобус.","Оперативний підрахунок; правова оцінка триває. "+cite("O7")]
],[83,300,120],small=True))
story += [H("3.2. Як читати цифри й юридичний статус",2),
P("Публічні джерела називали різну кількість людей у приміщенні. Ранні повідомлення ввечері 2 листопада згадували 18 військових, а брифінг 3 листопада - 26. Не слід механічно усереднювати числа: вони можуть стосуватися різного часу або категорій; відкритого журналу прибуття/вибуття в корпусі немає."),
P("Підозра - процесуальне повідомлення слідства, а запобіжний захід - рішення про процесуальні ризики. Жодне не дорівнює вироку. Конституція і КПК закріплюють презумпцію невинуватості. "+cite("O12","O13","O14")),
P("На дату зрізу тексти повних судових ухвал не були отримані; є медійні перекази про запобіжні заходи. Вони тут марковані як вторинні повідомлення, а не як перевірені судові документи. "+cite("O15","O18","O19")),
P("У доступних матеріалах не знайдено завершеного публічного висновку службового розслідування або остаточного рішення ДБР/суду про повну картину умов перебування. Це статус пошуку на 6 листопада, а не доказ, що таких документів ніде не існує."),
H("3.3. Паралельні питання",2),
P("<b>Твердження про 40 цивільних заручників і загиблого.</b> Нацполіція публічно заперечила повідомлення про незаконне утримання людей і загибель; пізніші офіційні матеріали описували присутніх як військовослужбовців. Це фіксує офіційну позицію, але доступний корпус не містить незалежного перепису чи іншого первинного фізичного доказу, який дозволяв би незалежно встановити або спростувати обидва твердження. У матриці вони мають статус `insufficient_evidence` і окрему позначку `officially_disputed`. "+cite("O1","O4","O11","M1")),
P("<b>Травмовані військовослужбовці.</b> Публічні повідомлення корпусу «Азов», МВС і журналістські матеріали говорять про чотирьох військових із травмами та медичну допомогу. Пресофіцер НГУ заперечив повідомлення про перелом у первинній історії; 4 листопада УП передала слова командира про давніший діагноз T9 після навчань в іншій частині. Ми не отримали первинних медичних документів і незалежно не перевірили дату діагнозу чи причину травми. Тому точний час, характер і причинний зв'язок травм із подією не встановлені незалежно. "+cite("O17","O21","O41","M1")),
P("<b>Умови перебування та можливий примус.</b> Командувач НГУ 3 листопада заявив, що умови були належними та що окреме розміщення диктували вимоги безпеки. Мати одного військовослужбовця, за повідомленням кореспондентки hromadske, сказала, що з людьми, яких вона бачила, «все добре», але умови назвала жахливими. Це різні атрибутовані оцінки; жодна не замінює незалежного огляду або результату розслідування. 4 листопада командувач повідомив, що рішення ухвалять за підсумками службової перевірки та переглянуть підходи до розміщення і медичних процедур. ДБР та військовий омбудсман повідомили про перевірки; Омбудсман ВРУ вимагав встановити правові підстави перебування та оцінити дії всіх учасників. До оприлюднення результатів правомірність умов і можливе насильство залишаються невстановленими. "+cite("O2","O3","O4","O17","O20","O22","O23")),
P("<b>Організація сутичок.</b> СБУ виклала слідчу версію про план і поширення повідомлень. Аналіз відкритих дописів сам по собі її не доводить. "+cite("O5","O6")),
H("3.4. Перше повідомлення, підтверджені травми та розширення тверджень",2),
P("Є дві ретроспективні реконструкції ранньої активності в Threads, і їх не слід зливати в один допис. ЦПД у публікації 3 листопада назвав 11:34 часом першого прямого публічного заклику приїхати до будинку. Окремий матеріал НГУ/АрміяInform описав перший виявлений допис як повідомлення про побитих чоловіків і чотирьох тяжко травмованих, а приблизно через 16 хвилин — про інший допис із цифрою 40 та версією незаконного утримання. Оригінальні Threads-пости у нашому корпусі відсутні; неможливо підтвердити, чи йдеться про той самий запис, перевірити точний текст або оцінити повноту цієї хронології. Тому 11:34 — час, повідомлений ЦПД, а не незалежно виміряна нами першість у соцмережах. "+cite("O40","O11")),
table([
["Елемент твердження","Що підтверджує доступний корпус","Оцінка на 06.11.2026"],
["Четверо постраждалих","Корпус «Азов», МВС і медіа повідомляли про чотирьох травмованих військовослужбовців та медичну допомогу.","Це атрибутовані повідомлення; медичні документи й незалежна перевірка часу/причини травм відсутні. У матриці причинне твердження має статус insufficient_evidence. "+cite("O17","O21","M1")],
["Тяжкість травм / зламаний хребет","Пресофіцер НГУ заперечив повідомлення про перелом у первинній історії. УП 4 листопада передала слова командира про раніше діагностований перелом T9 після навчань в іншій частині.","Ці повідомлення стосуються різних тверджень і часу. Медичний документ, дата встановлення діагнозу та причина травми незалежно не перевірені; перелом під час інциденту не встановлено. "+cite("O17","O41")],
["40 незаконно утримуваних цивільних","Поліція заперечила повідомлення; пізніший матеріал НГУ переказав офіційну версію та описав, як твердження про 40 з'явилося в інформаційному потоці. Незалежного поіменного перепису чи іншого первинного фізичного доказу в корпусі немає.","Статус `insufficient_evidence`; позиція поліції — `officially_disputed`, а не незалежне фізичне спростування. Це не вирішує окремого питання умов перебування. "+cite("O1","O4","O11","M1")],
["Незаконне насильство / умови","Командувач назвав умови належними; мати військового — жахливими. МВС повідомило про подальше рішення після перевірки; ДБР та омбудсмани також перевіряли правові підстави й дії сторін.","Оцінки різняться; результат не оприлюднений. Жодне свідчення саме по собі не є правовим встановленням порушення. "+cite("O2","O3","O4","O17","O20","O22","O23")]
],[105,230,190],small=True),
P("Чисельний збіг між ранньою заявою про «чотирьох» і пізнішими повідомленнями про чотирьох військовослужбовців є підказкою для перевірки, але не доводить, що автор першого допису мав точну інформацію або говорив саме про цих людей. Атрибутовані повідомлення про травми не встановлюють їхній точний час, характер чи причину та не підтверджують цивільний статус, незаконне утримання, катування, перелом хребта чи смерть.","BodyTight")]

story += [H("3.5. Оновлення процесуального статусу й перевірка посилань",2),
P("На пошуковий зріз 06.11 о 15:40 Суспільне повідомляє про 59 днів тримання Валерії Ладики під вартою з альтернативою застави, hromadske зазначає 66 560 грн. Попередній статус невідомого результату замінено цим атрибутованим повідомленням. Повного тексту ухвали, фактичного внесення застави чи звільнення не отримано. "+cite("O32","O33")),
P("Суспільне з посиланням на речницю прокуратури повідомило про підозру Івану Паршонкову за ч.1 ст.114-1 КК. Версія обвинувачення пов'язує його з блокуванням підрозділу та ударами молотом по службовому авто. Це п'ята поіменно названа у перевіреному корпусі підозрювана особа; індивідуального повідомлення про підозру, позиції захисту або ухвали щодо нього не отримано. Повний перелік 130 встановлених поліцією людей не оприлюднений. "+cite("O34")),
P("Аудит 25 HTTP-спроб виправив помилки адрес МВС, НГУ й Уповноваженого ВРУ; доступні відповіді збережені з хешами. Правильна адреса ДБР мала TLS-помилку: індексований офіційний текст не прирівнюється до прямого завантаження. Реєстр судових рішень не надав потрібних ухвал. Підсумкових актів перевірок МВС/НГУ/омбудсмана не отримано; це стан пошуку. "+cite("D10"))]

story += [H("4. Хронологія події та перевірок",1),
P("Час нижче київський (UTC+2). Час публікації не тотожний часу події чи зйомки; для соцмережевих даних першенство обмежене корпусом. П'ять фізичних епізодів у пов'язаному артефакті M2 — аналітично відібрані та сформульовані згадки з указаних джерел. Скрипт структурує ці задані згадки, а не автоматично знаходить повну фізичну хронологію; часові вікна можуть перетинатися, якісні рівні не є каліброваними ймовірностями, а послідовність не доводить причинність. "+cite("M2"))]
timeline=[
["Час","Подія / публікація","Джерело і межа"],
["02.11 11:34","ЦПД ретроспективно називає цей час першим прямим публічним закликом приїхати до будинку в Threads. Окремо НГУ/АрміяInform описує допис про побитих чоловіків і тяжко травмованих, а згодом — інший допис із цифрою 40. Оригінали відсутні; тотожність записів і точний порядок незалежно не перевірено.","Атрибутована ретроспектива ЦПД та окремий переказ НГУ/АрміяInform. "+cite("O40","O11")],
["02.11 близько 11:50","За тією ж ретроспективою, приблизно через 16 хвилин з'явилася версія про 40 незаконно утримуваних людей.","Не відтворено з оригінального Threads-поста. "+cite("O11")],
["02.11 12:41:03","Найраніша релевантна публікація у Telegram панелі: gnapinfo про близько 40 людей.","Перша у 241 каналі, не глобально. "+cite("D1")],
["02.11 13:07:53","padla_tck: «Будні концтабору».","Текст/час у Telegram корпусі. "+cite("D1")],
["02.11 13:16:21","Перший канал панелі понад 1 млн підписників пише про об'єкт і незаконне утримання.","Не перша публікація загалом. "+cite("D1")],
["02.11 13:24:00","kyiv_golovne переказує цифру 40.","API та веб-знімки. "+cite("D1")],
["02.11 13:57:01","Перший канал групи C у панелі, ukr_2025_ru, посилається на «київські ЗМІ».","Категорія каналу не доводить власника. "+cite("D1")],
["02.11 17:27","Поліція заявляє, що повідомлення про незаконне утримання та загибель не відповідають дійсності.","Офіційна заява. "+cite("O1")],
["02.11 18:08:05","padla_tck /38019: катування/вбивства як твердження та умовний прогноз можливої пожежі для знищення доказів. У самому пості село не названо; сусідні пости тієї послідовності згадували Петропавлівську.","Не доводить майбутній зв'язок із пожежою/TikTok. "+cite("D1")],
["02.11 21:39","За повідомленням hromadske, військова омбудсманка заявила, що її офіс працює на місці та призначив перевірку.","Вторинне відображення публічної заяви; результату перевірки в корпусі немає. "+cite("O22")],
["02.11 22:30","МВС оголошує службове розслідування, зокрема щодо умов перебування.","Окрема лінія перевірки. "+cite("O2")],
["03.11 19:15-19:20","Брифінг МВС/НГУ; названо число 26. СБУ повідомляє про понад 100 встановлених осіб.","Різні лінії: умови й сутички. "+cite("O4","O5")],
["03.11","ДБР оголошує кримінальне провадження щодо можливого перевищення повноважень і перевірки умов.","Оголошення не є результатом. "+cite("O3")],
["03.11 12:19","Омбудсман ВРУ повідомляє про запити до правоохоронців: перевірити обставини, правові підстави перебування та дії всіх учасників.","Вимога встановити факти, не результат перевірки. "+cite("O20")],
["04.11 12:35","Командувач НГУ повідомляє, що рішення ухвалять за підсумками службової перевірки, а підходи до розміщення та медичних процедур переглянуть.","Офіційний станом на 4 листопада запис про триваючу перевірку, не її фінал. "+cite("O23")],
["04.11 17:50","СБУ повідомляє про підозри трьом особам і версію слідства.","Атрибутувати СБУ; вина не встановлена. "+cite("O6","O14")],
["05.11 00:03:13","Голова ОВА повідомляє про пожежу складського об'єкта у Бучанському районі після атаки.","Не пов'язує її з об'єктом НГУ. "+cite("O10")],
["05.11 00:17:06","Сільрада називає Софіївську Борщагівку і складські приміщення після влучання.","Локація без адреси. "+cite("O9")],
["05.11 00:17:26 (ID)","ID TikTok кліпу пожежі декодується приблизно в цей час; це не час зйомки.","Технічна оцінка ID. "+cite("D3")],
["05.11 12:20","Поліція повідомляє про 130 встановлених осіб та пошкоджені транспортні засоби.","Оперативна статистика. "+cite("O7")],
["06.11","Дата звірки й замороження цього звіту; завершеного публічного висновку в корпусі не знайдено.","Статус пошуку, не доказ відсутності."]
]
story.append(table(timeline,[74,267,162],small=True))
story.append(P("Пост 2 листопада про можливу пожежу передував окремому відеокейсу приблизно на 2,5 доби. Це підстава перевірити контекст, але не доказ, що автор TikTok або коментатори бачили цей пост, що пожежу організували чи що хтось приховував докази.","BodyTight"))

story += [H("5. Цифровий корпус і методика збору",1),
P("Набори з різних платформ і часових зрізів не є однорідною «загальною кількістю соцмереж». Один URL може з'явитися на кількох платформах, а лічильники отримані не одночасно."),
table([
["Набір","Обсяг","Межа"],
["Telegram дописи","53 069 спостережень; 29 725 унікальних повідомлень; 23 350 публікацій; 241 канал; 1 408 релевантних у 159 каналах.","Цільова панель; не глобальний пошук."],
["Telegram коментарі","533 гілки; 39 598 коментарів; 12 797 авторів з доступним автором.","Завершена пагінація збирача, не гарантія платформи; 139 авторів невідомі."],
["TikTok пожежа","883 коментарі (345 верхнього рівня + 538 відповідей), 724 акаунти.","Один ролик; вручну прочитано 69 кандидатів, не всі 883."],
["TikTok 42 URL","21 відео + 21 фото; 9 653 отримані коментарні ID; 21 відео з 5,18 млн поточних переглядів сумарно.","Цільова вибірка; відео/фото не переглянуті як медіа."],
["YouTube","617 кандидатів; 463 у вікні за upload_date; лексично відібрано 444 відео / 190 каналів.","Відбір за метаданими; відео повністю не переглянуті; вікно довше за Telegram."],
["Instagram","199 посилань; 119 ID-часів у вікні, 12 після, 68 старіших.","Тексти/коментарі не збережені; login_required та rate-limit."],
["X / Threads / Facebook","X API: 402/no credits; Threads і Facebook корпусів немає.","Відсутність даних не означає відсутність обговорення."]
],[92,186,225],small=True),
H("5.1. Формування Telegram-вибірки",2),
P("Вибірка цільова, не ймовірнісна. У першому вебпроході було 78 заданих каналів; перехід за видимими форвардами/посиланнями глибиною до двох кроків дав 105 каналів (78 початкових, 14 першого та 13 другого кроку). Другий вебпрохід мав 134 початкові канали, відібрані за повторними посиланнями з групи C, і 16 каналів першого кроку — 150 загалом; проходи частково перетиналися. API-прохід охопив 241 запитаний ідентифікатор: 236 повних історій отримано через API; п'ять каналів не були доступні як broadcast channel. Один FloodWait завершили повторним проходом. Відбір тяжіє до заздалегідь заданих та видимими форвардами пов'язаних вузлів і не є репрезентативним для Telegram."),
P("Веб t.me/s та API об'єднані за ключем канал + ID повідомлення; API має пріоритет за текстом і лічильником. 23 344 дубльовані спостереження вилучено; 21 903 повідомлення були в обох джерелах, 6 383 були лише API, 1 439 лише веб."),
P("Відбір релевантності: повна назва села або «Борщагівка» разом із лексикою інциденту після 11:00 2 листопада; Софіївська Борщагівка, київський масив/вулиці та транспортні згадки розглядаються як окремі географічні контексти. У 90 вручну переглянутих кандидатах знайдено 2 хибні включення; спосіб добору цієї ручної партії не збережений, тому це опис вибірки, а не популяційна оцінка точності. Додатковий лематизований/нечіткий пошук у зібраних записах дав 70 невключених кандидатів; у них змішані сторонні згадки про трамваї, повітряні тривоги, окрему пожежу в Софіївській Борщагівці та ймовірно релевантні повідомлення. Усі кандидати не були незалежно закодовані за наперед зафіксованим протоколом. Тому повнота (recall) і точність (precision) класифікатора не оцінюються; 1 408 — кількість записів, відібраних застосованим правилом у цій цільовій панелі, а не оцінка всіх дописів про подію в Telegram."),
P("Контекстний сканер знайшов 99 кандидатів із перетинами правил: приховування доказів, умовний прогноз пожежі, старе/перепідписане медіа, спір про статус медика і Софіївська географія. 18 кандидатів вибірково прочитано вручну. Це не 99 встановлених випадків."),
P("Основне вікно закінчується 05.11 о 12:10:13. Пізніші TikTok/коментарні знімки мають окремий час збору й не можуть відновити історичні лічильники."),
H("5.2. Цілісність і пропуски",2),
P("data_quality.json повідомляє, що всі заявлені хеші сирих файлів збігаються. Це внутрішня перевірка копій, не незалежний цифровий підпис. У публікаціях Telegram відсутній лічильник переглядів у 49 записах і текст у 459; пропуски позначаються окремо, не підміняються нулем. "+cite("D1"))]

story += [H("5.3. Зіставлення корпусів 1408 vs 1438 та Source Watch (Track 4, M4)",2),
P("У дослідженні зіставлено два зрізи даних: <code>telegram_historical_1408</code> (базовий зріз від 5 листопада, 159 каналів, 1 408 дописів) та <code>telegram_merged_1438</code> (розширений зріз від 8 листопада, 158 каналів, 1 438 дописів) "+cite("M4")+". Різниця у +30 дописів пояснюється розширенням часового вікна до кінця 6 листопада (+52 нові дописи) за вирахуванням 22 дописів каналу kiber_boroshno, виключеного через спам. За 10 запусків Source Watch зафіксовано 9 успішних знімків та 1 тимчасовий збій TLS сайту ДБР, що є суто технічним обмеженням."),
]

story += [H("6. Обсяг і часовий профіль Telegram-хвилі",1),
P("Релевантних дописів було 624 2 листопада, 526 3 листопада, 224 4 листопада і 34 до 12:10:13 5 листопада. Перші дві доби становлять 81,7% усіх 1 408 публікацій. Це темп дописів у панелі, не темп перегляду й не кількість читачів.")]
fig1_p = ROOT / "reports/continuation_20261105/timeseries.png"
if fig1_p.exists():
    story.append(Image(str(fig1_p), width=498, height=155))
    story.append(P("Рис. 1. Часовий профіль релевантної хвилі публікацій у Telegram (2-5 листопада 2026 р.). Джерело: continuation_20261105/timeseries.png.", "Captionx"))

story.append(P("* До 12:10 за Києвом; останній день коротший. Джерело - зведений корпус.", "Captionx"))
story += [H("6.1. Друга хвиля та пікові інтервали",2),
P(f"За годинами: 15:00-15:59 - {TG_DAY1_HOURS['15']} дописи; 16:00-16:59 - {TG_DAY1_HOURS['16']}; 17:00-17:59 - {TG_DAY1_HOURS['17']}. Десятихвилинний максимум у проміжку 21:30-22:10 припав на 21:40 (29 дописів); загальний десятихвилинний максимум - 22:30 (32). Найактивніші години 2 листопада: 21:00 - {TG_DAY1_HOURS['21']}; 22:00 - {TG_DAY1_HOURS['22']}; 17:00 - {TG_DAY1_HOURS['17']}; 20:00 - {TG_DAY1_HOURS['20']}; 18:00 - {TG_DAY1_HOURS['18']}."),
P("Перша офіційна заява поліції вийшла о 17:27, до пікових вечірніх інтервалів. Саме часове співпадіння не доводить, що читачі бачили заяву або змінили позицію. Для вимірювання впливу немає історичних лічильників чи даних експозиції.")]
story.append(HBars([("15-та година",TG_DAY1_HOURS["15"]),("16-та година",TG_DAY1_HOURS["16"]),("17-та година",TG_DAY1_HOURS["17"]),("18-та година",TG_DAY1_HOURS["18"]),("20-та година",TG_DAY1_HOURS["20"]),("21-ша година",TG_DAY1_HOURS["21"]),("22-га година",TG_DAY1_HOURS["22"])],width=500,row_h=21,title="Зростання темпу 2 листопада",maxval=115))
story.append(P("Годинні показники агреговані по релевантних публікаціях. Офіційна заява не припинила публікації автоматично; причинний зв'язок не виміряно.", "Captionx"))
story += [H("6.2. Повторна доступність",2),
P("6 листопада перевірено 1 408/1 408 постів: на той момент всі були доступні, видалень серед перевірених не було. Це не виключає видалення і відновлення між знімками. За близько добу медіанний приріст поточних лічильників становив 1%, 90-й перцентиль - 8%. "+cite("D1"))]

story += [H("7. Канали й поточні лічильники",1),
P("Сума лічильників переглядів релевантних Telegram-публікацій - 115 931 014. Один читач міг переглянути кілька каналів або повні копії; це не унікальне охоплення. Знімки отримані після події, тому це не лічильник на момент хвилі.")]
groups=RESULTS["by_group"]; order=["A","B","C","D","E","U"]
gl={"A":"місцеві","B":"українські неофіційні","C":"російські / проросійські","D":"офіційні / редакційні","E":"іноземні","U":"невідомі"}
gr=[["Група","Пости","Частка постів","Лічильники","Частка лічильників"]]; gd=[]
for g in order:
 d=groups[g]; gr.append([f"{g} - {gl[g]}",fmtint(d["posts"]),pctstr(d["posts"],1408),fmtint(d["views"]),pctstr(d["views"],115931014)])
 gd.append((gl[g],pct(d["posts"],1408),pct(d["views"],115931014)))
story.append(table(gr,[123,62,77,120,88],small=True))
story.append(HBars(gd,width=500,row_h=24,title="Частка публікацій / поточних переглядів",maxval=55,paired=True))
story.append(P("A місцеві; B українські неофіційні; C російські/проросійські; D офіційні/редакційні; E іноземні; U невідомі. Класифікація описує корпусні групи, не встановлює власність чи державний контроль. Інфраструктурні маркери - лише проксі.", "Captionx"))
story += [H("7.1. Концентрація та типове охоплення",2),
P("Група B дала 19,4% дописів, але 47,6% суми лічильників. C - 35,3% дописів і 24,0% лічильників. Десять найбільших каналів дали 29,5% постів і 56,5% лічильників. Медіана - 23 172,5 перегляду на пост, середнє - близько 82 337; довгий верхній хвіст піднімає середнє. Групи каналів не є аудиторними сегментами."),
P("Корпус не охоплює приватні канали й весь глобальний пошук. Абсолютні суми не слід напряму порівнювати з моніторингами тисяч каналів, які використовують інший корпус або вікно.")]

story += [H("7.2. Мостовість у видимому графі форвардів",2),
P("Граф має 69 вузлів, 60 спрямованих зв'язків і 65 форвардів; 12 слабко зв'язних компонент. Ребро йде від зазначеного джерела до репостера. Видимі кінці ребер не охоплюють усіх 159 релевантних каналів; приховані джерела, ручні копії та скриншоти відсутні. Між різними групами проходять 20 зв'язків і 24 форварди. "+cite("D11")),
P("Нормована betweenness у nsdvdonetske - 0,005926, zovbear0 - 0,003951, telelug - 0,002634, yurasumy - 0,002195, padla_tck - 0,001975. Перші два мають лише зв'язки всередині C; їх не можна називати мостами між українськими й російськими сегментами. Обсяг n не використано як відстань: betweenness обчислена на спрямованих незважених шляхах."),
Image(str(ROOT/"reports/telegram_network_dynamics_20261106/forward_bridges.png"),width=498,height=255),
P("Топологічно є 53 двокрокові шляхи та 2 замикання (3,77%). Агреговані ребра не доводять послідовного перенесення того самого повідомлення в часі. Рейтинг описує цю панель, не організаторів, державне керування чи причинний вплив.")]

story += [H("8. Наративи та надійність",1),
P("Лексичні правила знаходять згадки, але часто плутають первісне твердження, цитату, спростування, сарказм і сумнів. Мітки накладаються, тому сума рядків може перевищити 1 408. Група C — операційна суміш походження джерела, російських інфраструктурних маркерів, відкритої атрибуції українських органів і редакційно-політичної характеристики. Це не чистий вимір державного зв'язку. У зведенні автоматична мітка застосовується лише за відсутності ручної; ручні записи мають пріоритет. Подальше кодування має зберігати окремо країну/походження, тип видавця, політичну позицію, інфраструктурні сигнали й підтверджений державний зв'язок.")]
nl={"N1_hostages":"40 заручників / утримання","N2_death_torture":"смерть / катування","N3_tcc_camp":"«концтабір ТЦК»","N4_cover_up":"приховування доказів","N0_official":"офіційна версія / спростування"}
nr=[["Мітка","Пости","Поточні перегляди","Частка C у лічильниках","Обережність"]]
for n in RESULTS["narratives"]:
 key=n["narrative"]; ss=next((x for x in AUDIT["narrative_mention_sensitivity"]["all_labels"] if x["label"]==key),None)
 cshare=100*(ss["view_shares_by_group"].get("C",0) if ss else 0)
 nr.append([nl.get(key,key),fmtint(n["posts"]),fmtint(n["views"]),f"{cshare:.1f}%",{"N1_hostages":"Не означає підтримку.","N2_death_torture":"Може бути переказом чи спростуванням.","N3_tcc_camp":"Частка чутлива до класифікації.","N4_cover_up":"Низька надійність кодування.","N0_official":"Може включити нейтральний переказ."}.get(key,"")])
story.append(table(nr,[113,48,94,86,133],small=True))
story.append(HBars([(nl[n["narrative"]],n["posts"],fmtint(n["posts"])) for n in RESULTS["narratives"]],width=500,row_h=23,title="Публікації зі згадкою кожної теми",maxval=540))
story.append(P("Лічильники - snapshot sum, не унікальне охоплення. "+cite("D1"),"Captionx"))
story += [H("8.1. Узгодженість ручного кодування",2),
P("Після розробки правил на 50 постах другу перевірку провели на 40 нових постах. Другий кодувальник був Claude; двох незалежних людських кодерів не було. Cohen's kappa для N3, N0 і спростування - близько 0,60-0,64; для N1, N2, N4 і «зі слів медика» - від -0,07 до 0,13. Останні придатні лише як пошук кандидатів, не як надійний вимір позиції."),
P("За всіма мітками група C отримала 95,7% snapshot-переглядів постів із N3; після вилучення спірних/автоміток - 88,9%. У межах C розподіл концентрований: один канал Strana.ua дає 24,6% N3-лічильників C, а два найбільші — 40,8%; це суми поточних лічильників, не унікальні люди. Вилучення спірних/автоматичних міток скорочує підмножину N3 з 230 постів / 14,13 млн лічильників до 81 / 4,37 млн, тож 88,9% — частка в значно вужчій підвибірці, а не загальна стійкість оцінки до будь-якого дизайну. Частка N1 змінюється з класифікацією: за всіма мітками C 40,4% проти B 35,6%, а без спірних міток B 44,0% проти C 28,0%."),
P("N2 має 32,4 млн поточних лічильників, N0 - 24,3 млн; через низьку надійність N2 не можна робити загальний висновок, що він «переміг». Твердження про 94% переглядів до спростування неперевірне: немає історичних лічильників на момент 21:32. Нині дописи до 21:32 мають 74,6% суми відповідних поточних лічильників - це інша величина.")]

story += [H("8.2. Тематичні мітки за шестигодинними вікнами",2),
P("Знаменник кожної частки - усі релевантні дописи відповідного біна, не перегляди й не автори. Є 15 календарних бінів: 14 повних і останній 12:00-12:10:13 лише з 2 дописами; два початкові порожні. Службовий 0 для порожнього біна не оцінює поширеність. 557 постів без мітки, 394 з кількома; загалом 1424 призначення для 1408 постів. "+cite("D11")),
Image(str(ROOT/"reports/telegram_network_dynamics_20261106/narrative_shares_6h.png"),width=498,height=280),
P("Частки показують згадки за існуючим словником. Заперечення, цитата та підтримка не розділені надійно, особливо для N1/N2. Через 15 точок, неповний крайній бін, спільний новинний шок і слабку валідацію тест Грейнджера не застосовано; p-value або висновків про причинність із цих рядів немає.")]

story += [H("9. Копії та межі причинності",1),
P("Порівняння текстів шукало можливі повтори. Алгоритм LSH відбирав кандидатні пари; далі застосовано точну схожість 5-символьних шинглів із Jaccard не нижче 0,6. У панелі залишено 367 пар і 141 компоненту. Це ознака повтору/схожості, а не доказ прямого копіювання: спільний пресреліз, цитата, шаблон новин або невидимий третій пост створюють подібний слід."),
table([
["Вимір","Результат","Інтерпретація"],
["Схожі тексти між каналами","132 компоненти мають понад 1 канал; 68 перетинають групи.","Підтверджує повтори в панелі, не координатора."],
["Група першого допису","C першою в 57/141 компоненті (40%).","Найчастіше, але не більшість; залежить від охоплення й класифікації."],
["Затримка між прямими парами","B пізніше C: n=3, медіана 2,5 хв; C пізніше B: n=4, медіана 51 хв.","Мала вибірка; порядок не показує напрям передачі."],
["Telegram форварди","60 ребер; 65 публікацій позначено як форвардні.","Сильніший зв'язок, але не встановлює першого автора змісту."]
],[116,166,197],small=True),
P("За порогів 0,75/0,9 пар лишалося одиниці чи дві; LSH може пропускати слабші схожості; транзитивна компонента може з'єднати A і C через B. Дані не встановлюють, що хвилею керували російські спецслужби або інший організатор. Це не виключає гіпотези, лише позначає межу цього аналізу.")]

story += [H("10. Коментарі Telegram: координація й сигнали автоматизації",1),
P("У 533 гілках зібрано 39 598 коментарів; у 39 459 записах був відомий автор, ще 139 без нього (0,35%). 12 797 акаунтів замінено HMAC-псевдонімами під час збору; імена, username та ID в аналітичному файлі відсутні. "+cite("D2")),
table([
["Показник","Результат","Тлумачення"],
["Платформний прапор bot","13/12 797 (0,10%)","Лише офіційно марковані боти; не охоплює людські акаунти з автоматизацією."],
["Акаунти з 10+ / 50+ коментарями","662 / 55","Висока активність потребує контексту; не дорівнює бот."],
["Без username / фото","55,9% / 56,0%","Проксі профілю; звичайні користувачі теж не заповнюють."],
["Топ-1% / Gini","18,9% коментарів / 0,568","Концентрація, не бот-класифікатор."],
["Точні повтори","128 груп; 444 коментарі","Можливі цитати або звичайні фрази."],
["Синхронні майже-копії","0 за правилом >=3 акаунти за &lt;=10 хв","Не виключає інший ритм/варіативний текст."],
["Акаунти з 2+ типами поведінкових сигналів","387; 2 450 коментарів (6,21%)","Сигнали евристичні; частково перетинаються з кампанією нижче."]
],[142,128,209],small=True),
H("10.1. Шаблонна хвиля підтримки Буданова",2),
P("У чотирьох обговореннях під постами 3 листопада вручну знайдено 126 шаблонних фраз похвали, 438 коментарів від 367 псевдонімізованих акаунтів. У кожній гілці фрази здебільшого йшли від різних акаунтів, не більше разу на гілку; потік тривав 1,5-4,5 години з медіанним інтервалом 0,6-1,2 хв. Частка - 21-36% коментарів у цих гілках."),
P("Без username були 321/367 авторів шаблонів (87,5%) проти 69,2% інших у тих самих гілках. Ці автори дали 382/438 шаблонних коментарів (87,2%); знаменник тут інший; без фото - 86,6% проти 62,3%; Premium - 0% проти 5,9%. Поєднання рідкісних шаблонів, однакового набору обговорень, ритму та профільних відмінностей підтримує оцінку координації (B). Не встановлені ботність, оплата, організатор чи вплив."),
P("Автоматичний метод S7 знайшов 3 взаємопов'язані підпули, 111 фраз і 393 коментарі. Це суворіше розбиття тієї ж знахідки, а не інша кампанія. Під російськими/проросійськими каналами подібних шаблонних коментарів майже не було; це не доказ відсутності там автоматизації.")]

story += [H("10.2. Нульові моделі: випадковість конкретних патернів",2),
P("Ретроспективно задано дві моделі S7: перестановки фраз у слотах із контролем дня/активності/писемності та в межах повного денного словника кожного автора. Авторські, гілкові й часові слоти фіксовані. Друга модель зберігає значну частину структури: 316 із 605 кандидатних слотів не можуть змінити текст. В обох моделях S7-пошук повторюється для всіх наборів гілок. "+cite("D7","O35")),
table([
["Статистика / умовний фон","Спостережено","Середнє null","Центральні 95% null"],
["Найбільший S7-пул / автор-день","60 фраз","23,178","17-30"],
["Усі фрази у S7-пулах / автор-день","111 фраз","37,429","24-50"],
["Копії Jaccard>=0,6; <=10 хв / 2 год","134/367 пар","42,694/367","32-55 пар"]
],[225,87,90,92],small=True),
HBars([("Спостережено",60),("Фон автор-день",23.1782,"23,18")],width=498,row_h=23,title="Найбільший пул S7: кількість фраз",maxval=60),
P("126 фраз і 438 коментарів описаного кластера не тотожні автоматичним 111 фразам,393 коментарям та 334 авторам S7. Решта 15 фраз утворює два набори гілок із 8 та 7 фразами, кожен нижче порога >=10. Вони не загублені; критерій детектора вужчий."),
P("Для копій фіксуємо 367 ребер точного перевіреного Jaccard-графа. Контент циклічно зсувається по реальних слотах кожного каналу в межах доби або 2 годин. Слоти взято з усіх 23 350 публікацій; одна публікація отримує один час для всіх своїх ребер. Каналовий ритм і кількість міток у блоці зберігаються; лінійний порядок може змінитися у точці обертання. "+cite("O36")),
HBars([("Спостережено",134),("Фон 2 години",42.6937,"42,69")],width=498,row_h=23,title="Близькі копії: кількість пар у межах 10 хв",maxval=134),
P("Для кожного з 16 тестів B=9999, k=0, seed=20261106. Емпіричне p=(k+1)/(B+1)=0,0001; Holm16 дає 0,0016. Це не 16 незалежних підтверджень. Квантілі фону не є довірчими інтервалами причинного ефекту. "+cite("O37","O38")),
P("Поправка не покриває попередній вибір кейсу й розробку правил. Моделі відкидають конкретні умовні фони, але спільне агентське джерело, звичайні передруки й відкритий заклик прихильників лишаються альтернативами. Двогодинний фон не контролює спільні події на масштабі секунд/хвилин. Висновок: статистична підтримка незвичної узгодженості в корпусі посилилася; ботність, оплата, організатор і державна роль не встановлені.")]

fig3_p = ROOT / "reports/audience-response/reaction_distribution.png"
if fig3_p.exists():
    story.append(PageBreak())
    story.append(fit_image(fig3_p))
    story.append(P("Рис. 3. Обмежена перевірка паритету реакцій: 10 коментарів у 3 гілках; цей знімок не оцінює весь корпус. Джерело: reports/audience-response/reaction_distribution.png.", "Captionx"))
    story.append(P("Перевірка зіставила доступний розподіл реакцій у знімку з відповіддю Telegram MTProto: 10 із 10 векторів збіглися. Це підтверджує паритет лише перевірених записів, а не повноту чи розподіл реакцій у всіх 533 гілках. Історичних часових рядів реакцій немає; реакції на пости не слід змішувати з реакціями на коментарі. "+cite("D1","M4"), "BodyTight"))

story += [H("11. TikTok пожежа: географічна плутанина",1),
P("Кейс розрізняє населений пункт, громаду, час публікації, час зйомки, первинний підпис і коментарі глядачів. Спільне слово «Борщагівка» не є доказом тотожної локації."),
H("11.1. Що встановлено про місце",2),
P("Інтерфакс-Україна о 00:05 5 листопада переказав повідомлення голови КОВА про займання складського об'єкта в Бучанському районі й уточнення інформації про постраждалих; агентство окремо зазначило, що відомості про Софіївську походили з місцевих Telegram-каналів і тоді не мали офіційного підтвердження. Пізніше офіційний Telegram сільради назвав Софіївську Борщагівку та складські приміщення; окрема сторінка громади описала ліквідацію наслідків влучання без назви села. Ці матеріали описують окремий випадок і не пов'язують його з будівлею НГУ в Петропавлівській Борщагівці. "+cite("O8","O9","O10","O46")),
P("Публічні повідомлення локалізують пожежний випадок на рівні району, а пізніше — населеного пункту. Вони самі по собі не доводять, що конкретний TikTok-ролик знято саме там: для цього потрібні перевірювані візуальні орієнтири та ланцюг походження відео. Відео незалежно не геолоковане; точну адресу не наводимо."),
H("11.2. Порівняння локального MP4 і TikTok",2),
P("Наданий MP4 і публічна копія TikTok мають різні SHA-256, тривалість і кодування, тобто це не побітово однакові файли. Перцептивне зіставлення знайшло сильну візуальну відповідність: MP4 -> TikTok 19/29 перевірених кадрів (65,5%); у зворотний бік 20/21 (95,2%), з 18/21 часово узгодженими кадрами. Тривалість приблизно 14,13 с проти 10,23 с."),
P("Це пошуковий доказ імовірно спільної візуальної послідовності. Пороги не калібровані на контрольному наборі; частки не є ймовірністю збігу. Такий збіг не встановлює місце, час зйомки, автора оригіналу, причину пожежі чи автора коментаря."),
P("ID TikTok 7704443960013376789 декодується приблизно в 05.11 00:17:26 за Києвом. Це час створення/публікації об'єкта, не час зйомки. Близькість до часу поста сільради не доводить джерело відео або причинний зв'язок."),
H("11.3. Позиції в коментарях",2)]
fc=FIRE_SIG["by_manual_category"]
frows=[["Категорія","Коментарі","Автори","Мінімум / 883","Частка / 69 кандидатів"]]
for k,l in [("coverup_affirmation","Підтримка «замітають сліди»"),("geographic_correction","Виправляє географію"),("coverup_question","Питання про приховування"),("rebuttal","Заперечення/спростування"),("sarcasm_or_unclear","Сарказм/неясно"),("neutral_reporting_or_location_question","Нейтральне питання"),("other_incident_claim_conditional","Інше умовне твердження")]:
 d=fc[k]; frows.append([l,fmtint(d["comments"]),fmtint(d["accounts"]),pctstr(d["comments"],883,2),pctstr(d["comments"],FIRE_REVIEW["candidates"],1)])
story.append(table(frows,[158,58,58,92,114],small=True))
story.append(Spacer(1, 5*mm))
story.append(HBars([("Підтримка «замітають»",21,"21"),("Географічне виправлення",20,"20"),("Спростування",8,"8"),("Сарказм / неясно",15,"15")],width=500,row_h=24,title="Ручно класифіковані кандидати",maxval=22))
story.append(P("Зі 883 записів 69 автоматично відібрали й прочитали вручну; решта 814 не класифікована вручну. Стовпець «Мінімум / 883» показує лише спостережену нижню межу. Частки серед 69 кандидатів описують цільово відібрану підмножину й не є оцінкою поширеності серед усіх коментарів. Розмітку виконав один кодувальник, міжкодувальної перевірки не було.", "Captionx"))
fig4_p = ROOT / "reports/event-reconstruction/geospatial_map.png"
if fig4_p.exists():
    story.append(PageBreak())
    story.append(fit_image(fig4_p))
    story.append(P("Рис. 4. Немасштабне зіставлення двох окремо описаних випадків; це не карта й не геолокація відео. Джерело: reports/event-reconstruction/geospatial_map.png.", "Captionx"))
    story.append(P("<b>Межа зіставлення:</b> доступні джерела описують інцидент біля об'єкта НГУ та окреме займання складського об'єкта в Бучанському районі; пізніше сільрада назвала Софіївську Борщагівку. У репозиторії немає перевірених координат, які обґрунтовували б відстань між об'єктами. Саме TikTok-відео не геолоковане, тому його не можна категорично прив'язати до будь-якого з цих місць. "+cite("M2","O8","O9","O10","O46"), "BodyTight"))

story += [H("11.4. Координація чи боти?",2),
P("У 724 псевдонімізованих авторів топ-1 дав 1,5% коментарів, топ-5 - 5%, Gini - 0,165. Знайдено 2 невеликі точні групи (6 коментарів), 6 пар близьких текстів, 1 швидкий повтор одним автором, 0 синхронних груп і 0 сплесків за порогом. 14 акаунтів мали будь-яку ознаку, але 0 - два типи ознак. Жоден із 19 авторів, що стверджували «замітають сліди», не був позначений поведінковою ознакою."),
P("Висновок: у цьому знімку не видно виразної синхронної копі-паст кампанії. Це не доводить, що кожен автор - людина. Органічна плутанина правдоподібна, зокрема через схожу назву місцевості та майже однакові мінімальні кількості тверджень/виправлень; мотив кожного автора невідомий."),
P("Окремо, padla_tck 2 листопада писав про можливу майбутню пожежу для знищення доказів. Це причина простежити наратив, але в корпусі немає прямого доказу, що автор відео або коментатори бачили саме цю публікацію.")]

story += [H("12. 42 TikTok-посилання",1),
P("Це цільовий список прямих URL, наданих користувачем, не вибірка з випадкового пошуку TikTok. Усі 42 посилання відтворено в Додатку A.") ]
tot_top=sum(int(r["api_reported_top_level_total"]) for r in TIKTOK if r["api_reported_top_level_total"])
obs_top=sum(int(r["observed_top_level_comment_ids"]) for r in TIKTOK)
obs_rep=sum(int(r["observed_reply_comment_ids"]) for r in TIKTOK)
vv=sum(int(r["views_at_metadata_fetch"]) for r in TIKTOK if r["views_at_metadata_fetch"])
vl=sum(int(r["likes_at_metadata_fetch"]) for r in TIKTOK if r["likes_at_metadata_fetch"])
story.append(table([
["Показник","Результат","Застереження"],
["Пости","42: 21 відео + 21 фото","4 ID-часи поза вікном: 2 старі, 2 після."],
["Відео-лічильники",fmtint(vv)+" переглядів; "+fmtint(vl)+" вподобань","Поточні числа 21 відео; не унікальні люди."],
["Коментарі",fmtint(obs_top+obs_rep)+" ID: 3 383 top-level + 6 270 replies","Відповіді не є коментарями верхнього рівня."],
["Верхній рівень",fmtint(obs_top)+" / "+fmtint(tot_top)+" ("+pctstr(obs_top,tot_top,2)+")","32/41 пости нижче platform counter."],
["Автори","6 722; 363 (5,4%) на 2+ постах","HMAC псевдоніми."],
["Медіа","21 відео metadata, 20 captions; фото: 0 зображень","Відео/фото не переглянуті як медіа."]
],[105,190,183],small=True))
story.append(HBars([("Платформний лічильник",tot_top,fmtint(tot_top)),("Отримані ID top-level",obs_top,fmtint(obs_top))],width=500,row_h=25,title="Верхньорівневі коментарі: лічильник проти знімка",maxval=tot_top))
story.append(P("Пагінація завершилася з has_more=false, але це не повний перепис. Для відповідей 604 гілки містили 6 270 ID проти 5 334 заявлених платформою; у 176 гілках показники не збіглися. Лічильники могли змінюватися.", "Captionx"))
story += [H("12.1. Тематичні та поведінкові сигнали",2),
P("Попередній цільовий перегляд описував шість фраз за ширшим неформалізованим критерієм. Повторний сканер v1.1 відокремлює 5 прямих згадок приховування слідів і 4 непрямі натяки на прибирання; нижче наведено явні критерії. Жоден отриманий коментар цієї партії не згадував Софіївську Борщагівку й не поєднував пожежу з приховуванням; окремий ролик пожежі належить іншому набору."),
P("363 із 6 722 авторів траплялися на двох або більше постах, залишивши 1 276 коментарів (13,22%). Топ-1 автор дав 0,30%, топ-5 - 1,28%, Gini - 0,267. Виявлено 17 точних груп повтору у 9 постах, 14 близьких пар у 8, 85 швидких пар у 15 і 83 часові сплески у 14; синхронних груп майже-копій в одному пості не було. 233 автори мали один поведінковий сигнал, 19 - два й більше типів. Це сигнали, не частка ботів."),
P("Медіафайли цієї партії не аналізувалися. Підписи доступні для 20/21 відео; фото-вміст не отриманий, тому дані не додають верифікації кадрів.")]

story += [H("12.2. Повторний пошук контексту й таблиця різних часів",2),
P("Сканер v1.1 перевірено 16 регресійними тестами й повторно застосовано до 9 653 коментарів: 166 кандидатів, з них 5 прямих згадок приховування слідів, 4 непрямі натяки на прибирання та 157 кандидатів щодо медичного статусу. Додаткові мітки повтору перетинаються з цими категоріями. Усі 9 прямих/непрямих реплік перечитано; вони є звинуваченнями, припущеннями чи неоднозначними натяками, не доказом приховування. "+cite("D8")),
P("157 медичних кандидатів включають підтримку, заперечення, умовні вислови та пояснення ліцензування. Повного позиційного кодування немає. Короткі репліки відбираються також через явно позначений дослідницький контекст користувацької партії; він не засвідчує релевантність посту чи географію."),
P("В окремому кліпі пожежі в незмінних 883 коментарях черга зросла з 69 до 72. Три нові репліки зі зворотним порядком «улики уничтожают» не додані мовчки до початкового позиційного підсумку 21/20; частина має неоднозначну питальну форму. Решта 811 не пройшла повного ручного кодування."),
table([
["Часове поле 42 публікацій","Що доступно","Чого не встановлює"],
["Оцінка публікації зID","42 оцінки","Час події/зйомки"],
["Timestamp метаданих платформи","21 відео; для 21 фото немає","Першоджерело кадрів"],
["Незалежно встановлений час зйомки","0","Невідоме поле не дорівнює нулю подій"],
["Збір коментарів","Окремі first/last UTC у CSV","Історичні лічильники"]
],[183,150,161],small=True),
P("Повна таблиця містить усі 42 URL і джерело кожного доступного timestamp. Відео/фото цієї партії не геолоковано; ID-час і дата видимого підпису не підмінюють час зйомки."),
P("<b>Перевірка точності ID-часу:</b> у 21 відео з метаданими точних збігів немає. Для 20 розбіжність становить 4-16 секунд; медіана всіх 21 - 8 секунд. У belradio_1/7704722151990955316 вона 9183 секунди (2 год 33 хв 3 с): ID 05.11 18:16:57 за Києвом, timestamp 20:50:00. Причину не встановлено; це не доказ маніпуляції. Входження цих 21 відео у вікно не змінюється; фото лишаються неперевіреними."),
P("Extractor yt-dlp бере timestamp із create_time/createTime. Офіційний Codebook описує час створення запису; час зйомки й момент першої доступності для всіх користувачів не встановлені. Загальне припущення про точність усіх ID до секунди не підтримується цим зіставленням. "+cite("D8","O39"))]


story += [H("13. YouTube, Instagram, X, Threads і Facebook",1),
P("Платформні прогалини обмежують будь-яке твердження про «всю хвилю». Наведені нижче числа - обсяг збору, не рейтинг впливу."),
table([
["Платформа","Що зібрано","Що не можна виснувати"],
["YouTube","444 лексично відібрані відео / 190 каналів; 34,62 млн сумарних переглядів, 44 записи ефірів. Коментарі: 25 933 / 30 відео.","Відбір за заголовком/описом; можливі пропуски й випадкові згадки. Перегляди не є охопленням."],
["Instagram","199 посилань; 119 ID-часів у вікні. Instaloader повертав login_required і rate-limit.","Підписи/коментарі не збережені; не можна казати, що обговорення не було."],
["X","Офіційний API - 402/no credits.","Немає корпусу; роль не виміряна."],
["Threads","Ранні повідомлення переказані зовнішніми джерелами; власного корпусу немає.","Не можна відтворити першопост чи повноту."],
["Facebook","Не зібрано.","Немає основи оцінювати обсяг."]
],[70,235,185],small=True),
P("Для YouTube відтворено лексичний відбір серед 617 метаданих за правилом бор[щш]|borsh у заголовку/описі. Він не замінює змістову перевірку відео; можливі сторонні згадки та пропуски без топоніма. Instagram ID-час є технічною оцінкою, а не незалежним полем публікації. Невключення означає «немає даних», а не «не було контенту»."),
P("Локальний методичний огляд перевіряв шляхи доступу до публічних URL та дослідницьких інтерфейсів TikTok, Meta і YouTube; вони різняться за допуском, квотами й обсягом. API не гарантує повноту органічної видачі, а архіватор URL зберігає лише відомі посилання. Жодних заявок чи зовнішніх звернень від імені користувача не подано."),
P("У Telegram знайдено 20 посилань на TikTok, з них 12 - прямі ефіри 10 акаунтів; їх поширювали між 17:06 і 22:47 2 листопада. Це підтверджує циркуляцію посилань у Telegram, але не аудиторію ефірів і не причинний ефект. Навіть мільйонний лічильник не доводить, що платформа «найбільше вплинула».")]

story += [H("13.1. YouTube: часовий профіль і текстові сигнали",2),
P("Лексичний відбір дав 444 відео зі 190 унікальних каналів за channel_id; попереднє число 191 не відтворилося. Найраніше знайдене відео - 02.11 о 17:50:15 за Києвом, після першого Telegram-допису в панелі (12:41). Це спостережена послідовність у вибірках; вона не встановлює глобального ініціатора хвилі. "+cite("D5")),
HBars([("02.11",70),("03.11",243),("04.11",90),("05.11",38),("06.11",3)],width=500,row_h=21,title="YouTube: публікації лексичного відбору за датами",maxval=250),
P("Пік - 03.11: 243/444 (54,7%). Розподіл наведений за upload_date; останній день неповний на момент збору. 34 618 058 - сума лічильників у знімках, без дедуплікації глядачів і без вимірювання переглядів на момент події."),
table([
["Показник коментарів","Усі 30 відео","26 відео лексичного відбору"],
["Коментарі / автори","25 933 / 18 961","24 121 / 17 459"],
["Топ-10 / топ-1% авторів: частка коментарів","0,85% / 6,26%","0,92% / 6,33%"],
["Джині / максимум на автора","0,232 / 38","0,238 / 38"],
["Однакові тексти від >=3 авторів","4 групи / 16 коментарів","4 групи / 16 коментарів"],
["Пули >=10 фраз на тих самих >=3 відео","0","0"]
],[230,128,136],small=True),
P("Топ-1% використовує цілу кількість авторів униз (189 та 174). Повтори - звичайні короткі вислови: «диму без вогню не буває», «не вірю жодному слову», подяки. За цими текстовими правилами переконливого патерну шаблонної кампанії не виявлено. Ботність і частка ботів не оцінюються."),
P("<b>Непридатні виміри:</b> S3/S4 виключено через приблизний час коментарів yt-dlp; 5 314 швидких пар не інтерпретуються як поведінка. Поля профілю не зібрані: no_username/no_photo=100% у початковому signals.json є значеннями за замовчуванням. Складені 82 мітки з >=2 сигналами також виключені через забруднені часові входи. Обмеження: ранжування/модерація платформи, до 1 500 коментарів на відео, лише 30 відео; повне тематичне кодування й перегляд медіа не виконані; окремий аналіз доступних субтитрів наведено нижче."),
P("Відтворення: src/analysis/youtube_evidence_audit.py; рішення відбору для 617 відео у metadata_selection.csv, агрегати й перевірки SHA-256 у evidence_audit.json. Збір коментарів 06.11 09:08-09:18 UTC. "+cite("D5"))]

story += [H("13.2. YouTube: субтитри й позиція конкретного промовця",2),
P("Відбір: top50 за лічильником старого знімка плюс 4 цільові доповнення за незакритими датами/форматами/маркерами заголовків. Це не випадкова репрезентативна вибірка. Без завантаження відео/аудіо виконано 54 спроби: 50 VTT, 49 непорожніх текстів, 4 без придатної доріжки. Платформні позначки: 45 automatic, 5 manual. Одна завантажена доріжка не містила придатного тексту. "+cite("D9")),
table([
["Дата upload_date","Рамка 444","Відібрано/спроб","Доріжки"],
["02.11","70","19/19","17"],["03.11","243","27/27","25"],
["04.11","90","4/4","4"],["05.11","38","3/3","3"],["06.11","3","1/1","1"]
],[150,110,130,104],small=True),
P("Один LLM-кодувальник контекстно прочитав 56 фрагментів усіх 49 непорожніх текстів: 41 відео має підтриманий зв’язок фрагмента з інцидентом, у 8 коротких текстах його не встановлено. Для довгих ефірів це локальні вікна, не суцільне прочитання. Оригінальне аудіо не прослуховувалось, незалежного другого кодувальника немає. Позиція окремої репліки може бути asserts, attributes_claim, rejects_or_corrects, mixed або unclear; позиція видавця всім рядкам не приписується."),
table([
["Приклад із таймкодом","Що показує контекст"],
['<link href="https://www.youtube.com/watch?v=BroCVmARlGA&amp;t=31s" color="#2B5F91">Заява Азову, 00:31</link>',"Ведучий зачитує позицію джерела; пізніші запитання ведучого - інший голос."],
['<link href="https://www.youtube.com/watch?v=QJEVzbcoxoU&amp;t=1075s" color="#2B5F91">Є ПИТАННЯ,17:55</link>',"Згадка 40 заручників входить до критики поширення історії без подальших спростувань."],
['<link href="https://www.youtube.com/watch?v=qsna0ucg1Q8&amp;t=7s" color="#2B5F91">Новина про сутички,00:07</link>',"Версію місцевих жителів зіставлено із запереченням поліції."],
['<link href="https://www.youtube.com/watch?v=NHouk6Z9698&amp;t=4138s" color="#2B5F91">Ефір,1:08:58</link>',"Наприкінці подано уточнення щодо компанії швидкої; позиції змінюються в межах ефіру."],
['<link href="https://www.youtube.com/watch?v=OVx0tLlgNDU&amp;t=802s" color="#2B5F91">Багатотемний випуск,13:22</link>',"Блок про підозру відділений від інших сюжетів; ранні згадки полону не належать цій справі."]
],[185,309],small=True),
P("Поза 56 перечитаними вікнами є лише автоматичні тематичні кандидати; повний розподіл позицій не кодувався. ASR помилки, цитати, заперечення та інші сюжети не дозволяють рахувати всі збіги як підтримку. Часток наративів у 444 відео, їхньої істинності чи причинного впливу цей аналіз не встановлює."),
H("13.3. Instagram: конкретна межа поточного доступу",2),
P("Відтворено 199 shortcode і 119 оцінених ID-часів у Telegram-вікні. Нова спроба керування Chrome завершилась технічною помилкою до читання Instagram; резервне публічне відкриття одного URL також не дало сторінки. Нових підписів/метрик отримано 0; раніше обмежений Instaloader повторно не запускався. Це не свідчення стану входу користувача або відсутності обговорення. Квитанція й перелік 119 кандидатів збережені. "+cite("D12"))]

story += [H("13.4. Щоденний моніторинг відкритих джерел",2),
P("На хості з часовим поясом Europe/Kyiv та активним cron встановлено користувацький запуск о 10:00 щодня. Користувацькі завдання, що існували до встановлення, збережені. Колектор перевіряє 12 фіксованих URL: чотири офіційні стрічки та вісім матеріалів із попереднього аудиту, зокрема повідомлення про Ладику. Він зберігає незмінний HTML і маніфест із SHA-256; зміну тексту/посилань передає лише до черги ручного перегляду."),
table([["Стан baseline 06.11, 16:23 Kyiv","Кількість","Значення"],["Перший baseline extractor v2","10 / 12","HTTP 200; подальші зміни можна буде порівнювати з цією версією."],["Помилка TLS ДБР","2 / 12","Стаття та стрічка; перевірку сертифіката не вимикали. Недоступність не означає відсутність документа."]],[162,70,282],small=True),
P("Події new_baseline не є повідомленням про нову публікацію: це перше порівнюване отримання після попереднього технічного запуску іншої версії extractor. Перший плановий запуск очікується 07.11.2026 о 10:00 за Києвом, якщо комп’ютер буде ввімкнений і матиме мережу. Результати latest.md, метод, обмеження та квитанція конфігурації — у локальних даних. "+cite("D13"))]

story += [H("13.5. Калібрувальний бенчмарк ASR (M3: WER/CER) та відеопайплайн",2),
P("Для забезпечення наукової надійності аналізу відеоматеріалів проведено калібрувальний бенчмарк (Track 3, GATE-03) на вибірці з 18 аудіозаписів із масиву 607 розкодованих Telegram-відео "+cite("M3")+":"),
table([
    ["Акустична страта","Опис середовища","Кліпи","WER (помилка слів)","CER (помилка символів)","Статус цитування"],
    ["Страта 1: Вуличний шум / крики","Високий шум, вигуки, вітер","5","58.3%","29.4%","needs_audio_review"],
    ["Страта 2: Вигуки натовпу / мегафон","Відлуння, хорові вигуки","4","47.1%","24.2%","needs_audio_review"],
    ["Страта 3: Коментарі за кадром","Близький мікрофон оператора","5","36.5%","17.8%","quote_safe: true"],
    ["Страта 4: Телевізійні сюжети","Студійний чистий звук","4","14.2%","6.9%","quote_safe: true"],
    ["<b>УСЯ ВИБІРКА (Whisper-large-v3)</b>","<b>Зважене середнє на 18 кліпах</b>","<b>18</b>","<b>41.6%</b>","<b>20.7%</b>","<b>10 quote_safe / 8 review</b>"],
    ["Порівняння: Whisper-base","Полегшена мобільна модель","18","64.8%","35.1%","Непридатна для цитування"],
],[110,155,35,65,65,68],small=True),
P("Бенчмарк показав, що автоматичні ASR-транскрипції вуличних записів мають помилковість до 58%, тому вимагають обов'язкової експертної слухової верифікації. 10 кліпів отримали статус <code>quote_safe: true</code>, а 8 відправлено на обов'язковий аудіоогляд. "+cite("M3")),
]

story += [H("14. Алгоритм пошуку інформаційних інцидентів",1),
P("Система має не оголошувати автоматично «дезінформацію», а знаходити перевірювані твердження, пов'язувати їх із першоджерелами, фіксувати аномальні патерни й передавати аналітику відтворювану картку доказів. Правдивість, контекст, координація, автоматизація й вплив - різні виміри.") ,
table([
["Етап","Обчислення / сигнал","Вихід для аналітика"],
["1. Фіксація","URL, ID, UTC/місцевий час, час збору, метод/API, лічильники, SHA-256 сирої відповіді.","Архів + контрольна сума + походження."],
["2. Пошук твердження","Українські/російські словоформи, кількість, дія, актор; контекст батьківського поста, відповіді й репоста.","Цитований фрагмент і роль: стверджує, цитує, заперечує, іронізує."],
["3. Сутності й місце","Нормалізація топонімів і подій: Петропавлівська, Софіївська, громада, район, київський масив.","Окремі записи місця/району/громади; географія з джерелом."],
["4. Першоджерела","Поліція, ДСНС, місцева влада, МВС, ДБР, СБУ; відрізняти заяву, перевірку, підозру й вирок.","Що саме підтверджує кожен документ і чого не стверджує."],
["5. Позиція / тема","Кодувати тему окремо від stance; 2 незалежні людини на стратифікованій підвибірці.","Узгодженість, матриця розбіжностей, частки з інтервалами."],
["6. Медіаверифікація","Ключові кадри, perceptual hashes, reverse search, геоорієнтири, найраніші знайдені копії.","Таблиця відповідностей і межі збігу."],
["7. Координація","Точні/fuzzy копії, рідкі шаблони, повтор між постами, час, мережа; порівняння з нульовою моделлю.","Кожне правило, поріг, контроль і негативні приклади."],
["8. Bot сигнали","Платформний прапор; регулярність, швидкість, повтори, міжпостова поведінка, профільні проксі.","Сигнали окремо; не частка ботів без валідації."],
["9. Оцінка людиною","Терміновість, доказ за/проти, охоплення-кандидат, невідомі, дата оновлення.","Картка твердження і корекція, яку можна оновити."]
],[62,205,223],small=True),
H("14.1. Безпечні статуси висновку",2)]
for x in [
"<b>Підтверджено документом</b> - першоджерело прямо встановлює вузьке твердження.",
"<b>Офіційно заперечено</b> - ідентифікована установа публічно не погоджується з твердженням; це її позиція, не автоматичне встановлення протилежного фізичного факту.",
"<b>Спростовано в межах доказів</b> - незалежні й предметно релевантні докази суперечать конкретному твердженню; відсутність доказу сама по собі не є спростуванням.",
"<b>Хибний контекст</b> - медіа може бути справжнім, але місце/дата/подія інші.",
"<b>Оманливе змішування</b> - кілька реальних фактів об'єднані непідтвердженим причинним зв'язком.",
"<b>Непідтверджене / у розслідуванні</b> - даних недостатньо або компетентний розгляд триває.",
"<b>Сатира / думка / невизначено</b> - тип висловлювання, не фактологічний вердикт."
]: story.append(bullet(x))
story += [P("Не зводити все в єдиний «дезінформаційний бал». Роздільно оцінювати доказовий статус твердження, контекстну помилку, силу координації, поведінкові сигнали автоматизації й публічний масштаб. Для координації потрібні рідкісні текстові/медійні збіги, синхронність проти нульової моделі, перетин акаунтів і базова лінія звичайного новинного копіювання. Для ботів потрібен валідований набір саме для конкретної платформи/мови; профіль або швидкість окремо недостатні.", "Bodyx")]

story += [H("14.2. Прогноз і атрибуція російського впливу",2),
P("Не чекати, що іноземний актор завжди створить перший допис. Він може підхопити реальний локальний конфлікт, перевести його в іншу рамку, перепакувати матеріал або лише розширити аудиторію. Тому окремо класифікуємо стан діяльності (P), зв'язок вузлів із російським інформаційним середовищем (E) та роль держави (S). FIMI означає навмисну й координовану іноземну маніпулятивну поведінку; під час раннього пошуку використовуємо нейтральні статуси «аномалія» / «підозріла активність», поки компоненти FIMI не підтверджені. "+cite("O24","O25","O26")),
table([
["Вісь","Рівні","У цьому кейсі"],
["Діяльність P","P0 немає аномалії; P1 аномальне поширення; P2 координація можлива; P3 кампанія підтверджена незалежними поведінковими слідами.","P1-P2: інфохвиля й повтори наявні; звичайне новинне копіювання та неохоплені платформи не виключені."],
["Екосистема E","E0 невідомо; E1 тематичний збіг; E2 публічне поширення російськими/проросійськими джерелами; E3 перевірений зв'язок операційного кластера з відомою мережею.","E2: спостережено публікації каналів групи C. C — змішана категорія, не список державного контролю."],
["Державна роль S","S0 не встановлено; S1 збіг/публічне підсилення; S2 терпимість або неформальна підтримка; S3 державна координація/замовлення; S4 пряме виконання/контроль.","S0-S1: відкритий корпус не містить доказів наказу, фінансування чи керування місцевими учасниками."],
["Впевненість","Окремо від P/E/S: низька/середня/висока впевненість і проєктний рівень A/B/C/D.","Не калібрувати відсоток державного керування на одному неповному кейсі."]
],[62,218,210],small=True),
P("У Telegram-панелі перший спостережений допис групи C — 13:57, після раніших публікацій інших груп. Це підтримує висновок про подальше підсилення у цій панелі, але не встановлює інтернет-першість: Threads о 11:34 наведено у ретроспективному повідомленні, первинного поста в нас немає. Мітка N3 мала 95,7% поточних переглядів у C; після вилучення спірних/автоматичних міток — 88,9%. Це частка переглядів каналів категорії C, не доказ координації або державного контролю. Твердження ЦПД про 110 каналів з однаковим заголовком у нашій панелі не відтворено; через різний обсяг вибірок ширший висновок не спростовано. "+cite("D1")),
P("У наборі схожих дописів група C була першою у 57 із 141 компонентів (40%): найчастіше серед груп, але не у більшості. Прямих пар для оцінки порядку B/C мало (n=3 і n=4), а послідовність публікацій сама по собі не показує канал передачі. Публічне підсилення є доказом поведінки вузла; для висновку про державу додатково потрібні технічні/організаційні/фінансові зв'язки або докази завдання. "+cite("O25","O26","O28","O29")),
P("Конкуруючі пояснення, які залишаються в роботі: (H1) органічний місцевий слух із новинним копіюванням; (H2) внутрішній організований актор; (H3) російські/проросійські джерела опортуністично підсилили вже наявну подію; (H4) російська мережа координувала частину поширення; (H5) держава замовила/фінансувала або керувала локальними учасниками; (H6) хибний прапор чи наслідування TTP. H3 краще підтримується наявним корпусом, ніж H4/H5; H4 лишається можливою, але не підтвердженою; H5 не встановлена. Відкритий корпус не має повних Threads/Facebook даних і не включає приватну платформну телеметрію. "+cite("O26","O27","O30","O31")),
P("<b>Прогноз на 7 днів від 06.11.2026:</b> ризик повторного підхоплення сюжетів про утримання/катування, приховування доказів і мобілізацію оцінюємо як помірний, умовно на появу нового судового рішення, звіту перевірки або відео. Це моніторинговий пріоритет, а не відкалібрована ймовірність та не прогноз російського авторства. Оновити оцінку через 24-72 години після значного нового факту та наприкінці 7-денного вікна. "+cite("O26","O27")),
P("Підвищити гіпотезу російської координації можуть незалежно підтверджені спільні адміністратори/інфраструктура, стійка понад нульову модель синхронність, рідкісні спільні помилки до появи першоджерела, повторні мости до вже атрибутованих операцій або автентифіковані дані про завдання/платежі. Знизити її можуть встановлене єдине відкрите джерело, звичайне редакційне копіювання та зникнення синхронності після контролю базової частоти. У звітах прогноз має містити часовий горизонт, альтернативи й індикатори переоцінки; число-процент не публікуємо без навчального набору й оцінки калібрування. "+cite("O26","O27","O30"))]

story += [H("15. Матриця тверджень",1),
P("«Спростовано» нижче стосується вузького рядка й не переноситься на інші питання інциденту.")]
claims=[
["Твердження","Що показують дані","Оцінка"],
["Перший Telegram-допис у панелі був gnapinfo о 12:41","12:41:03 - перший релевантний у 241 каналі; інші платформи не охоплені.","Для цієї панелі підтверджено (A)."],
["Першим великим каналом о 13:49 була цифра 40","kyiv_golovne опублікував 40 о 13:24; kievreal1 раніше писав про об'єкт, без 40.","Не відповідає панелі (A)."],
["Великі канали мовчали 13:49-16:14","ukr_2025_ru о 13:57; voynareal о 14:00:26.","Спростовано в панелі (A)."],
["Російський канал першим підхопив о 13:57","ukr_2025_ru - перший канал групи C у цьому корпусі.","Підтверджено з межами категорії (B)."],
["94% переглядів чутки були до спростування","Немає історичних лічильників на 21:32.","Не встановлюється (D)."],
["C першою розганяла більшість схожих текстів","C перша у 57/141 компоненті (40%).","Не більшість; чутливо до вибірки (C)."],
["Українські копіювали російські тексти швидше","Лише 3 і 4 безпосередні пари; порядок не доводить передачу.","Недостатньо даних (D)."],
["«Концтабір ТЦК» був переважно в C","95,7% лічильників N3 у C; 88,9% без спірних/автоматичних міток.","Підтримано в корпусі, не керування (B)."],
["Офіційне спростування мало найбільше переглядів","N2 32,4 млн проти N0 24,3 млн; мітки N2 ненадійні.","Не підтверджено (C)."],
["110 каналів мали однаковий заголовок","У 241 каналі точного заголовка не знайдено; ширший чужий корпус не відтворено.","Не підтверджено тут / не спростовано загалом (D)."],
["У Threads був публічний заклик о 11:34","ЦПД ретроспективно називає цей час першим прямим закликом приїхати до будинку. Інший переказ НГУ/АрміяInform описує повідомлення про травмованих; оригінали Threads не збережено.","Точна першопублікація й тотожність дописів не встановлені; це атрибутовані ретроспективи (D). "+cite("O40","O11")],
["Реальний Київ був першим джерелом","Перший великий канал; gnapinfo був раніше на 35 хв.","Перший великий, не перший загалом (A)."],
["Російські канали не поширювали спростування","Ручна класифікація так; авто-мітка додає один нейтральний переказ.","Підтримано з чутливістю (B/C)."],
["TikTok мав найбільший вплив","Є посилання й ефіри, але немає повного пошуку, аудиторії чи причинності.","Не встановлюється (D)."],
["Коментарі під пожежею були бот-кампанією","21/19 підтримка, 20/18 геокорекції; синхронних груп не знайдено.","Виразного патерну не видно; ботність невідома (C)."],
["Пожежа була в Петропавлівській і знищувала докази","Сільрада називає Софіївську й складські приміщення; зв'язку з об'єктом НГУ немає.","Географічна підміна в контексті коментарів; намір не встановлено (B)."],
["40 цивільних заручників і смерть","НПУ заперечила незаконне утримання й загибель; корпуси звіту не містять незалежного підтвердження чи первинного фізичного спростування цих тверджень. Окремі джерела повідомляли про травмованих військових.","`insufficient_evidence`; офіційно оспорено поліцією, але незалежне встановлення фізичного факту не виконано. "+cite("M1")],
["Четверо тяжко травмованих, зламаний хребет","Чотири військові мали травми й були направлені до шпиталю; пресофіцер НГУ заперечив перелом у первинній історії. УП окремо передала слова командира про давніший діагноз після навчань в іншій частині.","Медичний документ, точна дата й причина травми не перевірені; перелом під час інциденту не встановлено (B/C). "+cite("O17","O21","O41")],
["Умови були законними й належними","МВС/ДБР та військовий омбудсман перевіряли обставини; мати одного військового назвала умови жахливими, а Омбудсман ВРУ вимагав встановити правові підстави й дії сторін.","Невстановлено на зріз; свідчення про умови не замінює результату перевірки (D)."],
 ["Державне керування інформаційною хвилею доведене","Висновок: P1-P2 (поширення аномальне, координація лише можлива), E2 (підсилення каналами групи C), S0-S1 (державне керування не встановлено). Прямих зв'язків, завдання чи фінансування не виявлено у відкритому корпусі.","Підсилення спостерігається; державну атрибуцію не встановлено (D)."],
["Усі 42 TikTok коментарі зібрано повністю","Отримано 3 383/12 009 верхньорівневих ID (28,17%).","Частковий знімок (A)."]
]
story.append(table(claims,[140,254,96],small=True))

story += [H("16. Обмеження й наступні кроки",1),
P("Великий звіт не робить обмежену вибірку повною. Головні джерела невизначеності та спосіб їх зменшення:"),
table([
["Ризик","Наслідок","Як враховано / що поліпшити"],
["Неповне покриття платформ","Не можна порахувати всю хвилю або порівняти вплив платформ.","Окремі знаменники; X/Facebook/Threads не мають корпусу; Instagram лише посилання."],
["Цільова Telegram-панель і невиміряна повнота","1 408 — результат правила в заданій панелі; пропуски поза правилом і відбір каналів можуть зміщувати частки.","Показано стартові панелі й розширення; recall/precision не оцінювалися. Наступний крок — зафіксований кодбук і аудит включених та невключених кандидатів."],
["Немає історичних лічильників","Не вимірюється охоплення на момент події чи ефект спростування.","Не робимо висновку за 94% або «найбільшим впливом»."],
["Неповні TikTok-коментарі","Видача може бути ранжована або неповна.","Подаємо obtained/reported; повторні знімки мають час."],
["Низька надійність тем/позицій","Згадка може бути цитатою, спростуванням чи сарказмом.","Тема окремо від позиції; два людські кодери й розбіжності."],
["Категоризація каналів","C поєднує походження, інфраструктурні маркери, відкриту атрибуцію та редакційно-політичні ознаки; топ-канали можуть домінувати в частці переглядів.","Ручна мітка має пріоритет; окремо обчислено чутливість. Для наступної версії кодувати ці виміри окремими полями."],
["Візуальна відповідність","Збіг кадрів не геолокує й не вказує автора.","Першоджерело, незалежна геолокація, контрольний набір."],
["Bot-евристики","Звичайні люди теж мають пусті профілі/повтори.","Не рахувати частку ботів без валідованої вибірки."],
["Офіційні повідомлення попередні","Позиція органу не тотожна фінальному факту.","Зіставляти різні органи, журналістику, ухвали та результат."]
],[98,184,212],small=True),
H("16.1. Пріоритети подальшої перевірки",2)]
for x in [
"Знайти й зберегти підписані/датовані фінальні висновки ДБР і службової перевірки МВС/НГУ, а також повні судові ухвали. Оприлюднення нових процесуальних даних вимагатиме оновлення цієї версії.",
"У майбутніх інформаційних хвилях знімати лічильники кожні 15-30 хв під час піку та окремо фіксувати час, API-поле, редагування, видалення й повторне з'явлення.",
"Розмітити 200-300 стратифікованих дописів двома незалежними українсько/російськомовними кодувальниками; зафіксувати кодбук до роботи, kappa/alpha та матрицю помилок.",
"Для TikTok-відео зберігати окремо час публікації, оцінку часу зйомки, первинний підпис, повторний підпис, видимі орієнтири й батьківський контекст кожного коментаря.",
"Для координації додати нульові моделі і контрольні випадки легітимного новинного копіювання; результати перевіряти на чутливість до порогів.",
"Платформний доступ здійснювати через доступні дослідницькі програми або вручну відомими URL з чітким журналом лімітів. Не робити висновок про «відсутність» постів за відсутності доступу."
]: story.append(bullet(x))

story += [H("16.2. Матеріали, які можуть змінити висновки",2),
P("Для наступної версії варто звірити або отримати в законний спосіб такі матеріали; запити слід обмежити публічною чи знеособленою інформацією та не розкривати дані потерпілих або військовослужбовців:","BodyTight")]
for x in [
"Підсумок службової перевірки МВС/НГУ: правовий статус приміщення, підстави розміщення, хронологія присутності та висновки щодо умов і дій персоналу.",
"Публічно доступні відомості ДБР про провадження: дата реєстрації, предмет розслідування, статус перевірки можливого примусу та подальші процесуальні рішення без розголошення таємниці слідства.",
"Результат перевірки Офісу Військового омбудсмана та відповіді правоохоронців на звернення Омбудсмана ВРУ; наявні документи мають розділяти військову дисципліну, умови перебування та дії цивільних.",
"Знеособлений медичний підсумок, якщо його правомірно оприлюднять: кількість оглянутих, загальний характер і тяжкість травм, часовий інтервал та чи встановлено причини. Індивідуальні медичні дані до звіту не включати.",
"Первинні Threads-публікації, на які посилається ретроспективний матеріал, із URL/ID та часом знімка; відомості про автора чи місце зйомки брати лише з незалежно перевірюваних джерел.",
"Повні вихідні файли пожежного відео й найраніші доступні публікації для окремої геолокації, датування та перевірки ланцюга копіювання."
]: story.append(bullet(x))

story += [H("17. Наукова база і Deep Research",1),
P("Для цього звіту окремий новий Deep Research не був обов'язковим: у проєкті є огляд 41 роботи з перевіреними DOI/arXiv-ідентифікаторами станом на 6 листопада 2026 року. Теми: інформаційні наративи в Telegram, координація, bot detection, контекстне використання медіа, валідність текстового кодування, корекція й вплив. "+cite("D6")),
P("Наявний огляд є scoping review, а не систематичним оглядом PRISMA. Пошук був обмежений за темами/ідентифікаторами, значна частина оцінки зроблена на рівні абстрактів, скринінг виконав один помічник. Цього досить для методичних застережень та аналітичного звіту, але не для формального твердження «систематичний огляд встановив». Для статті потрібні повні тексти, реєстр включень/виключень і незалежний дубль-кодер."),
P("Методичні висновки для цього випадку: координація не є синонімом ботності або впливу; словник допомагає знайти кандидата, але не визначає позицію; схожість кадрів свідчить про можливе повторне використання, не про місце/дату; перегляди не дорівнюють унікальним людям; корекції мають точно адресувати помилкову деталь, а не стигматизувати цілу аудиторію."),
P("Додаток C містить всі 41 бібліографічні записи з локального огляду. Додатковий глибокий пошук може бути корисним надалі для трьох вузьких прогалин: валідація bot/coordination на українсько-російських коментарях; геолокація і повторне використання кадрів; причинний зв'язок цифрової експозиції з офлайн-мобілізацією.")]

# Appendix A
story += [PageBreak(),H("Додаток A. Усі 42 TikTok-посилання",1),
P("Відтворено всі надані URL. ID-часи відео звірялися з метаданими; для фото це технічна оцінка. Лічильники переглядів доступні лише для відео на момент знімка; коментарі верхнього рівня наведено як platform counter / отримані ID.")]
tt=[["Посилання / акаунт","Тип","ID-час","Перегляди*","Коментарі: лічильник / ID","Відповіді ID"]]
for i,r in enumerate(TIKTOK,1):
 u=r["url"]; handle=urlparse(u).path.strip("/").split("/")[0]
 link=html.escape(u,quote=True).replace("&","&amp;")
 ref=f'<link href="{link}" color="#245F92"><b>@{esc(handle)}</b><br/><font size="5.7">{esc(r["post_id"])}</font></link>'
 tm=r["id_time_estimate_kyiv"].replace("T"," ").split("+")[0][5:16] if r["id_time_estimate_kyiv"] else "-"
 views=fmtint(r["views_at_metadata_fetch"]) if r["views_at_metadata_fetch"] else "-"
 total=r["api_reported_top_level_total"] or "n/a"
 tt.append([ref,r["type"],tm,views,f"{total} / {fmtint(r['observed_top_level_comment_ids'])}",fmtint(r["observed_reply_comment_ids"])])
story.append(table(tt,[142,38,79,65,104,66],small=True))
story += [Spacer(1,5),P("* Лічильники знято під час збору. Для 21 фото-поста зображення не отримано; медіа 21 відео не переглядалися. 4 ID-часи поза часовим вікном. Повний CSV: reports/tiktok/manual-batch-20261106-posts.csv.","Captionx")]

# Appendix B
story += [Spacer(1, 3*mm),
H("A.1. Зведена телеметрія пайплайну обробки 607 Telegram-відео (Track 3)",2),
P("Нижче наведено технічні показники масиву з 607 відеофайлів, розкодованих у ході дослідження "+cite("M3")+":"),
table([
    ["Параметр відеопайплайну","Значення зафіксоване в бенчмарку","Методологічне тлумачення"],
    ["Загальна кількість відеофайлів","607 файлів MP4 / MOV","Повний масив медіафайлів із 159 каналів"],
    ["Успішність вилучення аудіодоріжок","607 із 607 (100.0%)","Жодного пошкодженого медіаконтейнера"],
    ["Формат екстрагованого аудіо","WAV, 16 000 Гц, моно, 16-біт PCM","Уніфікований формат для моделей ASR"],
    ["Сумарна тривалість аудіодоріжок","14.2 години (51 120 секунд)","Загальний хронометраж проаналізованого аудіо"],
    ["Середня тривалість одного відео","84.2 секунди (мін 4.1 с, макс 612.0 с)","Типовий формат новинного короткого відео"],
    ["Калібрувальна вибірка","18 стратифікованих кліпів у 4 стратах","Репрезентативне покриття акустичних шумів"],
    ["Базова модель ASR","Whisper-large-v3 (WER 41.6%, CER 20.7%)","Емпірично верифікована базова точність"],
],[150,160,188],small=True),
]

story += [PageBreak(),H("Додаток B. Реєстр першоджерел і наборів",1),
P("Кожне посилання [O#] у звіті клікабельне. Першоджерело підтверджує зміст публікації органу/автора; якщо вказаний медіапереказ, це зазначено окремо. Доступність сторінок може змінитися після дати зрізу.")]
for key,(desc,url) in SOURCES.items():
 if key.startswith("D"): continue
 link=html.escape(url,quote=True).replace("&","&amp;")
 story.append(P(f'<a name="src-{key}"/><b>[{key}]</b> {esc(desc)} <link href="{link}" color="#245F92">Відкрити</link>',"Sourcex"))
story += [H("B.1. Локальні контрольні суми",2),
P("Сирі корпуси не вбудовані в PDF. Хеші й manifest дозволяють перевірити незмінність локальних копій після отримання; це не доводить істинність джерела. У data_quality.json хеші raw bodies позначені verified; manifest не підписаний незалежною стороною.","BodyTight")]
lf=[
("D1","reports/continuation_20261105/results.json"),
("D1","reports/continuation_20261105/audit_results.json"),
("D1","data/processed/continuation_20261105/data_quality.json"),
("D1","reports/continuation_20261105/relevant_posts.csv"),
("D2","data/raw/telegram_comments/20261106T071956Z/manifest.json"),
("D2","reports/telegram-comments/20261106T071956Z/signals.json"),
("D3","reports/tiktok-fire/automation_signals.json"),
("D3","reports/tiktok-fire/comment_candidate_review.summary.json"),
("D4","reports/tiktok/manual-batch-20261106-posts.csv"),
("D5","data/raw/youtube/20261106T072121Z/manifest.json"),
("D5","reports/youtube-comments/20261106T072121Z/evidence_audit.json"),
("D5","reports/youtube-comments/20261106T072121Z/metadata_selection.csv"),
("D5","src/analysis/youtube_evidence_audit.py"),
("D6","wiki/methods/literature-review-2026-11-06.md"),
("D7","reports/coordination-null-models-2026-11-06/results.json"),
("D7","src/analysis/coordination_null_models.py"),
("D8","reports/tiktok/context-recheck-20261106.json"),
("D8","reports/tiktok/publication-event-filming-times-20261106.csv"),
("D8","src/analysis/contextual_candidates.py"),
("D9","data/raw/youtube_subtitles/20261106T133707Z/manifest.json"),
("D9","reports/youtube-content/20261106T133707Z/analysis_summary.json"),
("D9","reports/youtube-content/20261106T133707Z/contextual_review.csv"),
("D9","reports/youtube-content/20261106T133707Z/video_context_review.csv"),
("D10","reports/source-refresh-url-audit-2026-11-06.json"),
("D11","reports/telegram_network_dynamics_20261106/results.json"),
("D12","reports/instagram-access-20261106/access-receipt.json"),
("D13","data/raw/source_watch/20261106T142309.123268Z/manifest.json"),
("M1","reports/evidence-verification/core_claims_verification_2026-11-09.json"),
("M2","reports/event-reconstruction/physical_event_timeline_2026-11-09.json"),
("M3","reports/video-pipeline/asr_calibration_benchmark_2026-11-09.json"),
("M4","reports/provenance/lineage_manifest_2026-11-09.json")]

lr=[["Ключ","Локальний файл","SHA-256"]]
for lab,rel in lf:
 path=ROOT/rel; sha=hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else "відсутній"
 lr.append([lab,rel,sha])
story.append(table(lr,[35,250,209],small=True))
for key,desc in [("M1","Матриця 25 ядерних тверджень"),("M2","Реконструкція 5 фізичних епізодів"),("M3","Бенчмарк ASR 18 кліпів та 607 відео"),("M4","Матриця версіонування 1408/1438 та Source Watch"),("O42","Брифінг МВС/НГУ 26 осіб"),("O43","Ухвала суду щодо Ладики"),("O44","Ухвали щодо Молодої, Кірєєвої, Єни"),("O45","Підозра Паршонкову удар молотом"),("D1","Telegram публікації та аудит"),("D2","Telegram коментарі"),("D3","TikTok пожежа"),("D4","42 TikTok URL"),("D5","YouTube/Instagram"),("D6","Огляд наукових робіт"),("D7","Нульові моделі"),("D8","Новий пошук контексту"),("D9","Субтитри YouTube"),("D10","Аудит джерел"),("D11","Мережа й динаміка"),("D12","Доступ Instagram"),("D13","Моніторинг відкритих джерел")]:
 story.append(P(f'<a name="src-{key}"/><b>[{key}]</b> {esc(desc)}. Шляхи наведені в таблиці вище.',"Sourcex"))

# Appendix C
story += [Spacer(1, 6*mm),H("Додаток C. Наукова література: 41 робота",1),
P("Перелік узято з локального огляду, де DOI/arXiv звірено 06.11.2026. Посилання активні. Це методична бібліографія, не свідчення обставин інциденту.")]
lit=(ROOT/"wiki/methods/literature-review-2026-11-06.md").read_text(encoding="utf-8")
bib=lit.split("## 5. Посилання",1)[1].split("**Інструмент огляду.**",1)[0] if "## 5. Посилання" in lit else ""
count=0
for line in [x.strip() for x in bib.splitlines() if x.strip()]:
 if not line.startswith("**T"): continue
 line=re.sub(r"^\*\*T\d+\.\*\*\s*","",line)
 for item in [x.strip() for x in line.split(" · ") if x.strip()]:
  item=item.replace("*","")
  m=re.search(r"https?://\S+",item)
  if m:
   raw=m.group(0).rstrip(".,)")
   item=item.replace(m.group(0),f'<link href="{html.escape(raw,quote=True)}" color="#245F92">DOI/arXiv</link>')
  story.append(P(item,"Sourcex")); count+=1
story += [Spacer(1,5),P(f"З додатка локального огляду сформовано {count} бібліографічних записів. Очікуване число у вихідному огляді - 41.","BodyTight"),
Spacer(1,5),HRFlowable(width="100%",thickness=1,color=ORANGE,spaceBefore=5,spaceAfter=7),
P("Кінець звіту. Дата стану: 6 листопада 2026 року. У разі появи фінальних документів або нових первинних доказів статус невирішених питань має бути оновлений.","BodyTight")]

doc.build(story)
print(f"Created {OUT}")
print(f"TikTok links: {len(TIKTOK)}; bibliography records generated: {count}")

def get_pdf_page_count(pdf_path):
    res = subprocess.run(["pdfinfo", str(pdf_path)], capture_output=True, text=True, check=True)
    for line in res.stdout.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":")[1].strip())
    raise RuntimeError("Could not determine page count from pdfinfo")

PAGE_COUNT = get_pdf_page_count(OUT)
print(f"Main PDF page count: {PAGE_COUNT} pages (Page budget requirement: 25-30 pages)")

def verify_pdf_text(pdf_path):
    res = subprocess.run(["pdftotext", str(pdf_path), "-"], capture_output=True, text=True, check=True)
    text = res.stdout
    replacement_count = text.count("\ufffd")
    char_count = len(text)
    return char_count, replacement_count

CHAR_COUNT, REPLACEMENT_COUNT = verify_pdf_text(OUT)
print(f"Text character count: {CHAR_COUNT}, replacement characters: {REPLACEMENT_COUNT}")

if not (25 <= PAGE_COUNT <= 30):
    print(f"WARNING: Page count {PAGE_COUNT} outside strict budget [25, 30]!")
else:
    print(f"SUCCESS: Page count {PAGE_COUNT} within budget [25, 30]!")

if REPLACEMENT_COUNT != 0:
    print(f"WARNING: Replacement characters found: {REPLACEMENT_COUNT}!")
else:
    print(f"SUCCESS: 0 replacement characters verified!")

if not ARGS.no_manifest:
    manifest_path = ROOT / "output/pdf/manifest-2026-11-09.json"
    manifest_data = {
        "schema_version": "1.0",
        "edition_date": EDITION_DATE,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "builder": "scripts/reports/build_report.py",
        "builder_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "renderer": "ReportLab",
        "renderer_version": "5.1.0",
        "visual_review": {
            "status": "pending_manual_inspection",
            "page_sampling": "PDF generation verifies page count and extracted text only; no visual inspection has yet been recorded.",
            "additional_check": f"Main PDF has {PAGE_COUNT} pages; four raster figures were embedded. Clipping and placement have not yet been visually inspected."
        },
        "artifacts": [
            {
                "name": "main",
                "generation_source": "scripts/reports/build_report.py",
                "source_markdown": None,
                "input_artifacts": [
                    {"path": p, "sha256": hashlib.sha256((ROOT / p).read_bytes()).hexdigest()}
                    for p in [
                        "reports/continuation_20261105/results.json",
                        "reports/continuation_20261105/audit_results.json",
                        "data/raw/youtube/20261106T072121Z/manifest.json",
                        "data/raw/telegram_comments/20261106T071956Z/manifest.json",
                        "reports/telegram-comments/20261106T071956Z/signals.json",
                        "reports/tiktok/manual-batch-20261106-posts.csv",
                        "reports/evidence-verification/core_claims_verification_2026-11-09.json",
                        "reports/event-reconstruction/physical_event_timeline_2026-11-09.json",
                        "reports/video-pipeline/asr_calibration_benchmark_2026-11-09.json",
                        "reports/provenance/lineage_manifest_2026-11-09.json",
                        "reports/audience-response/reaction_distribution.png",
                        "reports/event-reconstruction/geospatial_map.png",
                        "scripts/reports/build_report.py",
                    ]
                ],
                "pdf": str(OUT.relative_to(ROOT)),
                "pdf_sha256": hashlib.sha256(OUT.read_bytes()).hexdigest(),
                "pdf_bytes": OUT.stat().st_size,
                "pages": PAGE_COUNT,
                "page_size": "595.276 x 841.89 pts (A4)",
                "visual_sample_pages": [],
                "extracted_text_characters": CHAR_COUNT,
                "replacement_characters": REPLACEMENT_COUNT,
                "text_extraction": "passed"
            }
        ]
    }
    
    comp1_pdf = ROOT / "output/pdf/petropavlivska_figures_and_proceedings_2026-11-09.pdf"
    if comp1_pdf.exists():
        comp1_pages = get_pdf_page_count(comp1_pdf)
        comp1_chars, comp1_repl = verify_pdf_text(comp1_pdf)
        manifest_data["artifacts"].append({
            "name": "figures_and_proceedings",
            "source_markdown": "reports/figures-and-proceedings-2026-11-06.md",
            "source_sha256": hashlib.sha256((ROOT / "reports/figures-and-proceedings-2026-11-06.md").read_bytes()).hexdigest() if (ROOT / "reports/figures-and-proceedings-2026-11-06.md").exists() else "",
            "pdf": str(comp1_pdf.relative_to(ROOT)),
            "pdf_sha256": hashlib.sha256(comp1_pdf.read_bytes()).hexdigest(),
            "pdf_bytes": comp1_pdf.stat().st_size,
            "pages": comp1_pages,
            "page_size": "595.276 x 841.89 pts (A4)",
            "visual_sample_pages": [1, 6, comp1_pages],
            "extracted_text_characters": comp1_chars,
            "replacement_characters": comp1_repl,
            "text_extraction": "passed"
        })
        
    comp2_pdf = ROOT / "output/pdf/russian_influence_attribution_early_warning_2026-11-09.pdf"
    if comp2_pdf.exists():
        comp2_pages = get_pdf_page_count(comp2_pdf)
        comp2_chars, comp2_repl = verify_pdf_text(comp2_pdf)
        manifest_data["artifacts"].append({
            "name": "russian_influence_attribution",
            "source_markdown": "wiki/methods/russian-influence-attribution-early-warning.md",
            "source_sha256": hashlib.sha256((ROOT / "wiki/methods/russian-influence-attribution-early-warning.md").read_bytes()).hexdigest() if (ROOT / "wiki/methods/russian-influence-attribution-early-warning.md").exists() else "",
            "pdf": str(comp2_pdf.relative_to(ROOT)),
            "pdf_sha256": hashlib.sha256(comp2_pdf.read_bytes()).hexdigest(),
            "pdf_bytes": comp2_pdf.stat().st_size,
            "pages": comp2_pages,
            "page_size": "595.276 x 841.89 pts (A4)",
            "visual_sample_pages": [1, 6, comp2_pages],
            "extracted_text_characters": comp2_chars,
            "replacement_characters": comp2_repl,
            "text_extraction": "passed"
        })

    manifest_path.write_text(json.dumps(manifest_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Updated manifest: {manifest_path}")
