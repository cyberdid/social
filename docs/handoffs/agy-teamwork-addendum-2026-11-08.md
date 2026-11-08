# Додаток до AGY Teamwork handoff — нові локальні результати

Цей addendum підготовано після основного [handoff](agy-teamwork-masterplan-handoff-2026-11-08.md). Якщо Teamwork уже отримав основний prompt, передай йому цей додаток окремо. Якщо ні — нехай прочитає цей файл разом із handoff. Новий аналіз у цьому додатку не використовує сирих текстів, приватних ID, реакторів, медіа або абсолютних локальних шляхів.

## 1. W05 / P0.2 — bounded source-lineage input audit

Прочитай:

- [`source-lineage-input-audit-2026-11-08.md`](../../reports/automated-case-run-2026-11-08/source-lineage-input-audit-2026-11-08.md)
- [`source-lineage-input-audit-2026-11-08.json`](../../reports/automated-case-run-2026-11-08/source-lineage-input-audit-2026-11-08.json)

Підсумок: у приватному source-linked наборі є 30 passage rows і 574 report-bundle evidence rows. За bounded перевіркою 30 passages мають 30 унікальних source/artifact/lineage-family значень; повторів нормалізованого точного passage text між source IDs не знайдено. Окремі 574 bundle evidence rows посилаються лише на 2 distinct source/artifact/hash значення. Ні passages, ні bundle evidence rows не містять `claim_id` або явних dependency references, тому case-level claim-scoped lineage з цих двох об'єктів запустити коректно не можна. У висновку встановлено 0 підтверджених dependency edges і 0 незалежних roots; відсутність знайдених дублікатів не означає незалежність.

Врахуй ці результати у W05 та P0.2 як перевірку недостатності входу. Не створюй `claim_id ↔ evidence_id` зв'язок із BM25 candidate match без самостійного scope/evidence обґрунтування. Не знижуй статус unknown і не називай 574 evidence records незалежними джерелами.

## 2. W14 / P0 — одиниці платних Telegram reactions

Прочитай [`telegram-reaction-units-and-privacy-2026-11-08.md`](../research/telegram-reaction-units-and-privacy-2026-11-08.md). Офіційна документація Telegram розрізняє звичайні й custom reactions та платні Star reactions; `messages.getMessagesReactions` повертає агрегатний update, а `MessageReactions` також може містити `recent_reactions` і `top_reactors`. Локальний serializer уже зберігає `paid` тип і відкидає ці поля з вихідного запису.

Конкретний code review finding: `src/analysis/audience_aggregation.py` зараз сумує всі counts у Telegram vector для `largest_available_reaction_comments`; платні Star units можуть бути додані до emoji reaction counts. Потрібен unit-aware результат: rankувати `emoji` + `custom_emoji`, показувати `paid_star_amount` окремо, не включати невідомий тип у mixed-unit ranking. Додай regression tests для одночасних emoji/custom/paid/unknown rows та онови `docs/specs/audience-response-v1.md`. Не трактуй ні реакції, ні Star amount як унікальних людей або підтримку claim.

Перевірені офіційні джерела:

- [Telegram Message reactions API](https://core.telegram.org/api/reactions)
- [Telegram `messages.getMessagesReactions`](https://core.telegram.org/method/messages.getMessagesReactions)
- [Telegram `MessageReactions` constructor](https://core.telegram.org/constructor/messageReactions)
- [Telegram `messages.getMessageReactionsList`](https://core.telegram.org/method/messages.getMessageReactionsList)

## Додаткові вимоги до фінального closeout

- Відобрази ці два findings у відповідних W05/P0.2 та W14/P0 gates і звітах, не переписуючи первинні receipts.
- Якщо виправляєш код W14, додай regression tests і запусти щонайменше цільові та повний suite. Не торкайся чужих незавершених змін і не staged/commit/push.
- Після Teamwork змін перевір внутрішні посилання, JSON receipts, `git diff --check` та актуальні release-manifest hashes. Не називай весь masterplan завершеним, якщо лишилися невиконані acceptance gates.
