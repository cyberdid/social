# Звіт реалізації Phase 4 / W06 — Retrieval і claim verification

## Статус

Реалізовано локальний перший рівень W06 окремим модулем. Legacy collectors і `EvidenceLedger` не змінювалися. Модуль автономно ранжує надані passages, відсікає матеріали після `as_of`, перевіряє точні citation spans і може обчислити обмежений open-world статус з уже прийнятих passage assessments.

## Зміни

- `src/analysis/claim_verification.py`: детермінований multilingual lexical BM25, два маршрути пошуку (`claim_terms`, `counterevidence_terms`), exact offsets, hash/queries/parameters у search receipt, дедуплікація кандидатів тільки за явним lineage family, typed passage relations, scope/value checks, status aggregation, append-only `EvidenceLedger` adapter й package exports.
- `tests/test_claim_verification.py`: перевірки двох напрямів пошуку та claim-token overlap, `as_of`, цитатних offsets, duplicate roots, numeric omissions/mismatch, exact scope, correction history, missingness, provenance, ledger append idempotence, package exports і unresolved queue.
- `docs/specs/claim-verification-v1.md`: український контракт і межі застосування.

## Захисні правила

1. Ретривер ніколи сам не встановлює stance або truth.
2. Passage relation може бути лише кандидатом; прийняття вимагає `human_adjudication` або `validated_rule` із provenance.
3. У статуси входять тільки assessments того самого claim і точного scope, записані станом на `as_of`.
4. Для `supported_within_scope` / `refuted_within_scope` рахуються лише явно задані, upstream підтверджені independent roots; копії одного root лічаться один раз.
5. Якщо фактів немає, статус буде `unverified` або `insufficient_evidence`, не `refuted`.
6. Кожне `claim.key_values` має бути присутнє у accepted `supports`; serialized assessment проходить повторну перевірку.
7. Одна коренева сім'я на обох сторонах лишається conflict; перетин і per-side counts явно записані.
8. Assessment ID враховує весь запис і змінюється при зміні його provenance.
9. Correction/retraction не видаляє попередній результат; новий as-of projection посилається через `supersedes`.
10. Ledger rationale зберігає assessments, citations, assessor/rule/time/root provenance та exclusions.

## Перевірки

```text
PYTHONPATH=. pytest -q tests/test_claim_verification.py
29 passed

PYTHONPATH=. pytest -q tests/test_claim_verification.py tests/test_evidence_ledger.py
45 passed

python -m py_compile src/analysis/claim_verification.py
exit 0

git diff --check
exit 0
```

## Review follow-up

Закрито п'ять re-review findings: support більше не обходить numeric `key_values`; counter-search вимагає і claim-token, і correction-cue overlap; shared support/contradiction roots дають `conflicting_evidence` та збережені per-side counts; result ID включає scope, decision parameters і навіть виключені assessment provenance; EvidenceLedger rationale зберігає повний assessment provenance. Додано експорти assessment/result/search receipt, claim matrix і unresolved retrieval queue, із тестом, що assessment поза `as_of` лишає retrieval відкритим. Повний assessment payload тепер впливає на `assessment_id`, а незадокументовані чи дубльовані assessment IDs блокуються.

Другий re-review закрив дві додаткові прогалини. Тепер `supports` fail-closed перевіряє числа й базові українські/російські/англійські числівники у формулюванні claim: кількість людей без `key_values.count` не приймається; несемантичний `year=40` не задовольняє count assertion. Агрегатор повторює цю перевірку для serialized assessments. Експорт `evidence_assessments.jsonl` додає для кожного рядка явну `as_of_projection` із cutoff, result ID, прапорцем включення та кодом виключення, зберігаючи assessment payload для аудиту.

Перевірки другого re-review:

```text
PYTHONPATH=. pytest -q tests/test_claim_verification.py
35 passed

PYTHONPATH=. pytest -q tests/test_claim_verification.py tests/test_evidence_ledger.py
51 passed

python -m py_compile src/analysis/claim_verification.py
exit 0

git diff --check
exit 0
```

## Що не доведено / подальша межа

BM25 — retrieval baseline, а не семантичний claim verifier; його recall/precision не вимірювалися на незалежному retrieval gold set. Двомовні cue-слова можуть пропускати інші форми спростування. Жодного LLM/API виклику або мережевого збору не було. Автоматичний NLI/LLM relation classifier, dense retrieval, correction lineage extraction і end-to-end integration з case reports лишаються окремою роботою. Цей модуль не доводить upstream незалежність коренів; він лише не дозволяє вважати невідомі зв'язки незалежними.
