# W07 — Консервативна реконструкція подій

## Результат

Додано `src/analysis/event_reconstruction.py`, `src/analysis/event_reconstruction_cli.py`, JSON Schema та українську специфікацію. Компонент приймає вже вилучені `EventMention` записи, залишає кожну згадку окремою, формує роздільні фізичну й комунікаційну часові шкали, відношення інтервалів і лише кандидатні `possible_same` посилання.

CLI створює `events.jsonl`, `event_links.jsonl`, `temporal_relations.jsonl`, `unresolved.jsonl`, `unresolved_constraints.jsonl`, `timeline.json`, `timeline.md` і `run_receipt.json`. Перед записом bundle перевіряється JSON Schema. Receipt містить хеш джерела, хеші виходів, `incident_id`, `run_id`, `as_of_utc`, Git commit, параметри та обмеження.

## Перевірені інваріанти

- Час публікації не підміняє фізичний час події.
- Комунікаційні записи з різними time bases мають `unknown` temporal relation; ці бази не створюють заборону на кандидатний link.
- Timestamp intervals порівнюються як parsed UTC datetimes, а не як рядки.
- Entity aliases зіставляються лише точно; неоднозначні aliases залишаються `ambiguous`.
- Event similarity не зливає записи; `cannot_link` блокує link, а відсутня ціль обмеження записується як unresolved.
- `before` не породжує причинність.
- CLI перевіряє вхід/out директорію, symlink, регулярні типи файлів та сторонні файли; `--overwrite` замінює лише відомий bundle.
- Input типи суворо перевіряються, output валідовується JSON Schema до запису.

## Перевірка

```bash
uv run --with pytest --with jsonschema -- python -m pytest -q tests/test_event_reconstruction.py
python -m py_compile src/analysis/event_reconstruction.py src/analysis/event_reconstruction_cli.py
git diff --check
```

Результат: **22 тести пройшли**; компіляція й diff check пройшли. Незалежний read-only review після виправлень — PASS.

## Межі

Це не extractor з raw text і не case-level реконструкція. Він упорядковує лише передані source-linked event mentions. Поточний кейс не отримав нових установлених фактів від цього модуля, бо W06 retrieval/assessment ще інтегрується. `as_of_utc` записується, але вхідний файл має бути попередньо відфільтрований за cutoff.
