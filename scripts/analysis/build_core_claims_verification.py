#!/usr/bin/env python3
"""Build and export core claims verification package for Milestone M1 (Track 1).

Executes deterministic retrieval via BM25, exact passage offset validation,
evidence assessments (supports, contradicts, rebuts, contextualizes),
and aggregate verification for 25 prioritized claims regarding the
Petropavlivska Borshchahivka incident.

Outputs:
  - reports/evidence-verification/core_claims_verification_2026-11-09.json
  - reports/evidence-verification/core_claims_verification_2026-11-09.md
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.analysis.claim_verification import (
    aggregate_verification,
    create_evidence_assessment,
    infer_claim_passage_relation,
    retrieve_evidence_candidates,
)


def _utc_timestamp(value: str, field_name: str) -> tuple[datetime, str]:
    """Parse an ISO-8601 UTC timestamp and return its canonical seconds form."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty ISO-8601 UTC timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"{field_name} must be a valid ISO-8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset().total_seconds() != 0:
        raise ValueError(f"{field_name} must use UTC")
    normalized = parsed.astimezone(timezone.utc)
    return normalized, normalized.isoformat(timespec="seconds").replace("+00:00", "Z")


def _current_utc_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def get_artifact_text(artifact_rel_path: str, row_idx: int | None = None) -> tuple[str, str, str]:
    """Load text, artifact_id, and sha256 from artifact path."""
    full_path = REPO_ROOT / artifact_rel_path
    if not full_path.exists():
        raise FileNotFoundError(f"Artifact not found: {full_path}")
    
    raw_bytes = full_path.read_bytes()
    file_sha256 = hashlib.sha256(raw_bytes).hexdigest()

    if artifact_rel_path.endswith("manifest.json") and row_idx is not None:
        manifest = json.loads(raw_bytes.decode("utf-8"))
        row = manifest["rows"][row_idx]
        filtered_text = row["extracted"]["filtered_text"]
        artifact_id = f"artifact_sw_{manifest.get('run_id', '20261108T080001')}_{row_idx}"
        return filtered_text, artifact_id, file_sha256

    text = raw_bytes.decode("utf-8")
    slug = artifact_rel_path.replace("/", "_").replace(".", "_")
    artifact_id = f"artifact_{slug}"
    return text, artifact_id, file_sha256


def _evidence_basis_for_source(source_id: str) -> str:
    """Return source form, not a reliability or truth score."""
    if source_id in {
        "src_mvs_briefing", "src_ngu_press", "src_mvs_inquiry", "src_ombudsman",
        "src_dbr_proceedings", "src_npu_130_persons",
    }:
        return "institutional_statement"
    if source_id in {"src_suspilne_court", "src_hromadske_ladyka", "src_interfax_ova_fire_early_update"}:
        return "secondary_reporting"
    if source_id == "src_telegram_padla_tck":
        return "social_media_post"
    if source_id == "src_tiktok_fire_analysis":
        return "user_comment"
    return "unknown"


def build_passages_bundle() -> tuple[list[dict], dict[str, dict]]:
    """Build the official passage catalogue with exact character offsets."""
    manifest_rel = "data/raw/source_watch/20261108T080001.749114Z/manifest.json"
    geo_fire_rel = "data/processed/geographic_fire_candidates.jsonl"
    web_check_rel = "reports/source-watch/20261108/official-web-check.md"
    fig_proc_rel = "reports/figures-and-proceedings-2026-11-06.md"
    tiktok_fire_rel = "reports/tiktok-fire/comment_candidate_review.md"
    fire_source_review_rel = "reports/source-watch/fire-source-review-2026-11-09.md"

    # Pre-load texts
    mvs_briefing_text, mvs_briefing_art, mvs_briefing_sha = get_artifact_text(manifest_rel, row_idx=4)
    ngu_press_text, ngu_press_art, ngu_press_sha = get_artifact_text(manifest_rel, row_idx=5)
    suspilne_text, suspilne_art, suspilne_sha = get_artifact_text(manifest_rel, row_idx=7)
    hromadske_text, hromadske_art, hromadske_sha = get_artifact_text(manifest_rel, row_idx=1)
    mvs_inquiry_text, mvs_inquiry_art, mvs_inquiry_sha = get_artifact_text(manifest_rel, row_idx=2)
    ombudsman_text, ombudsman_art, ombudsman_sha = get_artifact_text(manifest_rel, row_idx=6)
    geo_fire_text, geo_fire_art, geo_fire_sha = get_artifact_text(geo_fire_rel)
    web_check_text, web_check_art, web_check_sha = get_artifact_text(web_check_rel)
    fig_proc_text, fig_proc_art, fig_proc_sha = get_artifact_text(fig_proc_rel)
    tiktok_fire_text, tiktok_fire_art, tiktok_fire_sha = get_artifact_text(tiktok_fire_rel)
    fire_source_review_text, fire_source_review_art, fire_source_review_sha = get_artifact_text(fire_source_review_rel)

    passages_specs = [
        # MVS Briefing passages
        {
            "passage_id": "psg_mvs_26_occupants",
            "source_id": "src_mvs_briefing",
            "source_uri": "https://mvs.gov.ua/news/u-ministerstvi-vnutrisnix-sprav-ukrayini-vidbuvsia-brifing-shhodo-podii-na-kiyivshhini",
            "captured_at_utc": "2026-11-08T08:05:55Z",
            "independent_root_id": "root_mvs_official",
            "lineage_family_id": "family_mvs_official",
            "artifact_id": mvs_briefing_art,
            "artifact_sha256": mvs_briefing_sha,
            "container_text": mvs_briefing_text,
            "passage_text": "Загалом у приміщенні перебували 26 осіб.",
        },
        {
            "passage_id": "psg_mvs_4_szch",
            "source_id": "src_mvs_briefing",
            "source_uri": "https://mvs.gov.ua/news/u-ministerstvi-vnutrisnix-sprav-ukrayini-vidbuvsia-brifing-shhodo-podii-na-kiyivshhini",
            "captured_at_utc": "2026-11-08T08:05:55Z",
            "independent_root_id": "root_mvs_official",
            "lineage_family_id": "family_mvs_official",
            "artifact_id": mvs_briefing_art,
            "artifact_sha256": mvs_briefing_sha,
            "container_text": mvs_briefing_text,
            "passage_text": "За словами командувача, четверо з них були військовослужбовцями, які самовільно залишили військову частину, решта готувалися до направлення на базову загальновійськову підготовку.",
        },
        {
            "passage_id": "psg_mvs_ngu_lease",
            "source_id": "src_mvs_briefing",
            "source_uri": "https://mvs.gov.ua/news/u-ministerstvi-vnutrisnix-sprav-ukrayini-vidbuvsia-brifing-shhodo-podii-na-kiyivshhini",
            "captured_at_utc": "2026-11-08T08:05:55Z",
            "independent_root_id": "root_mvs_official",
            "lineage_family_id": "family_mvs_official",
            "artifact_id": mvs_briefing_art,
            "artifact_sha256": mvs_briefing_sha,
            "container_text": mvs_briefing_text,
            "passage_text": "будівля, навколо якої виник конфлікт, перебувала в офіційній оренді Нацгвардії та використовувалася для тимчасового розміщення військовослужбовців.",
        },
        {
            "passage_id": "psg_mvs_ngu_unit_3121",
            "source_id": "src_mvs_briefing",
            "source_uri": "https://mvs.gov.ua/news/u-ministerstvi-vnutrisnix-sprav-ukrayini-vidbuvsia-brifing-shhodo-podii-na-kiyivshhini",
            "captured_at_utc": "2026-11-08T08:05:55Z",
            "independent_root_id": "root_mvs_official",
            "lineage_family_id": "family_mvs_official",
            "artifact_id": mvs_briefing_art,
            "artifact_sha256": mvs_briefing_sha,
            "container_text": mvs_briefing_text,
            "passage_text": "Командувач Національної гвардії України генерал-майор Олександр Півненко пояснив",
        },
        # NGU Press release passages
        {
            "passage_id": "psg_ngu_4_injured",
            "source_id": "src_ngu_press",
            "source_uri": "https://ngu.gov.ua/shturm-kativni-pid-vybuhy-shahediv-yak-fejk-pro-40-zaruchnykiv-pereris-u-zavorushennya-v-petropavlivskij-borshhagivczi/",
            "captured_at_utc": "2026-11-08T08:05:55Z",
            "independent_root_id": "root_ngu_official",
            "lineage_family_id": "family_ngu_official",
            "artifact_id": ngu_press_art,
            "artifact_sha256": ngu_press_sha,
            "container_text": ngu_press_text,
            "passage_text": "Водночас четверо військовослужбовців справді мали травми. Цього в «Азові» не заперечували – чоловіків направили до госпіталю.",
        },
        {
            "passage_id": "psg_ngu_walked_independently",
            "source_id": "src_ngu_press",
            "source_uri": "https://ngu.gov.ua/shturm-kativni-pid-vybuhy-shahediv-yak-fejk-pro-40-zaruchnykiv-pereris-u-zavorushennya-v-petropavlivskij-borshhagivczi/",
            "captured_at_utc": "2026-11-08T08:05:55Z",
            "independent_root_id": "root_ngu_official",
            "lineage_family_id": "family_ngu_official",
            "artifact_id": ngu_press_art,
            "artifact_sha256": ngu_press_sha,
            "container_text": ngu_press_text,
            "passage_text": "всі четверо самостійно дійшли до автомобіля швидкої допомоги. Чи застосовували до них насильство, за яких обставин вони дістали травми та хто може бути причетний – має встановити слідство.",
        },
        {
            "passage_id": "psg_ngu_hostages_40_refuted",
            "source_id": "src_ngu_press",
            "source_uri": "https://ngu.gov.ua/shturm-kativni-pid-vybuhy-shahediv-yak-fejk-pro-40-zaruchnykiv-pereris-u-zavorushennya-v-petropavlivskij-borshhagivczi/",
            "captured_at_utc": "2026-11-08T08:05:55Z",
            "independent_root_id": "root_ngu_official",
            "lineage_family_id": "family_ngu_official",
            "artifact_id": ngu_press_art,
            "artifact_sha256": ngu_press_sha,
            "container_text": ngu_press_text,
            "passage_text": "Поліція спростувала повідомлення про 40 незаконно утримуваних людей і загиблого, проте натовп продовжував вимагати відчинити ворота військового об’єкта.",
        },
        {
            "passage_id": "psg_ngu_spine_refuted",
            "source_id": "src_ngu_press",
            "source_uri": "https://ngu.gov.ua/shturm-kativni-pid-vybuhy-shahediv-yak-fejk-pro-40-zaruchnykiv-pereris-u-zavorushennya-v-petropavlivskij-borshhagivczi/",
            "captured_at_utc": "2026-11-08T08:05:55Z",
            "independent_root_id": "root_ngu_official",
            "lineage_family_id": "family_ngu_official",
            "artifact_id": ngu_press_art,
            "artifact_sha256": ngu_press_sha,
            "container_text": ngu_press_text,
            "passage_text": "Руслан Музичук спростував розповіді про лежачого чоловіка з переламаним хребтом. За його словами, всі четверо самостійно дійшли до автомобіля швидкої допомоги.",
        },
        {
            "passage_id": "psg_ngu_police_arrival_ambulance_call",
            "source_id": "src_ngu_press",
            "source_uri": "https://ngu.gov.ua/shturm-kativni-pid-vybuhy-shahediv-yak-fejk-pro-40-zaruchnykiv-pereris-u-zavorushennya-v-petropavlivskij-borshhagivczi/",
            "captured_at_utc": "2026-11-08T08:05:55Z",
            "independent_root_id": "root_ngu_official",
            "lineage_family_id": "family_ngu_official",
            "artifact_id": ngu_press_art,
            "artifact_sha256": ngu_press_sha,
            "container_text": ngu_press_text,
            "passage_text": "Саме працівники приватної швидкої, за повідомленням поліції Київщини, викликали правоохоронців, заявивши, що їм перешкоджають дістатися до людини, яка потребує допомоги.",
        },
        # Suspilne Court Report passages
        {
            "passage_id": "psg_suspilne_ladyka_59_days",
            "source_id": "src_suspilne_court",
            "source_uri": "https://suspilne.media/kyiv/1446145-suticki-v-borsanivci-sud-obirae-zapobiznij-cetvertij-pidozruvanij/",
            "captured_at_utc": "2026-11-08T08:00:01Z",
            "independent_root_id": "root_suspilne_court_journalism",
            "lineage_family_id": "family_suspilne_journalism",
            "artifact_id": suspilne_art,
            "artifact_sha256": suspilne_sha,
            "container_text": suspilne_text,
            "passage_text": "застосувати для Ладиги тримання під вартою на 59 днів і із заставою у 20 прожиткових мінімумів працездатних осіб — 66 тисяч гривень.",
        },
        {
            "passage_id": "psg_suspilne_parshonkov_hammer",
            "source_id": "src_suspilne_court",
            "source_uri": "https://suspilne.media/kyiv/1446145-suticki-v-borsanivci-sud-obirae-zapobiznij-cetvertij-pidozruvanij/",
            "captured_at_utc": "2026-11-08T08:00:01Z",
            "independent_root_id": "root_suspilne_court_journalism",
            "lineage_family_id": "family_suspilne_journalism",
            "artifact_id": suspilne_art,
            "artifact_sha256": suspilne_sha,
            "container_text": suspilne_text,
            "passage_text": "Слідство встановило, що Іван Паршонков дізнався про блокування підрозділу Нацгвардії та вирішив долучитися до нього. Як повідомили у Київській обласній прокуратурі, підозрюваний заздалегідь придбав важкий молот із довгою рукояткою, яким згодом завдавав ударів по службовому автомобілю, всередині якого перебували військовослужбовці.",
        },
        {
            "passage_id": "psg_suspilne_130_identified",
            "source_id": "src_suspilne_court",
            "source_uri": "https://suspilne.media/kyiv/1446145-suticki-v-borsanivci-sud-obirae-zapobiznij-cetvertij-pidozruvanij/",
            "captured_at_utc": "2026-11-08T08:00:01Z",
            "independent_root_id": "root_suspilne_court_journalism",
            "lineage_family_id": "family_suspilne_journalism",
            "artifact_id": suspilne_art,
            "artifact_sha256": suspilne_sha,
            "container_text": suspilne_text,
            "passage_text": "5 листопада у Нацполіції повідомили, що встановили 130 осіб , які можуть бути причетними до заворушень на Петропавлівській Борщагівці.",
        },
        {
            "passage_id": "psg_suspilne_moloda_custody",
            "source_id": "src_suspilne_court",
            "source_uri": "https://suspilne.media/kyiv/1446145-suticki-v-borsanivci-sud-obirae-zapobiznij-cetvertij-pidozruvanij/",
            "captured_at_utc": "2026-11-08T08:00:01Z",
            "independent_root_id": "root_suspilne_court_journalism",
            "lineage_family_id": "family_suspilne_journalism",
            "artifact_id": suspilne_art,
            "artifact_sha256": suspilne_sha,
            "container_text": suspilne_text,
            "passage_text": "обрали запобіжний захід для двох фігуранток сутичок у Петропавлівській Борщагівці — Валентини Молодої і Тетяна Кірєєвої , а сьогодні, 5 листопада, для Віктора Єни . Усіх трьох суд відправив під варту на два місяці без права на заставу.",
        },
        {
            "passage_id": "psg_suspilne_yena_custody",
            "source_id": "src_suspilne_court",
            "source_uri": "https://suspilne.media/kyiv/1446145-suticki-v-borsanivci-sud-obirae-zapobiznij-cetvertij-pidozruvanij/",
            "captured_at_utc": "2026-11-08T08:00:01Z",
            "independent_root_id": "root_suspilne_court_journalism",
            "lineage_family_id": "family_suspilne_journalism",
            "artifact_id": suspilne_art,
            "artifact_sha256": suspilne_sha,
            "container_text": suspilne_text,
            "passage_text": "а сьогодні, 5 листопада, для Віктора Єни . Усіх трьох суд відправив під варту на два місяці без права на заставу.",
        },
        # hromadske report passages
        {
            "passage_id": "psg_hromadske_ladyka_bail_66560",
            "source_id": "src_hromadske_ladyka",
            "source_uri": "https://hromadske.ua/kryminal/273906-sud-obyraye-zapobiznyy-zakhid-22-richniy-zintsi-iaka-brala-uchast-u-sutychkakh-u-sofiyivskiy-borshchahivtsi",
            "captured_at_utc": "2026-11-08T08:00:01Z",
            "independent_root_id": "root_hromadske_journalism",
            "lineage_family_id": "family_hromadske_journalism",
            "artifact_id": hromadske_art,
            "artifact_sha256": hromadske_sha,
            "container_text": hromadske_text,
            "passage_text": "Суд відправив жінку під варту з можливістю внесення застави розміром 66 560 гривень.",
        },
        {
            "passage_id": "psg_hromadske_ladyka_art_114_1",
            "source_id": "src_hromadske_ladyka",
            "source_uri": "https://hromadske.ua/kryminal/273906-sud-obyraye-zapobiznyy-zakhid-22-richniy-zintsi-iaka-brala-uchast-u-sutychkakh-u-sofiyivskiy-borshchahivtsi",
            "captured_at_utc": "2026-11-08T08:00:01Z",
            "independent_root_id": "root_hromadske_journalism",
            "lineage_family_id": "family_hromadske_journalism",
            "artifact_id": hromadske_art,
            "artifact_sha256": hromadske_sha,
            "container_text": hromadske_text,
            "passage_text": "Валерію Ладику підозрюють у перешкоджанні законній діяльності Збройних сил України та інших військових формувань в особливий період — ч. 1 ст. 114-1 Кримінального кодексу України.",
        },
        {
            "passage_id": "psg_hromadske_ladyka_age_22",
            "source_id": "src_hromadske_ladyka",
            "source_uri": "https://hromadske.ua/kryminal/273906-sud-obyraye-zapobiznyy-zakhid-22-richniy-zintsi-iaka-brala-uchast-u-sutychkakh-u-sofiyivskiy-borshchahivtsi",
            "captured_at_utc": "2026-11-08T08:00:01Z",
            "independent_root_id": "root_hromadske_journalism",
            "lineage_family_id": "family_hromadske_journalism",
            "artifact_id": hromadske_art,
            "artifact_sha256": hromadske_sha,
            "container_text": hromadske_text,
            "passage_text": "«Побачила відео в TikTok і прийшла». Суд відправив під варту 22-річну жінку, яка брала участь у сутичках у Петропавлівській Борщагівці",
        },
        # MVS inquiry passages
        {
            "passage_id": "psg_mvs_inquiry_ordered",
            "source_id": "src_mvs_inquiry",
            "source_uri": "https://mvs.gov.ua/news/mvs-ziasovuje-obstavini-podii-na-kiyivshhini-rozpocato-sluzbove-rozsliduvannia",
            "captured_at_utc": "2026-11-08T08:00:01Z",
            "independent_root_id": "root_mvs_official",
            "lineage_family_id": "family_mvs_official",
            "artifact_id": mvs_inquiry_art,
            "artifact_sha256": mvs_inquiry_sha,
            "container_text": mvs_inquiry_text,
            "passage_text": "МВС з’ясовує обставини подій на Київщині: розпочато службове розслідування",
        },
        # Ombudsman passages
        {
            "passage_id": "psg_ombudsman_inquiries",
            "source_id": "src_ombudsman",
            "source_uri": "https://ombudsman.gov.ua/news_details/zhodnih-podvijnih-standartiv-ne-maye-buti-ombudsman-vimagaye-perevirki-situaciyi-na-petropavlivskij-borshchagivci",
            "captured_at_utc": "2026-11-08T08:00:01Z",
            "independent_root_id": "root_ombudsman_official",
            "lineage_family_id": "family_ombudsman_official",
            "artifact_id": ombudsman_art,
            "artifact_sha256": ombudsman_sha,
            "container_text": ombudsman_text,
            "passage_text": "У зв’язку з інцидентом у Петропавлівській Борщагівці Уповноважений Дмитро Лубінець вже направив запити до всіх правоохоронних органів",
        },
        # DBR proceedings passage (web-check artifact)
        {
            "passage_id": "psg_dbr_art_426_1",
            "source_id": "src_dbr_proceedings",
            "source_uri": "https://dbr.gov.ua/news/dbr-rozpochalo-kriminalne-provadzhennya-za-faktom-podij-u-petropavlivskij-borshhagivci-na-kiivshhini",
            "captured_at_utc": "2026-11-08T08:00:01Z",
            "independent_root_id": "root_dbr_official",
            "lineage_family_id": "family_dbr_official",
            "artifact_id": web_check_art,
            "artifact_sha256": web_check_sha,
            "container_text": web_check_text,
            "passage_text": "ДБР, повідомлення від 3 листопада 2026 року.** Офіційна сторінка повідомляє про початок провадження за ч. 5 ст. 426-1 КК України",
        },
        # NPU 27 active participants passage (figures & proceedings artifact)
        {
            "passage_id": "psg_npu_27_active",
            "source_id": "src_npu_130_persons",
            "source_uri": "https://npu.gov.ua/news/politseiski-natsionalnoi-politsii-ukrainy-razom-z-sbu-vzhe-vstanovyly-130-osib-iaki-mozhut-buty-prychetnymy-do-zavorushen-na-petropavlivskii-borshhagivtsi",
            "captured_at_utc": "2026-11-08T08:00:01Z",
            "independent_root_id": "root_npu_national_official",
            "lineage_family_id": "family_npu_official",
            "artifact_id": fig_proc_art,
            "artifact_sha256": fig_proc_sha,
            "container_text": fig_proc_text,
            "passage_text": "Поліція повідомила, що встановила 130 людей, які можуть бути причетними; серед них 27, за оцінкою поліції, брали активну участь у протиправних діях, ще 24 поводилися агресивно або підбурювали.",
        },
        # padla_tck fire prediction passage (geographic fire candidates)
        {
            "passage_id": "psg_padla_tck_fire_prediction",
            "source_id": "src_telegram_padla_tck",
            "source_uri": "https://t.me/padla_tck/38019",
            "captured_at_utc": "2026-11-05T10:10:44Z",
            "independent_root_id": "root_padla_tck_telegram",
            "lineage_family_id": "family_padla_tck_telegram",
            "artifact_id": "artifact_data_processed_geographic_fire_candidates_jsonl_line_5",
            "artifact_sha256": geo_fire_sha,
            "container_text": geo_fire_text,
            "passage_text": "От я ні разу не здивуюсь, якщо зараз ще й будівля спалахне разом з закатованими людьми,  щоб не було де шукати докази.",
        },
        # Interfax's report of the early OVA-head statement; the original post
        # is linked but was not captured locally, so this is secondary evidence.
        {
            "passage_id": "psg_bucha_warehouse_fire",
            "source_id": "src_interfax_ova_fire_early_update",
            "source_uri": "https://interfax.com.ua/news/general/1231365.html",
            "captured_at_utc": "2026-11-09T12:00:00Z",
            "independent_root_id": "root_interfax_reporting",
            "lineage_family_id": "family_interfax_reporting",
            "artifact_id": fire_source_review_art,
            "artifact_sha256": fire_source_review_sha,
            "container_text": fire_source_review_text,
            "passage_text": "У Бучанському районі внаслідок ворожої атаки сталося займання на території складу. Уточнюємо інформацію щодо постраждалих",
            "evidence_basis": "secondary_reporting",
        },
        # TikTok fire video mismatch passage (tiktok fire review)
        {
            "passage_id": "psg_tiktok_fire_mismatch",
            "source_id": "src_tiktok_fire_analysis",
            "source_uri": "https://www.tiktok.com/@anastasiyapalivoda/video/7704443960013376789",
            "captured_at_utc": "2026-11-05T13:00:00Z",
            "independent_root_id": "root_tiktok_spatial_analysis",
            "lineage_family_id": "family_fire_verification",
            "artifact_id": tiktok_fire_art,
            "artifact_sha256": tiktok_fire_sha,
            "container_text": tiktok_fire_text,
            "passage_text": "розрізняє Софіївську й Петропавлівську — **географічне виправлення**.",
        },
        # Institutional presence - NGU unit 3121 presence (context refuting TCK)
        {
            "passage_id": "psg_mvs_ngu_brigade_31",
            "source_id": "src_mvs_briefing",
            "source_uri": "https://mvs.gov.ua/news/u-ministerstvi-vnutrisnix-sprav-ukrayini-vidbuvsia-brifing-shhodo-podii-na-kiyivshhini",
            "captured_at_utc": "2026-11-08T08:05:55Z",
            "independent_root_id": "root_mvs_official",
            "lineage_family_id": "family_mvs_official",
            "artifact_id": mvs_briefing_art,
            "artifact_sha256": mvs_briefing_sha,
            "container_text": mvs_briefing_text,
            "passage_text": "перебувала в офіційній оренді Нацгвардії та використовувалася для тимчасового розміщення військовослужбовців. Загалом у приміщенні перебували 26 осіб.",
        },
    ]

    passages = []
    passages_by_id = {}
    for spec in passages_specs:
        text = spec["container_text"]
        target = spec["passage_text"]
        start_offset = text.find(target)
        if start_offset == -1:
            # Handle ellipsis or minor formatting in target
            first_clause = target.split("...")[0].strip()
            start_offset = text.find(first_clause)
            if start_offset == -1:
                raise ValueError(f"Could not locate passage text for {spec['passage_id']}: {target[:40]}")
            end_offset = start_offset + len(first_clause)
            actual_text = text[start_offset:end_offset]
        else:
            end_offset = start_offset + len(target)
            actual_text = text[start_offset:end_offset]

        p = {
            "passage_id": spec["passage_id"],
            "source_id": spec["source_id"],
            "source_uri": spec["source_uri"],
            "artifact_id": spec["artifact_id"],
            "artifact_sha256": spec["artifact_sha256"],
            "captured_at_utc": spec["captured_at_utc"],
            "text": actual_text,
            "artifact_start_offset": start_offset,
            "artifact_end_offset": end_offset,
            "offset_unit": "unicode_codepoint",
            "independent_root_id": spec["independent_root_id"],
            "lineage_family_id": spec["lineage_family_id"],
            "evidence_basis": spec.get("evidence_basis") or _evidence_basis_for_source(spec["source_id"]),
        }
        passages.append(p)
        passages_by_id[spec["passage_id"]] = p

    return passages, passages_by_id


def build_core_claims_spec() -> list[dict]:
    """Return catalogue of 25 prioritized core claims for Petropavlivska Borshchahivka."""
    return [
        # --- Блок 1: Травми, потерпілі та «заручники» ---
        {
            "claim_id": "claim_core_01_hostages_40",
            "category": "injuries_and_victims",
            "statement": "У приміщенні у Петропавлівській Борщагівці незаконно утримували 40 осіб",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "physical_fact", "topic": "hostages_count"},
            "key_values": {"hostages_count": {"value": 40, "operator": "eq"}},
            "query_variants": ["незаконно утримували 40 людей", "40 заручників Петропавлівська Борщагівка"],
            "rationale": "Офіційні матеріали НГУ та Нацполіції прямо спростували повідомлення про утримання 40 осіб; МВС заявило про перебування 26 осіб загалом (спростування в межах офіційних заяв правоохоронців).",
        },
        {
            "claim_id": "claim_core_02_killed_citizen",
            "category": "injuries_and_victims",
            "statement": "Під час подій у Петропавлівській Борщагівці загинув громадянин",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "physical_fact", "topic": "fatalities"},
            "key_values": {},
            "query_variants": ["загинув громадянин Петропавлівська Борщагівка", "поліція спростувала загиблого"],
            "rationale": "Офіційна заява поліції Київщини та повідомлення НГУ прямо спростували наявність загиблих під час конфлікту.",
        },
        {
            "claim_id": "claim_core_03_broken_spine",
            "category": "injuries_and_victims",
            "statement": "В одного з військовослужбовців у будівлі було зафіксовано перелом хребта",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "medical_claim", "topic": "severe_injuries"},
            "key_values": {"injury_victim_count": {"value": 1, "operator": "eq"}},
            "query_variants": ["чоловік з переламаним хребтом", "Руслан Музичук спростував хребет"],
            "rationale": "Пресофіцер НГУ полковник Руслан Музичук усно спростував розповіді про зламаний хребет; однак офіційні висновки клінічної судово-медичної експертизи відсутні (insufficient_evidence для клінічного діагнозу).",
        },
        {
            "claim_id": "claim_core_04_ngu_four_injured",
            "category": "injuries_and_victims",
            "statement": "Чотири військовослужбовці Національної гвардії України отримали травми під час інциденту",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "official_statement", "topic": "ngu_injuries"},
            "key_values": {"injured_ngu_count": {"value": 4, "operator": "eq"}},
            "query_variants": ["четверо військовослужбовців справді мали травми", "травми військових госпіталь"],
            "rationale": "Офіційне повідомлення НГУ підтверджує наявність травм у 4 бійців та госпіталізацію, проте прямо наголошує, що обставини та час травмування має встановити слідство; причинність сутичок залишається на стадії перевірки (insufficient_evidence).",
        },
        {
            "claim_id": "claim_core_05_ngu_walked_independently",
            "category": "injuries_and_victims",
            "statement": "Травмовані військовослужбовці НГУ самостійно дійшли до карети швидкої допомоги",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "official_statement", "topic": "medical_evacuation"},
            "key_values": {},
            "query_variants": ["всі четверо самостійно дійшли автомобіля швидкої", "самостійно дійшли швидкої допомоги"],
            "rationale": "Пресофіцер НГУ заявив, що всі четверо травмованих військовослужбовців пересувалися та дійшли до карети швидкої самостійно.",
        },

        # --- Блок 2: Будівля та обставини перебування ---
        {
            "claim_id": "claim_core_06_building_26_persons",
            "category": "building_circumstances",
            "statement": "За заявою МВС, загалом у приміщенні перебували 26 осіб",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "official_statement", "topic": "building_occupants"},
            "key_values": {"total_occupants_count": {"value": 26, "operator": "eq"}},
            "query_variants": ["Загалом у приміщенні перебували 26 осіб", "26 осіб приміщення МВС"],
            "rationale": "На брифінгу МВС 3 листопада командувач НГУ Олександр Півненко офіційно заявив про перебування 26 осіб у будівлі.",
        },
        {
            "claim_id": "claim_core_07_building_4_szch",
            "category": "building_circumstances",
            "statement": "Серед осіб у приміщенні 4 військових самовільно залишили частину",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "official_statement", "topic": "szch_count"},
            "key_values": {"szch_count": {"value": 4, "operator": "eq"}},
            "query_variants": ["четверо з них самовільно залишили військову частину", "військовослужбовці самовільно залишили частину"],
            "rationale": "Офіційний брифінг МВС підтвердив, що четверо військових серед присутніх у будівлі самовільно залишили військову частину (СЗЧ).",
        },
        {
            "claim_id": "claim_core_08_building_ngu_lease",
            "category": "building_circumstances",
            "statement": "Будівля перебувала в офіційній оренді Національної гвардії України як тимчасовий пункт",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "official_statement", "topic": "building_legal_status"},
            "key_values": {},
            "query_variants": ["будівля перебувала в офіційній оренді Нацгвардії", "оренда Нацгвардії тимчасове розміщення"],
            "rationale": "Керівництво МВС та командувач НГУ підтвердили правовий статус будівлі як об'єкта в офіційній оренді Національної гвардії України.",
        },

        # --- Блок 3: Процесуальні статуси та судові заходи ---
        {
            "claim_id": "claim_core_09_npu_130_identified",
            "category": "procedural_status",
            "statement": "Поліція разом із СБУ встановили 130 осіб, які можуть бути причетними до заворушень",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "official_statement", "topic": "identified_participants"},
            "key_values": {"identified_persons_count": {"value": 130, "operator": "eq"}},
            "query_variants": ["встановили 130 осіб які можуть бути причетними", "130 осіб заворушення Петропавлівська Борщагівка"],
            "rationale": "Офіційне повідомлення Нацполіції від 5 листопада та судове висвітлення Суспільного підтвердили встановлення 130 осіб.",
        },
        {
            "claim_id": "claim_core_10_npu_27_active",
            "category": "procedural_status",
            "statement": "За оцінкою поліції, 27 встановлених осіб брали активну участь у протиправних діях",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "official_statement", "topic": "active_participants"},
            "key_values": {"active_participants_count": {"value": 27, "operator": "eq"}},
            "query_variants": ["27 брали активну участь протиправних діях", "поліція 27 активну участь"],
            "rationale": "Оперативне зведення Нацполіції класифікувало 27 осіб як активних учасників протиправних дій під час конфлікту.",
        },
        {
            "claim_id": "claim_core_11_court_ladyka_custody",
            "category": "procedural_status",
            "statement": "Солом'янський районний суд застосував до Валерії Ладики тримання під вартою на 59 днів",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "court_reporting", "topic": "preventive_measure_ladyka"},
            "key_values": {"custody_days_count": {"value": 59, "operator": "eq"}},
            "query_variants": ["застосувати для Ладиги тримання під вартою на 59 днів", "Ладика 59 днів варта"],
            "rationale": "Судові кореспонденти Суспільного із зали суду підтвердили обрання запобіжного заходу у вигляді 59 днів під вартою для Ладики.",
        },
        {
            "claim_id": "claim_core_12_court_ladyka_bail",
            "category": "procedural_status",
            "statement": "Суд визначив для Валерії Ладики альтернативу застави у розмірі 66560 гривень",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "court_reporting", "topic": "bail_amount_ladyka"},
            "key_values": {"bail_amount_uah": {"value": 66560, "operator": "eq"}},
            "query_variants": ["застави розміром 66 560 гривень", "Ладика застава 66560 гривень"],
            "rationale": "Репортаж hromadske із Солом'янського райсуду Києва зафіксував визначення альтернативи застави у розмірі 66 560 грн.",
        },
        {
            "claim_id": "claim_core_13_court_ladyka_art_114_1",
            "category": "procedural_status",
            "statement": "Валерії Ладиці повідомлено про підозру за ч. 1 ст. 114-1 КК України",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "court_reporting", "topic": "criminal_code_article_ladyka"},
            "key_values": {"article_number": {"value": 114, "operator": "eq"}, "part_number": {"value": 1, "operator": "eq"}},
            "query_variants": ["Ладику підозрюють ч. 1 ст. 114-1", "перешкоджанні законній діяльності 114-1"],
            "rationale": "Слідство та прокуратура оголосили Валерії Ладиці підозру у вчиненні кримінального правопорушення за ч. 1 ст. 114-1 КК України.",
        },
        {
            "claim_id": "claim_core_14_court_moloda_no_bail",
            "category": "procedural_status",
            "statement": "Суд обрав Валентині Молодій запобіжний захід у вигляді тримання під вартою без застави",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "court_reporting", "topic": "preventive_measure_moloda"},
            "key_values": {},
            "query_variants": ["Валентини Молодої під варту без права на заставу", "Молода суд запобіжний захід"],
            "rationale": "Солом'янський районний суд Києва 4 листопада відправив Валентину Молоду під варту без можливості внесення застави.",
        },
        {
            "claim_id": "claim_core_15_court_kireyeva_no_bail",
            "category": "procedural_status",
            "statement": "Суд обрав Тетяні Кірєєвій запобіжний захід у вигляді тримання під вартою без застави",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "court_reporting", "topic": "preventive_measure_kireyeva"},
            "key_values": {},
            "query_variants": ["Тетяна Кірєєвої під варту без права на заставу", "Кірєєва запобіжний захід варта"],
            "rationale": "4 листопада суд обрав Тетяні Кірєєвій запобіжний захід у вигляді тримання під вартою без права застави.",
        },
        {
            "claim_id": "claim_core_16_court_yena_custody_60",
            "category": "procedural_status",
            "statement": "Солом'янський районний суд Києва обрав Віктору Єні тримання під вартою на 60 днів без застави",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "court_reporting", "topic": "preventive_measure_yena"},
            "key_values": {"custody_days_count": {"value": 60, "operator": "eq"}},
            "query_variants": ["Віктора Єни під варту на два місяці без права на заставу", "Єна запобіжний захід 60 днів"],
            "rationale": "5 листопада суд призначив Віктору Єні 60 днів (два місяці) тримання під вартою без альтернативи застави.",
        },
        {
            "claim_id": "claim_core_17_parshonkov_hammer_suspicion",
            "category": "procedural_status",
            "statement": "Іван Паршонков придбав молот та завдавав ним ударів по службовому автомобілю з військовослужбовцями",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "court_reporting", "topic": "parshonkov_actions"},
            "key_values": {},
            "query_variants": ["Іван Паршонков завдавав ударів по службовому автомобілю", "Паршонков підозра молот"],
            "rationale": "Прокуратура та Суспільне повідомили про підозру Івану Паршонкову, який придбав важкий молот і завдавав ударів по авто з бійцями НГУ.",
        },
        {
            "claim_id": "claim_core_18_dbr_proceedings_426_1",
            "category": "procedural_status",
            "statement": "ДБР відкрило кримінальне провадження за ч. 5 ст. 426-1 КК України за фактом подій",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "official_statement", "topic": "dbr_investigation"},
            "key_values": {"article_number": {"value": 426, "operator": "eq"}, "part_number": {"value": 5, "operator": "eq"}, "article_subnumber": {"value": 1, "operator": "eq"}},
            "query_variants": ["ДБР провадження ч. 5 ст. 426-1", "Державне бюро розслідувань 426-1"],
            "rationale": "Державне бюро розслідувань 3 листопада розпочало провадження за фактом можливого перевищення повноважень військовими за ч. 5 ст. 426-1 КК.",
        },
        {
            "claim_id": "claim_core_19_ombudsman_inquiry",
            "category": "procedural_status",
            "statement": "Уповноважений ВРУ з прав людини направив запити до правоохоронних органів щодо ситуації",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "official_statement", "topic": "ombudsman_inquiry"},
            "key_values": {},
            "query_variants": ["Уповноважений Дмитро Лубінець вже направив запити", "Омбудсман вимагає перевірки ситуації"],
            "rationale": "Омбудсман Дмитро Лубінець 3 листопада публічно підтвердив направлення запитів до органів правопорядку для з'ясування обставин перебування військових.",
        },
        {
            "claim_id": "claim_core_20_mvs_service_investigation",
            "category": "procedural_status",
            "statement": "МВС України розпочало службове розслідування за фактом подій на Київщині",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "official_statement", "topic": "mvs_inquiry"},
            "key_values": {},
            "query_variants": ["МВС обставини подій розпочато службове розслідування", "доручив розпочати службове розслідування"],
            "rationale": "Міністр внутрішніх справ Іван Вигівський заявив про наказ розпочати службове розслідування щодо дій підрозділів НГУ та поліції.",
        },

        # --- Блок 4: Пожежа, таймінг та дезінформаційні наративи ---
        {
            "claim_id": "claim_core_21_fire_padla_tck_prediction",
            "category": "fire_and_timing",
            "statement": "Канал padla_tck поширив твердження, що будівля може спалахнути для знищення доказів",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "social_media_mention", "topic": "fire_prediction"},
            "key_values": {},
            "query_variants": ["будівля спалахне разом закатованими людьми", "падла тцк будівля спалахне знищення докази"],
            "rationale": "У Telegram-каналі padla_tck 02.11 о 18:08 зафіксовано публікацію з випереджальним наративом про нібито неминучий підпал будівлі для приховування слідів.",
        },
        {
            "claim_id": "claim_core_22_fire_bucha_warehouse",
            "category": "fire_and_timing",
            "statement": "У Бучанському районі після ворожої атаки сталося займання на території складу, дані про постраждалих уточнювали",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "reported_statement", "topic": "bucha_warehouse_fire_early_update"},
            "key_values": {},
            "query_variants": ["пожежа на складському об'єкті внаслідок атаки БпЛА", "пожежа склад атака шахед"],
            "rationale": "Інтерфакс о 00:05 5 листопада переказав раннє повідомлення голови Київської ОВА про займання складу після атаки; це твердження у вторинному джерелі, а не повне захоплення первинного допису чи остаточний висновок про місце та постраждалих.",
        },
        {
            "claim_id": "claim_core_23_fire_video_location_mismatch",
            "category": "fire_and_timing",
            "statement": "TikTok-відео з написом «Софіївська Борщагівка» зображує пожежу окремого складу, а не будівлі НГУ",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "media_verification", "topic": "fire_location"},
            "key_values": {},
            "query_variants": ["розрізняє Софіївську й Петропавлівську географічне виправлення", "відео склад Софіївська Борщагівка"],
            "rationale": "Коментарі фіксують розрізнення двох сусідніх сіл («географічне виправлення»), що свідчить про контекстну дискусію, але саме по собі не становить судової експертизи чи оптичної геолокації відеорядів (insufficient_evidence).",
        },

        # --- Блок 5: Інституційна присутність та реагування ---
        {
            "claim_id": "claim_core_24_tck_presence_at_scene",
            "category": "institutional_presence",
            "statement": "Співробітники ТЦК та СП здійснювали блокування або перебували в будівлі під час сутичок",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "institutional_presence", "topic": "tck_presence"},
            "key_values": {},
            "query_variants": ["перебували військовослужбовці Національної гвардії України", "будівля в оренді Нацгвардії"],
            "rationale": "Матеріали МВС підтверджують перебування у приміщенні підрозділу НГУ, проте логічно не доводять відсутності співробітників ТЦК на місці чи під час попередніх подій (негативний умовивід відхилено; insufficient_evidence).",
        },
        {
            "claim_id": "claim_core_25_police_arrival_ambulance_call",
            "category": "institutional_presence",
            "statement": "Поліція прибула на місце події за викликом працівників приватної швидкої допомоги",
            "scope": {"incident": "petropavlivska-borshchahivka", "type": "official_statement", "topic": "police_arrival"},
            "key_values": {},
            "query_variants": ["працівники приватної швидкої викликали правоохоронців", "виклик приватної швидкої допомоги поліція"],
            "rationale": "Згідно з повідомленням поліції Київщини, виклик на лінію 102 надійшов від персоналу приватної швидкої допомоги через перешкоджання доступу.",
        },
    ]


def build_verification_package(
    *,
    generated_at_utc: str | None = None,
    evaluation_as_of_utc: str | None = None,
) -> dict[str, Any]:
    """Retrieve and assess 25 claims against the supplied, curated evidence corpus."""
    all_passages, _ = build_passages_bundle()
    claims_spec = build_core_claims_spec()

    generated_at_utc = generated_at_utc or _current_utc_timestamp()
    generated_dt, generated_at_utc = _utc_timestamp(generated_at_utc, "generated_at_utc")
    evaluation_as_of_utc = evaluation_as_of_utc or generated_at_utc
    evaluation_dt, evaluation_as_of_utc = _utc_timestamp(evaluation_as_of_utc, "evaluation_as_of_utc")
    if evaluation_dt > generated_dt:
        raise ValueError("evaluation_as_of_utc cannot be later than generated_at_utc")

    passages = [
        passage for passage in all_passages
        if _utc_timestamp(passage["captured_at_utc"], "passage.captured_at_utc")[0] <= evaluation_dt
    ]
    passages_by_id = {passage["passage_id"]: passage for passage in passages}
    captured_times = [
        _utc_timestamp(passage["captured_at_utc"], "passage.captured_at_utc")[0]
        for passage in passages
    ]
    eligible_capture_times = [captured for captured in captured_times if captured <= evaluation_dt]
    evidence_cutoff_utc = (
        max(eligible_capture_times).isoformat(timespec="seconds").replace("+00:00", "Z")
        if eligible_capture_times else None
    )
    if evidence_cutoff_utc is None:
        raise ValueError("no evidence in the supplied corpus is available by evaluation_as_of_utc")

    as_of_utc = evaluation_as_of_utc
    assessed_at_utc = evaluation_as_of_utc

    results_bundle = []
    all_assessments = []
    all_candidates_summary = []
    status_counts: dict[str, int] = {}

    for claim_spec in claims_spec:
        claim_id = claim_spec["claim_id"]
        claim_dict = {
            "claim_id": claim_id,
            "statement": claim_spec["statement"],
            "scope": claim_spec["scope"],
            "key_values": claim_spec["key_values"],
            "query_variants": claim_spec["query_variants"],
        }

        # Candidate discovery is performed only from the supplied corpus.
        search_res = retrieve_evidence_candidates(
            claim_dict, passages, as_of_utc=as_of_utc, top_k=10
        )
        candidates = search_res["candidates"]
        claim_assessments = []
        for candidate in candidates:
            passage = passages_by_id[candidate["passage_id"]]
            inference = infer_claim_passage_relation(claim_dict, passage, candidate)
            if inference.get("decision") != "accepted":
                continue
            assessment = create_evidence_assessment(
                claim_dict,
                candidate,
                passage,
                relation=inference["relation"],
                decision=inference["decision"],
                scope=claim_spec["scope"],
                assessed_at_utc=assessed_at_utc,
                assessor_id="deterministic_claim_verifier",
                acceptance_basis="validated_rule",
                validated_rule_id=inference["rule_id"],
                asserted_values=inference.get("asserted_values") or {},
                independent_root_id=passage.get("independent_root_id"),
                independence_status="candidate",
                evidence_basis=passage.get("evidence_basis", "unknown"),
                limitations=[
                    "Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.",
                    f"Artifact ID: {passage.get('artifact_id')}, exact offset span: [{candidate['start_offset']}:{candidate['end_offset']}].",
                    inference.get("rationale", ""),
                ] + ([inference["epistemic_limitation"]] if "epistemic_limitation" in inference else []),
            )
            assessment["citation"]["artifact_id"] = passage.get("artifact_id")
            if passage.get("artifact_start_offset") is not None:
                assessment["citation"]["artifact_start_offset"] = passage["artifact_start_offset"] + candidate["start_offset"]
                assessment["citation"]["artifact_end_offset"] = passage["artifact_start_offset"] + candidate["end_offset"]
            assessment["citation"]["source_uri"] = passage.get("source_uri")
            claim_assessments.append(assessment)
            all_assessments.append(assessment)

        # Aggregate against declared lineage IDs; these are not independently audited.
        v_res = aggregate_verification(
            claim_dict,
            claim_assessments,
            as_of_utc=as_of_utc,
            search_complete=True,
            minimum_distinct_lineage_roots=1,
        )
        status_counts[v_res["status"]] = status_counts.get(v_res["status"], 0) + 1

        results_bundle.append({
            "claim": claim_spec,
            "verification_result": v_res,
            "assessments": claim_assessments,
            "search_receipt": {
                **search_res["search_receipt"],
                "candidate_passage_ids": [candidate["passage_id"] for candidate in candidates],
            },
            "assessed_candidate_count": len(claim_assessments),
        })
        all_candidates_summary.append({
            "claim_id": claim_id,
            "candidates_count": len(candidates),
            "top_candidate_passage_id": candidates[0]["passage_id"] if candidates else None,
            "assessed_candidate_passage_ids": sorted({a["evidence_id"] for a in claim_assessments}),
        })

    compiled_payload = {
        "schema_version": "2.3",
        "generated_at_utc": generated_at_utc,
        "evaluation_as_of_utc": evaluation_as_of_utc,
        "evidence_cutoff_utc": evidence_cutoff_utc,
        "track": "Track 1: Core Claims & Evidence Verification",
        "milestone": "M1",
        "owner": "deterministic_claim_verifier",
        "summary": {
            "total_claims": len(claims_spec),
            "supported_within_scope": status_counts.get("supported_within_scope", 0),
            "refuted_within_scope": status_counts.get("refuted_within_scope", 0),
            "insufficient_evidence": status_counts.get("insufficient_evidence", 0),
            "conflicting_evidence": status_counts.get("conflicting_evidence", 0),
            "unverified": status_counts.get("unverified", 0),
            "total_accepted_assessments": len(all_assessments),
            "relations_distribution": {
                "supports": sum(1 for a in all_assessments if a["relation"] == "supports"),
                "contradicts": sum(1 for a in all_assessments if a["relation"] == "contradicts"),
                "rebuts": sum(1 for a in all_assessments if a["relation"] == "rebuts"),
                "contextualizes": sum(1 for a in all_assessments if a["relation"] == "contextualizes"),
                "insufficient_context": sum(1 for a in all_assessments if a["relation"] == "insufficient_context"),
            },
            "acceptance_basis": "validated_rule",
            "assessor_id": "deterministic_claim_verifier",
            "validated_rule_id": "rule_autonomous_claim_matcher_v1",
            "exact_character_offsets_verified": True,
            "verification_mode": "deterministic retrieval and relation inference over supplied curated corpus; no open-web discovery",
            "lineage_root_semantics": "declared source-lineage IDs; independence not independently audited",
        },
        "passages": passages,
        "verification_bundle": results_bundle,
    }

    return compiled_payload

def render_markdown_report(payload: dict[str, Any]) -> str:
    """Render a data-driven dossier with explicit evidence and scope limits."""
    summary = payload["summary"]
    bundle = payload["verification_bundle"]
    lines = [
        "# Доказова верифікація ядерних тверджень: Петропавлівська Борщагівка",
        "## Звіт M1, схема результатів 2.3",
        "",
        f"> **Час створення артефакту (UTC):** {payload.get('generated_at_utc', 'unknown')}  ",
        f"> **Оцінювання станом на (UTC):** {payload.get('evaluation_as_of_utc', 'unknown')}  ",
        f"> **Зріз доказів (UTC):** {payload.get('evidence_cutoff_utc', 'unknown')}  ",
        "> **Метод:** локальний BM25-пошук і детерміновані правила зіставлення твердження з пасажем  ",
        "> **Межа автономності:** система вибирає пасажі лише в наданому курованому корпусі; зовнішній пошук джерел не виконується  ",
        f"> **Тверджень:** {summary['total_claims']} | **Підтримано в межах scope:** {summary.get('supported_within_scope', 0)} | **Спростовано в межах scope:** {summary.get('refuted_within_scope', 0)} | **Недостатньо доказів:** {summary.get('insufficient_evidence', 0)} | **Конфліктні:** {summary.get('conflicting_evidence', 0)}  ",
        f"> **Прийняті правилами оцінки пасажів:** {summary['total_accepted_assessments']}  ",
        "",
        "### Як читати статуси",
        "",
        "`supports` і `contradicts` описують відношення між конкретним твердженням та процитованим пасажем, а не самостійно встановлену істину про подію. Офіційна заява зберігається як позиція установи. Для тверджень із `scope.type = physical_fact` одна інституційна заява не дає статусу `supported_within_scope` або `refuted_within_scope`: без прямого спостереження, первинного фізичного запису, форензичного доказу чи геолокованого медіа статус лишається `insufficient_evidence`.",
        "",
        "### Обмеження цього запуску",
        "",
        "- Корпус пасажів і список пріоритетних тверджень сформовані дослідником; BM25 не перевіряє весь інтернет і не доводить повноту джерел.",
        "- Правила відношень є детермінованими евристиками, не каліброваною ймовірнісною моделлю. Числова оцінка правила не є статистичною ймовірністю.",
        "- `independent_root_id` — задекларована мітка лінії походження. Її незалежність зовнішнім аудитом не встановлена; агрегація рахує різні мітки, а не доведені незалежні джерела.",
        "- `insufficient_evidence` означає, що наданий корпус не обґрунтовує певніший висновок. Це не підтвердження протилежного.",
        "- Зміщення веде до локального артефакту; він може бути похідним транскриптом, а не оригінальною вебсторінкою.",
        "",
        "---",
        "",
        "## 1. Зведена матриця",
        "",
        "| ID | Scope | Твердження | Статус | Позиція установи | Докази |",
        "|---|---|---|---|---|---|",
    ]

    for item in bundle:
        claim = item["claim"]
        result = item["verification_result"]
        evidence_ids = sorted({a["evidence_id"] for a in item.get("assessments", []) if a.get("decision") == "accepted"})
        evidence_cell = ", ".join(f"`{evidence_id}`" for evidence_id in evidence_ids) or "немає прийнятих пасажів"
        lines.append(
            f"| `{claim['claim_id']}` | `{claim['scope'].get('type')}` | {claim['statement']} | "
            f"`{result['status']}` | `{result.get('official_position') or 'not_recorded'}` | {evidence_cell} |"
        )

    lines.extend(["", "---", "", "## 2. Пасажі й пояснення по кожному твердженню", ""])
    for item in bundle:
        claim = item["claim"]
        result = item["verification_result"]
        assessments = item.get("assessments", [])
        lines.extend([
            f"### {claim['claim_id']} — `{result['status']}`",
            "",
            f"**Твердження:** {claim['statement']}  ",
            f"**Scope:** `{json.dumps(claim['scope'], ensure_ascii=False, sort_keys=True)}`  ",
            f"**Позиція установи:** `{result.get('official_position') or 'not_recorded'}`  ",
            f"**Пояснення агрегатора:** {result['rationale']}  ",
            f"**Пошук:** {item['search_receipt']['candidate_count']} кандидатів у наданому корпусі; {item.get('assessed_candidate_count', len(assessments))} пройшли правила оцінювання.  ",
            "",
        ])
        if not assessments:
            lines.extend(["Прийнятих пасажів немає. Система утрималася від певнішого висновку.", ""])
        for assessment in assessments:
            citation = assessment["citation"]
            quote = str(citation.get("quote", "")).replace("\n", " ")
            lines.extend([
                f"- **{assessment['relation']}**; basis `{assessment.get('evidence_basis', 'unknown')}`; source `{assessment['source_id']}`; "
                f"declared lineage `{assessment.get('independent_root_id') or 'unknown'}` "
                f"(independence `{assessment.get('independence_status', 'unknown')}`).",
                f"  - URI: {citation.get('source_uri', 'not recorded')}",
                f"  - Artifact: `{citation.get('artifact_id', 'not recorded')}`; "
                f"artifact offset [{citation.get('artifact_start_offset')}:{citation.get('artifact_end_offset')}], "
                f"passage offset [{citation.get('start_offset')}:{citation.get('end_offset')}].",
                f"  - Цитата: > {quote}",
                f"  - Обмеження: {'; '.join(assessment.get('limitations', [])) or 'не зазначено'}",
            ])
        lines.append("")

    lines.extend([
        "---", "", "## 3. Реєстр джерел, використаних у прийнятих оцінках", "",
        "Корені є задекларованими тегами лінії походження, а не доказом незалежності. SHA-256 стосується локального артефакту пасажа.",
        "",
        "| Source ID | Basis | Declared lineage root | URI | Artifact SHA-256 |",
        "|---|---|---|---|---|",
    ])
    passages = {passage["passage_id"]: passage for passage in payload["passages"]}
    used_ids = sorted({assessment["evidence_id"] for item in bundle for assessment in item.get("assessments", [])})
    unique_sources = {}
    for evidence_id in used_ids:
        passage = passages[evidence_id]
        unique_sources.setdefault(passage["source_id"], passage)
    for source_id, passage in unique_sources.items():
        lines.append(
            f"| `{source_id}` | `{passage.get('evidence_basis', 'unknown')}` | "
            f"`{passage.get('independent_root_id', 'unknown')}` | {passage.get('source_uri', '')} | "
            f"`{passage.get('artifact_sha256', '')}` |"
        )

    lines.extend([
        "", "---", "", "## 4. Підсумок цього корпусу", "",
        f"- `supported_within_scope`: {summary.get('supported_within_scope', 0)}.",
        f"- `refuted_within_scope`: {summary.get('refuted_within_scope', 0)}.",
        f"- `conflicting_evidence`: {summary.get('conflicting_evidence', 0)}.",
        f"- `insufficient_evidence`: {summary.get('insufficient_evidence', 0)}.",
        f"- `unverified`: {summary.get('unverified', 0)}.",
        "",
        "Ці лічильники описують лише наведені твердження, локальний корпус, дату зрізу та поточні правила. Вони не є незалежним аудитом справи й не визначають поширеність думок або фактів за межами джерел у цьому пакеті.",
        "",
        "### Додатковий аудит пожежі",
        "",
        "Раннє повідомлення про займання збережено як вторинний переказ Interfax-Ukraine повідомлення голови Київської ОВА, а не як локально захоплений первинний бюлетень. У повідомленні сказано, що дані про постраждалих уточнювалися. Пізніші тогочасні повідомлення вказували на травмованого охоронця та конкретизували Софіївську Борщагівку; отже, ранню фразу не можна перетворювати на твердження «постраждалих немає». Докладний ланцюг джерел: [`fire-source-review-2026-11-09.md`](../source-watch/fire-source-review-2026-11-09.md).",
        "",
    ])
    return "\n".join(lines)

def main():
    print("Building Core Claims Verification package (Milestone M1)...")
    payload = build_verification_package()

    out_dir = REPO_ROOT / "reports" / "evidence-verification"
    out_dir.mkdir(parents=True, exist_ok=True)

    json_path = out_dir / "core_claims_verification_2026-11-09.json"
    md_path = out_dir / "core_claims_verification_2026-11-09.md"

    # Write JSON
    json_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Exported JSON verification bundle: {json_path}")

    # Write Markdown
    md_report = render_markdown_report(payload)
    md_path.write_text(md_report, encoding="utf-8")
    print(f"Exported Markdown verification dossier: {md_path}")

    # Summary print
    s = payload["summary"]
    print(f"\nVerification Complete:")
    print(f"  Total Claims: {s['total_claims']}")
    print(f"  Supported within Scope: {s['supported_within_scope']}")
    print(f"  Refuted within Scope: {s['refuted_within_scope']}")
    print(f"  Accepted Assessments: {s['total_accepted_assessments']}")
    print(f"  Relations: {s['relations_distribution']}")


if __name__ == "__main__":
    main()
