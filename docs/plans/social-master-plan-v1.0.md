# SOCIAL — Автономний аналіз інцидентів і соціальних конфліктів
## Інтегрований master plan v1.0

> **Архівна версія.** Її твердження про відсутність поточних DR1 і DR3 були виправлені після знаходження фінальних PDF. Див. [чинний Master Plan v1.1](social-master-plan-v1.1.md) та [звіт інтеграції й closeout-аудиту](../../reports/orchestrator/masterplan-closeout-2026-11-08.md).

> **Дата:** 8 листопада 2026 року <br>
> **Статус документа:** чинний інтегрований план реалізації. <br>
> **Статус closeout:** **NOT COMPLETE — НЕ ЗАВЕРШЕНО.** Реалізація часткова; істотні acceptance gates на реальному кейсі залишаються відкритими. <br>
> **Межа цієї версії:** консолідація архітектури, фактичного стану, пріоритетів і перевірюваних критеріїв. Цей документ сам по собі не змінює програмний код і не є доказом завершення реалізації.
> **Мова звітів:** українська; вхідні матеріали можуть бути українською, російською, англійською або змішаними.

Версія **v1.0** позначає версію master plan, а не готовність продукту. Чинний стан коду та доказів наведено окремо від проєктних цілей. Наявність коду, схем або тестів не підтверджує семантичну точність, повне покриття джерел чи істинність висновку про подію.

## Як читати статуси

| Позначка | Значення |
|---|---|
| **Реалізовано — структура** | Є код, контракт або звітний gate; це підтверджує поведінку структури, не точність висновків. |
| **Частково реалізовано** | Є робочий компонент або обмежений пілот; покриття чи приймальні критерії ще не закриті. |
| **Не оцінено** | Немає незалежного локального еталона або потрібного вимірювання якості. |
| **Заплановано** | Реалізацію ще треба виконати. |
| **OPEN gate** | Перевірювана умова завершення наразі не виконана або не має достатнього свідчення. |
| **P0** | Коректність і доказовість першого обмеженого кейсу; блокує твердження про завершений інцидентний продукт. |
| **P1** | Валідація й розширення основних семантичних, медійних та аналітичних компонентів. |
| **P2** | Масштабування, міжкейсова переносність, додаткові моделі та інтерфейси після проходження P0/P1 gates. |

---

## 1. Продукт, межі та результат

Мета Social — автономно підготувати відтворюваний, доказово обмежений **Incident Analytical Package** для аналітика. Система має збирати доступні матеріали, відокремлювати публікації від реальних подій, зберігати походження тверджень, явно фіксувати суперечності та формувати обмежений висновок або abstention.

Пакет справи має містити:

1. короткий підсумок встановленого, спірного й невідомого;
2. окрему часову лінію фізичних подій і комунікацій;
3. матрицю атомарних claims із позицією мовця та оцінкою доказів;
4. карту джерельних залежностей і незалежних roots, де їх вдалося встановити;
5. інформаційну динаміку й координаційні сигнали з явним знаменником, рамкою вибірки та обмеженнями;
6. медійне досьє з точними фрагментами, технічними метаданими та невстановленими атрибутами;
7. coverage, невизначеність, відкриті питання й невдалі операції;
8. машинозчитувані записи, run manifest, версії, hashes і receipts.

Вихід чітко розрізняє:

- **спостережений цифровий факт** — наприклад, архівований пост із часом публікації;
- **атрибутоване твердження** — джерело повідомляє про подію;
- **підтверджений у межах scope висновок** — окремий доказ підтримує вузько визначену обставину.

### Негативні межі

Social не робить автоматичних правових висновків, не встановлює приховані мотиви чи державне управління без відповідних доказів, не виводить громадську думку з цільової панелі та не трактує кількість копій, переглядів, реакцій або узгодженість моделей як незалежне підтвердження. Автономне `unknown`, `insufficient_evidence` або `conflicting_evidence` є коректним результатом.

---

## 2. Джерела та походження плану

План використовує дві незалежні системи позначень. Архівний manifest від 5 листопада нумерує сім старіших звітів як DR1–DR7; у цьому документі вони названі **AR1–AR7** (Archive Reports), щоб відрізняти їх від поточних дослідницьких потоків **DR1–DR4**. Архівний реєстр: [manifest Deep Research від 5 листопада](../../raw/deep-research/manifest-2026-11-05.json). AR позначення нижче — лише читабельні aliases до фактичних archive IDs, воно не перейменовує збережені файли.

### Архівні звіти AR1–AR7

| Archive ID | Фактичний файл | Використання та межа |
|---|---|---|
| **AR1** (manifest DR1) | [Методологія аналізу інформаційних хвиль Telegram](../../raw/deep-research/DR1-2026-11-05.md) | Попереднє методологічне джерело щодо вибірки, класифікації та обережного тлумачення інформаційних хвиль. Не є поточним DR1 stream. |
| **AR2** (manifest DR2) | [Критерії класифікації Telegram-каналів](../../raw/deep-research/DR2-2026-11-05.md) | Архівний огляд походження/орієнтації каналів і меж категорій. Не є поточним DR2 stream про статистику й вибірку. |
| **AR3** (manifest DR3) | [Аналітичні публікації](../../raw/deep-research/DR3-2026-11-05.md) | Архівне зведення публічних аналітичних матеріалів та їхніх тверджень. Не є звітом про архітектуру incident reconstruction і не є поточним DR3 stream. |
| **AR4** (manifest DR4) | [Методи виявлення coordinated behavior](../../raw/deep-research/DR4-2026-11-05.md) | Архівний огляд CIB-сигналів і параметрів. Не є поточним DR4 stream про audience response. |
| **AR5** (manifest DR5) | [Підрахунок переглядів у Telegram](../../raw/deep-research/DR5-2026-11-05.md) | Архівне джерело щодо view counters; лічильники лишаються snapshot-метриками, не унікальним reach. |
| **AR6** (manifest DR6) | [Продовжувальний ефект і inoculation](../../raw/deep-research/DR6-2026-11-05.md) | Архівне джерело про prebunking/debunking; це не реалізаційне підтвердження. |
| **AR7** (manifest DR7) | [Доступ дослідників до даних соцмереж](../../raw/deep-research/DR7-2026-11-05.md) | Архівне джерело про доступ і обмеження платформ; конкретні доступи перевіряються для кожного запуску. |

Файли AR1–AR7 імпортовані з user-provided Deep Research results; маніфест фіксує їхні початкові назви, розміри й SHA-256. Їхні архівні ID не використовуються для позначення нинішніх DR1–DR4.

### Поточні дослідницькі потоки DR1–DR4

| Потік | Доступність і provenance | Використання у v1.0 |
|---|---|---|
| **DR1 — Scientific Validation / Narrative / Channel / Uncertainty** | Окремий фінальний звіт, на який посилається v0.1 як `Scientific_Validation_Narrative_Channel_Uncertainty_Social_2026.pdf`, не знайдений серед доступних локальних артефактів репозиторію або Downloads. Його зміст тут не вважається переглянутим. | Висновки з цього окремого DR1 не приписуються і не використовуються як перевірена підстава. Пов'язані методологічні питання лишаються вимогами до локальної валідації. |
| **DR2 — статистика, координація та межі вибірки** | [Фінальний звіт DR2 від 8 листопада](../research/DR2-coordination-statistics-sampling-2026-11-08.md). | Прийнята методологічна основа для W09, W11 і статистичних release gates; висновки залишаються умовними щодо зафіксованих даних і припущень нульової моделі, не є атрибуцією оператора. |
| **DR3 — Autonomous Social Conflict Incident Reconstruction** | Окремий фінальний звіт, на який посилається v0.1 як `Autonomous_Social_Conflict_Incident_Reconstruction_2026.pdf`, не знайдений серед доступних локальних артефактів репозиторію або Downloads. Його зміст тут не вважається переглянутим. | Звітні методи та висновки з цього DR3 не приписуються. Реконструкція W07/W08 у плані спирається на наявні локальні контракти, case receipts і явні acceptance gates. |
| **DR4 — Audience Response, Sentiment, Emotion and Engagement** | [Фінальна локальна копія DR4 від 8 листопада](../research/DR4-audience-response-2026-11-08.md), підготовлена з user-provided документа. | Прийнята методологічна та архітектурна основа W14: цілі аналізу, типи міток, реакції, знаменники, оцінювання та межі узагальнення. Реальний стан імплементації перевіряється окремо в §§4–6. |
| **VIDEO** | [Video Evidence Processing Pipeline v0.1](social-video-evidence-pipeline-v0.1.md), внутрішня копія вихідного документа. | Спеціалізована схема W10; архітектурний план не засвідчує повну реалізацію або достовірність медійних висновків. |
| **BASELINE** | [Базовий зріз і replay-обмеження](../../BASELINE.md), [поточний стан архітектури](../architecture/current_state.md). | Розділяє базовий код до поточного циклу, нові зміни й доступність локальних даних. Звіти про replay стосуються лише перелічених артефактів. |
| **Вихідний план** | `$DOWNLOADS_ROOT/Social_Autonomous_Incident_Analysis_Master_Plan_v0.1.md` | Вихідна архітектура та workstreams W00–W13. v1.0 оновлює застарілий статус очікування DR2, додає W14 і підтверджений стан; недоступні DR1/DR3 не трактуються як прочитані. |

### База проєкту станом на 8 листопада

[Baseline manifest](../../reports/baseline_manifest.json) і [звіт про replay legacy агрегатів](../../reports/operations/legacy-aggregate-reproduction-2026-11-08.md) підтверджують відтворення визначеного набору результатів із snapshot. Це не підтверджує коректність legacy міток або повну відтворюваність усіх попередніх виходів. Цільова Telegram-панель і суми snapshot counters не є переписом Telegram чи оцінкою унікального охоплення.

---

## 3. Архітектурна основа та інваріанти

Архітектурний принцип — **Evidence Ledger → Evidence Projection**:

- **Evidence Ledger** — append-only історія джерел, отриманих байтів, фрагментів, кандидатних витягів, залежностей, assessments, виправлень і повторних оцінок.
- **Evidence Projection** — версійований стан справи на задане `as_of`: джерельне покриття, unresolved claims, часові обмеження, конфліктні альтернативи й звіт.

Канонічний потік:

`IncidentSpec → coverage/collection → archive/artifacts → passages/media segments → relevance and normalization → claims/entities/events → lineage and retrieval → evidence assessment → timelines/conflict/information dynamics/audience response → findings → deterministic report gates → bounded report or abstention`

Обов'язкові інваріанти:

1. Оригінальні отримані байти не перезаписуються; похідні записи мають `derived_from`, версію інструмента й параметри.
2. Кожне емпіричне твердження у звіті має точний evidence locator, scope, часовий зріз і provenance.
3. `Claim`, `mention`, `stance`, `sentiment`, `emotion`, `reaction`, `verification` і `source attribution` є різними полями.
4. Цитування або спростування чужого claim не означає підтримки.
5. Repost/copy/near-duplicate не створює нового незалежного source root.
6. Час події, запису, публікації, спостереження, отримання та snapshot не взаємозамінні.
7. «До» не доводить причинність; популярність не доводить вплив або координацію.
8. Відсутність знайденого матеріалу не означає, що події не було.
9. `unknown` не прирівнюється до `false`; `not_found` не прирівнюється до `refuted`.
10. Автоматичні класифікації, lineage edges, VLM/ASR/OCR виходи та LLM оцінки лишаються кандидатними без окремої процедури прийняття.
11. Лічильники, знаменники, hashes, посилання та часові обмеження обчислюються детермінованим кодом.
12. Оцінки comment frame описують тільки фактично зібрані коментарі; вони не є громадською думкою.
13. Telegram reaction counts — платформні агрегати на час спостереження, не голоси за claim, не список унікальних людей і не емоція тексту.
14. `as_of` replay не використовує майбутні матеріали як contemporaneous support.

---

## 4. Фактичний стан реалізації на 8 листопада 2026 року

Поточне дерево містить незакомічені зміни цього циклу. Нижче «реалізовано» стосується наявності компонента й структурних перевірок. Воно не означає production-релізу, семантичної оцінки чи завершеної реконструкції реального кейсу.

| Сфера | Що має підтвердження зараз | Що не можна з цього виснувати |
|---|---|---|
| Базові агрегати | Частина legacy CSV/JSON була відтворена на збереженому processed snapshot; винятки описані в [replay receipt](../../reports/operations/legacy-aggregate-reproduction-2026-11-08.md). | Не підтверджено правильність legacy narrative labels, атрибуції каналів, незалежність джерел чи повноту інших виходів. |
| Кейсний pipeline | Окремий run опрацював надані файли й створив кандидатні виходи; останній source-linked run шукав 555 claim candidates у 30 passages, але прийнятих Evidence Assessments і Verification Results — **0**. Див. [автоматизований case-run receipt](../../reports/automated-case-run-2026-11-08/summary.md). | Це не верифікація claims і не завершений end-to-end випадок із прийнятим фактичним висновком. |
| Події | У case-run залишено 574 event mentions нерозв'язаними; physical-event timeline rows — **0**. | Порожня timeline не свідчить про відсутність фізичних подій; час і послідовність подій не встановлено. |
| W00 orchestrator | Є контракт і bounded dry-run із receipt. | Той run мав нуль цілей і нуль source snapshots; downstream стадії були `not_run`, тому це не повний автоматичний запуск. |
| W04/W05 | Є кандидатні channel-evidence та source-lineage експорти; вони зберігають невідомі й непідтверджені стани. | Origin/operator/orientation/operation attribution не встановлено; кандидатні edges не підтверджують незалежні roots. |
| W09 / DR2 | DR2 прийнято як методологічну основу; повторна перевірка LSH і null-model роботи задокументовані. | Один кейс і цільова панель не доводять універсальні пороги, організатора чи державну атрибуцію; matched organic controls та аудит відхилених записів лишаються відкритими. |
| W10 media | Є технічні декоди локальних відео, fingerprints та кандидатні ASR/VLM виходи. | Немає референсних транскриптів/WER, незалежної перевірки відеоцитат або встановлення часу/місця з медіа. |
| W12/W13 | Валідатори й структурні gates існують; наявний звіт зафіксував 6/6 frozen structural controls. | Це не semantic end-to-end benchmark. F16 prompt-injection контроль і повна incident-level оцінка лишаються відкритими. |
| W14 audience response | Типізований збір реакцій, bounded refresh, contracts, target/abstention shape, frame aggregation і compact per-platform stance/topic-emotion/reaction-count views реалізовані. Незалежний review після виправлень PASS; Task 6 Step 3 закрито. Пілот охопив один коментар. [W14 plan](../superpowers/plans/2026-11-08-audience-response-intelligence.md) | Семантичні classifier-и, gold set і валідований topic/emotion dashboard не реалізовані або не оцінені. Мовний regex — лише відомі лексичні шаблони, не семантична гарантія. Історична scalar-величина не дає відновити emoji types чи минулу динаміку. |

Нормативним джерелом для поточних виходів цього циклу є окремі receipts і специфікації, на які посилається цей план. Їхні кількісні результати описують відповідні зафіксовані inputs, а не всі джерела чи повний реальний інцидент.

---

## 5. Workstream map W00–W14

| ID | Напрям | Стан на 08.11.2026 | Наступний результат / критерій приймання |
|---|---|---|---|
| **W00** | Incident Orchestrator / Research Controller | Частково реалізовано; є схеми, dispatcher і bounded dry-run. Реальний запуск не відбувся: нуль цілей і snapshots. | Запустити на дозволеному case manifest із receipts на кожен етап; помилки мають бути `partial`, `blocked`, `not_found` або `failed`, без мовчазного пропуску. [Специфікація W00](../specs/incident-orchestrator-v1.md) |
| **W01** | Ingestion, immutable archive, source coverage | Collectors і archive baseline є; ledger/bridge/contracts додані структурно. | Для одного реального джерела пройти source → отримані bytes → hash → passage/media locator → receipt та відтворити його без overwrite. [Ledger/CLI](../specs/evidence-ledger-cli-v1.md), [run contract](../specs/run-contract-v1.md) |
| **W02** | Normalization, relevance, sampling audit | Нормалізація й audit tooling частково присутні; false-negative audit поки визначає sample, а не виміряний recall. | Провести й опублікувати незалежно ад'юдикований audit включених і відхилених матеріалів; зафіксувати coverage та reason codes. [W02](../specs/relevance-sampling-audit-v1.md) |
| **W03** | Atomic claims, stance, narrative v3 | Versioned code/contracts і candidate extraction є; незалежний semantic gold/per-class accuracy відсутні. | Перевірити target/commitment/stance labels на leakage-free UA/RU/mixed holdout; зберігати `unclear` та не змішувати stance із verification. [Codebook](../specs/narrative-v3-codebook.md), [verification contract](../specs/claim-verification-v1.md) |
| **W04** | Channel evidence and attribution | Є окремі evidence dimensions і candidate exporter. Наявні профілі лишають ключові осі `unknown`; атрибуція `unverified`. | Встановити кожне твердження про origin/operator/orientation окремими dated evidence records із contrary evidence; автоматичні маркери лишити кандидатами. [W04](../specs/channel-evidence-v2.md) |
| **W05** | Source lineage / independent evidence roots | Є explicit forward edges і similarity candidates; незалежні корені для кейсових claims не встановлені. | Підтвердити/відхилити напрямок і залежність на рівні конкретного claim; дублі не мають множити підтримку. [W05](../specs/source-lineage-v1.md) |
| **W06** | Evidence retrieval and claim verification | Є локальний BM25 та типізовані правила; у кейсовому source-linked run accepted assessments — 0. | Для frozen claims виконати двобічний пошук, зберегти точні passage locators, альтернативи й статус у scope; не приймати лише подібність тексту як доказ. [W06](../specs/claim-verification-v1.md) |
| **W07** | Entity, event, temporal reconstruction | Є модулі й контракти; у case run 574 mentions unresolved і 0 physical-event rows. | Пройти event/entity/time fixtures і сформувати bounded physical та communication timelines із часовими інтервалами, unresolved conflicts і версійованими links. [W07](../specs/event-reconstruction-v1.md) |
| **W08** | Automated social conflict analysis | Є компонентна схема; реальні typed physical-event/position inputs для кейсу відсутні. | Зібрати episodes із перевірюваних actions, demands, roles та institutional response; information activity не змінює фізичну ескалацію. [W08](../specs/conflict-analysis-v1.md) |
| **W09** | Information dynamics, coordination, cross-platform | Є legacy signals, permutation models і DR2 audit/reporting recommendations. | Зафіксувати scope, denominator, null assumptions, test family, corrections і controls у кожному релізі; matched organic controls і sampling audits закрити окремо. [W09](../specs/information-dynamics-v1.md), [DR2](../research/DR2-coordination-statistics-sampling-2026-11-08.md) |
| **W10** | Multimodal evidence: video, image, audio | Існують partial fingerprinting і локальні технічні/ASR/VLM пілоти без перевіреної точності. | Довести зв'язок із clip offsets і первинним asset; окремо виміряти ASR/OCR та перевірити claim relation, recording time, location й editing continuity. [Video pipeline](social-video-evidence-pipeline-v0.1.md), [local evidence](../specs/video-local-evidence-v1.md) |
| **W11** | Measurement uncertainty and robustness | Є scenario outputs; частина меж широка, а semantic error distributions не відкалібровані. | Показувати знаменник, sampling frame, label/lineage uncertainty і sensitivity; не називати сценарні межі довірчими інтервалами без обґрунтованого дизайну. [W11](../specs/measurement-uncertainty-v1.md), [DR2](../research/DR2-coordination-statistics-sampling-2026-11-08.md) |
| **W12** | Constrained analytical report generator | Є renderer/validator і structural gates; фактичні accepted verification findings не надані. | Блокувати твердження без evidence locator, scope, denominator і uncertainty; представити unresolved, conflicting та coverage gaps. [W12](../specs/constrained-analytical-report-v1.md) |
| **W13** | Evaluation harness and release gates | Є компонентні тести й 6/6 структурних frozen controls; повного semantic case benchmark немає. | Додати held-out incident-level benchmark, semantic scorecards, F16 prompt-injection control і release receipts; структурний pass не замінює оцінки висновків. [W13](../specs/evaluation-harness-v1.md) |
| **W14** | Audience response: topics, targets, stance, emotion, reactions, engagement | Reaction capture, contracts, target/abstention plumbing, frame aggregation і compact per-platform descriptive views пройшли структурну перевірку та незалежний scoped review. Семантична класифікація не реалізована й не оцінена. | Створити незалежний локальний gold set і виміряти target-aware classifiers; exact saved-row/live parity та повторні snapshots залишаються окремими відкритими перевірками. [W14 spec](../specs/audience-response-v1.md), [W14 implementation plan](../superpowers/plans/2026-11-08-audience-response-intelligence.md), [DR4](../research/DR4-audience-response-2026-11-08.md) |

---

## 6. W14 — Audience Response: межа реалізації та наступний цикл

DR4 прийнято як методологічну основу W14. Наявність DR4 не означає, що запропоновані ним моделі вже запущені. Реалізований стан звірено з [W14 component specification](../specs/audience-response-v1.md), [W14 implementation plan](../superpowers/plans/2026-11-08-audience-response-intelligence.md), [reaction pilot receipt](../../reports/audience-response/telegram-reaction-pilot-2026-11-08.md) і робочими контрактами/модулями. Task 8 закрито після виправлень і незалежного повторного review; compact per-platform views є структурно перевіреними, але не валідують семантичні класифікатори.

### Реалізовано

- Типізоване збереження агрегованих MTProto reaction counts для нових Telegram-коментарів.
- Обмежений MTProto refresh adapter із лімітом запитів і станом доступності; пілот підтвердив отримання типізованого агрегату лише для одного comment message.
- Версійовані contracts/snapshot record shape для `reaction_type`, `count`, `observed_at` і станів відсутності/доступу.
- Target-linked record shape для topic/claim/stance/sentiment/emotion/hostility labels, deterministic validation та явного `abstention`/`unclear` стану. Target IDs перевіряються відносно переданих Social targets; це не створює і не підтверджує сам target.
- Frame-conditional aggregation із заданим unit/denominator і окремими sensitivity-виключеннями.
- Structured report validation/rendering задає frame і provenance, блокує відомі лексичні форми популяційних формулювань і створює stance, topic/emotion та reaction-count views на платформу. Незалежний scoped review пройшов після виправлень. Фільтр популяційної лексики не є семантично повним.
- Emoji-only коментарі утримуються від sentiment/emotion навіть коли передано контекст чужого тексту; контекстні topic/claim/stance/hostility потребують звіреного текстового фрагмента й лишаються кандидатними мітками.

Це plumbing, який дозволяє надалі приймати й безпечно агрегувати candidate labels. Воно саме не класифікує тексти.

### Не реалізовано або не оцінено

- Topic discovery та semantic classifiers для topic, claim, stance, sentiment, emotion чи hostility.
- Незалежний frozen UA/RU/mixed gold set, міжанотаторська перевірка або per-class metrics.
- Локальний benchmark моделей, calibrated risk–coverage, а також помилки на сарказмі, коротких відповідях і multilingual slices.
- Валідований topic/emotion dashboard або case report із семантичними висновками. Compact per-platform views для stance, topic/emotion co-occurrence та reaction counts існують, але залишаються описовими й frame-conditional; точність їхніх semantic labels не оцінена.
- Повторний production-run реакцій із часовою історією; adapter дає обмежений snapshot-запит і самостійно не опитує платформу.
- Узагальнення reaction semantics між платформами або причинний аналіз engagement.

### Історичний корпус і правила звітування

Старий корпус 6 листопада містить 39 598 коментарів у 533 цільових гілках і лише сумарний scalar reaction count на comment. За цією сумою неможливо ретроактивно відновити тип emoji, окремі reaction counts чи історію snapshots. Нові типізовані дані застосовуються до нових зборів і явно позначених майбутніх snapshot refreshes; старі записи лишаються у своїй фактичній схемі.

Reaction counts, reply counts і sentiment не є взаємозамінними. Жоден із них сам собою не доводить підтримку claim, емоцію автора, кількість унікальних людей чи частку населення. Кожен W14 output має називати frame, unit, numerator, denominator, час спостереження, missingness і model/evaluation status.

---

## 7. Інтегрований roadmap за пріоритетами

Порядок прив'язаний до залежностей: evidence contracts і контроль coverage передують семантичним висновкам; case-level доказовий trace передує масштабуванню. Кожен етап завершується збереженим artifact/receipt і явним acceptance status.

### P0 — Коректність першого обмеженого кейсу

| Робота | Стан | Definition of done |
|---|---|---|
| **P0.1 Baseline і replay** | Частково закрито: відтворені лише перелічені legacy outputs, різниці tie order/PNG bytes описані. | Зберегти baseline hashes і відтворити всі outputs, заявлені у конкретному release; явно перелічити недоступні inputs і виключення. |
| **P0.2 Source-to-finding trace** | **OPEN:** є архів/ledger contracts, але source-linked run має 0 accepted assessments і 0 VerificationResults. | Один frozen subset реальних claims має повні source receipts, exact locators, supporting/contradicting evidence, bounded status та посилання зі звіту. Допустимий статус claim — unresolved; недопустимий — прихована прогалина. |
| **P0.3 Sampling/relevance** | **OPEN:** audit frame визначений, sample n=378 не ад'юдикований; false-negative rate невідомий. | Закодувати включені/відхилені страти за зафіксованим протоколом; оприлюднити precision/recall або обмеження, із sampling weights лише коли дизайн їх підтримує. |
| **P0.4 Narrative/claim acceptance** | **OPEN:** W03/W06 код існує, але локальні semantic metrics і independent gold відсутні. | Зафіксувати codebook і holdout без leakage; звітувати помилки окремо по label/language, unknown/abstention, а не лише загальний accuracy. |
| **P0.5 W09 statistical reporting** | DR2 прийнято; частина exact/null-model audit виконана. | Для кожного coordination результату зберігати graph/sampling scope, denominator, null assumptions, resolution, correction family, controls і твердження про те, чого сигнал не доводить. |
| **P0.6 Case reconstruction** | **OPEN:** 574 event mentions unresolved, physical timeline rows — 0; первинні подієві records не покривають критерій. | Для frozen case subset зберегти physical та communication events окремо, із source-backed interval, contradictions і невідомими. Не робити causal або actor merge без окремих підстав. |
| **P0.7 Report/release integrity** | Структурні gates працюють; фактичний case release не має достатнього verification evidence. | Усі empirical assertions traceable; 0 dangling IDs/невиправданих merge/time cycles/silent failed collectors; кожен numeric finding має знаменник; open gaps видимі у звіті. |
| **P0.8 W14 capture/report plumbing** | Typed capture, bounded adapter, contracts, target/abstention shape, frame aggregation і compact per-platform descriptive views пройшли focused і незалежну структурну перевірку; один-comment MTProto pilot підтверджує лише доступність на цьому зразку. | Перевірити exact saved-row/live parity та набрати повторні snapshots без reactor identities; забезпечити тип/count/time/state для нових записів. Legacy scalar записи не доповнюються вигаданими типами. |

### P1 — Семантична, подієва й медійна оцінка

1. Зібрати незалежний frozen benchmark для narrative/claim extraction, source assessment, event/time resolution і W14 labels.
2. Виміряти W14 target-aware topic/stance/sentiment/emotion/hostility classifiers на українській, російській і mixed мові; зафіксувати модель, версію, frame, контекст, abstention і per-class precision/recall/F1.
3. Закрити end-to-end evaluation на одному case snapshot із джерелами, первинними passages, доказовими assessments, report renderer і semantic review. Structural test pass є окремим рядком результату.
4. Для W10 перевірити транскрипти на reference sample, прив'язку PTS/clip offsets, editing/near-copy, час/місце та зв'язок із конкретним claim.
5. Виконати DR2 matched organic-event controls, sensitivity до часових меж і ад'юдикований relevance audit; thresholds фіксувати до перегляду outcome.
6. Перевірити correction/retraction і as-of replay на case-backed доказах, а не лише synthetic fixture.
7. Додавати topic/emotion dashboard лише після появи benchmarked model output і frame/coverage тексту в кожній візуалізації.

### P2 — Переносність і масштабування

- Кілька різнорідних кейсів і platform-specific calibration; cross-platform зіставлення лише після визначення семантики та coverage кожної платформи.
- Історичні reaction snapshots, conversation graph, opinion diversity та polarization за наявності належних даних і обмежень.
- Analyst UI, graph database, incremental re-computation і звіти-різниці після вимірювання потреби та вартості.
- Складні learned retrieval, геолокація, автоматичний VLM та інші моделі тільки з окремим benchmark і failure analysis.

---

## 8. Відкриті completion gates

Усі позиції нижче залишають closeout у стані **NOT COMPLETE**:

| Gate | Стан на 08.11.2026 | Потрібний доказ |
|---|---|---|
| Реальна end-to-end перевірка claim | **OPEN** — 0 accepted assessments / VerificationResults у source-linked run. | Повний source → passage → claim → assessment → finding → report trace із receipt. |
| Фізична хронологія | **OPEN** — 574 mentions unresolved, 0 physical-event rows. | Незалежні dated evidence, interval constraints, event decisions і unresolved alternatives. |
| Незалежні джерельні roots | **OPEN** — lineage має candidate edges; кейсові roots не встановлені. | Claim-level dependency adjudication і нижня межа roots із невідомими явно показаними. |
| Relevance/coverage recall | **OPEN** — audit design є, adjudication та оцінка false negatives відсутні. | Результати за inclusion strata й відхиленими записами, з design-aware невизначеністю. |
| Channel attribution | **OPEN** — автоматичні групи та інфраструктурні markers лишаються candidate signals. | Dated evidence на origin, operator, orientation та operation; contrary evidence і scope. |
| Семантична якість W03/W14 | **OPEN / NOT EVALUATED** — незалежного local gold set немає. | Frozen split, class/language/context metrics, abstention та out-of-domain limits. |
| Медіа-якість | **OPEN / NOT EVALUATED** — технічні декоди й candidate ASR/VLM не засвідчують зміст, час або місце. | Reference transcripts, точковий огляд clip, media provenance та окремі claim/time/location assessments. |
| Coordination transfer | **OPEN** — DR2 дає controls і sampling requirements; cross-case validity не доведена. | Matched organic controls, sensitivity до блоків/меж і негативні control diagnostics. |
| Звітний release | **OPEN** — structural controls пройшли, semantic case benchmark не повний; F16 відсутній. | Frozen end-to-end semantic suite, report audit, no hidden failures, complete run manifest. |
| W14 compact views / audience dashboard | **STRUCTURAL SLICE CLOSED; SEMANTIC ANALYTICS OPEN** — compact per-platform stance, topic/emotion co-occurrence and reaction-count views passed independent scoped review. Semantic outputs remain not evaluated. | Independent local gold set, classifier evaluation and documented denominators/frame for semantic findings; broader dashboard remains a separate deliverable. |

### Умова закриття master plan

**NOT COMPLETE** знімається лише після проходження P0 gates за перевірюваними case receipts, окремого статусу кожного P1 gate і переліку невирішених меж. Завершений bounded case може містити unresolved findings, якщо збір/coverage задокументовані й жоден висновок не виходить за свої докази. Це не дозволяє оголосити реалізованими неоцінені класифікатори, джерельну незалежність або відсутні події.

---

## 9. Мінімальна форма звіту для аналітика

1. **Scope і coverage:** джерела, відбір, часовий cutoff, доступність, невдалі операції.
2. **Короткий підсумок:** окремо підтверджене в межах scope, атрибутоване, конфліктне й невідоме.
3. **Physical timeline:** лише дії з подієвими evidence refs; інтервали й альтернативи.
4. **Communication timeline:** публікації/заяви/виправлення, не підмінює physical events.
5. **Claim matrix:** claim, мовець, scope, evidence roots, протиріччя, статус, as_of.
6. **Information dynamics:** чисельники, знаменники, snapshot time, sampling frame, null model і sensitivity.
7. **Media dossier:** asset/clip IDs, точні offsets, технічні та семантичні стани.
8. **Audience response, якщо доступна:** target, label/model/evaluation state, unit, denominator, reactions snapshot та обмеження.
9. **Measurement uncertainty:** selection, missingness, disagreement, lineage, модельні межі.
10. **Open questions:** що саме треба перевірити далі й чому звіт не встановлює ширший висновок.

---

## 10. Правила для наступних implementation tasks

Кожен наступний task має назвати один W-workstream, конкретні модулі/контракти, inputs/outputs, acceptance criteria й потрібний receipt. Перед зміною перевіряють актуальний worktree, а не покладаються на baseline чи старий DR snapshot. Нові стани мають бути версійовані; legacy data не переписуються заднім числом.

Для кожного релізного результату документувати:

- змінені файли та data snapshot hashes;
- виконані структурні й semantic перевірки окремо;
- чисельник, знаменник, coverage й out-of-scope стани;
- відкриті критерії та failed/blocked/not-found collector receipts;
- модель, prompt, provider, параметри й cost, якщо вони використовувалися;
- відхилення від очікуваного результату й те, який висновок через це лишається unresolved.

---

## 11. Критерій практичної цінності Social

Social корисний, коли він повторювано збирає дозволені джерела, зберігає точне походження, не множить залежні свідчення, відокремлює публічні повідомлення від фізичних подій, показує суперечності та формує числові висновки з правильними знаменниками. Система має завершуватися звітом із доказовими межами навіть тоді, коли факт лишається невідомим.

**Поточний closeout — NOT COMPLETE.** Наступна ціль — закрити відкрите P0 evidence-to-report trace для обмеженого реального кейсу, паралельно зберігаючи всі невизначеності й межі покриття.
