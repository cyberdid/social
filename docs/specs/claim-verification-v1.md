# Пошук доказів і перевірка тверджень Social v1

## Призначення

`src/analysis/claim_verification.py` додає локальний retrieval-крок і формування обмеженого статусу твердження поверх наявного `EvidenceLedger`. Результати пошуку є лише кандидатами. Ранг BM25, кількість публікацій і згода моделей не надають доказової підтримки.

## API

- `retrieve_evidence_candidates(claim, passages, as_of_utc, top_k=20)` — локальний детермінований BM25-пошук за текстом твердження й окремий пошук фраз спростування/виправлення. Повертає точний фрагмент passage, нуль-індексні offsets у Unicode code points, directions, score та `search_receipt`.
- `create_evidence_assessment(...)` — створює оцінку passage–claim з відношенням `supports`, `contradicts`, `mentions`, `quotes`, `contextualizes`, `rebuts`, `ambiguous` або `insufficient_context`. Цитату перевірено порівнянням `passage.text[start:end]` із записаним уривком.
- `aggregate_verification(...)` — створює `VerificationResult` із `as_of`, точним scope, supporting/contradicting evidence IDs та причиною статусу.
- `append_verification_result(ledger, result, producer, run_id)` — передає результат в наявний append-only `EvidenceLedger`. Перевірки існування Claim і evidence виконуються самим ledger.

## Retrieval і часовий зріз

Кожний passage повинен містити `passage_id`, `source_id`, `captured_at_utc`, `text`; необов'язково — `artifact_id`, `artifact_start_offset`, `lineage_family_id`, `independent_root_id`. Запис, отриманий після `as_of_utc`, не потрапляє до кандидатів. Зріз включає SHA-256 канонічного маніфесту IDs, джерел, часу отримання, хешів тексту, offsets і lineage refs; receipt також містить терми запиту та параметри BM25.

Пошукові напрями `claim_terms` і `counterevidence_terms` означають спосіб пошуку, а не позицію автора. Другий напрям вимагає одночасної наявності claim-токенів і хоча б одного заданого маркера заперечення/виправлення. Це збільшує точність маршрутизації, але може пропустити інакше сформульовані спростування. Можна додати `query_variants` та налаштований список counterevidence terms.

Дедуплікація top-k відбувається лише за явно наданим `lineage_family_id`; без нього candidate лишається окремим із `lineage_status=unknown`. Ця дедуплікація не підтверджує незалежність джерел.

## Оцінка evidence та статус

`decision=candidate` є типовим. `decision=accepted` вимагає `acceptance_basis=human_adjudication` або `validated_rule` із `validated_rule_id`; моделі без окремої валідованої процедури не можуть самостійно прийняти оцінку. Заявлені `asserted_values` перевіряються проти `claim.key_values`: різне точне значення не може пройти як `supports`, воно стає `ambiguous/candidate`.

Підсумок використовує лише accepted assessment з тим самим claim ID і точно таким самим JSON scope. `supported_within_scope` або `refuted_within_scope` вимагає заданої кількості `independent_root_id` з `independence_status=confirmed_independent`. Цей модуль не встановлює незалежність: такі ID мають бути верифіковані upstream. Одна сім'я, що одночасно підтримує та заперечує, не рахується як два незалежні корені.

- `unverified`: пошук не завершено.
- `insufficient_evidence`: завершений пошук не дав достатньої прийнятої evidence.
- `not_verifiable`: інцидентний контракт прямо позначив claim як поза спостережуваною сферою.
- `supported_within_scope`, `refuted_within_scope`, `conflicting_evidence`: застосовуються лише до вузького scope за наведеними правилами.
- `superseded`: модуль не присвоює автоматично; історія зберігається через новий результат із `supersedes`.

Відсутність знайденого доказу не є спростуванням. Один офіційний допис може підтвердити факт публікації, але не автоматично його реальний зміст. Кількісні поля потрібно розділяти у claim: наприклад, `count=40, operator=eq` не тотожне `count=40, operator=lte`.

## Відтворення

```bash
PYTHONPATH=. pytest -q tests/test_claim_verification.py
python -m py_compile src/analysis/claim_verification.py
```

## Межі v1

- Немає web/API-збирача, multilingual dense retrieval, reranker або NLI/LLM passage classifier.
- Власний BM25 — легкий базовий ретривер; він не моделює семантичні перефразування й має бути оцінений на case-specific retrieval benchmark.
- Relation annotations і підтверджені незалежні корені поки надходять ззовні; runtime кожної нової справи не вимагає ручного перегляду, але автоматична класифікація evidence ще не інтегрована.
- У відкритому корпусі неможливо зробити висновок про відсутність події лише з відсутності документів.
