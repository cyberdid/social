# Social — зміст

## Кейси
- Інцидент у Петропавлівській Борщагівці (02–05.11.2026): звіт `reports/borshchahivka-report.md` (v2.7), хронологія `wiki/borshchahivka-facts-timeline.md`; TikTok-вибірка 42 посилань — `reports/tiktok/manual-batch-20261106.md`
- Вибори США 2024 — дизайн `docs/specs/2026-11-05-us-2024-elections-design.md` (відкладено)

## Методи
- `wiki/methods/telegram-collection.md` — збір публічного Telegram без API
- `wiki/deep-research-prompts.md` — промпти Deep Research DR1–DR7

## Дані
- `data/raw/telegram_web/20261105T101013Z/` — основний знімок (не в git; маніфест із SHA-256)
- `reports/20261105T101013Z/` — results.json, CSV, графіки, валідація кодування

## Продовження (Codex + Claude, 05–06.11)
- `docs/plans/2026-11-05-research-continuation.md`, `wiki/precommit/2026-11-05-continuation-protocol.md`
- `wiki/research-source-audit.md` — аудит першоджерел (ЦПД, SPRAVDI, КіберБорошно, «Стоп паніка», ДБР)
- `wiki/methods/research-methodology-review.md`, `wiki/methods/cross-platform-collection-tools.md`, `wiki/methods/media-matching.md`
- `reports/contextual-misinformation-candidates.md` — сканер контекстної дезінформації
- `reports/telegram-comments/coordinated-comments.md` — коментарі Telegram, кампанія шаблонних коментарів
- `reports/tiktok-fire/` — коментарі TikTok: ручна розмітка позицій, `automation_signals.md` (сигнали ботів)
- `config/manual_tiktok_links_20261106.txt` — 42 прямі TikTok-посилання користувача, коментарний знімок і межі повноти — `reports/tiktok/manual-batch-20261106.md`
- `raw/deep-research/` — результати DR1–DR7 (без змін, з маніфестом)
- `wiki/methods/literature-review-2026-11-06.md` — огляд наукової літератури (41 робота, перевірені DOI)
- `wiki/methods/platform-access-2026-11-06.md` — що вдалося отримати безкоштовно та стан пошуку в Instagram/TikTok

## Доказове доповнення, 06.11.2026

- [Умовні нульові моделі](reports/coordination-null-models-2026-11-06.md) — S7, час копій, 9 999 реалізацій, множинні перевірки та межі атрибуції.
- [Субтитри YouTube](reports/youtube-content-2026-11-06.md) — 54 спроби, 49 непорожніх текстів, 56 контекстно прочитаних фрагментів.
- [Мережа й динаміка Telegram](reports/telegram-network-dynamics-2026-11-06.md) — форварди, betweenness та шестигодинні мітки.
- [Повторний TikTok-пошук](reports/tiktok/context-recheck-20261106.md), [таблиця часових полів](reports/tiktok/publication-event-filming-times-20261106.csv).
- [Оновлення джерел і проваджень](reports/source-refresh-2026-11-06.md), [довідка про фігурантів](reports/figures-and-proceedings-2026-11-06.md).
- [Стан Instagram](reports/instagram-access-20261106/README.md) — новий збір має технічну перешкоду, дані не вигадуються.
- [Протокол атрибуції](wiki/methods/russian-influence-attribution-early-warning.md), [побудова PDF](scripts/reports/README.md).
- [Щоденний моніторинг джерел](docs/source-watch.md) — 12 публічних адрес, незмінні знімки, cron 10:00 Europe/Kyiv.

## PDF, 06.11.2026
- [Основний аналітичний звіт, v2.7](output/pdf/petropavlivska_borshchahivka_report_2026-11-06.pdf)
- [Фігуранти й процесуальний статус](output/pdf/petropavlivska_figures_and_proceedings_2026-11-06.pdf)
- [Протокол раннього попередження й атрибуції](output/pdf/russian_influence_attribution_early_warning_2026-11-06.pdf)
- [Маніфест файлів PDF і контрольних сум](output/pdf/manifest-2026-11-06.json)
