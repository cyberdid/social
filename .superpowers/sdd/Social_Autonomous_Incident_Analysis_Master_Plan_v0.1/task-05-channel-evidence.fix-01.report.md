# Звіт про виправлення Task 05: Channel Evidence

Дата перевірки: 2026-11-07.

## Внесені зміни

- Для кожного не-`unknown` значення осей `origin`, `entity_type`, `operator` і `content_orientation` тепер обов'язкові ідентифікатори доказів, непорожній `scope` і `validity_interval`. Інтервал має часові мітки ISO 8601 із часовим поясом; `end: null` означає, що дату завершення не встановлено. `as_of` фіксує час створення запису й не замінює інтервал чинності.
- Підсумувач відхиляє JSON- і Markdown-шляхи, що після розв'язання вказують на той самий файл, до читання входів і запису виходів.
- CLI має окремі параметри `--manual-groups` і `--auto-groups`. Ручні мапи мають пріоритет незалежно від порядку аргументів; старий `--groups` збережено як сумісний параметр для ручних мап.
- До `source_refs` і `record_id` кожного запису додано роль, шлях і SHA-256 наявних файлів мап груп.
- Специфікацію, тексти генератора звіту та природномовні обмеження в JSONL-експортах перекладено українською.

## Перевірки

- `PYTHONPATH=. pytest -q tests/test_channel_evidence.py tests/test_channel_evidence_summary.py` — 20 тестів пройшли.
- `python -m py_compile src/analysis/channel_evidence.py src/analysis/channel_evidence_summary.py` — успішно.
- `git diff --check -- ...` для файлів Task 05 — успішно.
- CLI повторно створив усі три експорти та підсумки JSON і Markdown із наявних локальних знімків. Сирі файли не змінювалися.

## Експорти та квитанції

| Знімок | Записів | SHA-256 `channels.jsonl` | SHA-256 `posts.jsonl` | SHA-256 експорту |
|---|---:|---|---|---|
| `20261105T100537Z` | 44 | `ccb88ce3cb3ecb1acba2959e2c5b559d58a682aa0dd23be6c57d2081933aaa62` | `2f8e81ad6e5e32a90e42828a5dfa6791d8c96f0aa7d70b3fd601635e573e7fe4` | `53b812815730179a7764cae1ca9092cc1a3964c83d3ae2f6565ecfd978658d73` |
| `20261105T101013Z` | 102 | `70977f0354950f88239512ea371c5a5b055f66642f3f01eade4c55efede949a6` | `88948a1b593b2024ffff079585d37eee74948b79b869eab237e1a970b22bb85d` | `9f4a233c29b44f6ff672ce4298df1095fa9ef5dc76ca05a4c62b5973d08ae252` |
| `20261105T102914Z` | 144 | `97cbc052ae7976c28a94c9cdf5f322e969f30fe567c0dbbaf716b84833795e0e` | `e314b52702ff80243c2b2d87de1fae93e7d800abe8a06da68697d0dee066d6fd` | `0073fba2ad7c50278e31a47ed143afd913cb1b40230676ec195e8f27ce5bc2be` |

| Роль мапи | Файл | SHA-256 |
|---|---|---|
| Ручна | `config/channel_groups.csv` | `0cca1606c9b74e8818681e460659d76bba3d53dc3939814709a56559269cafd7` |
| Автоматична | `config/channel_groups_auto.csv` | `36a7a300d6d85e1ba5e0a72e2a1862d05b2257d22a3fc94c9bce7811873182aa` |

У підсумку: 290 записів із трьох знімків, 240 унікальних назв каналів і 143 записи з `infrastructure_candidate=true`. SHA-256 `summary.json`: `fc5b8eca938057ea2ed0cde4ec8776115f0f471692648abcff26c32eb40b9ad3`. SHA-256 `summary.md`: `f9aa5aaebc9fd8561d5974bd51d9211ca486489c27433b175adf2ab8199a5bab`.

## Обмеження

Усі 290 записів залишають `origin` і `content_orientation` як `unknown`; прапорець інфраструктурного кандидата лише спрямовує подальшу перевірку. Панель є цільовою вибіркою з трьох знімків і не представляє всі канали Telegram.
