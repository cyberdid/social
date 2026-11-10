#!/usr/bin/env python3
"""Render Ukrainian copies of the paper's figures from the unchanged English generators.

Text is translated at draw time and output goes to figures_uk/. Provenance JSON is left untouched,
so the English figures and their recorded hashes are not affected.
"""
import pathlib
import re
import runpy
import sys

import matplotlib

matplotlib.use("Agg")
from matplotlib.figure import Figure
from matplotlib.text import Text

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "figures_uk"
OUT.mkdir(exist_ok=True)
sys.path.insert(0, str(HERE))

UK = {
    "Platform collectors\nTelegram / selected platforms": "Збирачі платформ\nTelegram / обрані платформи",
    "Fixed Source Watch\nAllowlisted web captures": "Фіксований Source Watch\nКопії вебсторінок із переліку",
    "Local media archive\nFiles + source-post manifest": "Локальний медіаархів\nФайли + маніфест дописів",
    "Legacy information analysis\nNormalize / themes / copies\nGraphs / conditional nulls": "Застарілий аналіз інформації\nНормалізація / теми / копії\nГрафи / умовні нульові",
    "Source ingest bridge\nSource / Artifact / Passage\nSQLite EvidenceLedger": "Міст імпорту джерел\nSource / Artifact / Passage\nSQLite EvidenceLedger",
    "Separate local video runner\nIndex / audio / frames\nCandidate OCR + ASR": "Окремий запускач відео\nІндекс / аудіо / кадри\nКандидатні OCR + ASR",
    "Typed analytical inputs\nClaims / event mentions\nLineage / supplied labels": "Типізовані входи аналізу\nТвердження / згадки подій\nЛінії походження / мітки",
    "Offline case runner\nRetrieval / timelines\nConflict / uncertainty": "Офлайн-запускач кейсу\nПошук / часові шкали\nКонфлікт / невизначеність",
    "Report bundle + gates\nSupplied findings / results\nCitations / hashes / schemas": "Набір звіту + бар'єри\nНадані висновки / результати\nЦитати / хеші / схеми",
    "Solid: implemented exchange\nDashed: separate / curated handoff": "Суцільна: реалізований обмін\nШтрихова: окремо / вручну",
    "Source\nURI / publisher": "Source\nURI / видавець",
    "Artifact\nCaptured bytes / SHA-256": "Artifact\nЗібрані байти / SHA-256",
    "Passage\nText / locator": "Passage\nТекст / локатор",
    "Claim / mention\nStatement + scope\nAssertion ≠ event": "Твердження / згадка\nФормулювання + обсяг\nТвердження ≠ подія",
    "Evidence assessment\nRelation + rationale\nAcceptance provenance": "Оцінка доказів\nВідношення + обґрунтування\nПоходження прийняття",
    "Verification result\nScope + cutoff + state\nRetain unknown/conflict": "Результат перевірки\nОбсяг + межа + стан\n«Невідомо» і конфлікт",
    "Source dependency families\nCopies may share one root\nUnknown linkage ≠ independence": "Сім'ї залежних джерел\nКопії можуть мати один корінь\nНевідомий зв'язок ≠ незалежність",
    "Superseding assessment / finding\nPreserve earlier record; validate references\nNo physical truth inferred from a valid ID": "Оцінка / висновок, що заміщує\nЗапис лишається; посилання перевіряються\nДійсний ID не встановлює фізичної істинності",
    "Run receipts + unresolved queue + versioned outputs\nStructural checks do not establish semantic truth": "Квитанції запуску + черга нерозв'язаного + версіоновані результати\nСтруктурні перевірки не встановлюють семантичної істинності",
    "Information lineage is supplied or inferred separately from byte identity.": "Лінія походження інформації визначається окремо від тотожності байтів.",
    "IncidentSpec + budgets\nOptional collection execution": "IncidentSpec + бюджети\nНеобов'язковий збір",
    "Fixed Source Watch\nCapture → bridge → ledger": "Фіксований Source Watch\nЗбір → міст → реєстр",
    "Pretyped local inputs\nExplicit files + cutoff": "Типізовані локальні входи\nЯвні файли + межа часу",
    "Structural report gates\nReferences / hashes\nCutoffs / frozen controls": "Структурні бар'єри звіту\nПосилання / хеші\nМежі / фіксовані контролі",
    "Offline analytical stages\nRetrieve / organize / summarize\nUnknowns remain explicit": "Офлайн-етапи аналізу\nПошук / порядок / підсумки\n«Невідомо» лишається",
    "Report input bundle\nFindings / assessments\nSeparately supplied": "Вхідний набір звіту\nВисновки / оцінки\nНадаються окремо",
    "Demonstrated boundary: scripted / integrated bounded workflow (levels 1–2)\nNo independent end-to-end incident benchmark (levels 3–4 unestablished)\nPassing structural gates does not validate retrieval entailment or physical event truth": "Продемонстрована межа: скриптовий / інтегрований обмежений процес (рівні 1–2)\nНезалежного наскрізного бенчмарка інцидентів немає (рівні 3–4 не встановлено)\nПроходження структурних бар'єрів не валідує випливання чи істинність фізичних подій",
    "Local file + manifest\nHash / stat stability": "Локальний файл + маніфест\nХеш / стабільність stat",
    "Probe + strict decode\nTechnical readability only": "Суворе декодування\nЛише технічна читабельність",
    "Audio + sampled frames\nDerivative checksums": "Аудіо + вибіркові кадри\nКонтрольні суми похідних",
    "Perceptual candidates\npHash / dHash / alignment\nUncalibrated thresholds": "Перцептивні кандидати\npHash / dHash / порядок\nНекалібровані пороги",
    "Candidate text\nLocal OCR + ASR\nPreserve original segments": "Кандидатний текст\nЛокальні OCR + ASR\nСегменти зберігаються",
    "Correction sidecars\nAlternatives + uncertainty\nNo contextual word invention": "Файли виправлень\nВаріанти + невизначеність\nБез домислювання слів",
    "Independent contextual / acoustic / speaker / fact verification remains separate\nHistorical external Gemini pilot: 3 still frames from 1 clip; not integrated continuous video analysis": "Незалежна перевірка контексту, акустики, мовця й фактів лишається окремою\nІсторичний зовнішній пілот Gemini: 3 кадри з 1 кліпу; не інтегрований аналіз безперервного відео",
    "P1 Gathering mention": "P1 Згадка про збір людей",
    "P2 Clash mention": "P2 Згадка про сутички",
    "P3 Arrival / blockade mention": "P3 Згадка про прибуття / блокаду",
    "P4 Smoke / flare mention": "P4 Згадка про дим / фаєри",
    "P5 Resolution mention": "P5 Згадка про завершення",
    "C1 Police statement": "C1 Заява поліції",
    "C2 Telegram publication": "C2 Публікація в Telegram",
    "C3 Investigation announcement": "C3 Оголошення розслідування",
    "C4 Briefing publication": "C4 Публікація брифінгу",
    "C5 Fire statement": "C5 Заява про пожежу",
    "Supplied physical-event intervals (all unresolved)": "Надані інтервали фізичних подій (усі нерозв'язані)",
    "Communication publication times (not recording times)": "Час публікації комунікацій (не час запису)",
    "2026, UTC; assigned intervals are not independently validated bounds": "2026, UTC; призначені інтервали не є незалежно валідованими межами",
    "Exact": "Точний", "Legacy LSH": "Застарілий LSH",
    "Jaccard threshold / candidate recall": "Поріг Jaccard / повнота кандидатів",
    "Cross-channel pairs": "Міжканальні пари",
    "(a) Exact and legacy pairs": "(а) Точні й застарілі пари",
    "Observed": "Спостережено", "2h null": "Нульова 2 год", "24h null": "Нульова 24 год",
    "Pairs within 10 minutes": "Пари в межах 10 хвилин",
    "(b) Timing at Jaccard $\\geq$ 0.60": "(б) Час за Jaccard $\\geq$ 0,60",
    "Means and central 95% of null draws": "Середні й центральні 95% вибірок",
    "Historical eligible texts: n = 1,384.": "Історичні придатні тексти: n = 1 384.",
    "Null ranges are not confidence intervals.": "Діапазони не є довірчими інтервалами.",
}
_set_text = Text.set_text
_savefig = Figure.savefig
_write_text = pathlib.Path.write_text
USED = set()


def tr(value):
    if not isinstance(value, str):
        return value
    if value in UK:
        USED.add(value)
        return UK[value]
    value = re.sub(r"(\d\d) Nov\b", r"\1 лист.", value)
    return re.sub(r"(?<=\d)\.(?=\d)", ",", value)


def set_text(self, s):
    return _set_text(self, tr(s))


def savefig(self, fname, *args, **kwargs):
    return _savefig(self, OUT / pathlib.Path(fname).name, *args, **kwargs)


def write_text(self, *args, **kwargs):
    if "figure_data" in self.parts:
        return 0
    return _write_text(self, *args, **kwargs)


Text.set_text = set_text
Figure.savefig = savefig
pathlib.Path.write_text = write_text
for name in ("generate_system_figures.py", "generate_evaluation_figures.py"):
    runpy.run_path(str(HERE / name), run_name="__main__")
missing = sorted(set(UK) - USED)
print("unused translations:", missing)
