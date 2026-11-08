# SOCIAL — Автономний аналіз інцидентів і соціальних конфліктів
## Інтегрований master plan v1.1

> **Дата оновлення:** 8 листопада 2026 року  
> **Статус:** чинний master plan, що замінює v1.0 у частині реєстру Deep Research, їхнього зв'язку з реалізацією та актуальних доказів виконання.  
> **Статус closeout:** **NOT COMPLETE — НЕ ЗАВЕРШЕНО.** Реалізація й case acceptance залишаються частковими.  
> **Зміна v1.1:** виправлено помилкову позначку про відсутність DR1/DR3, інтегровано незалежні аудити DR1/DR3, оцінку DR4 та один bounded MTProto parity-check. Повний перелік змін і меж — у [звіті інтеграції та closeout-аудиту](../../reports/orchestrator/masterplan-closeout-2026-11-08.md).

Версія master plan не є оцінкою готовності продукту. Наявність коду, схем чи тестів не підтверджує семантичну точність, повне покриття джерел або істинність висновку про реальну подію. Для кожного workstream окремо вказані структурна готовність, case evidence та невирішені acceptance gates.

## 1. Метод читання і межі

| Позначка | Значення |
|---|---|
| **Реалізовано — структура** | Є код, контракт або звітний gate; це підтверджує поведінку структури, не точність висновків. |
| **Частково реалізовано** | Є робочий компонент або обмежений пілот; покриття чи приймальні критерії ще не закриті. |
| **Не оцінено** | Немає незалежного локального еталона або потрібного вимірювання якості. |
| **OPEN gate** | Перевірювана умова завершення наразі не виконана або не має достатнього свідчення. |
| **P0** | Коректність і доказовість першого обмеженого кейсу; блокує твердження про завершений інцидентний продукт. |
| **P1** | Валідація та розширення семантичних, медійних і аналітичних компонентів. |
| **P2** | Масштабування, міжкейсова переносність, додаткові моделі й інтерфейси після P0/P1 gates. |

Social готує відтворюваний, доказово обмежений Incident Analytical Package для аналітика. Система має зберігати джерела, твердження, суперечності, часи, невдалі операції й покриття, а також повертати `unknown`, `insufficient_evidence` або `conflicting_evidence`, коли даних недостатньо.

Social не робить автоматичних правових висновків, не встановлює приховані мотиви чи державне керування без належних доказів, не виводить громадську думку з цільової панелі та не трактує копії, перегляди, реакції або згоду моделей як незалежне підтвердження.

## 2. Deep Research: реєстр і provenance

Архівні звіти з manifest від 5 листопада тут позначені **AR1–AR7**, аби не плутати їх із поточними дослідницькими потоками **DR1–DR4**. Архівні файли збережено під початковими назвами; їхній зміст не підмінює сучасні DR1–DR4.

| Потік | Поточний документ і provenance | Як використовується в Master Plan |
|---|---|---|
| **DR1 — Scientific Validation: narratives, channel attribution, uncertainty** | [Фінальний PDF, 23 сторінки](../research/DR1-scientific-validation-2026.pdf), SHA-256 `e817f5340cf1869294ef6d3afe356146b36c027ac4348bcd2941c26451cc5e4b`. Точна копія звірена з вихідним PDF; подробиці — у [source manifest](../research/current-deep-research-source-manifest-2026-11-08.md). | Підстава для W03/W04/W11 і P0.3/P0.4: тема, claim, stance і verification розділяються; джерельна атрибуція багатовимірна; сценарні межі не видаються за репрезентативні оцінки. Поточні реалізації структурні, семантична якість не оцінена. |
| **DR2 — coordination, statistics, sampling** | [Фінальний огляд](../research/DR2-coordination-statistics-sampling-2026-11-08.md), доповнений [exact-graph аудитом](../../reports/coordination-null-models-2026-11-08-lsh-audit.md). | Методологічна основа W09 і статистичних release gates. Exact graph та null-model перевірки виконані на визначеній цільовій панелі; organic controls і міжкейсова переносність лишаються відкритими. Результати не доводять організатора чи державну атрибуцію. |
| **DR3 — autonomous social conflict and incident reconstruction** | [Фінальний PDF, 30 сторінок](../research/DR3-autonomous-incident-reconstruction-2026.pdf), SHA-256 `a451e0b517b20a0ddfbe58242048925fc8b90d8f57a4d8277ae1456d3bf8c7d6`. Точну копію та метадані звірено; source manifest містить деталі. | Підстава для W06–W10/W12/W13: physical і communication timelines різні; час події та публікації не зливаються; retrieval candidate не є verification; source roots треба відновлювати, а не рахувати повтори. Реальний case reconstruction і source-to-finding trace не пройшли acceptance. |
| **DR4 — audience response, sentiment, emotion, engagement** | [Наданий фінальний огляд](../research/DR4-audience-response-2026-11-08.md); [отримана рецензія](../research/DR4-review-received-2026-11-08.md). Оцінка 89/100 — це надана рецензентська оцінка документа, а не калібрована метрика точності Social. | Прийнята методологічна основа W14. MTProto typed aggregate capture перевірено на 10 коментарях/3 гілках: поточні collector vectors збіглися з API vectors 10/10; повне покриття, repeated snapshots і semantic validation відкриті. |
| **VIDEO** | [Video Evidence Processing Pipeline v0.1](social-video-evidence-pipeline-v0.1.md). | Архітектурна основа W10. Pipeline outputs — технічні спостереження-кандидати, а не підтвердження місця, часу, мовця, події чи claim. |

Файли `raw/deep-research/DR1–DR7-2026-11-05.md` — архівні звіти AR1–AR7, а не поточні DR1–DR7. Не використовувати їхні назви як ідентифікатори поточних потоків.

### 2.1. Висновки DR1/DR3, звірені з кодом

**DR1.** `src/analysis/narrative_v3.py` видає консервативні кандидатні мітки з окремими полями теми/claim/позиції, але це не повна, локально валідована реалізація рекомендованого класифікатора. Для корпусу є 555 candidate claims; `semantic_accuracy=not_evaluated`. Незалежного людського gold set і per-class/per-language метрик немає. `src/analysis/channel_evidence.py` відокремлює origin, entity type, operator, content orientation, infrastructure та operational attribution; у snapshot 246 профільних записів/239 назв лишилися невідомими за основними атрибуційними вимірами, а 137 infrastructure candidates — лише підстави для перевірки. `src/analysis/uncertainty_scenarios.py` дає сценарні/частково ідентифікаційні межі; це не калібрований joint measurement-error model і не інтервал для населення.

**DR3.** `src/analysis/event_reconstruction.py` зберігає часові типи й unresolved candidate links. Основний case run має 574 communication/event mentions, 0 фізичних event rows і жодної встановленої physical timeline; окремий bounded run додає одну unresolved day-level source-reported mention, не підтверджену хронологію. Source-linked run порівняв 555 candidate claims із 30 passages і 11 897 BM25 matches; початкові accepted Evidence Assessments і VerificationResults — 0. Claim-level source-lineage не запускався. Отже, структурні схеми й retrieval не є свідченням правильності реконструкції інциденту.

Повний шлях від аудиту DR1/DR3 до модулів, receipts і критеріїв closeout наведений у [closeout-аудиті](../../reports/orchestrator/masterplan-closeout-2026-11-08.md).

## 3. Архітектурні інваріанти

Канонічний потік:

`IncidentSpec → collection/coverage → immutable artifacts → passages/media segments → relevance/normalization → claims/entities/events → source lineage/retrieval → evidence assessment → timelines/conflict/information dynamics/audience response → findings → deterministic report gates → bounded report or abstention`

Обов'язкові правила:

1. Оригінальні отримані байти не перезаписуються; кожен похідний запис має `derived_from`, версію інструмента, час і параметри.
2. Кожне емпіричне твердження звіту має locator, scope, час зрізу і provenance.
3. `claim`, `mention`, `stance`, `sentiment`, `emotion`, `reaction`, `verification` і `source attribution` є різними вимірами.
4. Цитування чи спростування чужого claim не означає його підтримки.
5. Copy/repost/near-duplicate не є новим незалежним source root.
6. Event time, recording time, publication time і observation time не зливаються.
7. Відсутній, прихований, невідомий і нульовий показник — різні стани.
8. Популярність коментаря, сума Telegram views і частка реакцій не представляють населення.
9. BM25/LLM/ASR/OCR/VLM outputs залишаються кандидатними, поки нема точного scope й незалежної перевірки.
10. Підозра, оперативне повідомлення та судове встановлення — різні процесуальні статуси.

## 4. Реалізований стан робочих потоків

| Workstream | Наявне | Відкрите |
|---|---|---|
| **W00–W02 baseline/collection/contracts** | Є baseline manifest, схеми, snapshot-replay і collectors. Історичний та поточний bounded case-run: 8/8 входів і 16/16 виходів кожного запуску збігаються з відповідними локальними маніфестами; 5/16 спільних виходів ідентичні побайтно ([content-free audit](../../reports/automated-case-run-2026-11-08/replay-audit-2026-11-08.md)). | Це не семантична валідація; точний execution-time dirty diff та lockfile відсутні. Coverage джерел не є переписом платформ. |
| **W03 narrative/claim** | `narrative_v3.py`, codebook, candidate outputs і тести. | Незалежний UA/RU/mixed gold, per-class метрики, семантичне розділення multi-claim та stance. |
| **W04 channel evidence** | Багатовимірний evidence record і candidate infrastructure markers. | Ручна evidence-supported оцінка каналів; operator/state control/operation participation залишаються невідомими без доказів. |
| **W05 source lineage** | Консервативні quote/forward/copy relations і кандидатні графи. | Кейсові claim-level dependency roots не встановлені. |
| **W06 claim retrieval/verification** | Append-only evidence ledger, source ingestion, candidate BM25 і verification state model. | У case run 0 accepted assessments/VerificationResults; passage locators/semantic entailment недостатні. |
| **W07–W08 event/time/conflict reconstruction** | Типізовані часи, candidate entity resolution і conflict aggregation. | Main case run: 574 mentions unresolved, 0 physical-event rows, 0 typed participant-position rows. Supplement: one source-reported day-level physical mention and its separate publication event, both unresolved. |
| **W09 information dynamics/coordination** | Exact Jaccard audit 369 pairs проти 367 LSH edges (99.46% candidate recall при Jaccard ≥0.60); 9,999 permutations, 16 exploratory tests із нульовими перевищеннями, Holm p=.0016. | Немає matched organic controls; результати залежать від цільової панелі й заданої нульової моделі; відхилена вибірка n=378 не ад'юдикована. |
| **W10 media** | Усі 607 унікальних Telegram assets пройшли strict technical full decode; 607 мають OCR/ASR candidates; 20 TikTok assets у локальному runner. | ASR/OCR accuracy, source-to-claim media links, event time/place і semantic content не валідовані; 55 platform entries не мають локальних файлів; 10 Telegram Desktop videos без доведеного походження виключені. [Full-decode receipt](../../reports/video-pipeline/telegram-full-decode-2026-11-08.md). |
| **W11 uncertainty** | Сценарні межі, explicit unknowns і leave-top-k/coverage sensitivities. | Немає каліброваних помилок класифікаторів або joint propagation; purposive panel не дає population CI. |
| **W12 report generation** | Constrained renderer, citation/denominator gates і PDF outputs. | Усі case assertions ще не мають достатніх accepted evidence assessments; semantic citation entailment не закрита. |
| **W13 evaluation/operations** | Structural harness 6/6, synthetic evidence-to-report smoke test, diff/replay/dispatch plumbing. | Semantic incident benchmark, F16 live prompt-injection control, accepted real correction replay і full run manifest. |
| **W14 audience response** | Typed MTProto aggregate serialization, bounded `getMessagesReactions` adapter, schema/contracts, frame aggregation and descriptive report gates. New aggregates use schema 1.1; the renderer remains compatible with 1.0. 10/10 current live available-state type/count parity; synthetic contract tests distinguish `no_update` and `wrong_peer_update` from message reaction states. | Live parity still covers only available reactions; synthetic fixtures do not establish Telegram response prevalence/semantics. Historical 39,598 scalar rows cannot be backfilled; no semantic classifiers/local gold, repeated snapshots or cross-platform harmonization. See §5. |

## 5. W14 — Audience Response Intelligence: current acceptance

Наданий користувачем огляд DR4 оцінює документ у 89/100 і приймає його методологічною основою. Це якісна оцінка самого огляду, не вимірювання accuracy classifiers. Підтверджені окремі висновки: topics/claims/stance/sentiment/emotion/engagement треба розділяти; target має зв'язуватися з Social Claim/Entity/Event; reaction count не означає підтримку; агрегати описують лише зібраний frame.

`src/tg_comments_collect.py` зберігає типізовані `MessageReactions.results` (standard emoji, custom emoji, paid/unknown), стан, суму для legacy compatibility і timestamp. `src/analysis/telegram_reaction_snapshots.py` виконує bounded aggregate-only refresh через linked discussion peer і message ID; список користувачів-реакторів не запитується. Специфікація W14: [`docs/specs/audience-response-v1.md`](../specs/audience-response-v1.md).

**Live parity sample:** на 10 уже зібраних публічних коментарях із трьох linked discussion threads поточний serialized reaction state/type/count vector збігся з відповіддю `messages.getMessagesReactions` у 10/10 випадках; усі 10 були `available`. Публічний content-free receipt: [`telegram-reaction-parity-2026-11-08.md`](../../reports/audience-response/telegram-reaction-parity-2026-11-08.md). Детальні рядки з ID зберігаються лише у приватному локальному output, режим файла `0600`, каталог `0700`; їх не додаємо до Git. Старий 6 листопада corpus містить 39 598 коментарів у 533 цільових гілках, але має лише scalar reaction totals. Сума історичного рядка не дорівнює поточному API sum у зразку; це різні часові зрізи, тож не є parity failure або доказом причини зміни.

Локальні fake-response контракти покривають `empty`, `current_user_excluded` (`min=True`), `no_update`, `wrong_peer_update`, помилку запиту та окремий `not_reported` при отриманому message update без reaction object. Тепер `no_update`/`wrong_peer_update` мають null reaction state, не створюють reaction snapshot, не перезаписують старе спостереження й окремо рахуються у звіті. Валідатор читає legacy aggregate schema 1.0 з її первісними двома статусами запитів; у звітах ці відсутні в 1.0 статуси показуються як `not_recorded`, а числовий нуль лишається нулем лише в 1.1, коли він записаний явно. Нові aggregates виходять як 1.1. Цільові тести модулів: 56 passed; повний suite після replay-аудитів: **671 passed, 16 subtests passed**. Це перевіряє нашу обробку fixtures, не живе значення кожної відповіді Telegram. Залишаються відкритими: ширша live parity перевірка інших станів/груп; повторні reaction snapshots; локальний multilingual gold; benchmark моделей; semantic accuracy; topic/emotion dashboard. Немає підстав звітувати частки населення чи політичні переконання користувачів.

## 6. Пріоритети й acceptance gates

### P0 — коректність bounded case

| Gate | Стан | Потрібний доказ закриття |
|---|---|---|
| **P0.1 Baseline/replay** | Частково: перелічено 65 reader-package artifacts і перевірено їхні поточні SHA/розміри; історичний та поточний bounded case-run мають 8/8 входів і 16/16 виходів, що збігаються з відповідними маніфестами; 5/16 спільних outputs збігаються між запусками побайтно ([case replay audit](../../reports/automated-case-run-2026-11-08/replay-audit-2026-11-08.md)). Exact-graph coordination null replay окремо збігся у 6/6 файлах ([receipt](../../reports/coordination-null-models-2026-11-08-lsh-audit/replay_receipt_2026-11-08.json)). | Не відтворено кожен reader-facing artifact повним end-to-end шляхом; точний execution-time dirty diff, dependency lock та еквівалентність mutable source-watch входу frozen snapshot не встановлені. Release hashes не підтверджують семантичну істину. |
| **P0.2 Source-to-finding** | **Частково просунуто:** попередній source-linked run мав 0 accepted records; окремий append-only ledger copy додає чотири `published_claim` / `ClaimMention` пари, а report bundle містить п'ять точних `source_attributed` цитат із п'яти архівованих офіційних сторінок і окрему контекстну цитату для абзацу про 26 осіб. Є лише одна вузька `supported_within_scope` оцінка щодо змісту сторінки МВС; фізичні твердження не перевірені. | Потрібні контрджерела, source-lineage і семантична sentence-to-source перевірка повного звіту. [Bounded assessment and source-statement bundles](../../reports/automated-case-run-2026-11-08/bounded-source-statement-assessment-2026-11-08.md). |
| **P0.3 Relevance/coverage** | **OPEN:** source/frame counts, strata та всі 378 sample IDs відтворені replay utility; попередній frame digest не збігається через незафіксоване початкове перетворення input ([receipt](../../reports/relevance-audit/replay-receipt-2026-11-08.json)). Вибірка не ад'юдикована. | Фактичне кодування й design-aware estimate або чесна межа неперевіреного recall. |
| **P0.4 Narrative/claim validation** | **OPEN:** candidate parser є; незалежний gold і метрики відсутні. | Frozen leakage-safe benchmark, per-class/per-language precision/recall, abstention і failure analysis. |
| **P0.5 Statistical/coordination reporting** | Частково: exact graph/null audit задокументований, external organic controls відсутні. | Зафіксувати controls, frame, null assumptions і чутливість; не приписувати оператора. |
| **P0.6 Physical event reconstruction** | **OPEN:** основний case run має 574 unresolved mentions і 0 фізичних timeline rows. Окремий source-reported run має одну unresolved physical mention із точністю до дня та одну окрему MVS publication mention; passage IDs і source IDs тепер зберігаються окремо. Це не підтверджена хронологія. | Потрібні додаткові time-anchored джерела, контрджерела, інтервали фізичних етапів і перевірка суперечностей. [Bounded event-mention run](../../reports/automated-case-run-2026-11-08/reported-event-reconstruction-2026-11-08/timeline.md). |
| **P0.7 Report integrity** | Структурні gates працюють; повної case evidence entailment немає. | Sentence-to-source trace, denominators, dangling-ID checks, failed operations і coverage gaps у release receipt. |
| **P0.8 W14 typed reaction capture** | Частково: live parity `available` збіг у 10/10 зразках/3 threads; synthetic contract paths cover empty/min/not-reported/no-update/wrong-peer/request failure; schema 1.1 writes and 1.0 reads; повний suite 671+16 проходить. | Live-check інших станів і ширше group coverage; timestamped repeated snapshots без reactor IDs. Історичні scalar rows не backfill. |

### P1 — семантична й медійна валідація

1. Незалежний frozen benchmark для claims, stance, channel evidence, events/time і W14 labels.
2. Перевірити 378 relevance records або повідомити, що coverage recall не виміряний.
3. Ув'язати source-lineage з конкретними claims та вказати незалежні roots лише там, де це підтримується.
4. Окремо оцінити reference ASR/OCR sample, clip offsets, quotation accuracy та source-to-claim links.
5. Перевірити органічні контрольні події та sensitivity до меж нульової моделі.
6. Запустити semantic end-to-end report evaluation; structural pass не замінює її.
7. Зберігати correction/retraction history та перевірити as-of replay на реальному update.

### P2 — переносність

Кросплатформні зіставлення, більше кейсів, реакційна історія, поляризація, analyst UI, графове сховище й складні ML/VLM компоненти додаються лише після явної семантики, coverage і benchmark відповідної платформи.

## 7. Правило closeout

Master Plan залишається **NOT COMPLETE**, доки P0 acceptance gates не підтверджені receipts і реальними source-to-report трасами; окремі P1 статуси мають бути розкриті. Bounded case може чесно завершитися unresolved висновками, але не може називати невідоме підтвердженим або семантично точним.

Поточний список відкритих умов, доказів, обмежень відео й офіційного source-watch — у [closeout report](../../reports/orchestrator/masterplan-closeout-2026-11-08.md). Вихідна v1.0 збережена як історичний документ і має позначку superseded.
