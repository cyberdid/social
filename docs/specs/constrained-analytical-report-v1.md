# Constrained Analytical Report v1

`src/analysis/report_generator.py` формує звіт лише з типізованих findings, реєстру доказів і bounded `VerificationResult`. Модуль не викликає LLM, не пише довільні аналітичні абзаци й не вирішує семантично, чи доказ підтверджує claim.

## Вхідний контракт

Публічна функція:

```python
build_report_bundle(
    findings: list[dict],
    evidence_records: list[dict],
    verification_results: list[dict],
    context: dict,
    output_dir: str | Path,
    *,
    overwrite: bool = False,
) -> dict
```

`context` обов'язково містить `incident_id`, `run_id`, UTC `as_of_utc`, `working_title`, об'єкт `scope` та об'єкт `coverage`; `git_commit` може бути `null`. `scope` звіту описує загальні межі кейсу. Scope конкретного claim може бути вужчим, але мусить точно збігатися зі scope його VerificationResult.

Кожний evidence record містить `evidence_id`, `source_id`, `source_uri`, `artifact_id`, lowercase SHA-256 `artifact_sha256`, `captured_at_utc` і точний locator. Text locator має `kind=text_span`, `start_offset`, `end_offset`, `offset_unit=unicode_codepoint` та повний зареєстрований `text`; quote обчислюється як `text[start_offset:end_offset]`. За наявності переданий `quote` повинен точно збігатися зі зрізом. Video locator має `kind=video_segment`, невід'ємні `start_ms < end_ms` і `time_basis=original_media_pts`. Evidence, зафіксований після `context.as_of_utc`, не приймається.

VerificationResult приймає ідентифікатор `verification_result_id` або W06 `result_id`, `claim_id`, об'єкт `scope`, UTC `as_of_utc`, status та списки `supporting_evidence_ids` і `contradicting_evidence_ids`. Список evidence IDs у finding має точно відповідати обом відповідним спискам результату; додати лише зручну частину доказів або приховати протилежний бік не можна. W06 root counters та `minimum_independent_roots` перевіряються для status `supported_within_scope` / `refuted_within_scope`; суперечливий результат має зберігати обидва боки. Статуси, оцінки, корені чи незалежність не виводяться повторно цим renderer-ом.

Для кожного evidence ID, на який посилається VerificationResult, `captured_at_utc` мусить бути не пізніше за `VerificationResult.as_of_utc`; окрема перевірка також вимагає, щоб час доказу та зріз результату не були пізнішими за `context.as_of_utc`. У release evaluator той самий зв'язок перевіряється навіть без report context. Відсутній або некоректний час є hard-gate помилкою, а не підставою припускати, що доказ був доступний раніше.

## Типи findings

Спільні поля звичайного finding: `finding_id`, `kind`, `claim_id`, proposition `statement`, об'єкт `scope`, `evidence_refs` зі значеннями ролі та, коли потрібно, VerificationResult ID. Формальна JSON Schema: `schemas/analytical_finding.schema.json`. Невідомі поля відхиляються — так довільна model rationale не просочується до звіту. Одне finding має містити одну коротку proposition; складений абзац, кілька речень або `;` треба розбити на окремі записи.

| `kind` | Умови | Шаблонний зміст |
|---|---|---|
| `documented_fact` | `statement` — точний фрагмент із locator; тільки роль `source_attributed` | У збереженому матеріалі зазначеного джерела зафіксовано quote. Це твердження про вміст артефакту. |
| `source_attributed` | `statement` — точний fragment; обов'язкова роль `source_attributed`; необов'язкова роль `context` лише з того самого джерела | Джерело повідомляє процитоване твердження; точний контекстний фрагмент показується окремо й не вважається незалежною підтримкою або підтвердженням. |
| `supported_within_scope` | Точне claim/scope/status match; всі support і contradiction IDs із VerificationResult; мінімум незалежних support roots | У заданих межах матеріали підтримують proposition. Якщо існують contradiction records, їх також показано. |
| `refuted_within_scope` | Точне claim/scope/status match; всі support і contradiction IDs; мінімум незалежних contradiction roots | Лише у межах визначеного scope proposition спростована; збережені support records також показуються. |
| `conflicting` | Status `conflicting_evidence`; обидва набори evidence IDs повні | Окремо показуються supporting і contradicting цитати; winner не обирається. |
| `hypothesis` | Цитоване підґрунтя; числові tokens мають бути у cited text | Proposition позначається як гіпотеза. `alternatives` приймає лише фіксовані коди з `ALTERNATIVE_TEXT`. |
| `unresolved` | Обов'язковий узгоджений VerificationResult з одним із `unverified`, `insufficient_evidence`, `not_verifiable`; обидва evidence sets повні | Відкрито позначається як не встановлено; брак доказів не є спростуванням. |
| `methodological_limit` | Тільки фіксований `limitation_code` | Рендериться відомий текст обмеження, а не довільна проза. |

Для решти finding kinds дозволені лише коди `limitation_codes`, перетворені на фіксовані фрази. Довільні `alternatives`, `limitations`, rationales та model output не рендеряться. Кожен verification finding має один `claim_id` і scope.

## Перевірки та відмови

- Dangling або duplicated IDs, invalid SHA-256/timestamp, відсутній locator, невідповідні offsets/quote, майбутній evidence/result або mismatch claim/scope/status зупиняють формування пакета.
- Підтримане й спростоване твердження потребує точного набору refs із VerificationResult та кореневої кількості, що задовольняє заданий мінімум. VerificationResult зі статусом і root counts, які суперечать одне одному, блокується.
- Для підтриманих, спростованих, суперечливих та гіпотетичних propositions кожен числовий token має траплятися саме в процитованому locator quote, не просто деінде у ширшому passage. Це консервативна перевірка присутності тексту, не перевірка значення, заперечення, одиниці або арифметики.
- Часові слова відносного порядку у підтриманих/спростованих propositions блокуються, бо цей API не отримує `TemporalRelation`. Причинні слова теж блокуються без окремого causal contract. Це не замінює повної мовної перевірки.
- Markdown escaping не дає джерельному рядку стати керівною Markdown-структурою. Embedded JSON фіксується у fence-safe вигляді.
- Каталог результату не є symlink; існуючий пакет не перезаписується без `overwrite=True`; невідомі файли блокують заміну. Новий bundle готується у staging directory на тому самому filesystem. Перша публікація робиться `os.replace`; заміна на Linux використовує `renameat2(RENAME_EXCHANGE)`, щоб шлях результату весь час вказував або на повний попередній, або на повний новий bundle. Якщо атомарний обмін недоступний, команда завершується помилкою, не відсуваючи старий bundle.

## Виходи

- `incident_report.md` — звіт із покриттям, typed findings, scope і цитатами. У цитаті є evidence/source ID, URI, час отримання, artifact ID, SHA-256, точний текстовий offset або original-media PTS та роль (supporting/contradicting/атрибуція).
- `findings.jsonl` — нормалізовані findings з `citation_ids` і повними citation metadata без дублювання повного доказового корпусу.
- `report_quality.json` — structural counts. `unsupported_assertion_count=null` і `assertion_check_status=not_evaluated_semantic` прямо вказують, що entailment не перевірявся.
- `run_receipt.json` — `incident_id`, `run_id`, `as_of`, commit, хеш канонічних inputs та SHA-256 інших трьох outputs. Self-hash receipt не включає власний файл, щоб уникнути циклу.

Результат детермінований для однакового вмісту і порядку вхідних масивів. Finding-івідентифікатори та розділи виводяться у фіксованому порядку; citation refs сортуються за роллю та evidence ID.

## Зв'язок із W06/W07 та EvidenceLedger

Renderer є останнім форматувальним шаром після W06 `aggregate_verification()` і W07 event/timeline reconstruction. W06 result можна передати без перейменування ID (`result_id`), але evidence registry має включати всі посилання з VerificationResult. `evidence_id` у реєстрі має бути тим самим стабільним ID, який згадується в assessments/results (наприклад Passage ID); upstream adapter відповідає за збирання source/artifact/hash/capture/locator полів із EvidenceLedger. Для перевірених event timestamps W07 потрібні власні temporal evidence anchors; цей MVP не перетворює W07 timeline у prose автоматично.

## Що цей MVP не доводить

Structural/schema/citation integrity не є semantic entailment, перевіркою автентичності джерела чи артефакту, правдою події, повнотою пошуку, незалежністю джерел або правильністю upstream claim/evidence assessments. Наявність числа у процитованому рядку не встановлює, що воно означає потрібну величину або не є запереченим. Наявність hash не перевіряє його проти фізичного файла, якщо caller не передав artifact store для такого аудиту. Немає повного parser-а українських/російських compound claims, дат, займенникових посилань, сарказму, мотивів чи причинності; окремі регулярні блокери — лише консервативні guardrails. Для цих питань слід позначити результат unresolved/limitation або провести незалежний review, а не стверджувати, що їх вирішено.

## Перевірка

```bash
uv run --with pytest --with jsonschema -- python -m pytest -q tests/test_report_generator.py
python -m py_compile src/analysis/report_generator.py
git diff --check
```
