# Побудова фінальних PDF

Запуск із кореня проєкту:

```bash
.venv/bin/python scripts/reports/build_report.py
.venv/bin/python scripts/reports/build_figures_dossier.py
.venv/bin/python scripts/reports/build_figures_dossier.py --source wiki/methods/russian-influence-attribution-early-warning.md --output output/pdf/russian_influence_attribution_early_warning_2026-11-06.pdf
```

Фінальні PDF зберігаються в `output/pdf/`. Це результати для читача; їх можна комітити разом із вихідними звітами. `tmp/` містить проміжні рендери й виключений із git. Сирі тексти субтитрів, необроблені платформні знімки та покоментні/поакаунтні діагностики залишаються локально; агрегати, код і походження результатів придатні для версіонування. Перед явно запитаним завантаженням репозиторію перевіряйте список індексованих файлів на облікові дані й приватний матеріал сесій.

Чотири раніше відстежувані поакаунтні CSV прибрані лише з індексу git; локальні файли збережені для відтворення. Це не переписує попередню історію git.
