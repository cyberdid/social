# Контракт інциденту та запуску Social v1

Цей контракт реалізує початкову схему `IncidentSpec` і `RunManifest` з Master Plan. Він обмежує доступ до публічних джерел, фіксує час зрізу й бюджет, та не дозволяє external AI без окремого privacy-прапорця.

## Файли

- `schemas/common.schema.json` — UTC timestamp, SHA-256, provenance та limitations.
- `schemas/incident_spec.schema.json` — сфера, локації, часовий інтервал, мови, seeds, платформи, політика збору, моделі й бюджети.
- `schemas/run_manifest.schema.json` — стани запуску, джерельні snapshots, receipts завдань і хеші виходів.
- `src/contracts.py` — перевірка JSON Schema та додаткових інваріантів: `start <= end`, timestamps у UTC, `finished_at >= started_at`.

## Інваріанти

1. Збір дозволяє лише публічні API/вебсторінки або явно надані користувачем публічні URL/локальні файли; приватні джерела вимкнені.
2. `allow_external_ai=true` потребує `privacy_policy=explicit_external_ai_allowed`.
3. Вікна й час зрізу повинні мати timezone UTC; naïve datetimes не приймаються.
4. Будь-який `RunManifest` може завершитися зі станом `partial/blocked/failed`; збій джерела не кодується як відсутність факту.
5. Бюджети — конфігураційні обмеження користувача, не науково оптимальні рекомендовані значення.

## Перевірка

```bash
uv run --with pytest --with jsonschema -- python -m pytest tests/test_contracts.py -q
```

`src/contracts.py` потребує `jsonschema>=4.18.0,<5` і `referencing>=0.30` (див. `requirements-contracts.txt`), оскільки валідатори використовують сучасний параметр `registry=`. JSON Schema навмисно не містить автоматичного причинного чи джерельного рейтингу.
