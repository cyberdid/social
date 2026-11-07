# Звіт виконання Phase 6 / W12 — Constrained Analytical Report MVP

## Статус

Реалізовано окремий детермінований модуль генерації доказово обмеженого звіту. Він споживає типізовані findings, evidence registry та bounded VerificationResults; не викликає LLM і не пише довільний аналітичний текст.

## Змінені файли

- `src/analysis/report_generator.py` — валідація контрактів, Markdown renderer, JSONL, quality report, run receipt та атомарний bundle writer.
- `schemas/analytical_finding.schema.json` — Draft 2020-12 контракт типізованого finding.
- `tests/test_report_generator.py` — сфокусований набір тестів.
- `docs/specs/constrained-analytical-report-v1.md` — інтерфейс, статуси, citations, виходи й межі застосування.

## Перевірки, які тепер блокують звіт

1. Dangling/duplicate IDs, включно з недозволеним dangling VerificationResult ID на типі finding, неправильний SHA-256, timezone, cutoff, locator або quote/offset mismatch.
2. VerificationResult із невідомими evidence refs, несумісними claim/scope/status/root counts або evidence IDs, які у finding приховано чи подано лише частково.
3. `supported_within_scope` і `refuted_within_scope` без root threshold та точного підходящого verification status; conflict без повних evidence refs з обох боків.
4. Source-attributed/documented assertions, які не збігаються з точним cited quote. `documented_fact` рендерить факт про вміст архівного матеріалу; `source_attributed` зберігає атрибуцію твердження джерелу.
5. Числові tokens у supported/refuted/conflicting/hypothesis propositions, яких немає саме у процитованих locator quotes, а також прості причинні й часові-order cues без окремих causal/temporal contracts.
6. Довільні невідомі поля, багатореченнєві/складені propositions і вільний текст альтернатив/обмежень; дозволені лише фіксовані коди.
7. Silent overwrite або заміна каталогу, де є невідомі файли. Для наявного bundle використовується атомарний Linux `renameat2(RENAME_EXCHANGE)`; коли він недоступний, попередній шлях не відсувається.

Unresolved findings потребують bounded VerificationResult, показують усі refs з його обох сторін і прямо формулюють, що недостатність доказів не є спростуванням.

## Виходи

`incident_report.md`, `findings.jsonl`, `report_quality.json`, `run_receipt.json`. JSONL містить citation metadata (source ID/URI, artifact ID/hash, captured time і exact locator), а не лише citation IDs. Run receipt фіксує canonical input hash та хеші трьох інших outputs. Output hashes стабільні для повтору однакового впорядкованого input bundle.

## Перевірки

```text
uv run --with pytest --with jsonschema -- python -m pytest -q tests/test_report_generator.py
31 passed

python -m py_compile src/analysis/report_generator.py
exit 0

git diff --check
exit 0
```

Тести включають dangling evidence/verification IDs, locator, unsupported verification status, число за межами exact citation, обидва боки конфлікту, bounded refutation, лише-unresolved звіт, source quote для кожного процитованого джерела, narrower claim scope, майбутні evidence records, детерміновані hashes, успішний і зірваний atomic overwrite, не-boolean overwrite, Markdown link/fence escaping і JSON Schema.

## Відомі межі

Це structural/citation/status gate, не NLI і не детектор правди. Token presence не гарантує, що число використано в правильній ролі чи одиниці; citations не доводять семантичного entailment, автентичності джерела/файла, незалежності джерел або повноти збору. Causal/temporal regex-и — консервативні guardrails з неповним мовним покриттям. Модуль не перевіряє фізичний hash файла: caller має передати його верифікований registry record. JSON quality field явно використовує `unsupported_assertion_count=null` та `assertion_check_status=not_evaluated_semantic`, а не удає, що семантичні помилки дорівнюють нулю.

PDF та integration adapter з EvidenceLedger не входили до ізольованого W12 deliverable; downstream має передати Passage ID як стабільний evidence ID і відповідні provenance поля.
