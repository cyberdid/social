# Bounded audit входів для source-lineage — 08.11.2026

## Результат

Перевірено лише структуру й метадані двох збережених входів: 30 passages і 574 `evidence_records` із приватного `report_bundle`. Сирий текст, URL, source IDs, artifact IDs, lineage-family IDs та медіа не виводилися у звіт. Повний content-free receipt із SHA-256/розмірами: [`source-lineage-input-audit-2026-11-08.json`](source-lineage-input-audit-2026-11-08.json).

- У 30 passages є 30 унікальних `source_id`, 30 `artifact_id` і 30 `lineage_family_id`. Це унікальність переданих значень, не доказ незалежності джерел.
- На тому самому NFKC + casefold + whitespace-normalized exact-text правилі, яке використовує локальний `source_lineage.py`, не знайдено повтору passage-тексту між різними `source_id` у цій обмеженій вибірці.
- У passage rows та у 574 bundle evidence rows немає `claim_id`; explicit dependency-reference fields відсутні/порожні. Тому їх не можна коректно подати в claim-scoped `analyze_source_lineage` як готові зв'язки.
- 574 evidence rows мають лише 2 distinct `source_id`, `artifact_id` і `artifact_sha256` значення в межах bundle. Це показує повторне посилання на невелике число source artifacts, а не 574 незалежні джерела.
- Для цього аудиту встановлено **0 підтверджених dependency edges** і **0 незалежних source roots**. Невиявлення exact duplicates не означає, що джерела незалежні.

## Інтерпретація

Це покращує оцінку P0.2/W05: ми перевірили, чи достатньо наявних двох наборів, щоб запустити claim-level lineage, і підтвердили, що їх недостатньо. Потрібен окремий crosswalk `claim_id ↔ evidence_id/passage_id`, обґрунтований passage scope і явні dependency references тільки там, де їх підтверджує сам запис або архівований матеріал. BM25 candidate match не є достатньою підставою для цього зв'язку.

Цей аудит не встановлює джерело-оригінатор, напрямок копіювання, незалежність, правдивість claims або відсутність парафразів. Він покриває лише 30 наданих passages і 574 bundle rows; поза ними немає заяви про повноту.
