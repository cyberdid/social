# SOCIAL — Автономний аналіз інцидентів і соціальних конфліктів
## Інтегрований master plan v1.2

> **Дата оновлення:** 8 листопада 2026 року  
> **Статус:** чинний master plan, що замінює v1.1 та v1.0 у частині релізного аудиту артефактів, фінальної верифікації E2E тестів (745 passed, 16 subtests), результатів незалежного реал-тайм Red-Team аудиту (RT-FINDING-01..07), виправлення дефекту змішування валюти Telegram Stars у реакціях, узгодження криптографічних маніфестів і чесного закріплення залишкових блокерів acceptance gates.  
> **Статус closeout:** **NOT COMPLETE — НЕ ЗАВЕРШЕНО.** Локальні технічні структури, контракти валідації, 10/10 MTProto live reaction parity, 607/607 Telegram media full decode та розчеплення одиниць виміру повністю реалізовано й перевірено; однак кейсові емпіричні гейти P0.1 (`partial_open`), P0.2 (`partial_open`), P0.3 (`OPEN`), P0.4 (`OPEN`), P0.5 (`PARTIAL`), P0.6 (`OPEN`), P0.7 (`PARTIAL`), P0.8 (`PARTIAL / CLOSED (Contracts, Architecture & Parity)`) залишаються незакритими через об'єктивні залишкові блокери відповідно до мандату доброчесності (Integrity Mandate).  
> **Зміна v1.2:** 
> 1. Інтегровано результати 6 паралельних воркстрімів (M1 Replay & Release, M2 Evidence & Lineage, M3 Video & Transcript, M4 Audience & W14, M5 Red-Team, E2E Test Track).
> 2. Повністю узгоджено таблицю криптографічних гешів (RT-FINDING-01) з 65 reader-facing артефактами release manifest (1,408,889 байтів) та он-диск файлами.
> 3. Документовано багатосторонню розбіжність frame digest (RT-FINDING-02) та зафіксовано 100% неад'юдикованість n=378 вибірки релевантності (Gate P0.3 OPEN).
> 4. Розкрито залишкові блокери Gate P0.1 (`partial_open`): нефіксований execution-time dirty diff, відсутність lockfile та історичне використання mutable crawler snapshot.
> 5. Чітко контекстуалізовано два незалежні входження числа «367» (RT-FINDING-05): 367 акаунтів кампанії похвали Буданову проти 367 початкових LSH-ребер (369 у точному sweep).
> 6. Документовано виправлення розчеплення Telegram Stars у `src/analysis/audience_aggregation.py` та суворе збереження `quote_safe: false` для всіх 10 кандидатів правок ASR (RT-FINDING-06).
> 7. Посилено права директорії сирого ASR до `0700` (RT-FINDING-07).
> 8. Зафіксовано еволюцію тестового набору: 671/683 → 687 → 745 passed (16 subtests).

Версія master plan не є оцінкою готовності продукту. Наявність коду, схем чи тестів не підтверджує семантичну точність, повне покриття джерел або істинність висновку про реальну подію. Для кожного workstream окремо вказані структурна готовність, case evidence та невирішені acceptance gates.

---

## 1. Метод читання і межі

| Позначка | Значення |
|---|---|
| **Реалізовано — структура** | Є код, контракт або звітний gate; це підтверджує детерміністичну поведінку структури, не точність висновків. |
| **Частково реалізовано** | Є робочий компонент або обмежений пілот; покриття чи приймальні критерії ще не закриті. |
| **Не оцінено** | Немає незалежного локального еталона або потрібного вимірювання якості. |
| **OPEN gate** | Перевірювана умова завершення наразі не виконана або не має достатнього емпіричного свідчення. |
| **PARTIAL OPEN gate** | Технічні компоненти й часткові аудити зійшлися, але залишкові системні або джерельні блокери перешкоджають сертифікації. |
| **P0** | Коректність і доказовість першого обмеженого кейсу; блокує твердження про завершений інцидентний продукт. |
| **P1** | Валідація та розширення семантичних, медійних і аналітичних компонентів. |
| **P2** | Масштабування, міжкейсова переносність, додаткові моделі й інтерфейси після P0/P1 gates. |

Social готує відтворюваний, доказово обмежений Incident Analytical Package для аналітика. Система має зберігати джерела, твердження, суперечності, часи, невдалі операції й покриття, а також повертати `unknown`, `insufficient_evidence` або `conflicting_evidence`, коли даних недостатньо.

Social не робить автоматичних правових висновків, не встановлює приховані мотиви чи державне керування без належних доказів, не виводить громадську думку з цільової панелі та не трактує копії, перегляди, реакції або згоду моделей як незалежне підтвердження.

---

## 2. Deep Research: реєстр і provenance

Архівні звіти з manifest від 5 листопада тут позначені **AR1–AR7**, аби не плутати їх із поточними дослідницькими потоками **DR1–DR4**. Архівні файли збережено під початковими назвами; їхній зміст не підмінює сучасні DR1–DR4.

| Потік | Поточний документ і provenance | Як використовується в Master Plan |
|---|---|---|
| **DR1 — Scientific Validation: narratives, channel attribution, uncertainty** | [Фінальний PDF, 23 сторінки](../research/DR1-scientific-validation-2026.pdf), SHA-256 `e817f5340cf1869294ef6d3afe356146b36c027ac4348bcd2941c26451cc5e4b`. Точна копія звірена з вихідним PDF; подробиці — у [source manifest](../research/current-deep-research-source-manifest-2026-11-08.md). | Підстава для W03/W04/W11 і P0.3/P0.4: тема, claim, stance і verification розділяються; джерельна атрибуція багатовимірна; сценарні межі не видаються за репрезентативні оцінки. Поточні реалізації структурні, семантична якість не оцінена. |
| **DR2 — coordination, statistics, sampling** | [Фінальний огляд](../research/DR2-coordination-statistics-sampling-2026-11-08.md), доповнений [exact-graph аудитом](../../reports/coordination-null-models-2026-11-08-lsh-audit.md). | Методологічна основа W09 і статистичних release gates. Exact graph та null-model перевірки виконані на визначеній цільовій панелі; organic controls і міжкейсова переносність лишаються відкритими. Результати не доводять організатора чи державну атрибуцію. |
| **DR3 — autonomous social conflict and incident reconstruction** | [Фінальний PDF, 30 сторінок](../research/DR3-autonomous-incident-reconstruction-2026.pdf), SHA-256 `a451e0b517b20a0ddfbe58242048925fc8b90d8f57a4d8277ae1456d3bf8c7d6`. Точну копію та метадані звірено; source manifest містить деталі. | Підстава для W06–W10/W12/W13: physical і communication timelines різні; час події та публікації не зливаються; retrieval candidate не є verification; source roots треба відновлювати, а не рахувати повтори. Реальний case reconstruction і source-to-finding trace не пройшли acceptance. |
| **DR4 — audience response, sentiment, emotion, engagement** | [Наданий фінальний огляд](../research/DR4-audience-response-2026-11-08.md); [отримана рецензія](../research/DR4-review-received-2026-11-08.md). Оцінка 89/100 — це надана рецензентська оцінка документа, а не калібрована метрика точності Social. | Прийнята методологічна основа W14. MTProto typed aggregate capture перевірено на 10 коментарях/3 гілках: поточні collector vectors збіглися з API vectors 10/10; дефект сумування Telegram Stars із реакціями виправлено; повне покриття, repeated snapshots і semantic validation відкриті. |
| **VIDEO** | [Video Evidence Processing Pipeline v0.1](social-video-evidence-pipeline-v0.1.md). | Архітектурна основа W10. Pipeline outputs — технічні спостереження-кандидати, а не підтвердження місця, часу, мовця, події чи claim. |

Файли `raw/deep-research/DR1–DR7-2026-11-05.md` — архівні звіти AR1–AR7, а не поточні DR1–DR7. Не використовувати їхні назви як ідентифікатори поточних потоків.

### 2.1. Висновки DR1/DR3, звірені з кодом

**DR1.** `src/analysis/narrative_v3.py` видає консервативні кандидатні мітки з окремими полями теми/claim/позиції, але це не повна, локально валідована реалізація рекомендованого класифікатора. Для корпусу є 555 candidate claims; `semantic_accuracy=not_evaluated`. Незалежного людського gold set і per-class/per-language метрик немає. `src/analysis/channel_evidence.py` відокремлює origin, entity type, operator, content orientation, infrastructure та operational attribution; у snapshot 246 профільних записів/239 назв лишилися невідомими за основними атрибуційними вимірами, а 137 infrastructure candidates — лише підстави для перевірки. `src/analysis/uncertainty_scenarios.py` дає сценарні/частково ідентифікаційні межі; це не калібрований joint measurement-error model і не інтервал для населення.

**DR3.** `src/analysis/event_reconstruction.py` зберігає часові типи й unresolved candidate links. Основний case run має 574 communication/event mentions, 0 фізичних event rows і жодної встановленої physical timeline; окремий bounded run додає одну unresolved day-level source-reported mention, не підтверджену хронологію. Source-linked run порівняв 555 candidate claims із 30 passages і 11 897 BM25 matches; початкові accepted Evidence Assessments і VerificationResults — 0. Claim-level source-lineage не запускався. Отже, структурні схеми й retrieval не є свідченням правильності реконструкції інциденту.

### 2.2. Аудит DR2 та розмежування двох контекстів числа «367» (RT-FINDING-05)

Незалежний Red-Team аудит (Finding RT-FINDING-05) виявив потенційне джерело плутанини: ціле число **367** фігурує у двох абсолютно різних емпіричних контекстах проєкту:
1. **Кампанія похвали Буданову в коментарях:** 126 фраз-шаблонів, 438 коментарів у 4 обговореннях, опублікованих **367 обліковими записами користувачів** (`coordination_null_models.py:174`).
2. **Початковий граф координації MinHash-LSH:** **367 пар постів** із подібністю Jaccard $\ge 0.60$ між 354 постами та 113 каналами. Під час точного попарного аудиту (exact pairwise sweep) цей набір розширився до **369 пар** (повнота LSH склала 99.458%) на 357 постах та 113 каналах (`DR2-coordination-statistics-sampling-2026-11-08.md`).

Зсув знаменника з 367 до 369 у координаційному графі стався через виявлення 2 пар із часовими затримками 33.08 та 184.6 хвилин. Оскільки обидві затримки перевищують 30 хвилин, чисельники швидкої координації ($\le 10$ хв, $\le 30$ хв) не змінилися, але базовий знаменник пар зріс до 369.

### 2.3. Відеоконвеєр, цитатна безпека та права доступу (W10 / M3 / RT-FINDING-06, 07)

1. **Технічний Full Decode:** Усі 607 унікальних медіафайлів Telegram та 20 TikTok-відео декодовано в null-sink за допомогою `ffmpeg -xerror` без жодної помилки.
2. **Незмінність сирого ASR:** Файл сирих спостережень мовлення (`telegram_text_observations.jsonl`, 10,462,222 байтів, SHA-256 `987ee53ff...`) залишається 100% незмінним.
3. **Строга цитатна безпека (`quote_safe: false`):** Усі 10 кандидатів правок другого проходу (`correction_candidates.jsonl`) мають `quote_safe: false`, оскільки жодна правка не пройшла акустичного прослуховування людиною. Чутливі медичні та правові терміни («перелом хребта», «СЗЧ-шники») ізольовано в статусі `needs_audio_review`.
4. **Харденінг прав директорії:** Права директорії `$SOCIAL_MEDIA_ROOT/telegram/analysis/asr-bulk-20261108` посилено до `0700` (`drwx------`), усунувши зауваження RT-FINDING-07.

---

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
11. Telegram Stars (платні зірки) є грошовою транзакцією і категорично відокремлюються від підрахунку емодзі-реакцій (дефект виправлено у v1.2).

---

## 4. Реалізований стан робочих потоків

| Workstream | Наявне | Відкрите |
|---|---|---|
| **W00–W02 baseline/collection/contracts** | Є baseline manifest, схеми, snapshot-replay і collectors. 65 reader-facing release artifacts повністю верифіковані он-диск (1,408,889 байтів, нуль розбіжностей хешів). Історичний та поточний bounded case-run: 8/8 входів і 16/16 виходів кожного збігаються з локальними маніфестами; 5/16 спільних виходів ідентичні побайтно. | Це не семантична валідація; точний execution-time dirty diff та lockfile відсутні; історичний запуск використовував mutable crawler snapshot замість frozen директорії. Gate P0.1 кваліфіковано як `partial_open`. |
| **W03 narrative/claim** | `narrative_v3.py`, codebook, candidate outputs і тести. | Незалежний UA/RU/mixed gold, per-class метрики, семантичне розділення multi-claim та stance. Gate P0.4 залишається OPEN. |
| **W04 channel evidence** | Багатовимірний evidence record і candidate infrastructure markers. | Ручна evidence-supported оцінка каналів; operator/state control/operation participation залишаються невідомими без доказів. |
| **W05 source lineage** | Консервативні quote/forward/copy relations і кандидатні графи. Таблиця 8.2 узгоджена он-диск. | У 23,386 постах знайдено 0 підтверджених ребер залежності та 0 незалежних коренів (`independent_roots_lower_bound: 0`). Gate P0.2 залишається `partial_open`. |
| **W06 claim retrieval/verification** | Append-only evidence ledger, source ingestion, candidate BM25 і verification state model. | У case run 0 accepted assessments/VerificationResults з 555 кандидатних claims проти 30 уривків (11,897 попадань). Passage locators/semantic entailment недостатні. |
| **W07–W08 event/time/conflict reconstruction** | Типізовані часи, candidate entity resolution і conflict aggregation. | Main case run: 574 mentions unresolved, 0 physical-event rows, 0 typed participant-position rows. Повної фізичної хронології нема. Gate P0.6 залишається OPEN. |
| **W09 information dynamics/coordination** | Exact Jaccard audit 369 pairs проти 367 LSH edges (99.46% candidate recall при Jaccard ≥0.60); 9,999 перестановок, 16 exploratory tests із нульовими перевищеннями, Holm p=.0016. | Немає matched organic controls; результати залежать від цільової панелі й заданої нульової моделі; відхилена вибірка n=378 не ад'юдикована. Gate P0.5 PARTIAL. |
| **W10 media** | Усі 607 унікальних Telegram assets пройшли strict technical full decode; 607 мають OCR/ASR candidates; 20 TikTok assets у локальному runner. Сирий ASR незмінний. 10 кандидатів редакційних правок мають `quote_safe: false`. Права директорії ASR посилено до `0700`. | ASR/OCR accuracy, source-to-claim media links, event time/place і semantic content не валідовані акустично; 55 platform entries не мають локальних файлів; 10 Telegram Desktop videos виключені. Gate P1 OPEN. |
| **W11 uncertainty** | Сценарні межі, explicit unknowns і leave-top-k/coverage sensitivities. | Немає каліброваних помилок класифікаторів або joint propagation; purposive panel не дає population CI. |
| **W12 report generation** | Constrained renderer, citation/denominator gates і PDF outputs. | Усі case assertions ще не мають достатніх accepted evidence assessments; semantic citation entailment не закрита. Gate P0.7 PARTIAL. |
| **W13 evaluation/operations** | Незалежний 4-рівневий E2E тестовий набір (58 тестів). Повний репозиторний набір тестів: **745 passed, 16 subtests passed**. | Semantic incident benchmark, live prompt-injection control, accepted real correction replay і full run manifest. |
| **W14 audience response** | Typed MTProto aggregate serialization, bounded `getMessagesReactions` adapter, schema/contracts, frame aggregation and descriptive report gates. 10/10 live parity. Виправлено дефект змішування одиниць (Stars decoupling) у `audience_aggregation.py`. Тести чутливості та анти-генералізації. | Live parity охоплює available reactions; історичні 39,598 коментарів лишаються скалярними; семантичні класифікатори відсутні. Gate P0.8 PARTIAL / CLOSED (Contracts, Architecture & Parity). |

---

## 5. W14 — Audience Response Intelligence та виправлення Stars Decoupling

У версії v1.2 повністю розв'язано дефект змішування одиниць виміру у функціях ранжування реакцій (`src/analysis/audience_aggregation.py`):
1. **Розчеплення валюти й емодзі:** Платні зірки Telegram (`paid` / Telegram Stars) тепер зберігаються окремо як сума внесених зірок і не сумуються безпосередньо з кількістю стандартних реакцій (`non_paid_reaction_count`). Функція `largest_available_reaction_comments` ранжує коментарі виключно за кількістю реакцій або кортежем із пріоритетом емодзі-реакцій.
2. **Захист від деанонімізації:** Метод `messages.getMessageReactionsList` заблоковано архітектурно; жодні ідентифікатори реакторів не збираються й не зберігаються.
3. **Анти-генералізаційний валідатор:** Забезпечує лексичний контроль за відсутністю узагальнень реакцій аудиторії на все населення чи електорат.

---

## 6. Пріоритети й acceptance gates (Актуальний стан v1.2)

### P0 — коректність bounded case

| Gate | Стан v1.2 | Що є доказом | Залишкові блокери для завершення |
|---|---|---|---|
| **P0.1 Baseline/replay** | **PARTIAL OPEN** | 65 артефактів release manifest верифіковані он-диск (1,408,889 байтів, повний збіг SHA-256). Історичний та поточний bounded case-run: 8/8 входів і 16/16 виходів збігаються з відповідними маніфестами; 5/16 спільних outputs збігаються побайтно. Реплей координації збігся у 6/6 файлах. | Не відтворено кожен reader-facing artifact повним end-to-end шляхом. Відсутні зафіксований execution-time dirty diff і dependency lockfile (`requirements.lock`/`uv.lock`). Історичний запуск звертався до mutable crawler path (`reports/source-watch/latest.*`), а не до frozen snapshot (`20261108/`). |
| **P0.2 Source-to-finding** | **PARTIAL OPEN** | Офіційні заяви відокремлені від фізичних фактів. Заява МВС про 26 осіб оцінена як `supported_within_scope` щодо тексту заяви. Окремий ledger містить 4 пари claim/mention та 5 точних цитат. | 555 кандидатних claims проти 30 уривків дали **0 accepted VerificationResults** і **0 підтверджених ребер** (0 незалежних коренів). Фізичні факти не встановлені. |
| **P0.3 Relevance/coverage** | **OPEN** | Детерміністичний реплей із seed `20261108` відтворює всі 4 страти та точний список n=378 sample IDs з N=19,945 відхилених записів. | **Багатостороння невідтворюваність frame digest:** початковий `70155a55...` проти `ecdb98...` у нотатках проти `02ab55...` у поточному чеку через незафіксовані трансформації рядків. **0 з 378 записів ад'юдиковано людиною;** false-negative rate та recall залишаються повністю `unknown`. |
| **P0.4 Narrative/claim validation** | **OPEN** | Кандидатний парсер `narrative_v3.py`, схеми й контрактні тести працюють. | Відсутній незалежний людський gold set; відсутні per-class/per-language метрики точності/повноти та leakage-safe holdout. |
| **P0.5 Statistical/coordination reporting** | **PARTIAL** | Exact Jaccard sweep (369 пар, 99.46% повнота) та 9,999 перестановок нульової моделі підтверджено. | Відсутні зіставлені органічні контролі (matched organic controls). Висновки умовні на визначену цільову панель і не доводять організатора. |
| **P0.6 Physical event reconstruction** | **OPEN** | Офіційна комунікаційна хронологія відокремлена від фізичної; passage IDs відокремлено від source IDs. | У головному прогоні кейсу **574 нерозв'язані згадки подій і 0 рядків фізичного таймлайну**. Фізична хронологія інциденту відсутня. |
| **P0.7 Report/release integrity** | **PARTIAL** | 65 релізних артефактів мають перевірені розміри й геші. Аудит цитувань задокументовано. | Відсутня повна семантична перевірка відповідності тексту звіту первинним джерелам (semantic citation entailment). |
| **P0.8 W14 typed reaction capture** | **PARTIAL / CLOSED (Contracts, Architecture & Parity)** | Дефект змішування Stars decoupled; 10/10 live parity у стані `available`; контракти для `empty`, `current_user_excluded`, `not_reported`, `no_update`, `wrong_peer_update` перевірені; нуль реакторних ID. | Потребує ширшої live-перевірки інших станів та повторних знімків у часі; історичні 39,598 рядків залишаються скалярними. |

### P1 — семантична й медійна валідація (OPEN)
1. Відсутній незалежний frozen benchmark для claims, stance, channel evidence, events/time і W14.
2. 378 relevance records залишаються неад'юдикованими (recall не виміряний).
3. Source-lineage не має доведених незалежних коренів.
4. Медійні розшифровки не мають reference transcripts / WER / CER; акустичне прослуховування людиною не проводилося (`quote_safe: false` для всіх 10 кандидатів).

### P2 — переносність і масштабування (OPEN)
Кросплатформні зіставлення, міграція на інші кейси, граф-орієнтоване сховище та VLM-пайплайни відкриваються виключно після закриття P0/P1 гейтів.

---

## 7. Результати незалежного Red-Team аудиту (RT-FINDING-01..07)

1. **RT-FINDING-01 (HIGH, УЗГОДЖЕНО):** Таблиця 8.2 у звіті M2 містила застарілі розміри й геші для 6 артефактів. У v1.2 Таблицю 8.2 узгоджено з реальними он-диск файлами та release manifest.
2. **RT-FINDING-02 (HIGH, ПІДТВЕРДЖЕНО):** Розбіжність frame digest у реплеї релевантності та 0 ад'юдикованих записів із 378. Gate P0.3 залишається OPEN.
3. **RT-FINDING-03 (HIGH, ПІДТВЕРДЖЕНО):** Залишкові блокери Gate P0.1 (`partial_open`): dirty diff, відсутність lockfile, mutable crawler history.
4. **RT-FINDING-04 (MEDIUM, ПІДТВЕРДЖЕНО):** 0 прийнятих VerificationResults, 0 незалежних коренів лінеджу, 0 рядків фізичного таймлайну (574 unresolved mentions).
5. **RT-FINDING-05 (MEDIUM, ДИСАМБІГУЙОВАНО):** Контекстуалізовано різницю між 367 акаунтами коментарів та 367/369 ребрами координації.
6. **RT-FINDING-06 (LOW, ПІДТВЕРДЖЕНО):** Відсутність аудіо-прослуховування; 10/10 кандидатів правок ASR мають `quote_safe: false`.
7. **RT-FINDING-07 (LOW, ВИПРАВЛЕНО):** Права каталогу сирого ASR посилено до `0700`.
8. **RT-FINDING-08 (INFORMATIONAL, СИНХРОНІЗОВАНО):** Еволюція лічильників тестів (671/683 → 687 → 745 passed, 16 subtests).

---

## 8. Правило closeout і підсумковий вердикт

Master Plan залишається **NOT COMPLETE — НЕ ЗАВЕРШЕНО**. 

Відповідно до мандату доброчесності (Integrity Mandate), автоматичні програмні контракти, технічний декодинг і фасадні евристики категорично заборонено видавати за закриття наукових чи емпіричних гейтів. Доки не створено незалежний людський gold set, не проведено розмітку вибірки релевантності, не верифіковано фізичний таймлайн і не отримано контрджерела з оцінкою повної семантичної точності, Social Master Plan чесно, відкрито й доказово кваліфікується як незавершений на рівні емпіричних висновків про реальний інцидент.

Повний перелік доказів, гешів та матриць наведено у фінальному звіті [Master Plan Final Closeout](../../reports/orchestrator/masterplan-closeout-2026-11-08-final.md).
