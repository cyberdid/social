# Консервативна реконструкція подій Social v1

## Призначення

`src/analysis/event_reconstruction.py` будує впорядковану модель із уже вилучених згадок подій. Модуль не витягує події з довільного тексту та не доводить, що повідомлена подія справді сталася. Кожна згадка залишається окремим `event` із `merge_status=unresolved_event_mention`.

Запуск із JSONL:

```bash
python -m src.analysis.event_reconstruction_cli event_mentions.jsonl output/event-reconstruction
```

CLI також приймає `--incident-id`, `--run-id`, `--as-of-utc` та `--git-commit` для запису provenance. `--as-of-utc` лише фіксує cutoff у виході: CLI **не** фільтрує рядки за публікацією, тому передані mentions мають бути заздалегідь сформовані для потрібного зрізу.

Один рядок вхідного JSONL — один об'єкт:

```json
{
  "event_mention_id": "mention_001",
  "event_kind": "physical",
  "predicate": "прибув",
  "actor_entity_ids": ["entity_001"],
  "object_entity_ids": [],
  "place_id": "place_001",
  "time": {
    "kind": "claimed_event_time",
    "earliest_utc": "2026-11-02T16:00:00Z",
    "latest_utc": "2026-11-02T16:20:00Z",
    "precision": "interval",
    "raw_value": "після 18:00 за Києвом",
    "timezone_basis": "source_locale",
    "anchor_evidence_ids": ["passage_001"]
  },
  "publication_time_utc": "2026-11-02T17:15:00Z",
  "evidence_ids": ["passage_001"],
  "cannot_link_event_mention_ids": [],
  "attributed_relations": []
}
```

Часові значення в цьому прикладі ідентифікатори демонстраційні. Передавання сирої фрази як `raw_value` не означає, що межі інтервалу перевірені.

## Розділення часу

- `event_time` зберігає заявлений час описаної дії, сирий вислів, точність, межі та evidence anchors.
- `publication_time_utc` — окремий час публікації.
- Фізична шкала використовує лише bounded `event_time`; час допису його не замінює.
- Комунікаційна шкала пріоритетно використовує `publication_time_utc` і зберігає заявлений `event_time` окремо.
- Невизначені та частково обмежені часові вислови залишаються в записі, але не ставляться в лінійну шкалу.

Межі трактуються як замкнені інтервали в UTC. Відношення `before` виникає лише коли `latest(A) < earliest(B)`. Інтервали, що торкаються або перетинаються, позначаються `overlaps`; точного порядку між ними не нав'язується. Якщо записи використовують різні часові бази (наприклад, один час публікації, інший — заявлений час події), зв'язок `unknown` і `incomparable_time_bases`; їх не порівнюють як одну шкалу. Часовий порядок не породжує причинний зв'язок.

## Entity та event linking

- `resolve_entity_alias()` підтримує лише точний збіг нормалізованого alias. Нуль збігів → `unresolved`; кілька → `ambiguous`; fuzzy match не використовується.
- Кандидатне `possible_same` створюється лише за однаковими типом події, предикатом, явними actor/object ID та `place_id`, без `cannot_link`. Неперетинні інтервали блокують кандидата лише коли їхні часові бази збігаються; publication time не порівнюється з claimed event time.
- Кандидати ніколи не зливаються автоматично: різні повтори тієї самої дії можуть мати однакові атрибути.
- `cannot_link_event_mention_ids` має пріоритет над подібністю й блокує кандидатний зв'язок.
- Назви населених пунктів зіставляються тільки через заздалегідь нормалізовані `place_id`; схожість написання не зливає локації.

## Виходи

CLI створює:

- `events.jsonl` — незлиті кандидатні записи з посиланнями на докази;
- `event_links.jsonl` — тільки можливі, не підтверджені зв'язки;
- `temporal_relations.jsonl` — часовий порядок/перетин без причинності;
- `unresolved.jsonl` — записи, які залишаються твердженнями джерел;
- `unresolved_constraints.jsonl` — посилання `cannot_link`, ціль яких відсутня у вхідному зрізі;
- `timeline.json` і `timeline.md` — окремі шкали фізичних дій і комунікацій;
- `run_receipt.json` — SHA-256 вхідного JSONL, вихідні хеші, кількості та обмеження.

Кожен запис `events.jsonl` містить `schema_version`, `incident_id`, `run_id`, `producer`, `evidence_ids` і `source_refs`. Якщо ідентифікатор запуску або кейсу не подано, значення залишаються `null`, а не генеруються із припущення.

Перед записом CLI перевіряє результат через `schemas/event_reconstruction.schema.json`. CLI відмовляється перезаписувати наявний bundle без явного `--overwrite`, не приймає директорію результату як symlink, захищає вхідний файл від розміщення всередині каталогу результату (також через symlink) і не видаляє невідомі файли. `--overwrite` атомарно замінює bundle лише тоді, коли каталог містить тільки відомі виходи; інші користувацькі дані блокують заміну.

JSON Schema: `schemas/event_reconstruction.schema.json`.

## Обмеження

Це детермінований організатор уже наявних event mentions. Він не виконує NER, extraction, верифікацію доказів, оцінювання джерел, геолокацію, правову оцінку чи причинний аналіз. Ідентифікатори actor/object/place мають походити з окремих доказових процедур. Поточний модуль не виявляє суперечливі твердження про один і той самий фізичний епізод автоматично; такі твердження треба передавати як окремі mentions і зберігати їхні evidence references.

## Перевірка

```bash
uv run --with pytest --with jsonschema -- python -m pytest -q tests/test_event_reconstruction.py
python -m py_compile src/analysis/event_reconstruction.py src/analysis/event_reconstruction_cli.py
```
