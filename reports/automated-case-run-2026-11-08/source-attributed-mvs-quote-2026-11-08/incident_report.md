# Вузька перевірка атрибутованого формулювання МВС — аналітичний звіт

- Incident ID: petropavlivska-borshchahivka-2026-11
- Run ID: source-attributed-mvs-quote-2026-11-08
- Зріз as_of: 2026-11-08T17:50:00Z
- Сфера: Перевіряється лише наявність цього формулювання у захопленій сторінці МВС; фізична кількість осіб не встановлюється.

Цей звіт формується з типізованих записів. Наявність посилання підтверджує лише можливість перевірити процитований фрагмент; вона не гарантує семантичної правильності оцінки.

## Покриття джерел

```json
{
  "archived_sources": 1,
  "independent_sources": 1,
  "passages": 1
}
```

## Твердження, приписані джерелам

### finding\_mvs\_quote\_26\_people\_20261108

Контекст у джерелі: «Командувач Національної гвардії України генерал-майор Олександр Півненко пояснив». Джерело source\_57425990dc7315a1b617c61cbe596ec31d6c53e1add19fa8442a38e41578229f повідомляє: «Загалом у приміщенні перебували 26 осіб.»

Обмеження:
- Покриття джерел неповне; висновки обмежені наданим корпусом.

Доказові посилання:
- \[passage\_79d8f8728f5e054c4d41af8e2205bc963b31f9c6f64947ed617bc027bbfa26e9\] МВС: брифінг щодо подій на Київщині, 3 листопада 2026 року (source ID source\_57425990dc7315a1b617c61cbe596ec31d6c53e1add19fa8442a38e41578229f; https://mvs.gov.ua/news/u-ministerstvi-vnutrisnix-sprav-ukrayini-vidbuvsia-brifing-shhodo-podii-na-kiyivshhini); роль: context; captured 2026-11-08T08:05:55.795375Z; artifact artifact\_830f900203f4aa27f4285bc97e8818b7d35128104976965af3cd97a0e98b2f49 SHA-256 3aaf8cb5f02ab6b1228635d3a49ab9699c97cde2d49db993c84e84f3caef4f49; Unicode code points 3293–3373 — «Командувач Національної гвардії України генерал-майор Олександр Півненко пояснив»
- \[passage\_b1befbee74f5d623e709a2c4c2b36f723c1d6bd107411b2884e94812acfa3374\] МВС: брифінг щодо подій на Київщині, 3 листопада 2026 року (source ID source\_57425990dc7315a1b617c61cbe596ec31d6c53e1add19fa8442a38e41578229f; https://mvs.gov.ua/news/u-ministerstvi-vnutrisnix-sprav-ukrayini-vidbuvsia-brifing-shhodo-podii-na-kiyivshhini); роль: source\_attributed; captured 2026-11-08T08:05:55.795375Z; artifact artifact\_830f900203f4aa27f4285bc97e8818b7d35128104976965af3cd97a0e98b2f49 SHA-256 3aaf8cb5f02ab6b1228635d3a49ab9699c97cde2d49db993c84e84f3caef4f49; Unicode code points 3526–3566 — «Загалом у приміщенні перебували 26 осіб.»

Scope цього finding:
```json
{
  "description": "Перевіряється лише наявність цього формулювання у захопленій сторінці МВС; фізична кількість осіб не встановлюється.",
  "source_id": "source_57425990dc7315a1b617c61cbe596ec31d6c53e1add19fa8442a38e41578229f",
  "type": "source_content"
}
```

## Обмеження автоматизації

Схемна й citation-перевірка підтверджує цілісність посилань і межі формату, але не семантичне слідування, повноту джерел або істинність описаних подій.
