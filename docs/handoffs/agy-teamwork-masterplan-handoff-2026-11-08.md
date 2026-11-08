# AGY Gemini Teamwork handoff — Social Master Plan

**Для:** власника проєкту, який сам запускає AGY Teamwork з Gemini 3.8 Flash.  
**Підготовлено:** 8 листопада 2026 року.  
**Локальна гілка:** `codex/social-master-plan`; робоче дерево вже містить численні незакомічені зміни.  
**Статус:** готовий prompt і snapshot стану; AGY/Gemini тут не запускали.

## Як використати

Запусти AGY Teamwork у відкритому проєкті Social та передай йому блок **«Завдання для Teamwork»** нижче. Попроси команду почати з цього handoff і чинного Master Plan v1.1. Усі deliverables мають бути створені або оновлені файлами в цій робочій копії. Наприкінці попроси зберегти командні звіти, інтегрований план, перевірки та список невиконаних gates у репозиторії.

## Стан на момент передачі

- Чинний інтегрований план: [`docs/plans/social-master-plan-v1.1.md`](../plans/social-master-plan-v1.1.md). Він прямо позначений **NOT COMPLETE**.
- Актуальний closeout і P0/P1 gates: [`reports/orchestrator/masterplan-closeout-2026-11-08.md`](../../reports/orchestrator/masterplan-closeout-2026-11-08.md).
- Аудит приватного historical case-run та повторного bounded run: [`replay-audit-2026-11-08.md`](../../reports/automated-case-run-2026-11-08/replay-audit-2026-11-08.md) і повний content-free hash receipt [`replay-audit-2026-11-08.json`](../../reports/automated-case-run-2026-11-08/replay-audit-2026-11-08.json). 8/8 входів та 16/16 виходів кожного запуску збігаються з відповідними маніфестами; між двома запусками 5/16 виходів ідентичні побайтно. Це не семантична перевірка. Дерево було dirty; execution-time diff і lockfile не зафіксовані.
- Reader-facing case inventory: [`reports/case-release-manifest-2026-11-08.json`](../../reports/case-release-manifest-2026-11-08.json). Він потребує синхронізації з новим replay receipt та уточнення формулювань приватності.
- Координація: exact Jaccard/LSH audit і replay мають receipts у `reports/coordination-null-models-2026-11-08-lsh-audit/`; statistical anomaly не доводить кампанію/оператора; matched organic controls відсутні.
- Вибірка релевантності: [`reports/relevance-audit/design-2026-11-08.md`](../../reports/relevance-audit/design-2026-11-08.md) і replay receipt. Sample membership повторюється, але frame digest відрізняється через незаписану первинну трансформацію; немає незалежної розмітки rejected sample, тож recall невідомий.
- Відео: [`docs/plans/social-video-evidence-pipeline-v0.1.md`](../plans/social-video-evidence-pipeline-v0.1.md), `reports/video-pipeline/`. 607/607 локальних Telegram assets пройшли технічний full decode; це не підтверджує семантику відео, час/місце чи точність ASR/OCR. Немає незалежного transcript gold/WER/CER.
- Транскрипт: [`docs/specs/transcript-correction-v1.md`](../specs/transcript-correction-v1.md), [`reports/video-pipeline/asr-correction-review-2026-11-08.md`](../../reports/video-pipeline/asr-correction-review-2026-11-08.md). Raw ASR не переписувати. Логічно виправлений текст припустимий лише як окремий похідний кандидат із посиланням на audio segment; без прослуховування не ставити його як verbatim/quote-safe.
- DR4: методологічно прийнятий користувачем наданою рецензією 89/100; саму рецензію збережено у [`docs/research/DR4-review-received-2026-11-08.md`](../research/DR4-review-received-2026-11-08.md). W14 має live MTProto parity 10/10 на доступному стані, але не має повторних snapshots, локального semantic gold чи повної cross-platform гармонізації.
- Попередній повний Python suite: **671 passed, 16 subtests passed** після попередніх змін. Запусти відповідні перевірки лише після ознайомлення зі змінами, а повний suite — якщо команда торкається коду.
- Публічні звіти не повинні містити приватних корпусів, авторських/реакторських ID, токенів, сесій, псевдонімізаційних salt, особистих Telegram/Google credentials або локальних абсолютних шляхів.

## Відкриті gates за пріоритетом

1. **P0.1 release/replay:** нині є точний content-free crosswalk виходів, але не зафіксовано точний dirty code diff саме під час запуску та dependency lock. Узгодити reader artifact inventory, receipts і межі відтворюваності; не оголошувати gate закритим без усіх критеріїв.
2. **P0.2 source-to-finding:** candidate retrieval не дорівнює verification; потрібні source roots, passages/locators, незалежність і точний ланцюг від джерела до кожного звітного речення.
3. **P0.3 relevance:** відтворити sampler трансформацію, перевірити frame digest, підготувати чесний single-coder screening rejected sample та явно не називати його незалежним gold/recall.
4. **P0.4 narrative/claim:** немає незалежного UA/RU/mixed gold set та локальних per-class metrics. Зробити максимум без зовнішнього експерта й позначити, що саме потребує незалежної експертної оцінки.
5. **P0.5 coordination:** exact graph і нульова модель перевірені, але потрібні органічні контрольні хвилі; жоден результат не має автоматично доводити CIB, державне керування чи замовника.
6. **P0.6 physical event:** є багато повідомлень і publication chronology, але основна фізична timeline не встановлена. Збудувати only attributed reported-event timeline із competing evidence/unknowns; не перетворювати повідомлення органів або AI на факти.
7. **P0.7 report/release:** пов'язати кожне case finding з доказом, scope і часовим зрізом; виконати citation, denominator і contradiction audit.
8. **P0.8/W14:** далі перевірити MTProto reaction states і coverage в межах безпечного малого запиту; зберігати лише агрегати, не реакторів; правильно називати estimands.
9. **W10/video:** обмежено довести ASR/transcript і clip-to-claim validation. Не змінювати raw; кожну мовну правку вести окремо та лише якщо її підтверджує звук.
10. **P1:** semantic classifiers, uncertainty propagation, autonomous end-to-end QA, source lineage, cross-platform transfer. Синтетичний/структурний pass не замінює case-level benchmark.

## Збережені попередні результати

- DR1/DR3 PDFs, DR2 coordination/statistics review та DR4 audience review зведені в `docs/research/` і зареєстровані у Master Plan v1.1.
- Виправлено спосіб читання native `links` у relevance sampler; replay utility та regression tests додані.
- Exact coordination null replay побайтно збігся у 6/6 outputs.
- MTProto aggregate reaction representation, no-update/wrong-peer handling та legacy schema compatibility реалізовані з tests.
- Technical Telegram media decoding: 607/607; семантична перевірка ще не виконана.
- Transcript correction contract розрізняє raw transcript, correction candidates і quote-safe transcript.
- PDF artifacts побудовані; будь-яку повторну генерацію слід звірити з Markdown і manifest, перш ніж замінювати їх.

---

## Завдання для Teamwork

> Ти працюєш у локальному репозиторії `cyberdid/social`, у вже активній робочій копії та гілці `codex/social-master-plan`. Власник проєкту сам запустив AGY Teamwork і доручає команді автономно продовжити чинний Master Plan до максимально можливого завершення без сторонніх експертів. У цій задачі не проси власника вручну виконувати рутинні дії. Не заявляй, що masterplan завершено, поки acceptance gates справді не пройдені. Не підмінюй відсутні докази впевненим текстом.
>
> **Почни з інвентаризації:** прочитай цей файл, `docs/plans/social-master-plan-v1.1.md`, `reports/orchestrator/masterplan-closeout-2026-11-08.md`, новий replay audit/report, усі DR1–DR4 звіти, відео/transcript специфікації й відповідні receipts. Перевір `git status` і збережи наявні зміни. Нічого не reset/revert, не checkout чужих версій, не force push і не створюй/публікуй GitHub repository. Ключі, cookies, приватні сирі корпуси, псевдонімізаційні salts, user/reactor IDs та медіа не копіювати в Git і не додавати до cloud prompt.
>
> **Використай Teamwork для незалежних робіт із фіксованим ownership.** Якщо доступні менше виконавців — об'єднай послідовно, не створюй конкуренцію за одні файли:
>
> 1. **Replay/release auditor:** власник лише `reports/case-release-manifest-2026-11-08.json` та нових `reports/orchestrator/release-audit-*.md/json`. Синхронізуй артефакт inventory, розміри/хеші, вихідний crosswalk, mutable/frozen sources і privacy wording із `reports/automated-case-run-2026-11-08/replay-audit-2026-11-08.json`. Перевір кожен шлях/хеш; не вигадуй run-time dirty diff або dependency lock. Дай точний залишковий P0.1 status.
>
> 2. **Evidence/claims/lineage reviewer:** read-only аудит `P0.2`, `P0.3`, `P0.6`; результат у новий `reports/orchestrator/teamwork-evidence-lineage-2026-11-08.md`. Можна будувати лише перевірювані source-attributed relations/event reports і виправляти code-backed дефекти із тестами у чітко визначених файлах. Розрізняй claim про те, що джерело повідомило, і фізичний факт. Перевір 30 passage bundle, exact source locators, lineage roots, пропущені relevance frame елементи й rejected sample. Якщо ground truth/документів немає — зафіксуй `unknown`, не домислюй.
>
> 3. **Video/transcript engineer:** власник `src/analysis/video_*`, transcript correction module/spec/test files та окремого `reports/orchestrator/teamwork-video-2026-11-08.md`. Розбери ASR candidate queue, додай/виправляй лише такі транскриптні похідні записи, для яких відтворювано відомий audio segment і реальне слухове/модельне підтвердження доступне; raw ASR ніколи не змінюй. «Логічне виправлення» — окремий correction hypothesis із diff, evidence locator, confidence/calibration status і `quote_safe=false`, доки фраза не підтверджена аудіо. Не позначай модельну здогадку як дослівну цитату. Якщо локального аудіо/зразка не вистачає, заверши технічне доопрацювання й сформуй точну чергу невизначеностей.
>
> 4. **Audience/W14 analyst:** власник лише W14 модуля/spec/tests і нового `reports/orchestrator/teamwork-audience-2026-11-08.md`. Перевір live-safe MTProto aggregate states, reaction breakdown, repeat-snapshot feasibility, denominators, target linking до claims/entities/events і сценарії впливу гіперактивних/координованих коментаторів. Не збирай reactor identities; не називай reactions підтримкою без контекстної перевірки; не узагальнюй на населення. Урахуй окремо рецензію в `docs/research/DR4-review-received-2026-11-08.md`.
>
> 5. **Independent red-team reviewer:** read-only, власник лише `reports/orchestrator/teamwork-red-team-2026-11-08.md`. Перевір твердження в receipts, відтворюваність хешів, evidence/claim boundaries, статистичні знаменники, exposure bias, transcript quote-safety, security/privacy, inconsistent numbers and stale statuses. Не редагуй спільні файли; поверни findings із severity і конкретними evidence paths.
>
> **Інтегратор/головний агент** — єдиний власник `docs/plans/social-master-plan-v1.2.md`, `reports/orchestrator/masterplan-closeout-2026-11-08-final.md` та запису в `log.md`. Дочекайся звітів інших власників, виріши їхні суперечності з receipts, і тільки тоді онови masterplan. Збережи DR1–DR4 оцінки, статути P0/P1/P2, evidence gates, блокери і точні файли/команди. Не стирай історію v1.1.
>
> **Виконання:** закрий усі локально перевірювані кроки, що не потребують зовнішньої людини чи нових авторизованих доступів. Реалізацію роби лише коли є чітка специфікація і regression test; додавай тести до змін, запускай спершу targeted, а після code changes — повний suite. Використовуй локальні архіви та дозволені публічні джерела; не порушуй платформні ліміти й не масово автоматизуй login-gated scraping. Не витрачай токени на повторне формулювання планів без нових даних/коду/перевірки.
>
> **Після роботи обов'язково збережи у файлах:** (a) звіт кожного workstream; (b) `social-master-plan-v1.2.md`; (c) фінальний closeout із таблицею кожного gate `closed/partial/open`, доказом і залишковим blocker; (d) оновлений artifact/release manifest; (e) зміни в `log.md`; (f) targeted/full test receipts та hash/replay receipts без сирих приватних даних. Зроби `git diff --check`, перевір усі внутрішні посилання, хеші й застарілі статуси. Не commit/push: нехай власник перегляне конкретний, збережений результат. У фіналі дай короткий changelog, точні шляхи до файлів, виконані перевірки, актуальний відсоток/оцінку залишкового часу з поясненням і чесний статус Master Plan. Якщо blocker реально потребує незалежного експерта, вкажи вузьке питання й чому локальні цифрові докази його не вирішують; не став увесь інший прогрес на паузу.

## Очікувані вихідні файли від Teamwork

- `reports/orchestrator/teamwork-evidence-lineage-2026-11-08.md`
- `reports/orchestrator/teamwork-video-2026-11-08.md`
- `reports/orchestrator/teamwork-audience-2026-11-08.md`
- `reports/orchestrator/teamwork-red-team-2026-11-08.md`
- `reports/orchestrator/release-audit-2026-11-08.md` і супровідний JSON receipt
- `docs/plans/social-master-plan-v1.2.md`
- `reports/orchestrator/masterplan-closeout-2026-11-08-final.md`
- оновлений `log.md` і, якщо треба, reader release manifest

Фінальний артефакт має бути придатний для локальної перевірки в цьому worktree. Чатова відповідь без збережених файлів не вважається завершенням handoff.
