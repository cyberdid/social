# Реконструкція фізичного інциденту: с. Петропавлівська Борщагівка (2 листопада 2026 року)
## Структурована хронологія фізичних подій, делімітація та аналіз обмежень

> **Ідентифікатор документа:** `reports/event-reconstruction/physical_event_timeline_2026-11-09.md`  
> **Цільовий артефакт:** Social Master Plan v2.0 (Track 2, GATE-02)  
> **Статус валідації:** Схвалено за схемою `schemas/event_reconstruction.schema.json` v1.0  
> **Час генерації (As Of UTC):** `2026-11-09T08:00:00Z`  
> **Ідентифікатор прогону:** `run-m2-event-reconstruction-2026-11-09`  
> **Git Commit:** `9019afd896e57729acf5f20e07151b4e1437ad0a`  

---

## 1. Резюме та архітектурне розмежування рівнів (Epistemic Boundaries)

У попередньому автоматизованому звіті від 8 листопада 2026 року (`reports/automated-case-run-2026-11-08/event_reconstruction_summary.json`) було зафіксовано **0 фізичних подій** при наявності 574 комунікаційних згадок. Це було прямим наслідком відсутності структурованих часових меж інциденту (`earliest_utc` / `latest_utc`) та суворої архітектурної заборони підміняти час фізичної події часом публікації допису.

Цей звіт упорядковує **5 фізичних згадок про епізоди конфлікту**, які аналітик вручну відібрав і сформулював за переліченими повідомленнями джерел. Скрипт детерміновано структурує ці задані згадки; цей результат не є результатом автоматичного виявлення подій із первинних текстів, дописів або медіа. Часові інтервали можуть перетинатися й не означають, що кожен епізод був окремою послідовною дією.

### Ключові архітектурні принципи:
1. **Суворе онтологічне розділення:** Фізичний шар (`timelines.physical`) містить лише задані аналітиком згадки `event_kind: physical` з наведеними у джерелах часовими межами. Межі є кураторською нормалізацією тверджень джерел, а не незалежним підтвердженням фактичного часу. Комунікаційний шар (`timelines.communication`) базується на часі публікації (`publication_time_utc`), який не підставляється замість часу фізичної події.
2. **Дескриптивний некаузальний порядок:** Відношення `before` або `overlaps` відображають виключно взаємне розташування часових інтервалів і маркуються як `causal: false`. Часова послідовність не є доказом причинно-наслідкового зв'язку.
3. **Межі корпусу через негативні обмеження (`cannot_link`):** Згадка про окрему пожежу складського приміщення у Бучанському районі внесена до кураторського переліку як інший інцидент і відокремлена від фізичних згадок про події 2 листопада. Обмеження зберігають це задане розділення, але не є автоматичним виявленням помилкових тверджень чи мотивів їх поширення.
4. **Якісні evidence tiers:** `corroborated_multi_source` означає сумісну підтримку кількома згадками джерел; `official_proceedings` означає, що опис є в офіційних або судових матеріалах. Це категорії виду підстави, а не ранжування істинності чи калібровані ймовірності.

---

## 2. Структурована хронологія фізичних подій (`timelines.physical`)

| № | Ідентифікатор | Часовий інтервал (UTC) | Київський час | Локація | Якісний рівень доказової підтримки |
|---|---|---|---|---|---|
| **Згадка 1** | `phys_ev_01_ambulance_arrival_street` | `2026-11-02T09:00:00Z` … `2026-11-02T10:40:00Z` | Ранок 2 листопада 2026 року, орієнтовно 11:00–12:40 за київським часом (до появи перших повідомлень у соцмережах) | `place:petropavlivska_borshchahivka_street` | **corroborated_multi_source** |
| **Згадка 2** | `phys_ev_02_building_perimeter_clash` | `2026-11-02T11:00:00Z` … `2026-11-02T15:30:00Z` | День 2 листопада 2026 року, 13:00–17:30 за київським часом | `place:petropavlivska_borshchahivka_building` | **corroborated_multi_source** |
| **Згадка 3** | `phys_ev_03_law_enforcement_arrival_bus_block` | `2026-11-02T14:30:00Z` … `2026-11-02T18:00:00Z` | Друга половина дня 2 листопада 2026 року, 16:30–20:00 за київським часом | `place:petropavlivska_borshchahivka_building` | **official_proceedings** |
| **Згадка 4** | `phys_ev_04_pyrotechnics_and_flares_escalation` | `2026-11-02T18:00:00Z` … `2026-11-02T20:30:00Z` | Вечір 2 листопада 2026 року, 20:00–22:30 за київським часом | `place:petropavlivska_borshchahivka_building` | **corroborated_multi_source** |
| **Згадка 5** | `phys_ev_05_containment_and_detention` | `2026-11-02T20:30:00Z` … `2026-11-03T00:30:00Z` | Ніч з 2 на 3 листопада 2026 року, 22:30–02:30 за київським часом (приблизне часове вікно) | `place:petropavlivska_borshchahivka_building` | **official_proceedings** |

---

## 3. Детальний аналіз фізичних епізодів конфлікту

### 3.1. Епізод 1: Прибуття автомобіля з логотипом екстреної допомоги на вулицю Сонячна біля орендованої будівлі та початок публічного зібрання

- **Event Mention ID:** `phys_ev_01_ambulance_arrival_street` (Event ID: `event:phys_ev_01_ambulance_arrival_street`)
- **Тип події:** `physical`
- **Часовий інтервал (UTC):** `2026-11-02T09:00:00Z` — `2026-11-02T10:40:00Z` (точність: `hour`)
- **Локальний час (Europe/Kyiv):** Ранок 2 листопада 2026 року, орієнтовно 11:00–12:40 за київським часом (до появи перших повідомлень у соцмережах)
- **Локація:** `place:petropavlivska_borshchahivka_street`
- **Дійові особи (Actors):** `person:valentyna_moloda`, `person:viktor_yena`
- **Об'єкти (Objects):** `vehicle:ambulance_med_prestige`
- **Опорні докази:** `passage_kv_npu_20261102_1727`, `passage_suspilne_court_20261106`
- **Першоджерела:**
  - [https://kv.npu.gov.ua/news/shchodo-podii-u-seli-petropavlivska-borshchahivka-na-kyivshchyni](https://kv.npu.gov.ua/news/shchodo-podii-u-seli-petropavlivska-borshchahivka-na-kyivshchyni)
  - [https://suspilne.media/kyiv/1446145-suticki-v-borsanivci-sud-obirae-zapobiznij-cetvertij-pidozruvanij/](https://suspilne.media/kyiv/1446145-suticki-v-borsanivci-sud-obirae-zapobiznij-cetvertij-pidozruvanij/)
- **Просторові позиції учасників за згаданими джерелами (Participant Positions):**
  - *Зона `outside_street`:* `person:valentyna_moloda`, `person:viktor_yena`, `vehicle:ambulance_med_prestige`
  - *Зона `inside_building`:* `group:ngu_servicemembers_26`
- **Якісний рівень доказової підтримки:** `corroborated_multi_source` — *Офіційне повідомлення ГУНП про виклик приватної швидкої та судові матеріали, описані Суспільним, узгоджуються щодо учасників і первинного прибуття; час тут є інтервалом із формулювання джерел, а не окремим вимірюванням.*
- **Негативні обмеження (`cannot_link`):** `phys_ev_05_containment_and_detention`, `phys_ev_bucha_warehouse_fire_0511`

### 3.2. Епізод 2: Сутички біля огорожі та приміщення тимчасового пункту розміщення НГУ, спроби силового проникнення та пошкодження майна

- **Event Mention ID:** `phys_ev_02_building_perimeter_clash` (Event ID: `event:phys_ev_02_building_perimeter_clash`)
- **Тип події:** `physical`
- **Часовий інтервал (UTC):** `2026-11-02T11:00:00Z` — `2026-11-02T15:30:00Z` (точність: `hour`)
- **Локальний час (Europe/Kyiv):** День 2 листопада 2026 року, 13:00–17:30 за київським часом
- **Локація:** `place:petropavlivska_borshchahivka_building`
- **Дійові особи (Actors):** `group:protesters_crowd`, `person:ivan_parshonkov`
- **Об'єкти (Objects):** `structure:ngu_leased_building_fence`
- **Опорні докази:** `passage_b1befbee74f5d623e709a2c4c2b36f723c1d6bd107411b2884e94812acfa3374`, `passage_suspilne_parshonkov_20261106`
- **Першоджерела:**
  - [https://mvs.gov.ua/news/u-ministerstvi-vnutrisnix-sprav-ukrayini-vidbuvsia-brifing-shhodo-podii-na-kiyivshhini](https://mvs.gov.ua/news/u-ministerstvi-vnutrisnix-sprav-ukrayini-vidbuvsia-brifing-shhodo-podii-na-kiyivshhini)
  - [https://suspilne.media/kyiv/1446145-suticki-v-borsanivci-sud-obirae-zapobiznij-cetvertij-pidozruvanij/](https://suspilne.media/kyiv/1446145-suticki-v-borsanivci-sud-obirae-zapobiznij-cetvertij-pidozruvanij/)
- **Просторові позиції учасників за згаданими джерелами (Participant Positions):**
  - *Зона `perimeter_fence`:* `group:protesters_crowd`, `person:ivan_parshonkov`
  - *Зона `inside_building`:* `group:ngu_servicemembers_26`
- **Якісний рівень доказової підтримки:** `corroborated_multi_source` — *Брифінг МВС і командувача НГУ описує сутички біля будівлі; судові матеріали щодо Паршонкова стосуються пошкодження майна. Підстава підтримує згадку про зіткнення, але не встановлює кожну дію кожної присутньої особи.*
- **Негативні обмеження (`cannot_link`):** `phys_ev_bucha_warehouse_fire_0511`

### 3.3. Епізод 3: Прибуття підрозділів поліції та Нацгвардії на місце події, оточення території та блокування натовпом службового автобуса з військовослужбовцями

- **Event Mention ID:** `phys_ev_03_law_enforcement_arrival_bus_block` (Event ID: `event:phys_ev_03_law_enforcement_arrival_bus_block`)
- **Тип події:** `physical`
- **Часовий інтервал (UTC):** `2026-11-02T14:30:00Z` — `2026-11-02T18:00:00Z` (точність: `hour`)
- **Локальний час (Europe/Kyiv):** Друга половина дня 2 листопада 2026 року, 16:30–20:00 за київським часом
- **Локація:** `place:petropavlivska_borshchahivka_building`
- **Дійові особи (Actors):** `org:national_guard_ukraine`, `org:national_police_kyiv`, `person:valeria_ladyka`
- **Об'єкти (Objects):** `vehicle:ngu_service_bus`
- **Опорні докази:** `passage_24tv_broadcast_20261102`, `passage_hromadske_ladyka_20261106`, `passage_npu_130_persons_20261105`
- **Першоджерела:**
  - [https://hromadske.ua/kryminal/273906-sud-obyraye-zapobiznyy-zakhid-22-richniy-zintsi-iaka-brala-uchast-u-sutychkakh-u-sofiyivskiy-borshchahivtsi](https://hromadske.ua/kryminal/273906-sud-obyraye-zapobiznyy-zakhid-22-richniy-zintsi-iaka-brala-uchast-u-sutychkakh-u-sofiyivskiy-borshchahivtsi)
  - [https://kv.npu.gov.ua/news/politseiski-kyivshchyny-vstanovyly-ponad-130-osib](https://kv.npu.gov.ua/news/politseiski-kyivshchyny-vstanovyly-ponad-130-osib)
- **Просторові позиції учасників за згаданими джерелами (Participant Positions):**
  - *Зона `street_cordon`:* `org:national_police_kyiv`, `org:national_guard_ukraine`
  - *Зона `around_service_bus`:* `person:valeria_ladyka`, `group:protesters_crowd`
  - *Зона `inside_bus`:* `group:ngu_servicemembers_26`
- **Якісний рівень доказової підтримки:** `official_proceedings` — *Судова ухвала Солом'янського райсуду щодо Ладики описує обставини затримання; повідомлення Нацполіції про понад 130 осіб і відеоматеріал 24 каналу дають окремі згадки про присутність поліції та службового автобуса.*
- **Негативні обмеження (`cannot_link`):** `phys_ev_bucha_warehouse_fire_0511`

### 3.4. Епізод 4: Застосування піротехнічних засобів, запалювання фаєрів та задимлення біля будівлі під час вечірньої ескалації конфлікту

- **Event Mention ID:** `phys_ev_04_pyrotechnics_and_flares_escalation` (Event ID: `event:phys_ev_04_pyrotechnics_and_flares_escalation`)
- **Тип події:** `physical`
- **Часовий інтервал (UTC):** `2026-11-02T18:00:00Z` — `2026-11-02T20:30:00Z` (точність: `hour`)
- **Локальний час (Europe/Kyiv):** Вечір 2 листопада 2026 року, 20:00–22:30 за київським часом
- **Локація:** `place:petropavlivska_borshchahivka_building`
- **Дійові особи (Actors):** `group:protesters_crowd`
- **Об'єкти (Objects):** `item:pyrotechnic_flares`
- **Опорні докази:** `passage_borshchagovka_news_21859`, `passage_ngu_injuries_20261103`
- **Першоджерела:**
  - [https://ngu.gov.ua/shturm-kativni-pid-vybuhy-shahediv-yak-fejk-pro-40-zaruchnykiv-pereris-u-zavorushennya-v-petropavlivskij-borshhagivczi/](https://ngu.gov.ua/shturm-kativni-pid-vybuhy-shahediv-yak-fejk-pro-40-zaruchnykiv-pereris-u-zavorushennya-v-petropavlivskij-borshhagivczi/)
  - [https://t.me/BorshchagovkaNews/21859](https://t.me/BorshchagovkaNews/21859)
- **Просторові позиції учасників за згаданими джерелами (Participant Positions):**
  - *Зона `perimeter_and_street`:* `group:protesters_crowd`
  - *Зона `defensive_line`:* `org:national_police_kyiv`, `org:national_guard_ukraine`
  - *Зона `inside_building`:* `group:ngu_servicemembers_26`
- **Якісний рівень доказової підтримки:** `corroborated_multi_source` — *Відео BorshchagovkaNews, опубліковане о 18:08 UTC, показує фаєри й дим; повідомлення НГУ стосується отруєння димом чотирьох бійців, але не ідентифікує того, хто запалив фаєри.*
- **Негативні обмеження (`cannot_link`):** `phys_ev_bucha_warehouse_fire_0511`

### 3.5. Епізод 5: Локалізація конфлікту зведеними силами правоохоронців, розблокування проїзду, евакуація військовослужбовців та затримання активних правопорушників

- **Event Mention ID:** `phys_ev_05_containment_and_detention` (Event ID: `event:phys_ev_05_containment_and_detention`)
- **Тип події:** `physical`
- **Часовий інтервал (UTC):** `2026-11-02T20:30:00Z` — `2026-11-03T00:30:00Z` (точність: `approximate_window`)
- **Локальний час (Europe/Kyiv):** Ніч з 2 на 3 листопада 2026 року, 22:30–02:30 за київським часом (приблизне часове вікно)
- **Локація:** `place:petropavlivska_borshchahivka_building`
- **Дійові особи (Actors):** `org:national_guard_ukraine`, `org:national_police_kyiv`
- **Об'єкти (Objects):** `group:ngu_servicemembers_26`, `person:valentyna_moloda`
- **Опорні докази:** `passage_8c536c4bdffbe59705f39e03a13ca169104a6c2bbc88bb1178ea745cdb792e24`, `passage_b1befbee74f5d623e709a2c4c2b36f723c1d6bd107411b2884e94812acfa3374`
- **Першоджерела:**
  - [https://mvs.gov.ua/news/u-ministerstvi-vnutrisnix-sprav-ukrayini-vidbuvsia-brifing-shhodo-podii-na-kiyivshhini](https://mvs.gov.ua/news/u-ministerstvi-vnutrisnix-sprav-ukrayini-vidbuvsia-brifing-shhodo-podii-na-kiyivshhini)
  - [https://ngu.gov.ua/shturm-kativni-pid-vybuhy-shahediv-yak-fejk-pro-40-zaruchnykiv-pereris-u-zavorushennya-v-petropavlivskij-borshhagivczi/](https://ngu.gov.ua/shturm-kativni-pid-vybuhy-shahediv-yak-fejk-pro-40-zaruchnykiv-pereris-u-zavorushennya-v-petropavlivskij-borshhagivczi/)
- **Просторові позиції учасників за згаданими джерелами (Participant Positions):**
  - *Зона `building_exit_corridor`:* `group:ngu_servicemembers_26`, `org:national_guard_ukraine`
  - *Зона `street_detention_sector`:* `org:national_police_kyiv`, `person:valentyna_moloda`
- **Якісний рівень доказової підтримки:** `official_proceedings` — *Пресреліз НГУ та брифінг МВС описують локалізацію конфлікту й евакуацію; судові рішення стосуються затримань. Часова межа залишається широким нічним інтервалом.*
- **Негативні обмеження (`cannot_link`):** `phys_ev_01_ambulance_arrival_street`, `phys_ev_bucha_warehouse_fire_0511`

---

## 4. Комунікаційний шар подій (`timelines.communication`)

Комунікаційні згадки фіксують точний час оприлюднення офіційних релізів або публікацій у соцмережах і ніколи не змішуються з часом фізичних дій.

| № | Ідентифікатор | Час публікації (UTC) | Джерело / Автор | Зміст повідомлення |
|---|---|---|---|---|
| 1 | `comm_ev_01_npu_kyiv_initial_release` | `2026-11-02T15:27:00Z` | `org:national_police_kyiv` | Поліція Київщини оприлюднила перше офіційне спростування фейку про «заручників» та повідомила про виклик швидкої допомоги |
| 2 | `comm_ev_02_telegram_borshchagovka_news_flares` | `2026-11-02T18:08:44Z` | `channel:borshchagovka_news` | Публікація у Telegram-каналі BorshchagovkaNews відеозапису вечірнього задимлення та фаєрів біля будівлі |
| 3 | `comm_ev_03_dbr_criminal_proceeding_announcement` | `2026-11-03T11:00:00Z` | `org:state_bureau_investigation` | Державне бюро розслідувань повідомило про відкриття кримінального провадження за ч. 5 ст. 426-1 КК України |
| 4 | `comm_ev_04_mvs_ngu_official_briefing` | `2026-11-04T10:35:00Z` | `org:ministry_internal_affairs`, `org:national_guard_ukraine` | Керівництво МВС та командувач НГУ провели брифінг, на якому повідомили про 26 осіб у приміщенні та оренду будівлі |
| 5 | `comm_ev_05_kyiv_ova_bucha_warehouse_fire_post` | `2026-11-04T22:03:00Z` | `org:kyiv_regional_military_administration` | Київська ОВА повідомила про ворожу дронову атаку та пожежу складського приміщення в Бучанському районі |

---

## 5. Формулювання негативних обмежень та ізоляція пожежі у Бучанському районі

### 5.1. Фактична делімітація інцидентів
У процесі інформаційної ескалації проросійські Telegram-канали та TikTok-акаунти поширили відеоматеріали масштабної нічної пожежі з текстовим написом «Софіївська Борщагівка, 05.11.26», супроводжуючи їх твердженнями, що будівлю тимчасового розміщення військовослужбовців у Петропавлівській Борщагівці нібито «спалили, щоб замести сліди».

**Фактична розбіжність:**
1. **Об'єкт 1 (Фізичний конфлікт 2 листопада):** с. Петропавлівська Борщагівка, вул. Сонячна. Орендована приватна триповерхова будівля. Були застосовані димові шашки та фаєри (`phys_ev_04_pyrotechnics_and_flares_escalation`), що спричинило задимлення та отруєння чадним газом 4 бійців НГУ. Проте сама будівля **не згоріла і не була знищена пожежею**.
2. **Об'єкт 2 (Складська пожежа 4–5 листопада):** Бучанський район (Софіївська Борщагівка). Складське приміщення, загоряння якого сталося внаслідок ворожої атаки ударними БПЛА Shahed у ніч на 5 листопада (зафіксовано у повідомленнях начальника Київської ОВА о 00:03 та Борщагівської сільради о 00:17 05.11).

### 5.2. Негативні обмеження (`cannot_link`)
Щоб зберегти задані аналітиком межі інциденту, для фізичних згадок сформульовано негативні обмеження:

```json
[
  {
    "event_mention_id": "phys_ev_01_ambulance_arrival_street",
    "target_event_mention_id": "phys_ev_bucha_warehouse_fire_0511",
    "relation": "cannot_link",
    "status": "target_not_in_input"
  },
  {
    "event_mention_id": "phys_ev_02_building_perimeter_clash",
    "target_event_mention_id": "phys_ev_bucha_warehouse_fire_0511",
    "relation": "cannot_link",
    "status": "target_not_in_input"
  },
  {
    "event_mention_id": "phys_ev_03_law_enforcement_arrival_bus_block",
    "target_event_mention_id": "phys_ev_bucha_warehouse_fire_0511",
    "relation": "cannot_link",
    "status": "target_not_in_input"
  },
  {
    "event_mention_id": "phys_ev_04_pyrotechnics_and_flares_escalation",
    "target_event_mention_id": "phys_ev_bucha_warehouse_fire_0511",
    "relation": "cannot_link",
    "status": "target_not_in_input"
  },
  {
    "event_mention_id": "phys_ev_05_containment_and_detention",
    "target_event_mention_id": "phys_ev_bucha_warehouse_fire_0511",
    "relation": "cannot_link",
    "status": "target_not_in_input"
  }
]
```

Усі 5 відношень мають статус `target_not_in_input`, що формально виносить сторонній інцидент за межі корпусу фізичних подій Петропавлівської Борщагівки.

---

## 6. Часові відношення та частковий порядок (Temporal Relations)

Усього побудовано **20 парних часових відношень** між подіями.

| Подія А | Подія Б | Відношення | Базис | Каузальність |
|---|---|---|---|---|
| `event:comm_ev_01_npu_kyiv_initial_release` | `event:comm_ev_02_telegram_borshchagovka_news_flares` | `before` | `non_overlapping_time_intervals` | `False` |
| `event:comm_ev_01_npu_kyiv_initial_release` | `event:comm_ev_03_dbr_criminal_proceeding_announcement` | `before` | `non_overlapping_time_intervals` | `False` |
| `event:comm_ev_01_npu_kyiv_initial_release` | `event:comm_ev_04_mvs_ngu_official_briefing` | `before` | `non_overlapping_time_intervals` | `False` |
| `event:comm_ev_01_npu_kyiv_initial_release` | `event:comm_ev_05_kyiv_ova_bucha_warehouse_fire_post` | `before` | `non_overlapping_time_intervals` | `False` |
| `event:comm_ev_02_telegram_borshchagovka_news_flares` | `event:comm_ev_03_dbr_criminal_proceeding_announcement` | `before` | `non_overlapping_time_intervals` | `False` |
| `event:comm_ev_02_telegram_borshchagovka_news_flares` | `event:comm_ev_04_mvs_ngu_official_briefing` | `before` | `non_overlapping_time_intervals` | `False` |
| `event:comm_ev_02_telegram_borshchagovka_news_flares` | `event:comm_ev_05_kyiv_ova_bucha_warehouse_fire_post` | `before` | `non_overlapping_time_intervals` | `False` |
| `event:comm_ev_03_dbr_criminal_proceeding_announcement` | `event:comm_ev_04_mvs_ngu_official_briefing` | `before` | `non_overlapping_time_intervals` | `False` |
| `event:comm_ev_03_dbr_criminal_proceeding_announcement` | `event:comm_ev_05_kyiv_ova_bucha_warehouse_fire_post` | `before` | `non_overlapping_time_intervals` | `False` |
| `event:comm_ev_04_mvs_ngu_official_briefing` | `event:comm_ev_05_kyiv_ova_bucha_warehouse_fire_post` | `before` | `non_overlapping_time_intervals` | `False` |
| ... | ... | *(ще 10 відношень)* | ... | ... |

---

## 7. Обмеження та методологічні застереження

- This is an analyst-curated reconstruction from the companion source-event mention list; the script organizes supplied mentions and does not discover events in source material.
- Evidence tiers are qualitative analyst judgments grounded in each listed basis; they are not calibrated probabilities or truth scores.
- This deterministic module organizes supplied event mentions; it does not extract events from raw text.
- Exact entity identifiers, not names or fuzzy similarity, are required for candidate matching.
- No causal relation is inferred from temporal order.

---

## 8. Верифікаційний висновок

- [x] Структуровано **5 фізичних згадок, кураторськи відібраних аналітиком із повідомлень джерел**; скрипт не виконує автоматичного виявлення подій.
- [x] Часові інтервали пройшли перевірку формату; вони передають нормалізовані межі, наведені у джерелах, і можуть перетинатися.
- [x] Для фізичних згадок наведено якісний рівень доказової підтримки з описом його підстави; це не калібровані ймовірності.
- [x] Забезпечено математичну незалежність фізичного часу від часу публікацій.
- [x] Сформульовано 5 явних обмежень (`cannot_link`), що зберігають складську пожежу в Бучанському районі як окрему кураторську згадку.
- [x] Результуючий JSON успішно пройшов валідацію за схемою `schemas/event_reconstruction.schema.json` v1.0.
