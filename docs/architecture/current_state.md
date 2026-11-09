# Social: поточний стан коду й даних

**Базовий зріз:** `fc7e58d` (`github-upload-snapshot`), перевірено перед новою реалізацією. Нові коміти цього робочого циклу описані окремо; цей документ не приписує запропонованим компонентам production-готовність.

## Уже було в базовому зрізі

- Збирачі Telegram API/Web, Telegram-коментарів, YouTube, TikTok, Instagram та архіватор вебджерел у `src/`.
- Аналіз Telegram на основі підготовки корпусу, legacy regex-наративів, груп каналів, текстової схожості, мережевих/часових сигналів і permutation null models у `src/analysis/`.
- Часткові медіа fingerprinting, YouTube subtitle/content аналіз і звітні артефакти у `reports/`.
- Існуючі одиничні тестові файли для окремих collectors та аналізаторів у `tests/`; загальної end-to-end acceptance suite не було засвідчено у baseline.

## Дані

- Git checkout містить `raw/`, `reports/`, `wiki/`, код, конфігурації та документацію.
- Частина локального Telegram-корпусу в `$SOCIAL_REPO_ROOT/data/` є поза Git/ігнорується; її доступність не можна вважати властивістю клону. `reports/baseline_manifest.json` фіксує локальні файли лише їхніми шляхами, розмірами й хешами.
- Відеопілот зберігається поза Git у `~/Downloads/SocialIncidentVideos/`; у репозиторії залишаються лише технічні індекси та звіти.
- Вибірка Telegram є цільовою; підрахунки переглядів є snapshot counters, а не унікальне охоплення.

## Що було відсутнє у baseline

- Єдине append-only сховище source/artifact/passage/claim/assessment із перевіркою зв'язків.
- Окрема верифікаційна сутність із bounded scope, supporting/contradicting evidence і `as_of`.
- Автоматична версійована physical event timeline та граф зв'язку Claim–Evidence–Provenance.
- Наскрізний validator звіту, який забороняє dangling references, недоказові числа та причинність лише з temporal order.
- Єдині versioned `IncidentSpec`/`RunManifest` JSON Schema контракти.

## Поточний стан робочого циклу — 8 листопада 2026

Нижченаведені компоненти додані або змінені у поточному **незакоміченому** робочому дереві; наявність коду й успішні структурні тести не означають семантичної валідації висновків про реальний кейс.

- Є append-only evidence ledger, JSON Schema контракти, baseline manifest, синтетичні fixtures, source-lineage candidates, локальний BM25 retrieval, claim-verification правила, Narrative v3, channel-evidence експорт, event/conflict/information-dynamics модулі, uncertainty scenarios, constrained report generator, offline runner, orchestrator та incremental dispatcher.
- Підготовлений offline-прогін `run-post-fix` опрацював надані типізовані файли: 555 claim-кандидатів шукалися у 23 passage, але verification results — 0; 574 event mentions лишилися нерозв'язаними, physical-event rows — 0, conflict-position records — 0. Окремий source-linked повтор зі свіжими passage зі Source Watch шукав 555 claims у 30 passage; він повернув 11 897 BM25 кандидатів, але так само 0 прийнятих assessments і 0 VerificationResults. Семантична точність не оцінювалася.
- Окремий masterplan orchestrator run `masterplan-2026-11-08` завершився як `completed_bounded`, але це був `dry_run`: 0 цілей, 0 source snapshots, Telegram adapter відсутній; normalization, extraction, verification, reconstruction і reporting отримали `not_run`. Це не end-to-end запуск.
- Окремий інтеграційний прогін із вісьмома вже підготовленими typed artifacts перевірив локальні компоненти та структурні виходи; він також не збирав джерела й повернув 0 verification results. Його receipt: `reports/orchestrator/w00-integration-receipt-2026-11-08.md`.
- Relevance false-negative audit наразі є лише дизайном стратифікованої вибірки `n=378`; записи не ад'юдиковані, тому емпіричні recall і false-negative rate невідомі. Для Narrative v3 немає незалежного gold set з per-class semantic metrics.
- Channel evidence та source-lineage файли містять кандидатні сигнали, але походження/державний контроль/участь у кампанії не атрибутовані; незалежні roots для кейсових claims не встановлені.
- Відео: 12 локальних контрольних файлів технічно декодовані; окремо оброблено 607 унікальних Telegram archive assets для кандидатних ASR сегментів. Другий ASR-прохід зіставив 7 відео; приватний sidecar утримує raw текст і контекстні редакторські кандидати окремо. Для цих транскриптів немає reference transcript і WER/CER; аудіо-цитати, візуальна відповідність місцю, часу й подіям не перевірені. TikTok прогін покрив лише локально наявні матеріали з недоступними позиціями, а не повний перелік посилань.
- Повний проєктний тестовий набір у віртуальному середовищі пройшов: 551 tests + 16 subtests. Frozen harness має 6/6 структурних контролів; модульні тести поширюють покриття на частину сценаріїв F07–F15. Немає повного incident-level end-to-end semantic benchmark; F16 prompt-injection контроль не реалізований.
- Incremental replay/dispatch перевірено на синтетичних корекціях; реальну корекцію з прийнятим evidence та подальшу перебудову кейсового звіту не виконано.
- Основний PDF перепобудовано з актуального Markdown: 16 сторінок A4, оновлено artifact manifest, текст витягується без replacement characters; вибірковий візуальний огляд пройшли сторінки 1, 15 і 16. Це підтверджує якість файлу й розкладки, але не точність чи повноту фактичних висновків.

**Підсумок статусу:** masterplan частково реалізований, але не завершений. Повний список відкритих критеріїв і підстав — у `reports/orchestrator/masterplan-status-2026-11-08.md`. Деякі критерії можна закрити подальшою інженерною роботою; claims accuracy, реальна хронологія, source independence, медійна автентичність і geolocation залишаються невстановленими без придатних незалежних доказів/еталонів.
