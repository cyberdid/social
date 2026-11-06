# Огляд наукової літератури: алгоритми й методики аналізу інформаційних хвиль, координації, ботів і контекстної дезінформації

**Дата:** 2026-11-06. **Тип:** оглядове дослідження (scoping review), **не** систематичний огляд. **Мова:** українська; назви методів — в оригіналі.
**Доповнює** `wiki/methods/research-methodology-review.md` (Codex, 05.11, 19 джерел): роботи, які вже там є (Pacheco et al., CooRnet, Telegram CIB 2025, Ecker/Lewandowsky, Brashier, Roozenbeek, Vosoughi тощо), тут не дублюються.

## 1. Метод пошуку

| Крок | Що зроблено |
|---|---|
| Джерела | OpenAlex API (з 2015 р.) і arXiv API — безкоштовні, відкриті, без ключів |
| Запити | 24 запити за 6 темами (T1 хвилі в Telegram, T2 координація, T3 боти, T4 контекстна дезінформація, T5 надійність кодування, T6 спростування й вимірювання впливу). Кожен запит, URL, час і кількість результатів — `raw/literature/20261106T072201Z/queries.jsonl` |
| Код | `src/lit_search.py` (повторюваний пошук) |
| Записи | 502 записи → **480 унікальних** після дедуплікації за DOI/arXiv ID |
| Відбір | За назвою й анотацією, **один рецензент (Claude)**; критерії: метод застосовний до нашого конвеєра, емпіричні дані або огляд методів; не дублює набір Codex. Відібрано **41 роботу** (`included.txt`) |
| Перевірка | Усі 41 ідентифікатор перевірено: 35 DOI через Crossref, 6 через arXiv API (`included_verified.jsonl`) |
| Глибина читання | **Лише анотації** (для 3 робіт анотацій немає; там спираюся на метадані й позначаю це). Повні тексти не читалися, тож числа нижче — ті, що є в анотаціях |

**Обмеження.** Пошук ранжований: це не повне покриття. Відбір робив один рецензент, і перевірка тверджень іде на рівні анотацій. Перед використанням у препринті ключові роботи треба прочитати повністю.

## 2. Синтез за темами

### T1. Як науковці аналізують хвилі й наративи в Telegram

- **Наративи еволюціонують, і їх треба моделювати в часі, а не як фіксовані мітки.** Gerard et al. (2025) порівнюють проросійські й проукраїнські спільноти в Telegram у перші три місяці війни та моделюють, як змінюються наративи і що цю зміну рухає.
- **«Наратив» у Telegram не завжди зв'язний.** Willaert et al. (2023, PLOS ONE) проаналізували 2,7 млн повідомлень із 492 каналів і класифікували кожне за відповідністю сусіднім повідомленням. Канали мають різні «наративні профілі»: конспірологічні — розірвані, військово-дезінформаційні — змішані. Висновок для нас: закріплювати один наратив за каналом некоректно, позицію треба кодувати на рівні поста.
- **Вибірка «насіння + сніжна куля» — це стандарт галузі, але від неї залежить, що ви побачите.** Willaert et al. (2022) будують мережу від тематичних стартових каналів. Alvisi et al. (2025) розкривають конспірологічні сфери через пересилання (анотації немає, лише назва). Shah et al. (2024, arXiv) на 1 740 каналах показують, що канали-«мости» між ізольованими групами непропорційно поширюють уже спростовану дезінформацію, а більшість каналів, що її несуть, **не є її авторами**.
- **Автоматичне виявлення пропаганди мовами регіону** порівнюють Solopova et al. (2023): багатомовні методи для новин і постів Telegram, зокрема українською та російською.
- **Український контекст.** Баловсяк (Balovsiak, 2025): 14 тижнів моніторингу рейтингів Telemetrio і TGStat. Анонімні канали найстабільніше тримаються в топі, пропагандистські мають високе охоплення, а офіційні майже відсутні. Ghasiya & Sasahara (2023) порівнюють стратегії повідомлень офіційних українських каналів і RT.

**Що це означає для нас.** Наш підхід (стартові канали, пересилання, позиція на рівні поста) збігається з практикою. Варто додати міру «мостовості» каналу (bridging, Shah et al.), щоб знаходити не автора, а ключові вузли поширення. І не варто описувати хвилю як фіксований набір наративів (Gerard et al.).

### T2. Виявлення скоординованої поведінки (CIB)

- **Огляд поля.** Mannocci et al. (2026, ACM Computing Surveys) зводять промислові й академічні визначення координації та пропонують загальну рамку. Головна думка: координація ≠ неавтентичність, бо скоординовано діють і звичайні соціальні рухи.
- **Синхронні дії замість «загального детектора».** Magelinski et al. (2022) застерігають, що узагальнені детектори координації можуть посилити нерівність влади між державою і маргіналізованими групами. Тому вони пропонують шукати *синхронні дії* в багатовимірних мережах (той самий хештег, URL чи текст у вузькому вікні часу). Ng & Carley (2023) пропонують комбінований індекс синхронності (CSI) і виявляють, що **люди часто синхронніші за ботів**. Отже, сама синхронність ботів не доводить.
- **Мережі схожості.** Giglietto et al. (2020) — скоординоване поширення посилань у Facebook (основа CooRnet). Cinus et al. (2025, WWW) будують мережі схожості в X, Facebook і Telegram і знаходять координацію між платформами, зокрема системне просування афілійованих із Росією медіа в Telegram і X. Cinelli et al. (2022) досліджують CIB і поширення в Twitter (анотації немає).
- **TikTok.** Luceri et al. (2026, ICWSM) на 1,35 млн відео виборів у США 2024 року шукають синхронний постинг, повторне використання фрагментів мовлення й медіа, а потім проріджують граф. Важливе застереження: **відеовідповіді, Duet і Stitch переважно органічні**, а не ознака CIB.
- **Наявність координації ≠ її вплив.** Sarhan et al. (2025) через тест Ґрейнджера показали, що скоординована активність у німецькому дискурсі про COVID **не рухала** нескоординований дискурс, а видимість більше визначали алгоритми платформи.

**Що це означає для нас.**
1. Затримки копіювання між групами B і C варто доповнити нульовою моделлю синхронності: скільки збігів очікується випадково при такій інтенсивності постингу.
2. Для коментарів S4 «синхронність» — лише кандидат, бо люди теж синхронні.
3. Окремо від «чи була координація» ставити питання «чи вона вплинула», наприклад тестом Ґрейнджера між часовими рядами груп.

### T3. Виявлення ботів: що працює і чого не можна робити

- **Готові класифікатори ненадійні як інструмент вимірювання.** Rauchfleisch & Kaiser (2020) на 4 134 верифікованих акаунтах показали, що бали Botometer неточні, особливо не англійською, і нестабільні в часі. Пороги дають і хибнопозитивні, і хибнонегативні результати, тож більшість соціальнонаукових досліджень із цим інструментом рахує як ботів багато людей і навпаки.
- **Різні методи — різні «частки ботів».** Martini et al. (2021) порівняли Botometer, Tweetbotornot і «heavy automation» на 122 884 акаунтах і отримали **дуже різні результати**. Ні ручна перевірка, ні тріангуляція базової проблеми не розв'язують.
- **Практичні настанови.** Yang et al. (2022) — практикум Botometer для соціологів (анотації немає). Cresci (2020) — огляд десятиліття досліджень: детектори відстають від еволюції ботів, а оцінювання має бути змагальним.
- **Мультиплатформені детектори** працюють гірше поза Twitter. BotBuster (Ng & Carley 2023, суміш експертів за частинами профілю) має середній F1 0,74 на Twitter і близько 0,60 на Reddit та інших платформах.
- **Генеративні моделі ускладнюють задачу.** Ferrara (2023): текст ботів на основі LLM стає неможливо відрізнити за стилем, тому вагу мають поведінка й мережа, а не лексика.
- **Державні тролі — не боти.** Zannettou et al. (2019) аналізують поведінку й вплив державних тролів; це переважно люди, а не автоматика.

**Що це означає для нас.**
1. Наш підхід (сигнали замість частки ботів, жодного готового класифікатора, кілька незалежних поведінкових ознак) відповідає висновкам Rauchfleisch & Kaiser та Martini et al.
2. **Не додавати** Botometer-подібні бали навіть як «додаткову перевірку».
3. Профільні проксі (нік на кшталт `user123`) лишити слабким сигналом.
4. Для коментарів Telegram є прапор `bot` самого Telegram. Це рідкісний випадок справжньої мітки, але вона охоплює лише офіційних ботів, а не автоматизовані людські акаунти.

### T4. Контекстна дезінформація: справжнє медіа з хибним підписом, місцем чи датою

- **Найпоширеніша, а не екзотична форма.** Dufour et al. (2024, AMMeBa) за два роки людської розмітки фактчеків з розміткою ClaimReview встановили, що «прості» методи, **насамперед маніпуляції контекстом**, історично домінували й до листопада 2023 року лишалися більшістю. Генеративний ШІ став помітним лише нещодавно.
- **Автоматичні детектори невідповідності «зображення — текст» вчать на зсунутих датасетах.** Papadopoulos et al. (2024, VERITE) показують упередженість до однієї модальності в бенчмарках. У 2025 році ті самі автори показали, що простий базовий метод, який порівнює зображення й текст із зовнішніми доказами (MUSE), конкурує зі складними моделями за <1% обчислень. Вони прямо застерігають, що прогрес поля частково ілюзорний, бо моделі вловлюють поверхневі шаблони, а не фактичність. Sniffer (Qi et al. 2024, CVPR) — мультимодальна LLM із поясненнями.
- **Практика фактчекерів.** Khan et al. (2023, IEEE Access; arXiv 2023 про кейси війни Росії проти України) описують робочі процеси: геолокація, архіви, зворотний пошук, моніторинг. Автоматика лише допомагає, вирішує людина.

**Що це означає для нас.** Кейс «пожежа в Софіївській → сліди в Петропавлівській» — типовий приклад контекстної підміни **через коментарі**, а не через підпис. Це рідше досліджуваний варіант. Наш сканер (`contextual_candidates.py`) варто розвивати за логікою MUSE: шукати зовнішні докази (геолокація кадру, дата, інші публікації того самого відео), а не тренувати класифікатор.

### T5. Надійність кодування текстів (правила, моделі, люди)

- **Словники не досягають прийнятної валідності.** Van Atteveldt et al. (2021) порівняли ручне кодування, краудкодинг, словники й машинне навчання. Найкраще працюють навчені люди, **жоден словник не наблизився до прийнятної валідності**, машинне навчання — посередині. Головна рекомендація — завжди валідувати перед використанням. Це прямо пояснює наш результат: правила для N1/N2/N4 мають κ≈0,1.
- **Три прогалини обчислювального аналізу тексту** (Baden et al. 2021): технологія переважає валідність операціоналізації; методи витягують окремі ознаки, а соціологам потрібні складні конструкти; домінують англомовні інструменти. Для українсько-російського корпусу третя прогалина критична.
- **LLM як кодувальник.** Törnberg (2023): GPT-4 у zero-shot перевершив експертів і краудворкерів за точністю й надійністю у визначенні партійності за твітом. Alizadeh et al. (2024): відкриті LLM після донавчання на невеликій розмітці зрівнюються з GPT-3.5/4 у zero-shot. Chew et al. (2023) і Dunivin (2025) пропонують гібридні процедури, де людина зберігає інтерпретацію, а модель масштабує кодування.

**Що це означає для нас.** Правила (словники) годяться лише для пошуку кандидатів. Для позицій «поширює чи спростовує» потрібне валідоване кодування. За вашим рішенням локальні LLM не використовуємо, тому шлях такий: людська розмітка ~200 постів двома кодувальниками з κ або α Кріппендорфа, а правила лише пропонують кандидатів. Варіант із LLM можна буде розглянути пізніше, коли GPU буде вільний і якщо ви погодитеся.

### T6. Спростування і вимірювання впливу

- **Корекції працюють, але скромно.** Мета-аналіз Walter et al. (2020): k=24, N=6 086, середній ефект корекцій у соцмережах d=0,40 [0,25; 0,55], упередженість публікацій не виключена. Ефективніше, коли спростовують експерти і коли дезінформацію поширювали медіа, а не знайомі.
- **Формат корекції мало важить.** Swire-Thompson et al. (2021), чотири експерименти: ефект «майже не залежить від формату», якщо є ключові складники корекції. Інокуляція як превентивна стратегія — Lewandowsky & van der Linden (2021).
- **Побічний ефект.** Hoes et al. (2024, Nature Human Behaviour; США, Польща, Гонконг; n=6 127): фактчеки й поради з медіаграмотності знижують віру у фейки, **але й знижують довіру до правдивої інформації**.
- **Обережно з «епідемією дезінформації».** Altay et al. (2023) описують шість хибних уявлень: поширеність і вплив переоцінені, соцмережі вивчають, бо так зручно методично, а охоплення ≠ вплив. Adams et al. (2023) звели погляди 11 дисциплін на те, *чому* дезінформація взагалі є проблемою.

**Що це означає для нас.** Перегляди не є впливом (див. KB8 і DR5). Висновки на кшталт «хвиля вплинула на натовп» наші дані не підтримують, це рівень D. Офіційна комунікація мала затримку 4 год 26 хв, але на підставі цього не варто писати, що «швидкість вирішує все». Емпірично доведено лише, що корекції мають помірний ефект і можуть підривати довіру до правди.

## 3. Наш конвеєр і література: що змінити

| Крок конвеєра | Зараз | Література | Дія |
|---|---|---|---|
| Вибірка каналів | Стартові канали + пересилання + маркери інфраструктури | Willaert 2022; Shah 2024; Cinus 2025 | Додати метрику «мостовості», окремо звітувати канали-мости |
| Наративи | Правила (згадки); κ≈0,6 для N3/N0, ≈0,1 для N1/N2/N4 | Van Atteveldt 2021; Baden 2021 | Правила лише для пошуку кандидатів; позицію визначає людська розмітка (2 кодувальники, α Кріппендорфа) |
| Еволюція наративів | Статичні частки | Gerard 2025 | Часові частки наративів за 6-годинними вікнами |
| Копії та координація | Точний Jaccard, затримки по підтверджених парах | Magelinski 2022; Ng & Carley 2023; Mannocci 2026 | Нульова модель синхронності (перестановки часу); координацію і вплив розділяти (Ґрейнджер, Sarhan 2025) |
| Боти в коментарях | Поведінкові сигнали S1–S6, без частки ботів | Rauchfleisch 2020; Martini 2021; Ferrara 2023 | Лишити як є; Botometer-подібні бали не додавати; додати прапор `bot` Telegram |
| Контекстна дезінформація | Сканер кандидатів + ручний реєстр | Dufour 2024; Papadopoulos 2025; Khan 2023 | Перевірка на основі зовнішніх доказів (геолокація, дата, повторне використання медіа), а не класифікатор |
| Вплив і спростування | KB8 → D | Walter 2020; Hoes 2024; Altay 2023 | Не робити висновків про вплив з переглядів; для майбутніх кейсів знімати лічильники кожні 15–30 хв |

## 4. Прогалини, які видно з літератури

1. Майже немає робіт про **контекстну підміну через коментарі** (а не через підпис медіа).
2. Мало валідованих інструментів для **українсько-російського змішаного корпусу** (Baden et al. 2021).
3. Немає публічного еталону «бот / людина» для **Telegram і TikTok-коментарів**.
4. Майже немає досліджень **впливу** хвиль у Telegram на офлайн-дії. Наш кейс (натовп біля будинку) — саме такий випадок, але без даних про охоплення конкретних людей причинний висновок неможливий.

## 5. Посилання (41 робота; DOI/arXiv перевірено 06.11.2026)

**T1.** Gerard P. D. et al. (2025). Modeling Information Narrative Evolution on Telegram During the Russia-Ukraine War. *ICWSM*. https://doi.org/10.1609/icwsm.v19i1.35834 · Willaert T. et al. (2023). A computational analysis of Telegram's narrative affordances. *PLOS ONE*. https://doi.org/10.1371/journal.pone.0293508 · Willaert T. et al. (2022). Disinformation networks: A quali-quantitative investigation of antagonistic Dutch-speaking Telegram channels. *First Monday*. https://doi.org/10.5210/fm.v27i5.12533 · Solopova V. et al. (2023). Automated Multilingual Detection of Pro-Kremlin Propaganda in Newspapers and Telegram Posts. *Datenbank-Spektrum*. https://doi.org/10.1007/s13222-023-00437-2 · Ghasiya P. et al. (2023). Messaging strategies of Ukraine and Russia on Telegram during the 2022 Russian invasion of Ukraine. *First Monday*. https://doi.org/10.5210/fm.v28i8.12873 · Shah D. et al. (2024). Bridging Nodes and Narrative Flows: Identifying Intervention Targets for Disinformation on Telegram. arXiv:2411.05922. https://doi.org/10.48550/arXiv.2411.05922 · Alvisi L. et al. (2025). Unraveling the Italian and English Telegram Conspiracy Spheres Through Message Forwarding. *LNCS*. https://doi.org/10.1007/978-3-031-78538-2_18 · Balovsiak N. V. (2025). Anonymous and official Telegram channels in Ukraine: analysis of popularity during the hybrid war. *Current Issues of Mass Communication*. https://doi.org/10.17721/cimc.2025.37.30-42

**T2.** Giglietto F. et al. (2020). It takes a village to manipulate the media. *Information, Communication & Society*. https://doi.org/10.1080/1369118X.2020.1739732 · Magelinski T. et al. (2022). Synchronized Action Framework for Detection of Coordination on Social Media. *J. Online Trust and Safety*. https://doi.org/10.54501/jots.v1i2.30 · Ng L. H. X., Carley K. M. (2023). A combined synchronization index for evaluating collective action social media. *Applied Network Science*. https://doi.org/10.1007/s41109-022-00526-3 · Mannocci L. et al. (2026). Detection and Characterization of Coordinated Online Behavior: A Survey. *ACM Computing Surveys*. https://doi.org/10.1145/3839225 · Cinus F. et al. (2025). Exposing Cross-Platform Coordinated Inauthentic Activity in the Run-Up to the 2024 U.S. Election. *WWW '25*. https://doi.org/10.1145/3696410.3714698 · Luceri L. et al. (2026). Coordinated Inauthentic Behavior on TikTok. *ICWSM*. https://doi.org/10.1609/icwsm.v20i1.42711 · Sarhan H. et al. (2025). There was coordinated inauthentic user behavior in the COVID-19 German X-discourse, but did it really matter? *Frontiers in Communication*. https://doi.org/10.3389/fcomm.2025.1510144 · Cinelli M. et al. (2022). Coordinated inauthentic behavior and information spreading on Twitter. *Decision Support Systems*. https://doi.org/10.1016/j.dss.2022.113819

**T3.** Cresci S. (2020). A decade of social bot detection. *Communications of the ACM*. https://doi.org/10.1145/3409116 · Rauchfleisch A., Kaiser J. (2020). The False positive problem of automatic bot detection in social science research. *PLOS ONE*. https://doi.org/10.1371/journal.pone.0241045 · Yang K.-C. et al. (2022). Botometer 101: social bot practicum for computational social scientists. *J. Computational Social Science*. https://doi.org/10.1007/s42001-022-00177-5 · Martini F. et al. (2021). Bot, or not? Comparing three methods for detecting social bots in five political discourses. *Big Data & Society*. https://doi.org/10.1177/20539517211033566 · Ferrara E. (2023). Social bot detection in the age of ChatGPT. *First Monday*. https://doi.org/10.5210/fm.v28i6.13185 · Ng L. H. X., Carley K. M. (2023). BotBuster: Multi-Platform Bot Detection Using a Mixture of Experts. *ICWSM*. https://doi.org/10.1609/icwsm.v17i1.22179 · Zannettou S. et al. (2019). Disinformation Warfare: Understanding State-Sponsored Trolls on Twitter and Their Influence on the Web. *WWW '19 Companion*. https://doi.org/10.1145/3308560.3316495

**T4.** Qi P. et al. (2024). Sniffer: Multimodal LLM for Explainable Out-of-Context Misinformation Detection. *CVPR*. https://doi.org/10.1109/CVPR52733.2024.01240 · Papadopoulos S.-I. et al. (2024). VERITE: a robust benchmark for multimodal misinformation detection accounting for unimodal bias. *IJMIR*. https://doi.org/10.1007/s13735-023-00312-6 · Papadopoulos S.-I. et al. (2025). Similarity Over Factuality: Are we Making Progress on Multimodal Out-of-Context Misinformation Detection? *WACV*. https://doi.org/10.1109/WACV61041.2025.00544 · Dufour N. et al. (2024). AMMeBa: A Large-Scale Survey and Dataset of Media-Based Misinformation In-The-Wild. arXiv:2405.11697. https://doi.org/10.48550/arXiv.2405.11697 · Khan S. A. et al. (2023). Online Multimedia Verification with Computational Tools and OSINT: Russia-Ukraine Conflict Case Studies. arXiv:2310.01978. https://doi.org/10.48550/arXiv.2310.01978 · Khan S. A. et al. (2023). Visual User-Generated Content Verification in Journalism: An Overview. *IEEE Access*. https://doi.org/10.1109/ACCESS.2023.3236993

**T5.** van Atteveldt W. et al. (2021). The Validity of Sentiment Analysis. *Communication Methods and Measures*. https://doi.org/10.1080/19312458.2020.1869198 · Baden C. et al. (2021). Three Gaps in Computational Text Analysis Methods for Social Sciences. *Communication Methods and Measures*. https://doi.org/10.1080/19312458.2021.2015574 · Törnberg P. (2023). ChatGPT-4 Outperforms Experts and Crowd Workers in Annotating Political Twitter Messages with Zero-Shot Learning. arXiv:2304.06588. https://doi.org/10.48550/arXiv.2304.06588 · Chew R. et al. (2023). LLM-Assisted Content Analysis. arXiv:2306.14924. https://doi.org/10.48550/arXiv.2306.14924 · Alizadeh M. et al. (2024). Open-source LLMs for text annotation. *J. Computational Social Science*. https://doi.org/10.1007/s42001-024-00345-9 · Dunivin Z. O. (2025). Scaling hermeneutics: a guide to qualitative coding with LLMs for reflexive content analysis. *EPJ Data Science*. https://doi.org/10.1140/epjds/s13688-025-00548-8

**T6.** Hoes E. et al. (2024). Prominent misinformation interventions reduce misperceptions but increase scepticism. *Nature Human Behaviour*. https://doi.org/10.1038/s41562-024-01884-x · Altay S. et al. (2023). Misinformation on Misinformation: Conceptual and Methodological Challenges. *Social Media + Society*. https://doi.org/10.1177/20563051221150412 · Adams Z. et al. (2023). (Why) Is Misinformation a Problem? *Perspectives on Psychological Science*. https://doi.org/10.1177/17456916221141344 · Swire-Thompson B. et al. (2021). Correction format has a limited role when debunking misinformation. *Cognitive Research: Principles and Implications*. https://doi.org/10.1186/s41235-021-00346-6 · Walter N. et al. (2020). Evaluating the Impact of Attempts to Correct Health Misinformation on Social Media: A Meta-Analysis. *Health Communication*. https://doi.org/10.1080/10410236.2020.1794553 · Lewandowsky S., van der Linden S. (2021). Countering Misinformation and Fake News Through Inoculation and Prebunking. *European Review of Social Psychology*. https://doi.org/10.1080/10463283.2021.1876983

**Інструмент огляду.** Kassis T., Agarwal V., He Y., Patel D., Brueckner A. M. (2026). Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents. arXiv:2609.00065. https://doi.org/10.48550/arXiv.2609.00065
