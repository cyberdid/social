# Звіт реалізації Phase 4 / W06 — Retrieval і claim verification

## Статус

Реалізовано локальний перший рівень W06 окремим модулем. Legacy collectors і `EvidenceLedger` не змінювалися. Модуль автономно ранжує надані passages, відсікає матеріали після `as_of`, перевіряє точні citation spans і може обчислити обмежений open-world статус з уже прийнятих passage assessments.

## Зміни

- `src/analysis/claim_verification.py`: детермінований multilingual lexical BM25, два маршрути пошуку (`claim_terms`, `counterevidence_terms`), exact offsets, hash/queries/parameters у search receipt, дедуплікація кандидатів тільки за явним lineage family, typed passage relations, scope/value checks, status aggregation та adapter до append-only `EvidenceLedger`.
- `tests/test_claim_verification.py`: перевірки двох напрямів пошуку, `as_of`, цитатних offsets, duplicate roots, numeric mismatch, exact scope, correction history, missingness, citations, provenance й ledger append idempotence.
- `docs/specs/claim-verification-v1.md`: український контракт і межі застосування.

## Захисні правила

1. Ретривер ніколи сам не встановлює stance або truth.
2. Passage relation може бути лише кандидатом; прийняття вимагає `human_adjudication` або `validated_rule` із provenance.
3. У статуси входять тільки assessments того самого claim і точного scope, записані станом на `as_of`.
4. Для `supported_within_scope` / `refuted_within_scope` рахуються лише явно задані, upstream підтверджені independent roots; копії одного root лічаться один раз.
5. Якщо фактів немає, статус буде `unverified` або `insufficient_evidence`, не `refuted`.
6. Числова невідповідність не може автоматично лишитися `supports`.
7. Correction/retraction не видаляє попередній результат; новий as-of projection посилається через `supersedes`.

## Перевірки

```text
PYTHONPATH=. pytest -q tests/test_claim_verification.py
14 passed

PYTHONPATH=. pytest -q tests/test_claim_verification.py tests/test_evidence_ledger.py
30 passed

python -m py_compile src/analysis/claim_verification.py
exit 0

git diff --check
exit 0
```

## Що не доведено / подальша межа

BM25 — retrieval baseline, а не семантичний claim verifier; його recall/precision не вимірювалися на незалежному retrieval gold set. Двомовні cue-слова можуть пропускати інші форми спростування. Жодного LLM/API виклику або мережевого збору не було. Автоматичний NLI/LLM relation classifier, dense retrieval, correction lineage extraction і end-to-end integration з case reports лишаються окремою роботою. Цей модуль не доводить upstream незалежність коренів; він лише не дозволяє вважати невідомі зв'язки незалежними.
