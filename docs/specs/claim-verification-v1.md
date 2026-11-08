# Пошук доказів і перевірка тверджень Social v1

## Призначення

`src/analysis/claim_verification.py` додає локальний retrieval-крок і формування обмеженого статусу твердження поверх наявного `EvidenceLedger`. Результати пошуку є лише кандидатами. Ранг BM25, кількість публікацій і згода моделей не надають доказової підтримки.

## API

- `retrieve_evidence_candidates(claim, passages, as_of_utc, top_k=20)` — локальний детермінований BM25-пошук за текстом твердження й окремий пошук фраз спростування/виправлення. Повертає точний фрагмент passage, passage-relative offsets у Unicode code points, verified artifact offset (якщо наданий), locator, directions, score та `search_receipt`.
- `create_evidence_assessment(...)` — створює оцінку passage–claim з відношенням `supports`, `contradicts`, `mentions`, `quotes`, `contextualizes`, `rebuts`, `ambiguous` або `insufficient_context`. Цитату перевірено порівнянням `passage.text[start:end]` із записаним уривком.
- `aggregate_verification(...)` — створює `VerificationResult` із `as_of`, точним scope, supporting/contradicting evidence IDs та причиною статусу.
- `append_verification_result(ledger, result, producer, run_id)` — передає результат в наявний append-only `EvidenceLedger`. Перевірки існування Claim і evidence виконуються самим ledger.
- `export_verification_package(...)` — створює JSONL кандидатів/оцінок/результатів, JSON search receipt, `claim_matrix.md` та `unresolved_retrieval_queue.jsonl`.

## Retrieval і часовий зріз

Кожний passage повинен містити `passage_id`, `source_id`, `captured_at_utc`, `text`; необов'язково — `artifact_id`, `artifact_start_offset`, `locator`, `lineage_family_id`, `independent_root_id`. `artifact_start_offset` — перевірене зміщення початку passage у вихідному artifact. Якщо такого mapping немає, передайте `null` або опустіть поле: кандидат зберігає `artifact_start_offset: null` і `artifact_offset_status: unavailable`. Запис, отриманий після `as_of_utc`, не потрапляє до кандидатів. Зріз включає SHA-256 канонічного маніфесту IDs, джерел, часу отримання, хешів тексту, offsets, locator та lineage refs; receipt також містить терми запиту та параметри BM25.

`passage_start_offset` / `passage_end_offset` вказують точний фрагмент усередині `passage.text`; їхня одиниця — Unicode code point. Поля `start_offset` / `end_offset` збережені для сумісності та мають той самий passage-relative зміст. `artifact_start_offset` для кандидата обчислюється лише коли на вході є ціле перевірене зміщення; інакше він залишається `null`, а жодне passage-relative значення не видається за позицію в оригінальному файлі. Вихід кандидата зберігає `locator` без змін.

Source Watch bridge створює filtered `article_text` passage без відображення символів на байти/позиції оригінального HTML. Його locator пов'язує passage з manifest, body hash, source URL та extraction metadata, але не задає raw-HTML offset. Для такого passage використовується `artifact_start_offset: null`; quote offsets можна відтворити в filtered passage text, але не вважати точними координатами сирого HTML.

Пошукові напрями `claim_terms` і `counterevidence_terms` означають спосіб пошуку, а не позицію автора. Другий напрям вимагає одночасної наявності claim-токенів і хоча б одного заданого маркера заперечення/виправлення. Це збільшує точність маршрутизації, але може пропустити інакше сформульовані спростування. Можна додати `query_variants` та налаштований список counterevidence terms.

Дедуплікація top-k відбувається лише за явно наданим `lineage_family_id`; без нього candidate лишається окремим із `lineage_status=unknown`. Ця дедуплікація не підтверджує незалежність джерел.

## Оцінка evidence та статус

`decision=candidate` є типовим. `decision=accepted` вимагає `acceptance_basis=human_adjudication` або `validated_rule` із `validated_rule_id`; моделі без окремої валідованої процедури не можуть самостійно прийняти оцінку. Для `supports` усі значення з `claim.key_values` мають бути точно повторені в `asserted_values`. Додатково система витягає цифри й підтримувані словесні кількісні форми з тексту claim: кожне таке значення має бути присутнє в семантично відповідному структурованому полі. Наприклад, `40 people` потребує count/person field; `year=40` не замінює `count=40`, а `comment_count=40` не задовольняє `participant_count=40`. Для підрахунків звіряється обмежений набір явних кванторів: `до 40` → `lte`, `не менше` / російське `не меньше 40` → `gte`, `понад 40` → `gt`, `менше ніж 40` / `under 40` → `lt`, `приблизно 40` → `approx`. Символьні форми `<40`, `<=40` / `≤40`, `>40`, `>=40` / `≥40`, `≈40` зіставляються відповідно з `lt`, `lte`, `gt`, `gte`, `approx`. Неуточнене `40 людей` означає `eq`. Невідомий оператор, декілька несумісних кванторів або нерозпізнаний/заперечений квантор поблизу числа не трактуються як точний підрахунок. Несумісність повертає `numeric_operator_mismatch`; відсутність відповідного семантичного поля повертає `missing_structured_value:<value>`. Це fail-closed структурна узгодженість: вона не перевіряє, чи passage справді містить число або квантор, і не задає допуск для `approx`; це потребує окремої evidence assessment. `aggregate_verification` повторно виконує ті самі перевірки для serialized accepted records, тому пряме формування JSON не обходить guard. Обробка чисел охоплює Arabic digits і базові українські, російські та англійські cardinal words, але не є повним морфологічним парсером числівників.

`assessment_id` хешує повний структурований assessment payload, включно з assessor/rule/root/citation, тому зміна provenance створює окремий record ID.
Агрегатор вимагає унікальний непорожній assessment ID; записи без нього виключаються з вердикту, а повторне використання ID блокується.

Підсумок використовує лише accepted assessment з тим самим claim ID і точно таким самим JSON scope. `supported_within_scope` або `refuted_within_scope` вимагає заданої кількості `independent_root_id` з `independence_status=confirmed_independent`. Цей модуль не встановлює незалежність: такі ID мають бути верифіковані upstream. Якщо той самий корінь має accepted support і contradiction, результат зберігає `conflicting_evidence`; per-side root counts включають цей корінь, а `shared_root_ids` явно показує перетин. Таке внутрішнє протиріччя не подається як дві незалежні підтверджувальні сім'ї.

ID результату змінюється разом із scope, key values, cutoff, повним assessment/exclusion provenance, порогом root count, станом завершення пошуку та supersedes-зв'язком. Ledger adapter зберігає в полі `rationale` структурований JSON із assessment IDs, точними цитатами, датами, assessor/rule ID, root IDs, причинами виключення та параметрами агрегації, щоб не губити provenance у поточному контракті SQLite.

`export_verification_package` створює: `evidence_candidates.jsonl`, `evidence_assessments.jsonl`, `verification_results.jsonl`, `search_receipt.json`, `claim_matrix.md`, `unresolved_retrieval_queue.jsonl`. Кожен рядок `evidence_assessments.jsonl` зберігає assessment payload та має `as_of_projection` із `as_of_utc`, `verification_result_id`, `included_in_verification` і `exclusion_reason`. Отже, пізніші сирі оцінки залишаються в архівному експорті, але їх виключення з конкретного зрізу позначене явно. Queue бере лише assessments, включені у відповідну as-of проєкцію; оцінка, відхилена через час/scope/value, не закриває retrieval-задачу.

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
