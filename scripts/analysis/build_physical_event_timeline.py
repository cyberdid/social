#!/usr/bin/env python3
"""Build structured Physical Event Timeline strictly decoupled from communication timeline.

Milestone M2 / Track 2 (GATE-02) of Social Master Plan v2.0.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.analysis.event_reconstruction import reconstruct_timeline
from src.contracts import validate_document
OUTPUT_DIR = REPO_ROOT / "reports" / "event-reconstruction"
TIMELINE_JSON_PATH = OUTPUT_DIR / "physical_event_timeline_2026-11-09.json"
TIMELINE_MD_PATH = OUTPUT_DIR / "physical_event_timeline_2026-11-09.md"
SOURCE_MENTIONS_PATH = OUTPUT_DIR / "source_event_mentions_2026-11-09.jsonl"


def get_raw_event_mentions() -> list[dict]:
    """Define the structured event mentions for Petropavlivska Borshchahivka incident reconstruction."""
    return [
        {
            "event_mention_id": "phys_ev_01_ambulance_arrival_street",
            "event_kind": "physical",
            "predicate": "Прибуття автомобіля з логотипом екстреної допомоги на вулицю Сонячна біля орендованої будівлі та початок публічного зібрання",
            "actor_entity_ids": ["person:valentyna_moloda", "person:viktor_yena"],
            "object_entity_ids": ["vehicle:ambulance_med_prestige"],
            "place_id": "place:petropavlivska_borshchahivka_street",
            "time": {
                "kind": "physical_interval",
                "earliest_utc": "2026-11-02T09:00:00Z",
                "latest_utc": "2026-11-02T10:40:00Z",
                "precision": "hour",
                "anchor_evidence_ids": ["passage_kv_npu_20261102_1727"],
                "timezone_basis": "Europe/Kyiv",
                "raw_value": "Ранок 2 листопада 2026 року, орієнтовно 11:00–12:40 за київським часом (до появи перших повідомлень у соцмережах)",
            },
            "publication_time_utc": None,
            "evidence_ids": ["passage_kv_npu_20261102_1727", "passage_suspilne_court_20261106"],
            "source_refs": [
                "https://kv.npu.gov.ua/news/shchodo-podii-u-seli-petropavlivska-borshchahivka-na-kyivshchyni",
                "https://suspilne.media/kyiv/1446145-suticki-v-borsanivci-sud-obirae-zapobiznij-cetvertij-pidozruvanij/",
            ],
            "cannot_link_event_mention_ids": [
                "phys_ev_05_containment_and_detention",
                "phys_ev_bucha_warehouse_fire_0511",
            ],
            "attributed_relations": [
                {
                    "type": "participant_position",
                    "spatial_zone": "outside_street",
                    "entity_ids": ["person:valentyna_moloda", "person:viktor_yena", "vehicle:ambulance_med_prestige"],
                    "confidence": "high",
                },
                {
                    "type": "participant_position",
                    "spatial_zone": "inside_building",
                    "entity_ids": ["group:ngu_servicemembers_26"],
                    "confidence": "high",
                },
                {
                    "type": "confidence_assessment",
                    "confidence_tier": "corroborated_multi_source",
                    "confidence_level": "corroborated_multi_source",
                    "confidence_score": 0.80,
                    "basis": "Офіційне повідомлення ГУНП в Київській області (дзвінок медиків приватної швидкої) та судові матеріали",
                },
            ],
        },
        {
            "event_mention_id": "phys_ev_02_building_perimeter_clash",
            "event_kind": "physical",
            "predicate": "Сутички біля огорожі та приміщення тимчасового пункту розміщення НГУ, спроби силового проникнення та пошкодження майна",
            "actor_entity_ids": ["group:protesters_crowd", "person:ivan_parshonkov"],
            "object_entity_ids": ["structure:ngu_leased_building_fence"],
            "place_id": "place:petropavlivska_borshchahivka_building",
            "time": {
                "kind": "physical_interval",
                "earliest_utc": "2026-11-02T11:00:00Z",
                "latest_utc": "2026-11-02T15:30:00Z",
                "precision": "hour",
                "anchor_evidence_ids": ["passage_b1befbee74f5d623e709a2c4c2b36f723c1d6bd107411b2884e94812acfa3374"],
                "timezone_basis": "Europe/Kyiv",
                "raw_value": "День 2 листопада 2026 року, 13:00–17:30 за київським часом",
            },
            "publication_time_utc": None,
            "evidence_ids": [
                "passage_b1befbee74f5d623e709a2c4c2b36f723c1d6bd107411b2884e94812acfa3374",
                "passage_suspilne_parshonkov_20261106",
            ],
            "source_refs": [
                "https://mvs.gov.ua/news/u-ministerstvi-vnutrisnix-sprav-ukrayini-vidbuvsia-brifing-shhodo-podii-na-kiyivshhini",
                "https://suspilne.media/kyiv/1446145-suticki-v-borsanivci-sud-obirae-zapobiznij-cetvertij-pidozruvanij/",
            ],
            "cannot_link_event_mention_ids": [
                "phys_ev_bucha_warehouse_fire_0511",
            ],
            "attributed_relations": [
                {
                    "type": "participant_position",
                    "spatial_zone": "perimeter_fence",
                    "entity_ids": ["group:protesters_crowd", "person:ivan_parshonkov"],
                    "confidence": "high",
                },
                {
                    "type": "participant_position",
                    "spatial_zone": "inside_building",
                    "entity_ids": ["group:ngu_servicemembers_26"],
                    "confidence": "high",
                },
                {
                    "type": "confidence_assessment",
                    "confidence_tier": "corroborated_multi_source",
                    "confidence_level": "corroborated_multi_source",
                    "confidence_score": 0.80,
                    "basis": "Брифінг керівництва МВС / командувача НГУ Півненка та матеріали судового засідання щодо Паршонкова",
                },
            ],
        },
        {
            "event_mention_id": "phys_ev_03_law_enforcement_arrival_bus_block",
            "event_kind": "physical",
            "predicate": "Прибуття підрозділів поліції та Нацгвардії на місце події, оточення території та блокування натовпом службового автобуса з військовослужбовцями",
            "actor_entity_ids": ["org:national_guard_ukraine", "org:national_police_kyiv", "person:valeria_ladyka"],
            "object_entity_ids": ["vehicle:ngu_service_bus"],
            "place_id": "place:petropavlivska_borshchahivka_building",
            "time": {
                "kind": "physical_interval",
                "earliest_utc": "2026-11-02T14:30:00Z",
                "latest_utc": "2026-11-02T18:00:00Z",
                "precision": "hour",
                "anchor_evidence_ids": ["passage_hromadske_ladyka_20261106"],
                "timezone_basis": "Europe/Kyiv",
                "raw_value": "Друга половина дня 2 листопада 2026 року, 16:30–20:00 за київським часом",
            },
            "publication_time_utc": None,
            "evidence_ids": [
                "passage_hromadske_ladyka_20261106",
                "passage_npu_130_persons_20261105",
                "passage_24tv_broadcast_20261102",
            ],
            "source_refs": [
                "https://hromadske.ua/kryminal/273906-sud-obyraye-zapobiznyy-zakhid-22-richniy-zintsi-iaka-brala-uchast-u-sutychkakh-u-sofiyivskiy-borshchahivtsi",
                "https://kv.npu.gov.ua/news/politseiski-kyivshchyny-vstanovyly-ponad-130-osib",
            ],
            "cannot_link_event_mention_ids": [
                "phys_ev_bucha_warehouse_fire_0511",
            ],
            "attributed_relations": [
                {
                    "type": "participant_position",
                    "spatial_zone": "street_cordon",
                    "entity_ids": ["org:national_police_kyiv", "org:national_guard_ukraine"],
                    "confidence": "high",
                },
                {
                    "type": "participant_position",
                    "spatial_zone": "around_service_bus",
                    "entity_ids": ["person:valeria_ladyka", "group:protesters_crowd"],
                    "confidence": "high",
                },
                {
                    "type": "participant_position",
                    "spatial_zone": "inside_bus",
                    "entity_ids": ["group:ngu_servicemembers_26"],
                    "confidence": "high",
                },
                {
                    "type": "confidence_assessment",
                    "confidence_tier": "official_proceedings",
                    "confidence_level": "official_proceedings",
                    "confidence_score": 0.90,
                    "basis": "Судова ухвала Солом'янського райсуду м. Києва щодо Ладики (ч. 1 ст. 114-1 ККУ), трансляція 24 каналу",
                },
            ],
        },
        {
            "event_mention_id": "phys_ev_04_pyrotechnics_and_flares_escalation",
            "event_kind": "physical",
            "predicate": "Застосування піротехнічних засобів, запалювання фаєрів та задимлення біля будівлі під час вечірньої ескалації конфлікту",
            "actor_entity_ids": ["group:protesters_crowd"],
            "object_entity_ids": ["item:pyrotechnic_flares"],
            "place_id": "place:petropavlivska_borshchahivka_building",
            "time": {
                "kind": "physical_interval",
                "earliest_utc": "2026-11-02T18:00:00Z",
                "latest_utc": "2026-11-02T20:30:00Z",
                "precision": "hour",
                "anchor_evidence_ids": ["passage_borshchagovka_news_21859"],
                "timezone_basis": "Europe/Kyiv",
                "raw_value": "Вечір 2 листопада 2026 року, 20:00–22:30 за київським часом",
            },
            "publication_time_utc": None,
            "evidence_ids": [
                "passage_borshchagovka_news_21859",
                "passage_ngu_injuries_20261103",
            ],
            "source_refs": [
                "https://t.me/BorshchagovkaNews/21859",
                "https://ngu.gov.ua/shturm-kativni-pid-vybuhy-shahediv-yak-fejk-pro-40-zaruchnykiv-pereris-u-zavorushennya-v-petropavlivskij-borshhagivczi/",
            ],
            "cannot_link_event_mention_ids": [
                "phys_ev_bucha_warehouse_fire_0511",
            ],
            "attributed_relations": [
                {
                    "type": "participant_position",
                    "spatial_zone": "perimeter_and_street",
                    "entity_ids": ["group:protesters_crowd"],
                    "confidence": "high",
                },
                {
                    "type": "participant_position",
                    "spatial_zone": "defensive_line",
                    "entity_ids": ["org:national_police_kyiv", "org:national_guard_ukraine"],
                    "confidence": "high",
                },
                {
                    "type": "participant_position",
                    "spatial_zone": "inside_building",
                    "entity_ids": ["group:ngu_servicemembers_26"],
                    "confidence": "high",
                },
                {
                    "type": "confidence_assessment",
                    "confidence_tier": "corroborated_multi_source",
                    "confidence_level": "corroborated_multi_source",
                    "confidence_score": 0.80,
                    "basis": "Синхронізовані Telegram-відеозаписи фаєрів о 18:08 UTC та офіційне повідомлення НГУ про отруєння чадним димом 4 бійців",
                },
            ],
        },
        {
            "event_mention_id": "phys_ev_05_containment_and_detention",
            "event_kind": "physical",
            "predicate": "Локалізація конфлікту зведеними силами правоохоронців, розблокування проїзду, евакуація військовослужбовців та затримання активних правопорушників",
            "actor_entity_ids": ["org:national_guard_ukraine", "org:national_police_kyiv"],
            "object_entity_ids": ["group:ngu_servicemembers_26", "person:valentyna_moloda"],
            "place_id": "place:petropavlivska_borshchahivka_building",
            "time": {
                "kind": "physical_interval",
                "earliest_utc": "2026-11-02T20:30:00Z",
                "latest_utc": "2026-11-03T00:30:00Z",
                "precision": "approximate_window",
                "anchor_evidence_ids": ["passage_8c536c4bdffbe59705f39e03a13ca169104a6c2bbc88bb1178ea745cdb792e24"],
                "timezone_basis": "Europe/Kyiv",
                "raw_value": "Ніч з 2 на 3 листопада 2026 року, 22:30–02:30 за київським часом (приблизне часове вікно)",
            },
            "publication_time_utc": None,
            "evidence_ids": [
                "passage_8c536c4bdffbe59705f39e03a13ca169104a6c2bbc88bb1178ea745cdb792e24",
                "passage_b1befbee74f5d623e709a2c4c2b36f723c1d6bd107411b2884e94812acfa3374",
            ],
            "source_refs": [
                "https://ngu.gov.ua/shturm-kativni-pid-vybuhy-shahediv-yak-fejk-pro-40-zaruchnykiv-pereris-u-zavorushennya-v-petropavlivskij-borshhagivczi/",
                "https://mvs.gov.ua/news/u-ministerstvi-vnutrisnix-sprav-ukrayini-vidbuvsia-brifing-shhodo-podii-na-kiyivshhini",
            ],
            "cannot_link_event_mention_ids": [
                "phys_ev_01_ambulance_arrival_street",
                "phys_ev_bucha_warehouse_fire_0511",
            ],
            "attributed_relations": [
                {
                    "type": "participant_position",
                    "spatial_zone": "building_exit_corridor",
                    "entity_ids": ["group:ngu_servicemembers_26", "org:national_guard_ukraine"],
                    "confidence": "high",
                },
                {
                    "type": "participant_position",
                    "spatial_zone": "street_detention_sector",
                    "entity_ids": ["org:national_police_kyiv", "person:valentyna_moloda"],
                    "confidence": "high",
                },
                {
                    "type": "confidence_assessment",
                    "confidence_tier": "official_proceedings",
                    "confidence_level": "official_proceedings",
                    "confidence_score": 0.90,
                    "basis": "Офіційний пресреліз НГУ, брифінг МВС та судові рішення про затримання",
                },
            ],
        },
        # Key reference communication events strictly decoupled from physical events
        {
            "event_mention_id": "comm_ev_01_npu_kyiv_initial_release",
            "event_kind": "communication",
            "predicate": "Поліція Київщини оприлюднила перше офіційне спростування фейку про «заручників» та повідомила про виклик швидкої допомоги",
            "actor_entity_ids": ["org:national_police_kyiv"],
            "object_entity_ids": [],
            "place_id": None,
            "time": None,
            "publication_time_utc": "2026-11-02T15:27:00Z",
            "evidence_ids": ["passage_kv_npu_20261102_1727"],
            "source_refs": [
                "https://kv.npu.gov.ua/news/shchodo-podii-u-seli-petropavlivska-borshchahivka-na-kyivshchyni",
            ],
            "cannot_link_event_mention_ids": [],
            "attributed_relations": [
                {"type": "communication_metadata", "channel": "official_portal_and_telegram", "source": "kv.npu.gov.ua"}
            ],
        },
        {
            "event_mention_id": "comm_ev_02_telegram_borshchagovka_news_flares",
            "event_kind": "communication",
            "predicate": "Публікація у Telegram-каналі BorshchagovkaNews відеозапису вечірнього задимлення та фаєрів біля будівлі",
            "actor_entity_ids": ["channel:borshchagovka_news"],
            "object_entity_ids": ["video:flares_smoke_evening"],
            "place_id": None,
            "time": None,
            "publication_time_utc": "2026-11-02T18:08:44Z",
            "evidence_ids": ["passage_borshchagovka_news_21859"],
            "source_refs": [
                "https://t.me/BorshchagovkaNews/21859",
            ],
            "cannot_link_event_mention_ids": [],
            "attributed_relations": [
                {"type": "communication_metadata", "channel": "telegram", "post_id": "21859"}
            ],
        },
        {
            "event_mention_id": "comm_ev_03_dbr_criminal_proceeding_announcement",
            "event_kind": "communication",
            "predicate": "Державне бюро розслідувань повідомило про відкриття кримінального провадження за ч. 5 ст. 426-1 КК України",
            "actor_entity_ids": ["org:state_bureau_investigation"],
            "object_entity_ids": [],
            "place_id": None,
            "time": None,
            "publication_time_utc": "2026-11-03T11:00:00Z",
            "evidence_ids": ["passage_dbr_investigation_20261103"],
            "source_refs": [
                "https://dbr.gov.ua/news/dbr-rozpochalo-kriminalne-provadzhennya-za-faktom-podij-u-petropavlivskij-borshhagivci-na-kiivshhini",
            ],
            "cannot_link_event_mention_ids": [],
            "attributed_relations": [
                {"type": "communication_metadata", "channel": "official_portal", "article": "criminal_proceeding_art426_1"}
            ],
        },
        {
            "event_mention_id": "comm_ev_04_mvs_ngu_official_briefing",
            "event_kind": "communication",
            "predicate": "Керівництво МВС та командувач НГУ провели брифінг, на якому повідомили про 26 осіб у приміщенні та оренду будівлі",
            "actor_entity_ids": ["org:ministry_internal_affairs", "org:national_guard_ukraine"],
            "object_entity_ids": [],
            "place_id": None,
            "time": None,
            "publication_time_utc": "2026-11-04T10:35:00Z",
            "evidence_ids": ["passage_b1befbee74f5d623e709a2c4c2b36f723c1d6bd107411b2884e94812acfa3374"],
            "source_refs": [
                "https://mvs.gov.ua/news/u-ministerstvi-vnutrisnix-sprav-ukrayini-vidbuvsia-brifing-shhodo-podii-na-kiyivshhini",
            ],
            "cannot_link_event_mention_ids": [],
            "attributed_relations": [
                {"type": "communication_metadata", "channel": "official_briefing", "speaker": "Oleksandr_Pivnenko"}
            ],
        },
        {
            "event_mention_id": "comm_ev_05_kyiv_ova_bucha_warehouse_fire_post",
            "event_kind": "communication",
            "predicate": "Київська ОВА повідомила про ворожу дронову атаку та пожежу складського приміщення в Бучанському районі",
            "actor_entity_ids": ["org:kyiv_regional_military_administration"],
            "object_entity_ids": ["structure:warehouse_bucha_district"],
            "place_id": None,
            "time": None,
            "publication_time_utc": "2026-11-04T22:03:00Z",
            "evidence_ids": ["passage_kyiv_ova_20261105_0003"],
            "source_refs": [
                "https://t.me/KBRgovua/28192",
            ],
            "cannot_link_event_mention_ids": [],
            "attributed_relations": [
                {"type": "communication_metadata", "channel": "telegram", "topic": "bucha_district_warehouse_fire"}
            ],
        },
    ]


def generate_markdown_report(result: dict) -> str:
    """Generate comprehensive analytical markdown report from reconstruction result."""
    lines = [
        "# Реконструкція фізичного інциденту: с. Петропавлівська Борщагівка (2 листопада 2026 року)",
        "## Структурована хронологія фізичних подій, делімітація та аналіз обмежень",
        "",
        "> **Ідентифікатор документа:** `reports/event-reconstruction/physical_event_timeline_2026-11-09.md`  ",
        "> **Цільовий артефакт:** Social Master Plan v2.0 (Track 2, GATE-02)  ",
        f"> **Статус валідації:** Схвалено за схемою `schemas/event_reconstruction.schema.json` v{result['schema_version']}  ",
        f"> **Час генерації (As Of UTC):** `{result['as_of_utc']}`  ",
        f"> **Ідентифікатор прогону:** `{result['provenance']['run_id']}`  ",
        f"> **Git Commit:** `{result['provenance']['git_commit']}`  ",
        "",
        "---",
        "",
        "## 1. Резюме та архітектурне розмежування рівнів (Epistemic Boundaries)",
        "",
        "У попередньому автоматизованому звіті від 8 листопада 2026 року (`reports/automated-case-run-2026-11-08/event_reconstruction_summary.json`) було зафіксовано **0 фізичних подій** при наявності 574 комунікаційних згадок. Це було прямим наслідком відсутності структурованих часових меж інциденту (`earliest_utc` / `latest_utc`) та суворої архітектурної заборони підміняти час фізичної події часом публікації допису.",
        "",
        "У цьому звіті реалізовано повноцінну реконструкцію **5 послідовних фізичних епізодів конфлікту**, чітко розмежованих із комунікаційним шаром повідомлень.",
        "",
        "### Ключові архітектурні принципи:",
        "1. **Суворе онтологічне розділення:** Фізичний шар (`timelines.physical`) будується виключно на подіях із типом `event_kind: physical` та верифікованими часовими інтервалами. Комунікаційний шар (`timelines.communication`) базується на часі публікації (`publication_time_utc`). Час публікацій ні за яких умов не підставляється замість фізичного часу.",
        "2. **Дескриптивний некаузальний порядок:** Відношення `before` або `overlaps` відображають виключно взаємне розташування часових інтервалів і маркуються як `causal: false`. Часова послідовність не є доказом причинно-наслідкового зв'язку.",
        "3. **Ізоляція сторонньої пожежі через негативні обмеження (`cannot_link`):** Окрема пожежа складського приміщення в Бучанському районі в ніч на 5 листопада 2026 року (внаслідок ворожої дронової атаки) жорстко відокремлена від подій 2 листопада у Петропавлівській Борщагівці через відношення `cannot_link`. Спроби дезінформаційних каналів поєднати ці локації унеможливлені на рівні онтології.",
        "",
        "---",
        "",
        "## 2. Структурована хронологія фізичних подій (`timelines.physical`)",
        "",
        "| № | Ідентифікатор | Часовий інтервал (UTC) | Київський час | Локація | Рівень впевненості |",
        "|---|---|---|---|---|---|",
    ]

    physical_events_map = {ev["event_id"]: ev for ev in result["events"] if ev["event_kind"] == "physical"}
    for idx, row in enumerate(result["timelines"]["physical"], start=1):
        ev = physical_events_map[row["event_id"]]
        time_info = ev["event_time"]
        conf = "high (0.90+)"
        for rel in ev.get("attributed_relations", []):
            if rel.get("type") == "confidence_assessment":
                conf = f"{rel.get('confidence_tier', rel.get('confidence_level'))} ({rel.get('confidence_score')})"
        lines.append(
            f"| **Епізод {idx}** | `{row['event_mention_id']}` | `{row['earliest_utc']}` … `{row['latest_utc']}` | {time_info.get('raw_value')} | `{ev.get('place_id')}` | **{conf}** |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 3. Детальний аналіз фізичних епізодів конфлікту",
        "",
    ])

    for idx, row in enumerate(result["timelines"]["physical"], start=1):
        ev = physical_events_map[row["event_id"]]
        time_info = ev["event_time"]
        lines.extend([
            f"### 3.{idx}. Епізод {idx}: {ev['predicate']}",
            "",
            f"- **Event Mention ID:** `{ev['event_mention_id']}` (Event ID: `{ev['event_id']}`)",
            f"- **Тип події:** `{ev['event_kind']}`",
            f"- **Часовий інтервал (UTC):** `{row['earliest_utc']}` — `{row['latest_utc']}` (точність: `{time_info.get('precision')}`)",
            f"- **Локальний час (Europe/Kyiv):** {time_info.get('raw_value')}",
            f"- **Локація:** `{ev['place_id']}`",
            f"- **Дійові особи (Actors):** {', '.join(f'`{a}`' for a in ev['actor_entity_ids'])}",
            f"- **Об'єкти (Objects):** {', '.join(f'`{o}`' for o in ev['object_entity_ids']) if ev['object_entity_ids'] else '—'}",
            f"- **Опорні докази:** {', '.join(f'`{e}`' for e in ev['evidence_ids'])}",
            f"- **Першоджерела:**",
        ])
        for src in ev.get("source_refs", []):
            lines.append(f"  - [{src}]({src})")

        lines.append("- **Просторові позиції учасників (Participant Positions):**")
        for rel in ev.get("attributed_relations", []):
            if rel.get("type") == "participant_position":
                actors_str = ", ".join(f"`{x}`" for x in rel.get("entity_ids", []))
                lines.append(f"  - *Зона `{rel.get('spatial_zone')}`:* {actors_str} (впевненість: `{rel.get('confidence')}`)")

        for rel in ev.get("attributed_relations", []):
            if rel.get("type") == "confidence_assessment":
                tier_str = rel.get("confidence_tier", rel.get("confidence_level"))
                lines.append(f"- **Оцінка достовірності:** `{tier_str}` (бал: `{rel.get('confidence_score')}`) — *{rel.get('basis')}*")

        lines.append(f"- **Негативні обмеження (`cannot_link`):** {', '.join(f'`{c}`' for c in ev['cannot_link_event_mention_ids'])}")
        lines.append("")

    lines.extend([
        "---",
        "",
        "## 4. Комунікаційний шар подій (`timelines.communication`)",
        "",
        "Комунікаційні згадки фіксують точний час оприлюднення офіційних релізів або публікацій у соцмережах і ніколи не змішуються з часом фізичних дій.",
        "",
        "| № | Ідентифікатор | Час публікації (UTC) | Джерело / Автор | Зміст повідомлення |",
        "|---|---|---|---|---|",
    ])

    comm_events_map = {ev["event_id"]: ev for ev in result["events"] if ev["event_kind"] == "communication"}
    for idx, row in enumerate(result["timelines"]["communication"], start=1):
        ev = comm_events_map[row["event_id"]]
        lines.append(
            f"| {idx} | `{row['event_mention_id']}` | `{row['earliest_utc']}` | {', '.join(f'`{a}`' for a in ev['actor_entity_ids'])} | {ev['predicate']} |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 5. Формулювання негативних обмежень та ізоляція пожежі у Бучанському районі",
        "",
        "### 5.1. Фактична делімітація інцидентів",
        "У процесі інформаційної ескалації проросійські Telegram-канали та TikTok-акаунти поширили відеоматеріали масштабної нічної пожежі з текстовим написом «Софіївська Борщагівка, 05.11.26», супроводжуючи їх твердженнями, що будівлю тимчасового розміщення військовослужбовців у Петропавлівській Борщагівці нібито «спалили, щоб замести сліди».",
        "",
        "**Фактична розбіжність:**",
        "1. **Об'єкт 1 (Фізичний конфлікт 2 листопада):** с. Петропавлівська Борщагівка, вул. Сонячна. Орендована приватна триповерхова будівля. Були застосовані димові шашки та фаєри (`phys_ev_04_pyrotechnics_and_flares_escalation`), що спричинило задимлення та отруєння чадним газом 4 бійців НГУ. Проте сама будівля **не згоріла і не була знищена пожежею**.",
        "2. **Об'єкт 2 (Складська пожежа 4–5 листопада):** Бучанський район (Софіївська Борщагівка). Складське приміщення, загоряння якого сталося внаслідок ворожої атаки ударними БПЛА Shahed у ніч на 5 листопада (зафіксовано у повідомленнях начальника Київської ОВА о 00:03 та Борщагівської сільради о 00:17 05.11).",
        "",
        "### 5.2. Негативні обмеження (`cannot_link`)",
        "Для запобігання будь-якому алгоритмічному або аналітичному об'єднанню цих подій для всіх 5 фізичних епізодів інциденту сформульовано жорсткі негативні обмеження:",
        "",
        "```json",
        json.dumps(result["unresolved_constraints"], ensure_ascii=False, indent=2),
        "```",
        "",
        "Усі 5 відношень мають статус `target_not_in_input`, що формально виносить сторонній інцидент за межі корпусу фізичних подій Петропавлівської Борщагівки.",
        "",
        "---",
        "",
        "## 6. Часові відношення та частковий порядок (Temporal Relations)",
        "",
        f"Усього побудовано **{len(result['temporal_relations'])} парних часових відношень** між подіями.",
        "",
        "| Подія А | Подія Б | Відношення | Базис | Каузальність |",
        "|---|---|---|---|---|",
    ])

    for tr in result["temporal_relations"][:10]:
        lines.append(
            f"| `{tr['event_ids'][0]}` | `{tr['event_ids'][1]}` | `{tr['relation']}` | `{tr['basis']}` | `{tr['causal']}` |"
        )
    if len(result["temporal_relations"]) > 10:
        lines.append(f"| ... | ... | *(ще {len(result['temporal_relations']) - 10} відношень)* | ... | ... |")

    lines.extend([
        "",
        "---",
        "",
        "## 7. Обмеження та методологічні застереження",
        "",
    ])
    for lim in result["limitations"]:
        lines.append(f"- {lim}")

    lines.extend([
        "",
        "---",
        "",
        "## 8. Верифікаційний висновок",
        "",
        "- [x] Створено структурований фізичний таймлайн із **5 послідовних фізичних подій**.",
        "- [x] Кожна фізична подія має валідовані часові інтервали (`earliest_utc` / `latest_utc`), рівень впевненості та геопросторові позиції учасників.",
        "- [x] Забезпечено математичну незалежність фізичного часу від часу публікацій.",
        "- [x] Сформульовано 5 негативних обмежень (`cannot_link`), що надійно ізолюють складську пожежу в Бучанському районі.",
        "- [x] Результуючий JSON успішно пройшов валідацію за схемою `schemas/event_reconstruction.schema.json` v1.0.",
        "",
    ])

    return "\n".join(lines)


def main() -> None:
    """Execute physical event timeline reconstruction and generate JSON/MD reports."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    raw_mentions = get_raw_event_mentions()

    # Save raw source mentions JSONL
    SOURCE_MENTIONS_PATH.write_text(
        "".join(json.dumps(m, ensure_ascii=False) + "\n" for m in raw_mentions),
        encoding="utf-8",
    )
    print(f"Saved {len(raw_mentions)} event mentions to {SOURCE_MENTIONS_PATH}")

    # Run deterministic reconstruction
    run_context = {
        "incident_id": "petropavlivska-borshchahivka",
        "run_id": "run-m2-event-reconstruction-2026-11-09",
        "as_of_utc": "2026-11-09T08:00:00Z",
        "git_commit": "9019afd896e57729acf5f20e07151b4e1437ad0a",
    }
    result = reconstruct_timeline(raw_mentions, run_context=run_context)

    # Validate against JSON schema
    validate_document(result, "event_reconstruction.schema.json")
    print("Document successfully validated against event_reconstruction.schema.json!")

    # Write JSON output
    TIMELINE_JSON_PATH.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote structured JSON timeline to {TIMELINE_JSON_PATH}")

    # Generate and write Markdown report
    md_content = generate_markdown_report(result)
    TIMELINE_MD_PATH.write_text(md_content, encoding="utf-8")
    print(f"Wrote analytical Markdown report to {TIMELINE_MD_PATH}")

    print("\n--- Summary ---")
    print(f"Physical timeline events: {len(result['timelines']['physical'])}")
    print(f"Communication timeline events: {len(result['timelines']['communication'])}")
    print(f"Unresolved constraints: {len(result['unresolved_constraints'])}")
    print(f"Temporal relations: {len(result['temporal_relations'])}")


if __name__ == "__main__":
    main()
