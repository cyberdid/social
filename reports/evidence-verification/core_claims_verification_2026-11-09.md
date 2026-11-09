# Доказова верифікація ядерних тверджень: Петропавлівська Борщагівка
## Звіт M1, схема результатів 2.2

> **Дата формування:** 2026-11-09T13:30:00Z  
> **Метод:** локальний BM25-пошук і детерміновані правила зіставлення твердження з пасажем  
> **Межа автономності:** система вибирає пасажі лише в наданому курованому корпусі; зовнішній пошук джерел не виконується  
> **Тверджень:** 25 | **Підтримано в межах scope:** 19 | **Спростовано в межах scope:** 0 | **Недостатньо доказів:** 6 | **Конфліктні:** 0  
> **Прийняті правилами оцінки пасажів:** 36  

### Як читати статуси

`supports` і `contradicts` описують відношення між конкретним твердженням та процитованим пасажем, а не самостійно встановлену істину про подію. Офіційна заява зберігається як позиція установи. Для тверджень із `scope.type = physical_fact` одна інституційна заява не дає статусу `supported_within_scope` або `refuted_within_scope`: без прямого спостереження, первинного фізичного запису, форензичного доказу чи геолокованого медіа статус лишається `insufficient_evidence`.

### Обмеження цього запуску

- Корпус пасажів і список пріоритетних тверджень сформовані дослідником; BM25 не перевіряє весь інтернет і не доводить повноту джерел.
- Правила відношень є детермінованими евристиками, не каліброваною ймовірнісною моделлю. Числова оцінка правила не є статистичною ймовірністю.
- `independent_root_id` — задекларована мітка лінії походження. Її незалежність зовнішнім аудитом не встановлена; агрегація рахує різні мітки, а не доведені незалежні джерела.
- `insufficient_evidence` означає, що наданий корпус не обґрунтовує певніший висновок. Це не підтвердження протилежного.
- Зміщення веде до локального артефакту; він може бути похідним транскриптом, а не оригінальною вебсторінкою.

---

## 1. Зведена матриця

| ID | Scope | Твердження | Статус | Позиція установи | Докази |
|---|---|---|---|---|---|
| `claim_core_01_hostages_40` | `physical_fact` | У приміщенні у Петропавлівській Борщагівці незаконно утримували 40 осіб | `insufficient_evidence` | `officially_disputed` | `psg_ngu_hostages_40_refuted` |
| `claim_core_02_killed_citizen` | `physical_fact` | Під час подій у Петропавлівській Борщагівці загинув громадянин | `insufficient_evidence` | `officially_disputed` | `psg_ngu_hostages_40_refuted` |
| `claim_core_03_broken_spine` | `medical_claim` | В одного з військовослужбовців у будівлі було зафіксовано перелом хребта | `insufficient_evidence` | `not_recorded` | `psg_ngu_spine_refuted` |
| `claim_core_04_ngu_four_injured` | `official_statement` | Чотири військовослужбовці Національної гвардії України отримали травми під час інциденту | `insufficient_evidence` | `not_recorded` | `psg_dbr_art_426_1`, `psg_hromadske_ladyka_art_114_1`, `psg_mvs_ngu_unit_3121`, `psg_ngu_4_injured`, `psg_suspilne_parshonkov_hammer` |
| `claim_core_05_ngu_walked_independently` | `official_statement` | Травмовані військовослужбовці НГУ самостійно дійшли до карети швидкої допомоги | `supported_within_scope` | `not_recorded` | `psg_ngu_spine_refuted` |
| `claim_core_06_building_26_persons` | `official_statement` | За заявою МВС, загалом у приміщенні перебували 26 осіб | `supported_within_scope` | `not_recorded` | `psg_mvs_26_occupants` |
| `claim_core_07_building_4_szch` | `official_statement` | Серед осіб у приміщенні 4 військових самовільно залишили частину | `supported_within_scope` | `not_recorded` | `psg_mvs_4_szch`, `psg_ngu_4_injured`, `psg_ngu_walked_independently` |
| `claim_core_08_building_ngu_lease` | `official_statement` | Будівля перебувала в офіційній оренді Національної гвардії України як тимчасовий пункт | `supported_within_scope` | `not_recorded` | `psg_mvs_ngu_lease` |
| `claim_core_09_npu_130_identified` | `official_statement` | Поліція разом із СБУ встановили 130 осіб, які можуть бути причетними до заворушень | `supported_within_scope` | `not_recorded` | `psg_npu_27_active`, `psg_suspilne_130_identified` |
| `claim_core_10_npu_27_active` | `official_statement` | За оцінкою поліції, 27 встановлених осіб брали активну участь у протиправних діях | `supported_within_scope` | `not_recorded` | `psg_npu_27_active` |
| `claim_core_11_court_ladyka_custody` | `court_reporting` | Солом'янський районний суд застосував до Валерії Ладики тримання під вартою на 59 днів | `supported_within_scope` | `not_recorded` | `psg_suspilne_ladyka_59_days` |
| `claim_core_12_court_ladyka_bail` | `court_reporting` | Суд визначив для Валерії Ладики альтернативу застави у розмірі 66560 гривень | `supported_within_scope` | `not_recorded` | `psg_hromadske_ladyka_bail_66560` |
| `claim_core_13_court_ladyka_art_114_1` | `court_reporting` | Валерії Ладиці повідомлено про підозру за ч. 1 ст. 114-1 КК України | `supported_within_scope` | `not_recorded` | `psg_hromadske_ladyka_art_114_1` |
| `claim_core_14_court_moloda_no_bail` | `court_reporting` | Суд обрав Валентині Молодій запобіжний захід у вигляді тримання під вартою без застави | `supported_within_scope` | `not_recorded` | `psg_suspilne_moloda_custody` |
| `claim_core_15_court_kireyeva_no_bail` | `court_reporting` | Суд обрав Тетяні Кірєєвій запобіжний захід у вигляді тримання під вартою без застави | `supported_within_scope` | `not_recorded` | `psg_suspilne_moloda_custody` |
| `claim_core_16_court_yena_custody_60` | `court_reporting` | Солом'янський районний суд Києва обрав Віктору Єні тримання під вартою на 60 днів без застави | `supported_within_scope` | `not_recorded` | `psg_suspilne_yena_custody` |
| `claim_core_17_parshonkov_hammer_suspicion` | `court_reporting` | Іван Паршонков придбав молот та завдавав ним ударів по службовому автомобілю з військовослужбовцями | `supported_within_scope` | `not_recorded` | `psg_suspilne_parshonkov_hammer` |
| `claim_core_18_dbr_proceedings_426_1` | `official_statement` | ДБР відкрило кримінальне провадження за ч. 5 ст. 426-1 КК України за фактом подій | `supported_within_scope` | `not_recorded` | `psg_dbr_art_426_1` |
| `claim_core_19_ombudsman_inquiry` | `official_statement` | Уповноважений ВРУ з прав людини направив запити до правоохоронних органів щодо ситуації | `supported_within_scope` | `not_recorded` | `psg_ombudsman_inquiries` |
| `claim_core_20_mvs_service_investigation` | `official_statement` | МВС України розпочало службове розслідування за фактом подій на Київщині | `supported_within_scope` | `not_recorded` | `psg_mvs_inquiry_ordered` |
| `claim_core_21_fire_padla_tck_prediction` | `social_media_mention` | Канал padla_tck поширив твердження, що будівля може спалахнути для знищення доказів | `supported_within_scope` | `not_recorded` | `psg_padla_tck_fire_prediction` |
| `claim_core_22_fire_bucha_warehouse` | `reported_statement` | У Бучанському районі після ворожої атаки сталося займання на території складу, дані про постраждалих уточнювали | `supported_within_scope` | `not_recorded` | `psg_bucha_warehouse_fire` |
| `claim_core_23_fire_video_location_mismatch` | `media_verification` | TikTok-відео з написом «Софіївська Борщагівка» зображує пожежу окремого складу, а не будівлі НГУ | `insufficient_evidence` | `not_recorded` | `psg_tiktok_fire_mismatch` |
| `claim_core_24_tck_presence_at_scene` | `institutional_presence` | Співробітники ТЦК та СП здійснювали блокування або перебували в будівлі під час сутичок | `insufficient_evidence` | `not_recorded` | `psg_dbr_art_426_1`, `psg_hromadske_ladyka_art_114_1`, `psg_mvs_ngu_unit_3121`, `psg_padla_tck_fire_prediction`, `psg_suspilne_parshonkov_hammer` |
| `claim_core_25_police_arrival_ambulance_call` | `official_statement` | Поліція прибула на місце події за викликом працівників приватної швидкої допомоги | `supported_within_scope` | `not_recorded` | `psg_ngu_police_arrival_ambulance_call` |

---

## 2. Пасажі й пояснення по кожному твердженню

### claim_core_01_hostages_40 — `insufficient_evidence`

**Твердження:** У приміщенні у Петропавлівській Борщагівці незаконно утримували 40 осіб  
**Scope:** `{"incident": "petropavlivska-borshchahivka", "topic": "hostages_count", "type": "physical_fact"}`  
**Позиція установи:** `officially_disputed`  
**Пояснення агрегатора:** The supplied evidence does not meet the declared source-lineage threshold; absence of evidence is not refutation.  
**Пошук:** 6 кандидатів у наданому корпусі; 1 пройшли правила оцінювання.  

- **contradicts**; basis `institutional_statement`; source `src_ngu_press`; declared lineage `root_ngu_official` (independence `candidate`).
  - URI: https://ngu.gov.ua/shturm-kativni-pid-vybuhy-shahediv-yak-fejk-pro-40-zaruchnykiv-pereris-u-zavorushennya-v-petropavlivskij-borshhagivczi/
  - Artifact: `artifact_sw_20261108T080001_5`; artifact offset [1581:1611], passage offset [37:67].
  - Цитата: > 40 незаконно утримуваних людей
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_sw_20261108T080001_5, exact offset span: [37:67].; Passage contains a denial cue in the same substantive topic (cues: спростувала).; The passage records a denial; for physical facts this is an institutional position, not independent physical refutation.; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.

### claim_core_02_killed_citizen — `insufficient_evidence`

**Твердження:** Під час подій у Петропавлівській Борщагівці загинув громадянин  
**Scope:** `{"incident": "petropavlivska-borshchahivka", "topic": "fatalities", "type": "physical_fact"}`  
**Позиція установи:** `officially_disputed`  
**Пояснення агрегатора:** The supplied evidence does not meet the declared source-lineage threshold; absence of evidence is not refutation.  
**Пошук:** 6 кандидатів у наданому корпусі; 1 пройшли правила оцінювання.  

- **contradicts**; basis `institutional_statement`; source `src_ngu_press`; declared lineage `root_ngu_official` (independence `candidate`).
  - URI: https://ngu.gov.ua/shturm-kativni-pid-vybuhy-shahediv-yak-fejk-pro-40-zaruchnykiv-pereris-u-zavorushennya-v-petropavlivskij-borshhagivczi/
  - Artifact: `artifact_sw_20261108T080001_5`; artifact offset [1544:1623], passage offset [0:79].
  - Цитата: > Поліція спростувала повідомлення про 40 незаконно утримуваних людей і загиблого
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_sw_20261108T080001_5, exact offset span: [0:79].; Passage contains a denial cue in the same substantive topic (cues: спростувала).; The passage records a denial; for physical facts this is an institutional position, not independent physical refutation.; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.

### claim_core_03_broken_spine — `insufficient_evidence`

**Твердження:** В одного з військовослужбовців у будівлі було зафіксовано перелом хребта  
**Scope:** `{"incident": "petropavlivska-borshchahivka", "topic": "severe_injuries", "type": "medical_claim"}`  
**Позиція установи:** `not_recorded`  
**Пояснення агрегатора:** The supplied evidence does not meet the declared source-lineage threshold; absence of evidence is not refutation.  
**Пошук:** 3 кандидатів у наданому корпусі; 1 пройшли правила оцінювання.  

- **rebuts**; basis `institutional_statement`; source `src_ngu_press`; declared lineage `root_ngu_official` (independence `candidate`).
  - URI: https://ngu.gov.ua/shturm-kativni-pid-vybuhy-shahediv-yak-fejk-pro-40-zaruchnykiv-pereris-u-zavorushennya-v-petropavlivskij-borshhagivczi/
  - Artifact: `artifact_sw_20261108T080001_5`; artifact offset [5644:5723], passage offset [0:79].
  - Цитата: > Руслан Музичук спростував розповіді про лежачого чоловіка з переламаним хребтом
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_sw_20261108T080001_5, exact offset span: [0:79].; Spokesperson verbally refuted public reports; however verbal statement is not clinical forensic trauma documentation.; Spokesperson denial addresses social media allegation but is not clinical medical verification.; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.

### claim_core_04_ngu_four_injured — `insufficient_evidence`

**Твердження:** Чотири військовослужбовці Національної гвардії України отримали травми під час інциденту  
**Scope:** `{"incident": "petropavlivska-borshchahivka", "topic": "ngu_injuries", "type": "official_statement"}`  
**Позиція установи:** `not_recorded`  
**Пояснення агрегатора:** The supplied evidence does not meet the declared source-lineage threshold; absence of evidence is not refutation.  
**Пошук:** 5 кандидатів у наданому корпусі; 5 пройшли правила оцінювання.  

- **contextualizes**; basis `institutional_statement`; source `src_ngu_press`; declared lineage `root_ngu_official` (independence `candidate`).
  - URI: https://ngu.gov.ua/shturm-kativni-pid-vybuhy-shahediv-yak-fejk-pro-40-zaruchnykiv-pereris-u-zavorushennya-v-petropavlivskij-borshhagivczi/
  - Artifact: `artifact_sw_20261108T080001_5`; artifact offset [5489:5536], passage offset [9:56].
  - Цитата: > четверо військовослужбовців справді мали травми
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_sw_20261108T080001_5, exact offset span: [9:56].; Passage confirms servicemembers had injuries and were hospitalized, but does not verify that injuries were sustained during the incident (circumstances under investigation).; Official acknowledgment of injuries hedges event-specific causality.; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.
- **contextualizes**; basis `institutional_statement`; source `src_mvs_briefing`; declared lineage `root_mvs_official` (independence `candidate`).
  - URI: https://mvs.gov.ua/news/u-ministerstvi-vnutrisnix-sprav-ukrayini-vidbuvsia-brifing-shhodo-podii-na-kiyivshhini
  - Artifact: `artifact_sw_20261108T080001_4`; artifact offset [3304:3332], passage offset [11:39].
  - Цитата: > Національної гвардії України
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_sw_20261108T080001_4, exact offset span: [11:39].; Passage confirms servicemembers had injuries and were hospitalized, but does not verify that injuries were sustained during the incident (circumstances under investigation).; Official acknowledgment of injuries hedges event-specific causality.; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.
- **contextualizes**; basis `secondary_reporting`; source `src_hromadske_ladyka`; declared lineage `root_hromadske_journalism` (independence `candidate`).
  - URI: https://hromadske.ua/kryminal/273906-sud-obyraye-zapobiznyy-zakhid-22-richniy-zintsi-iaka-brala-uchast-u-sutychkakh-u-sofiyivskiy-borshchahivtsi
  - Artifact: `artifact_sw_20261108T080001_1`; artifact offset [710:813], passage offset [75:178].
  - Цитата: > України та інших військових формувань в особливий період — ч. 1 ст. 114-1 Кримінального кодексу України
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_sw_20261108T080001_1, exact offset span: [75:178].; Passage confirms servicemembers had injuries and were hospitalized, but does not verify that injuries were sustained during the incident (circumstances under investigation).; Official acknowledgment of injuries hedges event-specific causality.; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.
- **contextualizes**; basis `secondary_reporting`; source `src_suspilne_court`; declared lineage `root_suspilne_court_journalism` (independence `candidate`).
  - URI: https://suspilne.media/kyiv/1446145-suticki-v-borsanivci-sud-obirae-zapobiznij-cetvertij-pidozruvanij/
  - Artifact: `artifact_sw_20261108T080001_7`; artifact offset [3372:3390], passage offset [313:331].
  - Цитата: > військовослужбовці
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_sw_20261108T080001_7, exact offset span: [313:331].; Passage confirms servicemembers had injuries and were hospitalized, but does not verify that injuries were sustained during the incident (circumstances under investigation).; Official acknowledgment of injuries hedges event-specific causality.; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.
- **contextualizes**; basis `institutional_statement`; source `src_dbr_proceedings`; declared lineage `root_dbr_official` (independence `candidate`).
  - URI: https://dbr.gov.ua/news/dbr-rozpochalo-kriminalne-provadzhennya-za-faktom-podij-u-petropavlivskij-borshhagivci-na-kiivshhini
  - Artifact: `artifact_reports_source-watch_20261108_official-web-check_md`; artifact offset [1170:1177], passage offset [121:128].
  - Цитата: > України
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_reports_source-watch_20261108_official-web-check_md, exact offset span: [121:128].; Passage confirms servicemembers had injuries and were hospitalized, but does not verify that injuries were sustained during the incident (circumstances under investigation).; Official acknowledgment of injuries hedges event-specific causality.; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.

### claim_core_05_ngu_walked_independently — `supported_within_scope`

**Твердження:** Травмовані військовослужбовці НГУ самостійно дійшли до карети швидкої допомоги  
**Scope:** `{"incident": "petropavlivska-borshchahivka", "topic": "medical_evacuation", "type": "official_statement"}`  
**Позиція установи:** `not_recorded`  
**Пояснення агрегатора:** Accepted, scope-matched support from 1 declared source-lineage root(s) meets threshold 1; no contradiction root was accepted.  
**Пошук:** 3 кандидатів у наданому корпусі; 1 пройшли правила оцінювання.  

- **supports**; basis `institutional_statement`; source `src_ngu_press`; declared lineage `root_ngu_official` (independence `candidate`).
  - URI: https://ngu.gov.ua/shturm-kativni-pid-vybuhy-shahediv-yak-fejk-pro-40-zaruchnykiv-pereris-u-zavorushennya-v-petropavlivskij-borshhagivczi/
  - Artifact: `artifact_sw_20261108T080001_5`; artifact offset [5742:5802], passage offset [98:158].
  - Цитата: > всі четверо самостійно дійшли до автомобіля швидкої допомоги
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_sw_20261108T080001_5, exact offset span: [98:158].; Affirmative factual and numerical alignment (4 matching root concepts: допомог, дійш, самостійн).; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.

### claim_core_06_building_26_persons — `supported_within_scope`

**Твердження:** За заявою МВС, загалом у приміщенні перебували 26 осіб  
**Scope:** `{"incident": "petropavlivska-borshchahivka", "topic": "building_occupants", "type": "official_statement"}`  
**Позиція установи:** `not_recorded`  
**Пояснення агрегатора:** Accepted, scope-matched support from 1 declared source-lineage root(s) meets threshold 1; no contradiction root was accepted.  
**Пошук:** 2 кандидатів у наданому корпусі; 1 пройшли правила оцінювання.  

- **supports**; basis `institutional_statement`; source `src_mvs_briefing`; declared lineage `root_mvs_official` (independence `candidate`).
  - URI: https://mvs.gov.ua/news/u-ministerstvi-vnutrisnix-sprav-ukrayini-vidbuvsia-brifing-shhodo-podii-na-kiyivshhini
  - Artifact: `artifact_sw_20261108T080001_4`; artifact offset [3526:3565], passage offset [0:39].
  - Цитата: > Загалом у приміщенні перебували 26 осіб
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_sw_20261108T080001_4, exact offset span: [0:39].; Affirmative factual and numerical alignment (4 matching root concepts: загал, осіб, перебува).; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.

### claim_core_07_building_4_szch — `supported_within_scope`

**Твердження:** Серед осіб у приміщенні 4 військових самовільно залишили частину  
**Scope:** `{"incident": "petropavlivska-borshchahivka", "topic": "szch_count", "type": "official_statement"}`  
**Позиція установи:** `not_recorded`  
**Пояснення агрегатора:** Accepted, scope-matched support from 2 declared source-lineage root(s) meets threshold 1; no contradiction root was accepted.  
**Пошук:** 6 кандидатів у наданому корпусі; 3 пройшли правила оцінювання.  

- **supports**; basis `institutional_statement`; source `src_mvs_briefing`; declared lineage `root_mvs_official` (independence `candidate`).
  - URI: https://mvs.gov.ua/news/u-ministerstvi-vnutrisnix-sprav-ukrayini-vidbuvsia-brifing-shhodo-podii-na-kiyivshhini
  - Artifact: `artifact_sw_20261108T080001_4`; artifact offset [3591:3673], passage offset [24:106].
  - Цитата: > четверо з них були військовослужбовцями, які самовільно залишили військову частину
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_sw_20261108T080001_4, exact offset span: [24:106].; Affirmative factual and numerical alignment (4 matching root concepts: військов, залиши, самовільн).; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.
- **supports**; basis `institutional_statement`; source `src_ngu_press`; declared lineage `root_ngu_official` (independence `candidate`).
  - URI: https://ngu.gov.ua/shturm-kativni-pid-vybuhy-shahediv-yak-fejk-pro-40-zaruchnykiv-pereris-u-zavorushennya-v-petropavlivskij-borshhagivczi/
  - Artifact: `artifact_sw_20261108T080001_5`; artifact offset [5489:5556], passage offset [9:76].
  - Цитата: > четверо військовослужбовців справді мали травми. Цього в «Азові» не
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_sw_20261108T080001_5, exact offset span: [9:76].; Affirmative factual and numerical alignment (0 matching root concepts: ).; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.
- **supports**; basis `institutional_statement`; source `src_ngu_press`; declared lineage `root_ngu_official` (independence `candidate`).
  - URI: https://ngu.gov.ua/shturm-kativni-pid-vybuhy-shahediv-yak-fejk-pro-40-zaruchnykiv-pereris-u-zavorushennya-v-petropavlivskij-borshhagivczi/
  - Artifact: `artifact_sw_20261108T080001_5`; artifact offset [5746:5827], passage offset [4:85].
  - Цитата: > четверо самостійно дійшли до автомобіля швидкої допомоги. Чи застосовували до них
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_sw_20261108T080001_5, exact offset span: [4:85].; Affirmative factual and numerical alignment (0 matching root concepts: ).; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.

### claim_core_08_building_ngu_lease — `supported_within_scope`

**Твердження:** Будівля перебувала в офіційній оренді Національної гвардії України як тимчасовий пункт  
**Scope:** `{"incident": "petropavlivska-borshchahivka", "topic": "building_legal_status", "type": "official_statement"}`  
**Позиція установи:** `not_recorded`  
**Пояснення агрегатора:** Accepted, scope-matched support from 1 declared source-lineage root(s) meets threshold 1; no contradiction root was accepted.  
**Пошук:** 5 кандидатів у наданому корпусі; 1 пройшли правила оцінювання.  

- **supports**; basis `institutional_statement`; source `src_mvs_briefing`; declared lineage `root_mvs_official` (independence `candidate`).
  - URI: https://mvs.gov.ua/news/u-ministerstvi-vnutrisnix-sprav-ukrayini-vidbuvsia-brifing-shhodo-podii-na-kiyivshhini
  - Artifact: `artifact_sw_20261108T080001_4`; artifact offset [3378:3504], passage offset [0:126].
  - Цитата: > будівля, навколо якої виник конфлікт, перебувала в офіційній оренді Нацгвардії та використовувалася для тимчасового розміщення
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_sw_20261108T080001_4, exact offset span: [0:126].; Affirmative factual and numerical alignment (5 matching root concepts: будівля, оренд, офіційн).; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.

### claim_core_09_npu_130_identified — `supported_within_scope`

**Твердження:** Поліція разом із СБУ встановили 130 осіб, які можуть бути причетними до заворушень  
**Scope:** `{"incident": "petropavlivska-borshchahivka", "topic": "identified_participants", "type": "official_statement"}`  
**Позиція установи:** `not_recorded`  
**Пояснення агрегатора:** Accepted, scope-matched support from 2 declared source-lineage root(s) meets threshold 1; no contradiction root was accepted.  
**Пошук:** 5 кандидатів у наданому корпусі; 2 пройшли правила оцінювання.  

- **supports**; basis `secondary_reporting`; source `src_suspilne_court`; declared lineage `root_suspilne_court_journalism` (independence `candidate`).
  - URI: https://suspilne.media/kyiv/1446145-suticki-v-borsanivci-sud-obirae-zapobiznij-cetvertij-pidozruvanij/
  - Artifact: `artifact_sw_20261108T080001_7`; artifact offset [6936:6998], passage offset [40:102].
  - Цитата: > встановили 130 осіб , які можуть бути причетними до заворушень
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_sw_20261108T080001_7, exact offset span: [40:102].; Affirmative factual and numerical alignment (7 matching root concepts: 130, бут, встанови).; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.
- **supports**; basis `institutional_statement`; source `src_npu_130_persons`; declared lineage `root_npu_national_official` (independence `candidate`).
  - URI: https://npu.gov.ua/news/politseiski-natsionalnoi-politsii-ukrainy-razom-z-sbu-vzhe-vstanovyly-130-osib-iaki-mozhut-buty-prychetnymy-do-zavorushen-na-petropavlivskii-borshhagivtsi
  - Artifact: `artifact_reports_figures-and-proceedings-2026-11-06_md`; artifact offset [8463:8534], passage offset [0:71].
  - Цитата: > Поліція повідомила, що встановила 130 людей, які можуть бути причетними
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_reports_figures-and-proceedings-2026-11-06_md, exact offset span: [0:71].; Affirmative factual and numerical alignment (6 matching root concepts: 130, бут, встанови).; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.

### claim_core_10_npu_27_active — `supported_within_scope`

**Твердження:** За оцінкою поліції, 27 встановлених осіб брали активну участь у протиправних діях  
**Scope:** `{"incident": "petropavlivska-borshchahivka", "topic": "active_participants", "type": "official_statement"}`  
**Позиція установи:** `not_recorded`  
**Пояснення агрегатора:** Accepted, scope-matched support from 1 declared source-lineage root(s) meets threshold 1; no contradiction root was accepted.  
**Пошук:** 5 кандидатів у наданому корпусі; 1 пройшли правила оцінювання.  

- **supports**; basis `institutional_statement`; source `src_npu_130_persons`; declared lineage `root_npu_national_official` (independence `candidate`).
  - URI: https://npu.gov.ua/news/politseiski-natsionalnoi-politsii-ukrainy-razom-z-sbu-vzhe-vstanovyly-130-osib-iaki-mozhut-buty-prychetnymy-do-zavorushen-na-petropavlivskii-borshhagivtsi
  - Artifact: `artifact_reports_figures-and-proceedings-2026-11-06_md`; artifact offset [8463:8610], passage offset [0:147].
  - Цитата: > Поліція повідомила, що встановила 130 людей, які можуть бути причетними; серед них 27, за оцінкою поліції, брали активну участь у протиправних діях
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_reports_figures-and-proceedings-2026-11-06_md, exact offset span: [0:147].; Affirmative factual and numerical alignment (7 matching root concepts: активн, бра, діях).; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.

### claim_core_11_court_ladyka_custody — `supported_within_scope`

**Твердження:** Солом'янський районний суд застосував до Валерії Ладики тримання під вартою на 59 днів  
**Scope:** `{"incident": "petropavlivska-borshchahivka", "topic": "preventive_measure_ladyka", "type": "court_reporting"}`  
**Позиція установи:** `not_recorded`  
**Пояснення агрегатора:** Accepted, scope-matched support from 1 declared source-lineage root(s) meets threshold 1; no contradiction root was accepted.  
**Пошук:** 2 кандидатів у наданому корпусі; 1 пройшли правила оцінювання.  

- **supports**; basis `secondary_reporting`; source `src_suspilne_court`; declared lineage `root_suspilne_court_journalism` (independence `candidate`).
  - URI: https://suspilne.media/kyiv/1446145-suticki-v-borsanivci-sud-obirae-zapobiznij-cetvertij-pidozruvanij/
  - Artifact: `artifact_sw_20261108T080001_7`; artifact offset [2720:2773], passage offset [0:53].
  - Цитата: > застосувати для Ладиги тримання під вартою на 59 днів
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_sw_20261108T080001_7, exact offset span: [0:53].; Affirmative factual and numerical alignment (3 matching root concepts: вартою, днів, триман).; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.

### claim_core_12_court_ladyka_bail — `supported_within_scope`

**Твердження:** Суд визначив для Валерії Ладики альтернативу застави у розмірі 66560 гривень  
**Scope:** `{"incident": "petropavlivska-borshchahivka", "topic": "bail_amount_ladyka", "type": "court_reporting"}`  
**Позиція установи:** `not_recorded`  
**Пояснення агрегатора:** Accepted, scope-matched support from 1 declared source-lineage root(s) meets threshold 1; no contradiction root was accepted.  
**Пошук:** 2 кандидатів у наданому корпусі; 1 пройшли правила оцінювання.  

- **supports**; basis `secondary_reporting`; source `src_hromadske_ladyka`; declared lineage `root_hromadske_journalism` (independence `candidate`).
  - URI: https://hromadske.ua/kryminal/273906-sud-obyraye-zapobiznyy-zakhid-22-richniy-zintsi-iaka-brala-uchast-u-sutychkakh-u-sofiyivskiy-borshchahivtsi
  - Artifact: `artifact_sw_20261108T080001_1`; artifact offset [550:633], passage offset [0:83].
  - Цитата: > Суд відправив жінку під варту з можливістю внесення застави розміром 66 560 гривень
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_sw_20261108T080001_1, exact offset span: [0:83].; Affirmative factual and numerical alignment (4 matching root concepts: гривень, застав, розмір).; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.

### claim_core_13_court_ladyka_art_114_1 — `supported_within_scope`

**Твердження:** Валерії Ладиці повідомлено про підозру за ч. 1 ст. 114-1 КК України  
**Scope:** `{"incident": "petropavlivska-borshchahivka", "topic": "criminal_code_article_ladyka", "type": "court_reporting"}`  
**Позиція установи:** `not_recorded`  
**Пояснення агрегатора:** Accepted, scope-matched support from 1 declared source-lineage root(s) meets threshold 1; no contradiction root was accepted.  
**Пошук:** 3 кандидатів у наданому корпусі; 1 пройшли правила оцінювання.  

- **supports**; basis `secondary_reporting`; source `src_hromadske_ladyka`; declared lineage `root_hromadske_journalism` (independence `candidate`).
  - URI: https://hromadske.ua/kryminal/273906-sud-obyraye-zapobiznyy-zakhid-22-richniy-zintsi-iaka-brala-uchast-u-sutychkakh-u-sofiyivskiy-borshchahivtsi
  - Artifact: `artifact_sw_20261108T080001_1`; artifact offset [643:813], passage offset [8:178].
  - Цитата: > Ладику підозрюють у перешкоджанні законній діяльності Збройних сил України та інших військових формувань в особливий період — ч. 1 ст. 114-1 Кримінального кодексу України
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_sw_20261108T080001_1, exact offset span: [8:178].; Affirmative factual and numerical alignment (2 matching root concepts: 114, україн).; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.

### claim_core_14_court_moloda_no_bail — `supported_within_scope`

**Твердження:** Суд обрав Валентині Молодій запобіжний захід у вигляді тримання під вартою без застави  
**Scope:** `{"incident": "petropavlivska-borshchahivka", "topic": "preventive_measure_moloda", "type": "court_reporting"}`  
**Позиція установи:** `not_recorded`  
**Пояснення агрегатора:** Accepted, scope-matched support from 1 declared source-lineage root(s) meets threshold 1; no contradiction root was accepted.  
**Пошук:** 2 кандидатів у наданому корпусі; 1 пройшли правила оцінювання.  

- **supports**; basis `secondary_reporting`; source `src_suspilne_court`; declared lineage `root_suspilne_court_journalism` (independence `candidate`).
  - URI: https://suspilne.media/kyiv/1446145-suticki-v-borsanivci-sud-obirae-zapobiznij-cetvertij-pidozruvanij/
  - Artifact: `artifact_sw_20261108T080001_7`; artifact offset [3576:3803], passage offset [7:234].
  - Цитата: > запобіжний захід для двох фігуранток сутичок у Петропавлівській Борщагівці — Валентини Молодої і Тетяна Кірєєвої , а сьогодні, 5 листопада, для Віктора Єни . Усіх трьох суд відправив під варту на два місяці без права на заставу
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_sw_20261108T080001_7, exact offset span: [7:234].; Affirmative factual and numerical alignment (5 matching root concepts: валентин, запобіжн, застав).; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.

### claim_core_15_court_kireyeva_no_bail — `supported_within_scope`

**Твердження:** Суд обрав Тетяні Кірєєвій запобіжний захід у вигляді тримання під вартою без застави  
**Scope:** `{"incident": "petropavlivska-borshchahivka", "topic": "preventive_measure_kireyeva", "type": "court_reporting"}`  
**Позиція установи:** `not_recorded`  
**Пояснення агрегатора:** Accepted, scope-matched support from 1 declared source-lineage root(s) meets threshold 1; no contradiction root was accepted.  
**Пошук:** 2 кандидатів у наданому корпусі; 1 пройшли правила оцінювання.  

- **supports**; basis `secondary_reporting`; source `src_suspilne_court`; declared lineage `root_suspilne_court_journalism` (independence `candidate`).
  - URI: https://suspilne.media/kyiv/1446145-suticki-v-borsanivci-sud-obirae-zapobiznij-cetvertij-pidozruvanij/
  - Artifact: `artifact_sw_20261108T080001_7`; artifact offset [3576:3803], passage offset [7:234].
  - Цитата: > запобіжний захід для двох фігуранток сутичок у Петропавлівській Борщагівці — Валентини Молодої і Тетяна Кірєєвої , а сьогодні, 5 листопада, для Віктора Єни . Усіх трьох суд відправив під варту на два місяці без права на заставу
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_sw_20261108T080001_7, exact offset span: [7:234].; Affirmative factual and numerical alignment (5 matching root concepts: запобіжн, застав, захід).; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.

### claim_core_16_court_yena_custody_60 — `supported_within_scope`

**Твердження:** Солом'янський районний суд Києва обрав Віктору Єні тримання під вартою на 60 днів без застави  
**Scope:** `{"incident": "petropavlivska-borshchahivka", "topic": "preventive_measure_yena", "type": "court_reporting"}`  
**Позиція установи:** `not_recorded`  
**Пояснення агрегатора:** Accepted, scope-matched support from 1 declared source-lineage root(s) meets threshold 1; no contradiction root was accepted.  
**Пошук:** 2 кандидатів у наданому корпусі; 1 пройшли правила оцінювання.  

- **supports**; basis `secondary_reporting`; source `src_suspilne_court`; declared lineage `root_suspilne_court_journalism` (independence `candidate`).
  - URI: https://suspilne.media/kyiv/1446145-suticki-v-borsanivci-sud-obirae-zapobiznij-cetvertij-pidozruvanij/
  - Artifact: `artifact_sw_20261108T080001_7`; artifact offset [3720:3803], passage offset [29:112].
  - Цитата: > Віктора Єни . Усіх трьох суд відправив під варту на два місяці без права на заставу
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_sw_20261108T080001_7, exact offset span: [29:112].; Affirmative factual and numerical alignment (3 matching root concepts: віктор, застав, суд).; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.

### claim_core_17_parshonkov_hammer_suspicion — `supported_within_scope`

**Твердження:** Іван Паршонков придбав молот та завдавав ним ударів по службовому автомобілю з військовослужбовцями  
**Scope:** `{"incident": "petropavlivska-borshchahivka", "topic": "parshonkov_actions", "type": "court_reporting"}`  
**Позиція установи:** `not_recorded`  
**Пояснення агрегатора:** Accepted, scope-matched support from 1 declared source-lineage root(s) meets threshold 1; no contradiction root was accepted.  
**Пошук:** 2 кандидатів у наданому корпусі; 1 пройшли правила оцінювання.  

- **supports**; basis `secondary_reporting`; source `src_suspilne_court`; declared lineage `root_suspilne_court_journalism` (independence `candidate`).
  - URI: https://suspilne.media/kyiv/1446145-suticki-v-borsanivci-sud-obirae-zapobiznij-cetvertij-pidozruvanij/
  - Artifact: `artifact_sw_20261108T080001_7`; artifact offset [3083:3343], passage offset [24:284].
  - Цитата: > Іван Паршонков дізнався про блокування підрозділу Нацгвардії та вирішив долучитися до нього. Як повідомили у Київській обласній прокуратурі, підозрюваний заздалегідь придбав важкий молот із довгою рукояткою, яким згодом завдавав ударів по службовому автомобілю
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_sw_20261108T080001_7, exact offset span: [24:284].; Affirmative factual and numerical alignment (9 matching root concepts: автомобілю, військовослужбовц, завдавав).; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.

### claim_core_18_dbr_proceedings_426_1 — `supported_within_scope`

**Твердження:** ДБР відкрило кримінальне провадження за ч. 5 ст. 426-1 КК України за фактом подій  
**Scope:** `{"incident": "petropavlivska-borshchahivka", "topic": "dbr_investigation", "type": "official_statement"}`  
**Позиція установи:** `not_recorded`  
**Пояснення агрегатора:** Accepted, scope-matched support from 1 declared source-lineage root(s) meets threshold 1; no contradiction root was accepted.  
**Пошук:** 4 кандидатів у наданому корпусі; 1 пройшли правила оцінювання.  

- **supports**; basis `institutional_statement`; source `src_dbr_proceedings`; declared lineage `root_dbr_official` (independence `candidate`).
  - URI: https://dbr.gov.ua/news/dbr-rozpochalo-kriminalne-provadzhennya-za-faktom-podij-u-petropavlivskij-borshhagivci-na-kiivshhini
  - Artifact: `artifact_reports_source-watch_20261108_official-web-check_md`; artifact offset [1049:1177], passage offset [0:128].
  - Цитата: > ДБР, повідомлення від 3 листопада 2026 року.** Офіційна сторінка повідомляє про початок провадження за ч. 5 ст. 426-1 КК України
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_reports_source-watch_20261108_official-web-check_md, exact offset span: [0:128].; Affirmative factual and numerical alignment (4 matching root concepts: 426, дбр, проваджен).; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.

### claim_core_19_ombudsman_inquiry — `supported_within_scope`

**Твердження:** Уповноважений ВРУ з прав людини направив запити до правоохоронних органів щодо ситуації  
**Scope:** `{"incident": "petropavlivska-borshchahivka", "topic": "ombudsman_inquiry", "type": "official_statement"}`  
**Позиція установи:** `not_recorded`  
**Пояснення агрегатора:** Accepted, scope-matched support from 1 declared source-lineage root(s) meets threshold 1; no contradiction root was accepted.  
**Пошук:** 3 кандидатів у наданому корпусі; 1 пройшли правила оцінювання.  

- **supports**; basis `institutional_statement`; source `src_ombudsman`; declared lineage `root_ombudsman_official` (independence `candidate`).
  - URI: https://ombudsman.gov.ua/news_details/zhodnih-podvijnih-standartiv-ne-maye-buti-ombudsman-vimagaye-perevirki-situaciyi-na-petropavlivskij-borshchagivci
  - Artifact: `artifact_sw_20261108T080001_6`; artifact offset [179:259], passage offset [53:133].
  - Цитата: > Уповноважений Дмитро Лубінець вже направив запити до всіх правоохоронних органів
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_sw_20261108T080001_6, exact offset span: [53:133].; Affirmative factual and numerical alignment (5 matching root concepts: запи, направив, орган).; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.

### claim_core_20_mvs_service_investigation — `supported_within_scope`

**Твердження:** МВС України розпочало службове розслідування за фактом подій на Київщині  
**Scope:** `{"incident": "petropavlivska-borshchahivka", "topic": "mvs_inquiry", "type": "official_statement"}`  
**Позиція установи:** `not_recorded`  
**Пояснення агрегатора:** Accepted, scope-matched support from 1 declared source-lineage root(s) meets threshold 1; no contradiction root was accepted.  
**Пошук:** 3 кандидатів у наданому корпусі; 1 пройшли правила оцінювання.  

- **supports**; basis `institutional_statement`; source `src_mvs_inquiry`; declared lineage `root_mvs_official` (independence `candidate`).
  - URI: https://mvs.gov.ua/news/mvs-ziasovuje-obstavini-podii-na-kiyivshhini-rozpocato-sluzbove-rozsliduvannia
  - Artifact: `artifact_sw_20261108T080001_2`; artifact offset [8:82], passage offset [0:74].
  - Цитата: > МВС з’ясовує обставини подій на Київщині: розпочато службове розслідування
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_sw_20261108T080001_2, exact offset span: [0:74].; Affirmative factual and numerical alignment (5 matching root concepts: київщин, мвс, под).; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.

### claim_core_21_fire_padla_tck_prediction — `supported_within_scope`

**Твердження:** Канал padla_tck поширив твердження, що будівля може спалахнути для знищення доказів  
**Scope:** `{"incident": "petropavlivska-borshchahivka", "topic": "fire_prediction", "type": "social_media_mention"}`  
**Позиція установи:** `not_recorded`  
**Пояснення агрегатора:** Accepted, scope-matched support from 1 declared source-lineage root(s) meets threshold 1; no contradiction root was accepted.  
**Пошук:** 3 кандидатів у наданому корпусі; 1 пройшли правила оцінювання.  

- **supports**; basis `social_media_post`; source `src_telegram_padla_tck`; declared lineage `root_padla_tck_telegram` (independence `candidate`).
  - URI: https://t.me/padla_tck/38019
  - Artifact: `artifact_data_processed_geographic_fire_candidates_jsonl_line_5`; artifact offset [11732:11807], passage offset [42:117].
  - Цитата: > будівля спалахне разом з закатованими людьми,  щоб не було де шукати докази
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_data_processed_geographic_fire_candidates_jsonl_line_5, exact offset span: [42:117].; Affirmative factual and numerical alignment (3 matching root concepts: будівля, доказ, спалах).; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.

### claim_core_22_fire_bucha_warehouse — `supported_within_scope`

**Твердження:** У Бучанському районі після ворожої атаки сталося займання на території складу, дані про постраждалих уточнювали  
**Scope:** `{"incident": "petropavlivska-borshchahivka", "topic": "bucha_warehouse_fire_early_update", "type": "reported_statement"}`  
**Позиція установи:** `not_recorded`  
**Пояснення агрегатора:** Accepted, scope-matched support from 1 declared source-lineage root(s) meets threshold 1; no contradiction root was accepted.  
**Пошук:** 2 кандидатів у наданому корпусі; 1 пройшли правила оцінювання.  

- **supports**; basis `secondary_reporting`; source `src_interfax_ova_fire_early_update`; declared lineage `root_interfax_reporting` (independence `candidate`).
  - URI: https://interfax.com.ua/news/general/1231365.html
  - Artifact: `artifact_reports_source-watch_fire-source-review-2026-11-09_md`; artifact offset [498:617], passage offset [2:121].
  - Цитата: > Бучанському районі внаслідок ворожої атаки сталося займання на території складу. Уточнюємо інформацію щодо постраждалих
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_reports_source-watch_fire-source-review-2026-11-09_md, exact offset span: [2:121].; Affirmative factual and numerical alignment (9 matching root concepts: атак, бучанськ, ворожої).; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.

### claim_core_23_fire_video_location_mismatch — `insufficient_evidence`

**Твердження:** TikTok-відео з написом «Софіївська Борщагівка» зображує пожежу окремого складу, а не будівлі НГУ  
**Scope:** `{"incident": "petropavlivska-borshchahivka", "topic": "fire_location", "type": "media_verification"}`  
**Позиція установи:** `not_recorded`  
**Пояснення агрегатора:** The supplied evidence does not meet the declared source-lineage threshold; absence of evidence is not refutation.  
**Пошук:** 5 кандидатів у наданому корпусі; 1 пройшли правила оцінювання.  

- **contextualizes**; basis `user_comment`; source `src_tiktok_fire_analysis`; declared lineage `root_tiktok_spatial_analysis` (independence `candidate`).
  - URI: https://www.tiktok.com/@anastasiyapalivoda/video/7704443960013376789
  - Artifact: `artifact_reports_tiktok-fire_comment_candidate_review_md`; artifact offset [2306:2372], passage offset [0:66].
  - Цитата: > розрізняє Софіївську й Петропавлівську — **географічне виправлення
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_reports_tiktok-fire_comment_candidate_review_md, exact offset span: [0:66].; Passage documents user comments making geographic corrections, which does not constitute optical forensic geolocation of video frames.; Text comments distinguishing municipalities do not verify video scene.; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.

### claim_core_24_tck_presence_at_scene — `insufficient_evidence`

**Твердження:** Співробітники ТЦК та СП здійснювали блокування або перебували в будівлі під час сутичок  
**Scope:** `{"incident": "petropavlivska-borshchahivka", "topic": "tck_presence", "type": "institutional_presence"}`  
**Позиція установи:** `not_recorded`  
**Пояснення агрегатора:** The supplied evidence does not meet the declared source-lineage threshold; absence of evidence is not refutation.  
**Пошук:** 5 кандидатів у наданому корпусі; 5 пройшли правила оцінювання.  

- **contextualizes**; basis `social_media_post`; source `src_telegram_padla_tck`; declared lineage `root_padla_tck_telegram` (independence `candidate`).
  - URI: https://t.me/padla_tck/38019
  - Artifact: `artifact_data_processed_geographic_fire_candidates_jsonl_line_5`; artifact offset [11732:11739], passage offset [42:49].
  - Цитата: > будівля
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_data_processed_geographic_fire_candidates_jsonl_line_5, exact offset span: [42:49].; Passage describes institutional occupancy/activity without mentioning TCK; absence cannot be inferred from alternate occupancy.; Negative presence inference rejected under epistemic discipline.; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.
- **contextualizes**; basis `institutional_statement`; source `src_mvs_briefing`; declared lineage `root_mvs_official` (independence `candidate`).
  - URI: https://mvs.gov.ua/news/u-ministerstvi-vnutrisnix-sprav-ukrayini-vidbuvsia-brifing-shhodo-podii-na-kiyivshhini
  - Artifact: `artifact_sw_20261108T080001_4`; artifact offset [3304:3332], passage offset [11:39].
  - Цитата: > Національної гвардії України
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_sw_20261108T080001_4, exact offset span: [11:39].; Passage describes institutional occupancy/activity without mentioning TCK; absence cannot be inferred from alternate occupancy.; Negative presence inference rejected under epistemic discipline.; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.
- **contextualizes**; basis `secondary_reporting`; source `src_suspilne_court`; declared lineage `root_suspilne_court_journalism` (independence `candidate`).
  - URI: https://suspilne.media/kyiv/1446145-suticki-v-borsanivci-sud-obirae-zapobiznij-cetvertij-pidozruvanij/
  - Artifact: `artifact_sw_20261108T080001_7`; artifact offset [3111:3390], passage offset [52:331].
  - Цитата: > блокування підрозділу Нацгвардії та вирішив долучитися до нього. Як повідомили у Київській обласній прокуратурі, підозрюваний заздалегідь придбав важкий молот із довгою рукояткою, яким згодом завдавав ударів по службовому автомобілю, всередині якого перебували військовослужбовці
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_sw_20261108T080001_7, exact offset span: [52:331].; Passage describes institutional occupancy/activity without mentioning TCK; absence cannot be inferred from alternate occupancy.; Negative presence inference rejected under epistemic discipline.; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.
- **contextualizes**; basis `secondary_reporting`; source `src_hromadske_ladyka`; declared lineage `root_hromadske_journalism` (independence `candidate`).
  - URI: https://hromadske.ua/kryminal/273906-sud-obyraye-zapobiznyy-zakhid-22-richniy-zintsi-iaka-brala-uchast-u-sutychkakh-u-sofiyivskiy-borshchahivtsi
  - Artifact: `artifact_sw_20261108T080001_1`; artifact offset [710:813], passage offset [75:178].
  - Цитата: > України та інших військових формувань в особливий період — ч. 1 ст. 114-1 Кримінального кодексу України
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_sw_20261108T080001_1, exact offset span: [75:178].; Passage describes institutional occupancy/activity without mentioning TCK; absence cannot be inferred from alternate occupancy.; Negative presence inference rejected under epistemic discipline.; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.
- **contextualizes**; basis `institutional_statement`; source `src_dbr_proceedings`; declared lineage `root_dbr_official` (independence `candidate`).
  - URI: https://dbr.gov.ua/news/dbr-rozpochalo-kriminalne-provadzhennya-za-faktom-podij-u-petropavlivskij-borshhagivci-na-kiivshhini
  - Artifact: `artifact_reports_source-watch_20261108_official-web-check_md`; artifact offset [1170:1177], passage offset [121:128].
  - Цитата: > України
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_reports_source-watch_20261108_official-web-check_md, exact offset span: [121:128].; Passage describes institutional occupancy/activity without mentioning TCK; absence cannot be inferred from alternate occupancy.; Negative presence inference rejected under epistemic discipline.; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.

### claim_core_25_police_arrival_ambulance_call — `supported_within_scope`

**Твердження:** Поліція прибула на місце події за викликом працівників приватної швидкої допомоги  
**Scope:** `{"incident": "petropavlivska-borshchahivka", "topic": "police_arrival", "type": "official_statement"}`  
**Позиція установи:** `not_recorded`  
**Пояснення агрегатора:** Accepted, scope-matched support from 1 declared source-lineage root(s) meets threshold 1; no contradiction root was accepted.  
**Пошук:** 3 кандидатів у наданому корпусі; 1 пройшли правила оцінювання.  

- **supports**; basis `institutional_statement`; source `src_ngu_press`; declared lineage `root_ngu_official` (independence `candidate`).
  - URI: https://ngu.gov.ua/shturm-kativni-pid-vybuhy-shahediv-yak-fejk-pro-40-zaruchnykiv-pereris-u-zavorushennya-v-petropavlivskij-borshhagivczi/
  - Artifact: `artifact_sw_20261108T080001_5`; artifact offset [2800:2963], passage offset [5:168].
  - Цитата: > працівники приватної швидкої, за повідомленням поліції Київщини, викликали правоохоронців, заявивши, що їм перешкоджають дістатися до людини, яка потребує допомоги
  - Обмеження: Relation inferred by deterministic rules from a BM25-retrieved passage in the supplied corpus.; Artifact ID: artifact_sw_20261108T080001_5, exact offset span: [5:168].; Affirmative factual and numerical alignment (4 matching root concepts: допомог, працівник, приватної).; A passage-level relation is not by itself proof that the real-world claim is true or false.; A declared root ID is provenance input; this function does not establish the root's independence.

---

## 3. Реєстр джерел, використаних у прийнятих оцінках

Корені є задекларованими тегами лінії походження, а не доказом незалежності. SHA-256 стосується локального артефакту пасажа.

| Source ID | Basis | Declared lineage root | URI | Artifact SHA-256 |
|---|---|---|---|---|
| `src_interfax_ova_fire_early_update` | `secondary_reporting` | `root_interfax_reporting` | https://interfax.com.ua/news/general/1231365.html | `31cf5eae941e12cf1da1acf5c2689a5c8c0c44fc8ae2eaaa893f4a13ed26a8a6` |
| `src_dbr_proceedings` | `institutional_statement` | `root_dbr_official` | https://dbr.gov.ua/news/dbr-rozpochalo-kriminalne-provadzhennya-za-faktom-podij-u-petropavlivskij-borshhagivci-na-kiivshhini | `6e3374426fed34c85fb65b3720051dc74bb52bb56c9c0d9e63d2325a4e8b5faf` |
| `src_hromadske_ladyka` | `secondary_reporting` | `root_hromadske_journalism` | https://hromadske.ua/kryminal/273906-sud-obyraye-zapobiznyy-zakhid-22-richniy-zintsi-iaka-brala-uchast-u-sutychkakh-u-sofiyivskiy-borshchahivtsi | `44a252ca36b385bbd20ba64c57dc05a279dd379cdece0a1dcbace79f9b9738c6` |
| `src_mvs_briefing` | `institutional_statement` | `root_mvs_official` | https://mvs.gov.ua/news/u-ministerstvi-vnutrisnix-sprav-ukrayini-vidbuvsia-brifing-shhodo-podii-na-kiyivshhini | `44a252ca36b385bbd20ba64c57dc05a279dd379cdece0a1dcbace79f9b9738c6` |
| `src_mvs_inquiry` | `institutional_statement` | `root_mvs_official` | https://mvs.gov.ua/news/mvs-ziasovuje-obstavini-podii-na-kiyivshhini-rozpocato-sluzbove-rozsliduvannia | `44a252ca36b385bbd20ba64c57dc05a279dd379cdece0a1dcbace79f9b9738c6` |
| `src_ngu_press` | `institutional_statement` | `root_ngu_official` | https://ngu.gov.ua/shturm-kativni-pid-vybuhy-shahediv-yak-fejk-pro-40-zaruchnykiv-pereris-u-zavorushennya-v-petropavlivskij-borshhagivczi/ | `44a252ca36b385bbd20ba64c57dc05a279dd379cdece0a1dcbace79f9b9738c6` |
| `src_npu_130_persons` | `institutional_statement` | `root_npu_national_official` | https://npu.gov.ua/news/politseiski-natsionalnoi-politsii-ukrainy-razom-z-sbu-vzhe-vstanovyly-130-osib-iaki-mozhut-buty-prychetnymy-do-zavorushen-na-petropavlivskii-borshhagivtsi | `95d3ba72ba10007f76246926ed7a5da94a7edd3aac9d8c058d374275260816dd` |
| `src_ombudsman` | `institutional_statement` | `root_ombudsman_official` | https://ombudsman.gov.ua/news_details/zhodnih-podvijnih-standartiv-ne-maye-buti-ombudsman-vimagaye-perevirki-situaciyi-na-petropavlivskij-borshchagivci | `44a252ca36b385bbd20ba64c57dc05a279dd379cdece0a1dcbace79f9b9738c6` |
| `src_telegram_padla_tck` | `social_media_post` | `root_padla_tck_telegram` | https://t.me/padla_tck/38019 | `c1522ea4407eb2bd2358c1abf7188c7be45b4d01ef3b63e8a07c3abaaff974ec` |
| `src_suspilne_court` | `secondary_reporting` | `root_suspilne_court_journalism` | https://suspilne.media/kyiv/1446145-suticki-v-borsanivci-sud-obirae-zapobiznij-cetvertij-pidozruvanij/ | `44a252ca36b385bbd20ba64c57dc05a279dd379cdece0a1dcbace79f9b9738c6` |
| `src_tiktok_fire_analysis` | `user_comment` | `root_tiktok_spatial_analysis` | https://www.tiktok.com/@anastasiyapalivoda/video/7704443960013376789 | `4ad54b453ca068a978b983adc8741eb04c262eda8b6ce5dfcdc08113e0b9d35c` |

---

## 4. Підсумок цього корпусу

- `supported_within_scope`: 19.
- `refuted_within_scope`: 0.
- `conflicting_evidence`: 0.
- `insufficient_evidence`: 6.
- `unverified`: 0.

Ці лічильники описують лише наведені твердження, локальний корпус, дату зрізу та поточні правила. Вони не є незалежним аудитом справи й не визначають поширеність думок або фактів за межами джерел у цьому пакеті.

### Додатковий аудит пожежі

Раннє повідомлення про займання збережено як вторинний переказ Interfax-Ukraine повідомлення голови Київської ОВА, а не як локально захоплений первинний бюлетень. У повідомленні сказано, що дані про постраждалих уточнювалися. Пізніші тогочасні повідомлення вказували на травмованого охоронця та конкретизували Софіївську Борщагівку; отже, ранню фразу не можна перетворювати на твердження «постраждалих немає». Докладний ланцюг джерел: [`fire-source-review-2026-11-09.md`](../source-watch/fire-source-review-2026-11-09.md).
