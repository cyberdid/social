# Карта конфлікту та міжплатформенного покриття

**Інцидент:** Петропавлівська Борщагівка  
**Run:** run-post-fix · статус partial · зріз 2026-11-08T01:14:07Z  
**Вікно IncidentSpec (UTC):** 2026-11-02T09:00:00Z — 2026-11-05T10:31:42.738963Z

## Висновок

Цей запуск не містить типізованих фізичних подій чи записів позицій: **0** і **0** відповідно. Тому він не формує фізичні епізоди конфлікту, їхніх учасників або дій. Це обмеження вхідного покриття; воно не свідчить, що фізичних дій не було.

У реконструкції збережено **574** комунікаційних/подієвих згадок як невирішені кандидати; фізичних рядків хронології — **0**. Час публікації не встановлює час події, зйомки чи місце.

## Інформаційний шар

Конфліктний агрегатор обробив **13** інтервалів уваги окремо від фізичних індикаторів. У наданому Telegram-знімку зафіксовано **1 438** релевантних дописів із **158** каналів; найбільший шестигодинний інтервал містив **511** дописів. Це опис публікацій у цільовій панелі, а не інтенсивності фізичного конфлікту.

Детальна часова серія, її знаменники й обмеження наведені у звіті [Інформаційна динаміка Telegram у локальному знімку інциденту](../telegram-information-dynamics-2026-11-08.md); тут її не дубльовано.

## Покриття платформ у цьому запуску

| Платформа / шар | Наявний агрегований ввід | Межа висновку |
|---|---|---|
| Telegram | 1 438 дописів, 158 каналів; єдиний платформний ряд у первісному case-run | Цільова панель; не репрезентує весь Telegram або населення. |
| TikTok | 42 кандидатні посилання: 21 відео мали yt-dlp `create_time/createTime`, 19 timestamped відео у вікні (18 акаунтів), 2 поза ним; 21 фото не мало platform timestamp | До часової серії включено тільки 19 відеопублікацій з metadata timestamp. Це не час зйомки; ID-оцінки не використовувалися як заміна відсутнього platform timestamp. |
| YouTube | У первісний case-run типізований series не передавався; окремий follow-up зіставив 408 із 444 лексичних відеокандидатів (180 каналів) з timestamp у вікні IncidentSpec | Публікаційний ряд обмежений запитами й lexical metadata-відбором; це не повний моніторинг YouTube і не перевірка вмісту роликів. |
| Instagram | У case run немає придатного типізованого receipt | Покриття відсутнє для цього запуску; це не твердження про відсутність матеріалів на платформі. |

Окремий [міжплатформний ряд публікаційних кандидатів](../cross-platform-publication-candidates-2026-11-08.md) тепер зіставляє Telegram, YouTube і TikTok в однаковому часовому вікні. Він не є повною міжплатформною реконструкцією подій: для Instagram немає придатних platform timestamps, Facebook/Threads/X не передалися типізованими, а source-lineage зв'язків між платформами не встановлено. Фізична хронологія та причинність не виводяться.

## Машинний статус епізодів

[conflict_episodes.jsonl](conflict_episodes.jsonl) не містить жодного запису епізоду; там збережено лише контрольний рядок зі статусом **not_run** і причиною **no_typed_physical_event_or_position_records_supplied**. Зведення запуску позначає етап conflict_analysis як **complete**: він обробив інформаційні інтервали, але не мав фізичних подій або записів позицій для формування епізоду.

## Походження та перевірки

Підставою для карти є санітизовані агрегати запуску run-post-fix та окремого post-run зіставлення publication-candidate рядів: [зведення запуску](summary.md), [підсумок конфліктного аналізу](conflict_analysis_summary.json), [підсумок реконструкції подій](event_reconstruction_summary.json), [підсумок покриття джерел](source_coverage_summary.json), [інформаційна динаміка](information_dynamics_summary.json), [міжплатформний агрегат](../cross-platform-publication-candidates-2026-11-08.json) і [receipt із хешами](run_receipt.json). Приватні Telegram/YouTube тексти, повні рядки, транскрипти й медіафайли сюди не включено.


### Точна санітизована provenance

| Артефакт | SHA-256 | Використання |
|---|---|---|
| case_summary.json | f95058cb0fbdaad60dc7a1fb48cfbf809da4ad0449d21e43839d83f70adcd02b | run ID, cutoff, and stage states |
| conflict_analysis_summary.json | 5d19856440dae64133c0ffe3efef221c826475555905ee8fb830ae81a96142bb | physical-event and position counts; attention-bin count |
| event_reconstruction_summary.json | e32bdcbd22536254123453989c8d7a6af05519cb976ca2bbfe251867ef07f5e5 | candidate mention and timeline counts |
| information_dynamics_summary.json | 7c16448cb20041361faf347ffe2abf6f6e0e00bbae8199f1c97d154facf7b866 | Telegram denominators and attention bins |
| source_coverage_summary.json | 35956c900ccb965255e01cfad4c02aab1033ecf5cff87eecff7124159dbd0239 | platform coverage and TikTok metadata counts |
| uncertainty_summary.json | 0874c9218fddf4db65b14d5e31deced6436b9eaae5d931f188f4e7da08716b3a | unknown-label scenario bounds |
| conflict_input (external/private) | 0aef252b983080a19128bf7ab147ab62fa173a7eb5e86ec8e3511a1ea82a5711 | SHA-256; 7112 bytes |
| event_mentions (external/private) | c74195ca46d2e5636d5e6a8a1e43e8bf3dcc442dfb9857f4927b09dba63d5971 | SHA-256; 574 records |
| information_posts (external/private) | a1240963e20691743d72efcb3a0446c777c60c3e4ec162adaf4f4c0a9c0cf95c | SHA-256; 1438 records |
| uncertainty_records (external/private) | b4bdfa2e6ee937011f9e922fb78c99472c6c6828505aaa6c5801704565e8d506 | SHA-256; 1438 records |
| coverage input (external/private) | 2d77cb652e4db9ca0760fb39f396fca6bfc905a3397967a6940cf0ae36f46ed5 | SHA-256; 1406 bytes |
| Telegram processed snapshot (external) | d229d8618021cf285f24c712eb9cd37ca85eb0e8bee2d8a7f74b6e7c574cda3f | source snapshot hash |
| TikTok publication/event/filming-time table (tracked; response metadata kept external) | 219295ade4430ef804e7f0b4c93141a8112706a85353420bfb96f83bfcbe6f8d | 42 links; 21 video metadata timestamps; 19 within window |
| Cross-platform candidate dynamics JSON | a3f7e3135de1b4c0ec1e361d990283a020a90a449ec55cfe226541947fd0839e | aggregate-only Telegram + YouTube + TikTok follow-up |
| TikTok time ledger module | 9a0af5bbba52f4d396fe897230585e92107e99c0f6068f20408a7855920abeac | yt-dlp timestamp field mapped into the tracked time ledger |
| TikTok metadata-response bundle (local only) | c453f9ffd5bcba0a938e2ff7e9f2611aa5e445e941bc05daac1388d44041046f | 21 timestamped video metadata files; exact CSV timestamp matches |
| YouTube videos JSONL (external) | 271252858438010c604ff24b506b0bf40c4525ecc7577b9a249f85b38cb383aa | candidate metadata input hash |

Маніфест приватних inputs: a412331b4ab3ec4d84ba357354824f5708b3f7c9103b5ab84c852e2bb53450ff; маніфест приватного run: d0459a7ac9b581db99e96399bae51445f6bdc3f6a3d2581d35067b6174f4af1a. У цій карті наведено тільки агрегати та SHA-256; приватні текстові байти не розкривались і не включені.

Семантична точність лишається **not_evaluated**; джерельна автентичність, фактична хронологія, особи, причинність та позиції учасників цими агрегатами не встановлюються.
