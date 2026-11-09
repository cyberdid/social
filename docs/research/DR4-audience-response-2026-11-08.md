# Autonomous Audience Response, Sentiment, Emotion and Engagement Analysis
## Scientific Methods and Architecture for Social, 2026

**Дата огляду:** 8 листопада 2026 року  
**Призначення:** методична основа для Audience Response Intelligence Engine у Social  
**Обсяг:** коментарі, відповіді, реакції, теми, емоції, stance, дискусійна динаміка та межі узагальнення

> Документ підсумовує наукові публікації, офіційні документації платформ і фактичний огляд наявних модулів Social у локальній гілці станом на дату огляду. Репозиторій під час підготовки звіту не змінювався. Нові модулі нижче — пропозиції, а не наявний код.

---

## 1. Executive Summary

Автоматизований аналіз коментарів може дати корисний опис **спостережуваної онлайн-дискусії**, але не оцінку поглядів населення. Коментатори — самовибрана частина аудиторії; платформи показують різні фрагменти дискусій, ранжують коментарі й надають неоднакові поля. У Social збір цільовий, а не випадковий: Telegram вибирає гілки релевантних дописів із відповідями та сортує за числом відповідей; YouTube збирає відібрані відео й коментарі з сортуванням за новизною; Instagram залежить від доступу й відбору постів; TikTok — від видимості та доступного маршруту збору. Тому кожний відсоток має називати власний знаменник і межі покриття.

Головні висновки:

1. **Не зводити різні виміри до одного “настрою”.** Sentiment, emotion, stance, topic, toxicity, reactions та engagement відповідають на різні питання. Негативний тон не визначає позицію; лайк не доводить згоди; кількість відповідей не є підтримкою.
2. **Прив’язувати stance та emotion до цілі.** Один коментар може критикувати дії поліції, підтримувати право на протест і сумніватися у твердженні про травми. Потрібен зв’язок comment → target/claim → stance/emotion, із кількома цілями та явною невизначеністю.
3. **Перевіряти на українсько-російських коментарях Social.** На EmoBench-UA Multilingual-E5 Large отримав 0,62 macro-F1, а найкращий LLM-рядок — DeepSeek-V3 з англомовним промптом — 0,65 на українському тесті базових емоцій. COSMUS показує перевагу українсько-орієнтованої моделі й цільової заміни слів, тоді як back-translation погіршив результат. Ці task-specific оцінки не прогнозують якість на коментарях Social або stance-класах.
4. **Залишити LLM помічником, не еталоном.** Вони корисні для чернеткового маркування, опису тем і пошуку складних випадків. Самооцінка LLM не є каліброваною імовірністю; згода кількох моделей не усуває спільний bias.
5. **Відокремити відкриття тем від перевірки тверджень.** Topic discovery показує, *про що говорять*; claim extraction фіксує перевірювану тезу; stance — підтримку/заперечення тези. “Дії поліції” як тема не означають позицію.
6. **Зберігати реакції як платформні дії, а не як істину про думку.** YouTube надає comment likeCount, але viewerRating=none не розрізняє dislike від відсутності рейтингу. TikTok Research API повертає like/reply count. Telegram Bot API має окремі updates реакцій, але вимагає адмінправ і підписки на типи updates. Доступ Meta Research обмежений.
7. **Порівнювати лічильники лише за відомого часу/експозиції.** Вік коментаря й алгоритмічна видимість впливають на реакції. Якщо impressions конкретного коментаря невідомі, не можна оцінити “частку підтримки серед тих, хто побачив”. Можна подавати counts, однакові age snapshots, внутрішньогілкові ранги або обережну age-adjusted модель.
8. **Агрегувати кількома estimand-ами:** за коментарями, авторами, гілками й каналами. Це різні питання, і жодне не є репрезентативною громадською думкою.
9. **Вимірювати поляризацію як властивість дискусій.** Різноманітність позицій, розрив їхніх часток, конфлікт у відповідях і ворожість між групами — різні явища. Не виводити політичні профілі користувачів.
10. **Передбачити abstention.** Якщо контексту мало, текст саркастичний або змішаний, а моделі не погоджуються — повертати unclear/insufficient_context, а не вигадувати позицію.

### Рекомендований результат для Social

Найкраща практична система — не один універсальний LLM, а відтворюваний конвеєр:

~~~text
normalization/reply graph → topic/target resolution → target-aware stance/sentiment/emotion
→ separate toxicity labels → reaction snapshots → multiple aggregate estimands
→ temporal/manipulation sensitivity → quality and citation checks
~~~

Потрібно зберігати версії моделей, контекст і походження кожної мітки. Звіт має показувати покриття та невизначеність разом із висновком.

---

## 2. Перевірений стан репозиторію

Оглянуто локальну гілку codex/social-master-plan станом на 8 листопада 2026 року. Нижче — тільки те, що фактично знайдено:

| Компонент | Наявна функція | Наслідок |
|---|---|---|
| [src/tg_comments_collect.py]($SOCIAL_REPO_ROOT/src/tg_comments_collect.py) | Збирає Telegram comments із linked discussion threads під релевантними постами з відповідями; пише HMAC-псевдонім автора, час, текст, reply_to_comment, is_top_level, тип відправника та сумарне число реакцій. Вибірка сортується за кількістю відповідей; є ліміт гілки і статус complete/capped/error. | Це не перепис Telegram. Схема має тільки суму реакцій, без emoji breakdown та історії snapshots. |
| [src/analysis/tg_comment_signals.py]($SOCIAL_REPO_ROOT/src/analysis/tg_comment_signals.py) | Рахує концентрацію авторів, точні/схожі тексти, швидкі повтори, синхронність, шаблонні пули й слабкі профільні проксі; прямо позначає їх як сигнали, не частку ботів. | Це не stance/emotion/topic engine. Модуль згортає thread до URL початкового поста, тому не будує reply graph, хоча збирач зберігає parent ID. |
| [src/tiktok_public_collect.py]($SOCIAL_REPO_ROOT/src/tiktok_public_collect.py) | Зберігає comment/parent IDs, likes, replies, час і статуси пагінації. | Доступний snapshot/ranking не є повним архівом усіх comments. |
| [src/youtube_collect.py]($SOCIAL_REPO_ROOT/src/youtube_collect.py) | Зберігає псевдонімізованого автора, parent, likes і час; відео відбираються за метаданими/переглядами, comments — з порядком за новизною. | Немає знаменника показів конкретного comment для зовнішнього збирача. |
| [src/instagram_collect.py]($SOCIAL_REPO_ROOT/src/instagram_collect.py) | Збирає доступні comments, like counts, parent і timestamps через доступний сесійний шлях; відбір обмежено доступом і видимістю. | Не переносити на всі відкриті comments Instagram. |
| [src/analysis/information_dynamics.py]($SOCIAL_REPO_ROOT/src/analysis/information_dynamics.py) | Аналізує динаміку інформаційних публікацій. | Це не temporal emotion/stance аналіз comments. |
| [src/analysis/coordination_null_models.py]($SOCIAL_REPO_ROOT/src/analysis/coordination_null_models.py) | Статистично аналізує сигнали повторів/координації. | Може живити sensitivity scenarios, але flag не є підставою вилучати comment. |

Telegram-знімок 6 листопада 2026 у [reports/telegram-comments/coordinated-comments.md]($SOCIAL_REPO_ROOT/reports/telegram-comments/coordinated-comments.md) фіксує 39 598 сирих comments, 39 459 з доступним автором, 12 797 authors і 533 відібрані дискусії. У звіті зазначено, що всі 533 зібрані повністю. Повнота збору цих гілок не робить вибірку репрезентативною.

**Не знайдено в коді:** окремого comment topic-discovery, stance/sentiment/emotion classifier, reaction semantics, polarization, toxicity/incivility, comment temporal dynamics чи audience dashboard. Запропоновані компоненти нижче нові.

---

## 3. Sentiment, emotion, stance, topic та engagement — різні виміри

| Вимір | Питання | Приклад | Чого не доводить |
|---|---|---|---|
| Topic | Про що говорять? | Дії поліції, право на протест | Не показує позиції автора. |
| Claim | Яку перевірювану тезу висловлено? | Поліція застосувала газ о 18:00 | Не визначає правдивість чи підтримку. |
| Stance | Яка позиція щодо конкретної цілі? | Підтримує/заперечує втручання поліції | Не є загальним політичним профілем автора. |
| Sentiment | Яка полярна оцінка вислову щодо цілі? | Позитивна/негативна/змішана/нейтральна | Негативність не означає заперечення claim. |
| Emotion | Яку емоцію висловлює текст? | Гнів щодо дії, співчуття людям | Не встановлює внутрішній стан автора. |
| Toxicity/incivility | Чи є образа, дегуманізація, погроза, виключення? | Особиста образа чи заклик до шкоди | Не є синонімом гніву чи критики. |
| Engagement/reaction | Яка дія платформи зафіксована? | Лайк, emoji, reply | Не означає згоди з усім змістом comment. |

Емпіричні роботи показують, що sentiment і target-specific stance розходяться: навіть золоті sentiment/subjectivity features не замінюють stance. Див. [Mohammad, Sobhani & Kiritchenko, “Stance and Sentiment in Tweets” (2017)](https://doi.org/10.1145/3003433) та [Bestvater & Monroe, “Sentiment is Not Stance” (2023)](https://doi.org/10.1017/pan.2022.10). Виведена з соцмереж позиція також не завжди збігається із самозвітом в опитуванні: [Joseph et al., EMNLP 2021](https://aclanthology.org/2021.emnlp-main.27/). Отже, звітувати потрібно позицію, **виражену в тексті**, а не стійке переконання автора.

Рекомендована ієрархія:

~~~text
discussion topic → candidate claim/target → evidence span
→ stance + sentiment + expressed emotion → engagement signals
~~~

Topic, Claim, Narrative і Stance — різні сутності. Класифікація має зберігати relation до target ID, підтримувати кілька міток, а neutral, no_stance, mixed, unclear, not_about_target та insufficient_context не зливати.

---

## 4. Target-Aware Sentiment, Emotion and Stance Framework

### 4.1. Одиниця анотації

Використовувати зв’язок comment, target, evidence span, а не одну мітку на автора. Comment може мати кілька цілей; короткий reply може вимагати parent comment/root post. Контекст зберігається окремо, щоб текст батька не рахувався як слова відповідача.

### 4.2. Stance labels

- favor — явно підтримує пропозицію, дію, твердження або вимогу;
- against — явно заперечує або відкидає ціль;
- neutral — збалансований/фактичний текст без прихильності;
- no_stance — згадує ціль без позиції;
- mixed — підтримує й заперечує різні аспекти;
- unclear — неоднозначність, сарказм або брак контексту;
- not_about_target — не стосується заданої цілі.

Основний favor/against denominator не включає no_stance/not_about_target. Mixed та unclear показуються окремо, не перерозподіляються.

### 4.3. Sentiment та emotion

Sentiment: positive / negative / neutral / mixed / not_applicable — бажано щодо target.

Emotion — multi-label. Для першої перевіреної версії рекомендую anger, fear, sadness, disgust, joy, surprise, none/unclear. Не додавати автоматично outrage, anxiety, frustration, contempt, trust, hope, relief, empathy: для них мало локальних benchmark-ів, а частина є складеними/перекривними категоріями. Додавати їх після локального codebook та міжанотаторської перевірки. Emotion target і причина емоції різні: співчуття може бути до людини, а причиною — дія установи. Причину зберігати тільки коли вона виражена текстом.

Для кожного висновку фіксувати evidence span, target ID, context IDs, мову/code-switch, модель/версію, raw scores, calibration ID і abstention reason. Score не є імовірністю істинності.

### 4.4. Емпіричні орієнтири для української та російської

- **GoEmotions:** 58k англомовних Reddit comments, 27 emotions + neutral; baseline BERT F1 .46. Складність fine-grained multi-label emotion, не готовий український label set. [Demszky et al., ACL 2020](https://aclanthology.org/2020.acl-main.372/).
- **EmoBench-UA:** benchmark емоцій у відібраних українських твітах, не корпус коментарів Social. На його українському test split для binary multi-label basic-emotion detection Multilingual-E5 Large має 0,62 macro-F1 після навчання на природному українському train split; DeepSeek-V3 з англійським промптом — 0,65 (український промпт — 0,62). Ці числа не переносяться на російські/змішані тексти, stance чи інцидентні коментарі. [Dementieva et al., Findings EMNLP 2025, Table 1](https://aclanthology.org/2025.findings-emnlp.107.pdf).
- **COSMUS:** 12 224 текстів Telegram/відгуків/відкритих ресурсів українською, російською та code-switched, sentiment positive/negative/neutral/mixed. UkrRoberta із цільовою LLM word substitution дала до +2.2 percentage points accuracy; back-translation погіршувала результат. Складні випадки: sarcasm, negation, mixed affect. Це мовний sentiment орієнтир, не stance. [Shynkarov et al., UNLP 2025](https://aclanthology.org/2025.unlp-1.18/).
- **CEDR:** російський multi-label корпус близько 9 410 коротких текстів з п’ятьма емоціями. Корисний baseline, але не політичні Telegram comments. [CEDR resource](https://github.com/sag111/CEDR).
- **RuSentiment:** 31 185 російських VK-постів із п’ятьма sentiment labels; не stance/emotion gold set. [Rogers et al., COLING 2018](https://aclanthology.org/C18-1064/).

Оцінювати Ukrainian, Russian та mixed text окремо. Порівняти UkrRoberta/COSMUS, XLM-R, multilingual-E5 + classifier і один LLM baseline. Без локального gold set inference лишається exploratory незалежно від benchmark score.

### 4.5. Контекст, сарказм і короткі відповіді

Передбачити:
- parent і root post у контексті, але не як текст reply author;
- quoted text із позначенням джерела/мовця;
- sarcasm як окрему pragmatic uncertainty, не автоматичний polarity flip;
- code-switching, transliteration, slang, misspelling;
- emoji-only/короткі відповіді як insufficient_context без контексту;
- negation, rhetorical question, profanity, citation і mixed stance як тестові slices.

Контекст допомагав sarcasm analysis у досліджених англомовних корпусах, але перенос треба перевірити: [Ghosh et al., “Sarcasm Analysis Using Conversation Context”](https://aclanthology.org/J18-4009/). Модель описує емоцію, виражену текстом, не психологічний стан людини.

---

## 5. Topic discovery та opinion mining

### 5.1. Порівняння алгоритмів

| Метод | Переваги | Обмеження коротких коментарів | Роль |
|---|---|---|---|
| TF-IDF + NMF | Швидкий і прозорий baseline; читабельні слова/біграми | Розрідженість, словоформи, paraphrases | Обов’язковий baseline. |
| LDA | Зрозуміла generative model | Мало co-occurrence; нестійкий вибір k | Контрольний baseline, не єдиний метод. |
| Embedding clustering / BERTopic | Групує paraphrases; multilingual embeddings; має noise/outlier | Залежить від domain fit; нестійкі дрібні кластери | Основний challenger після порівняння з NMF. |
| Top2Vec | Автоматизований joint topic/document space | Менш керований; transfer треба тестувати | Лише якщо кращий за BERTopic за stability/usefulness. |
| Dynamic topic model | Моделює зміни в часі | Короткий кейс, малі bins, composition confounding | Спершу frozen topic map + часові частки. |
| LLM topic labels | Зручні природні короткі описи | Може домислити спільний сенс/злити теми | Чернетка з quoted examples, не validator. |

У [Rahimi et al. (Findings EACL 2024)](https://aclanthology.org/2024.findings-eacl.123/) contextualized topic coherence краще відображав людські оцінки на short texts у семи topic models. Це quality signal, не заміна representative examples чи перевірки.

### 5.2. Рекомендований метод

1. Зберігати original; нормалізувати окрему копію без втрати negation/quotes.
2. Групувати exact/near duplicates для topic training, але зберігати частоти для engagement/coordination.
3. Не кластеризувати однословні/emoji-only comments примусово.
4. Запустити multilingual embeddings + clustering, паралельно NMF TF-IDF.
5. Зберігати top terms, examples, noise share, cluster size, stability між seeds/subsamples, розподіл UA/RU/platform.
6. Називати описово (“обговорення дій поліції”), не встановлювати правдивість чи мотиви.
7. У часових зрізах використовувати frozen topic IDs, однакові 1h/6h bins та denominators.
8. Нові теми залишати novel_candidate/other до стабільного повторення.

Оцінювати coherence, diversity, redundancy, cluster stability (Jaccard/ARI після зіставлення тем), outlier share та зрозумілість прикладів. Нестабільну тему подавати як пошуковий кластер.

---

## 6. Reaction and Engagement Measurement Framework

### 6.1. Семантика реакцій

Like, heart, laugh, anger чи dislike залежать від теми, автора, адресата й платформи. Дослідження виявляють різні функції Like (підтримка стосунків, acknowledgement, аудиторний сигнал) та нестабільність розподілів реакцій між темами. [Sumner et al. (2018)](https://doi.org/10.1177/1461444817697917), [Paolillo (2023)](https://doi.org/10.5210/fm.v28i8.13157). У randomized field experiment [Muchnik, Aral & Taylor (2013)](https://doi.org/10.1126/science.1240466) ранній позитивний rating змінював ймовірність наступного позитивного rating. Лічильник сам може впливати на наступну дію, отже reactions не є незалежним голосуванням за claim.

Telegram-специфічний препринт [Tardelli et al. (2025)](https://arxiv.org/abs/2508.06349) аналізує 647 879 повідомлень у 993 криптовалютних чатах і знаходить переважання позитивних emoji reactions навіть під нейтральним і негативним текстом; понад 84% нейтральних/негативних повідомлень отримували позитивну реакційну тональність. Це сильний аргумент не використовувати reaction emoji як мітку емоції тексту. Перенос на політичні/воєнні канали Social не доведений: автори прямо вказують на доменну специфіку і невалідовані на власному корпусі автоматичні emotion/sentiment labels.

### 6.2. Метрики та знаменники

| Метрика | Значення | Обмеження |
|---|---|---|
| like_count, reaction_count_by_type | Сирі дії на snapshot | Популярність/активність, не підтримка, не унікальні люди, не exposure rate. |
| reply_count | Кількість відповідей | Активність/дискусійність; reply може бути згодою, запереченням, питанням чи спамом. |
| reactions_per_impression | Reactions / покази comment | Бажаний exposure denominator, зазвичай недоступний незалежному збирачу; не рахувати без поля. |
| reaction_per_follower | Reactions / followers | Потенційна аудиторія, не impressions. |
| within_thread_percentile | Ранг count у гілці | Внутрішньогілкова помітність, не корекція personalization чи віку. |
| same_age_snapshot_delta | Count(t₀+Δ) − Count(t₀) | Порівнює однаковий elapsed time, не impressions/унікальних людей. |
| age_adjusted_residual | NB/GAM count ~ f(age) + platform + thread/channel effects | Умовне порівняння, не CTR і не виправлення selection bias. |
| reaction_diversity | Entropy за типами | Різноманітність кнопок, не controversy без семантичної перевірки. |
| reaction_concentration | Частка реакцій на top comments | Концентрація engagement у вибірці, не підтримка позиції. |

Не ділити лічильник на години/дні з припущенням лінійного накопичення. [Vassio et al. (2022)](https://doi.org/10.1007/s13278-022-00928-2) дослідили приблизно 4 млн Facebook/Instagram posts і виявили різні age trajectories. Пріоритет — repeated snapshots у однакові elapsed-time windows. За одного snapshot age covariate є тільки умовним порівнянням.

### 6.3. Офіційні дані платформ станом на 08.11.2026

| Платформа | Документовані дані/умови | Невідоме — не нуль |
|---|---|---|
| **Telegram** | [Bot API](https://core.telegram.org/bots/api): message_reaction та message_reaction_count; потрібен bot admin і явне allowed_updates, агрегат може затриматись. Є emoji/custom emoji/paid ([reactions](https://core.telegram.org/api/reactions)). Канальні comments у linked discussion group/thread ([docs](https://core.telegram.org/api/discussion)). | Відсутній event може бути наслідком відсутніх прав/підписки або пізнього збору. Історичний повний список reactors/events не гарантований. Поточний Social collector сумує кількості, втрачаючи emoji type. |
| **YouTube** | comments має likeCount, publishedAt, parentId; viewerRating лише like/none, де none включає dislike і відсутність оцінки ([API](https://developers.google.com/youtube/data/reference/rest/v3/comments)). commentThreads може повертати підмножину replies; повні replies через comments.list(parentId=...) ([docs](https://developers.google.com/youtube/data/reference/rest/v3/commentThreads)). Відео dislikeCount доступний лише власнику відео ([docs](https://developers.google.com/youtube/data/reference/rest/v3/videos)). | viewerRating=none не є нуль dislikes. Покази конкретного comment зовнішньому збирачу невідомі. |
| **TikTok** | Схвалений [Research API](https://developers.tiktok.com/docs/en/research-api-specs-query-video-comments) має like_count, reply_count, parent_comment_id, create_time, text; batch до 100 і може бути неповним. Потрібен approved project ([access](https://developers.tiktok.com/docs/en/about-research-api)); архів відстає до 48 годин за відео й 10 днів за метриками ([FAQ](https://developers.tiktok.com/docs/en/research-api-faq)). | Developer account недостатньо; archive не live. Менший результат API не доводить, що решти comments немає. Emoji reaction types у comment schema не вказано. |
| **Instagram/Meta** | Стандартний [Instagram comment moderation API](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/comment-moderation/) прив’язаний до професійних акаунтів/доступів app. Meta заявляла про Content Library/API для кваліфікованих researchers; Instagram public comments в API з’явилися у 2024 ([announcement/update](https://about.fb.com/news/2023/11/new-tools-to-support-independent-research/)). | Не універсальний endpoint до кожного публічного поста. Фіксувати access scope, permissions і completeness. |

Зберігати reaction_type, count, observed_at, source_endpoint, access_scope, is_aggregate, completeness, unavailable_reason. Reactions root post не змішувати з reactions коментарів.

---

## 7. Conversation, hostility та polarization

### 7.1. Reply graph

Відтворити post → top-level comment → reply → reaction snapshot. Автор — локальний псевдонім. Telegram collector зберігає reply_to_comment, але analyzer зараз задає thread як post URL, не створюючи comment-to-comment graph. Додати перевірки orphan replies, roots і pagination.

Корисні метрики: top-level/reply share, depth/breadth, reply latency, stance transition parent→reply, question/argument/quote types, concentration. Reply count не є підтримкою.

### 7.2. Toxicity та ескалація

Окремо кодувати:
- interpersonal impoliteness/incivility (образа, vulgarity, name-calling);
- intolerant/exclusionary content (дегуманізація/виключення; потрібен контекст);
- threat (висловлена погроза/заклик, не доказ наміру чи здатності);
- hate/discriminatory target;
- anger/outrage (може бути легітимною критикою).

[Pendzel et al., EMNLP 2024](https://aclanthology.org/2024.emnlp-main.827/) відокремлюють impolite style від intolerant substance у 13K політичних твітів; best F1 близько .70 для impoliteness і .59 для intolerance, що ілюструє семантичну складність. Для української є [Toxicity Classification in Ukrainian (WOAH 2024)](https://aclanthology.org/2024.woah-1.19/), але не можна припускати відсутність хибних спрацьовувань на політичній критиці.

Виводити індикатори окремими рядами: hostile comments per 100, threats, addressed insults, reply depth/latency, disagreement vs abuse. Composite score без валідованої вагової схеми не створювати.

### 7.3. Opinion diversity та polarization

Для кожної цілі показувати:
- розподіл stance разом із mixed/unclear/no-stance;
- normalized entropy: H = −Σ pₖ log(pₖ) / log(K);
- favor/against imbalance: |p_favor − p_against|;
- частку reply edges з протилежними позиціями;
- cross-stance interaction і концентрацію за thread/channel;
- емоції до явних груп/цілей окремо від загального sentiment.

Низька entropy — концентрація розмічених позицій, не суспільна поляризація. Висока entropy може бути різноманіттям або помилкою класифікації. Affective polarization вимагає явних груп та in-group warmth/out-group hostility; anger/disgust цього не визначають. [Lerman et al. (2024)](https://www.nature.com/articles/s44260-024-00008-w) досліджують конкретний мережевий контекст, не універсальну діагностику.

Не створювати індивідуальні політичні профілі; висновки — про агрегати спостережуваних дискусій.

---

## 8. Statistical Framework: estimands, вибірка та невизначеність

### 8.1. Паралельні estimands

1. **Comment-weighted:** p₍c₎ = мітка коментарів s / визначені comments. Доля comments у зібраній вибірці; гіперактивні authors мають більшу вагу.
2. **Author-balanced:** середня частка мітки серед comments кожного спостережуваного автора. Кожен псевдоавтор має однакову вагу; не є часткою населення.
3. **Thread-balanced:** середнє часток stance за відібраними гілками; зменшує вагу найбільших потоків.
4. **Channel/platform-balanced:** рівна вага джерел; не є impression-based opinion.

Показувати окремо authors без ID, threads, channels, unclear rate, coverage.

### 8.2. Залежність і довірчі інтервали

Comments вкладені у threads та channels; рядки не незалежні. Використовувати hierarchical multinomial/logistic model із random effects thread/channel/author або cluster bootstrap на рівні thread/channel. Це оцінює мінливість у відібраних кластерах, **не створює випадкову вибірку населення**.

Для цільового corpus інтервал є conditional uncertainty, не survey CI для українців. Додати sensitivity до classifier labels, ваг, duplicate/coordination scenarios. Worst-case bounds щодо пропущених comments можна рахувати лише коли відома їхня кількість; без знаменника результат не ідентифікований.

### 8.3. Обсяг валідаційної вибірки

Для prevalence за простим випадковим відбором із N:

n₀ = z²p(1−p)/d²  
n = n₀ / [1+(n₀−1)/N]

Для N=39 598, 95% CI, d=.05 і conservative p=.5 виходить приблизно **381 comments**. Це лише SRS prevalence, не достатність для rare class або classifier F1.

Розділити:
- representative probability sample для prevalence/calibration;
- challenge sample із oversampling sarcasm, mixed language, short replies, rare emotion, threat/quotes для diagnostics. Challenge sample не використовувати для prevalence без design weights.

Recall оцінюється серед gold-positive прикладів, precision — серед predicted positives. Для rare class розмір sample розрахувати з потрібної ширини CI й очікуваної метрики: приблизно n ≈ z²q(1−q)/d²; звітувати support і Wilson/exact binomial interval. Train/test split — по thread, author, duplicate cluster.

### 8.4. Метрики якості

- Single-label stance/sentiment: per-class precision/recall/F1, macro-F1, confusion, MCC як додатковий balance-aware score.
- Multi-label emotion/toxicity: per-class F1, PR-AUC, micro/macro-F1, Hamming loss; subset accuracy лише додатково.
- Annotation reliability: Krippendorff α для кількох кодерів/missing labels; Cohen κ лише для двох. За rare labels додати positive agreement і prevalence; Gwet AC1/AC2 як sensitivity check.
- Calibration: Brier, reliability diagrams, ECE per language/platform/length/target; ECE залежить від binning.
- Abstention: risk–coverage — error серед прийнятих прикладів проти частки coverage.
- Не використовувати model confidence як calibrated probability без незалежного holdout.

### 8.5. Координаційна чутливість

Перераховувати: (A) усі comments, (B) без exact/near duplicates, (C) author-balanced/capped-author, (D) без multi-signal suspicious clusters, (E) suspicious clusters включені з sensitivity bounds. Зберігати всі comments; не auto-delete за weak flags.

---

## 9. Temporal Audience Response

Окремо зберігати comment_created_at, root_post_published_at, observed_at, reaction_snapshot_at і, якщо є, incident_event_time. fetched_at не дорівнює часу публікації.

Для короткого кейсу:
- фіксовані 1h bins для піків і 6h для багатоденної динаміки; порівняти обидва;
- counts і denominators у кожному bin: comments, authors, threads, language, platform coverage, decidable labels;
- frozen topic/stance/emotion model versions;
- change-point як кандидат, який перевіряється за іншим binning та складом джерел;
- incident events як часові маркери, не причинні змінні;
- reactions порівнювати за однаковим elapsed-time snapshot.

Коректне формулювання: “після заяви зросла частка X у спостережуваних comments; одночасно змінився склад platform/thread, причинний ефект не ідентифікований”. Не робити причинний висновок лише з temporal sequence.

---

## 10. Порівняння моделей

| Задача | Baseline | Практичний старт | Межі |
|---|---|---|---|
| Sentiment | Lexicon, TF-IDF + Logistic/SVM | UkrRoberta/COSMUS для UA; multilingual model для RU/mixed; local fine-tune | LLM лише challenger; calibration з іншого domain не переноситься. |
| Emotion | NRC/dictionary audit | Multilingual-E5-Large або XLM-R/UA encoder fine-tuned на gold | EmoBench-UA: benchmark-specific macro-F1 .62–.65 на відібраному українському тест-наборі; для Social якість невідома. |
| Target-aware stance | TF-IDF із target tokens | Cross-encoder XLM-R з target + comment + parent/root context | Zero-shot NLI/LLM не гарантує target transfer/sarcasm handling. |
| Topic | NMF TF-IDF | multilingual embeddings + BERTopic із outlier class | Порівняти stability/CTC/human examples. |
| Toxicity | UA keyword audit flags | Separate classifiers: impoliteness, threat, intolerance | Confound profanity, criticism and hate. |
| Reaction | Raw counts/snapshots | No semantic mapping by default; age-matched snapshots/thread ranks | Emoji → stance лише після локального експерименту. |

[Ziems et al., Computational Linguistics 2024](https://aclanthology.org/2024.cl-1.8/) порівняли 13 LLM на 25 англомовних CSS tasks; у taxonomic classification найкращі fine-tuned models перевершували LLM. [Gu et al., Findings ACL 2026](https://aclanthology.org/2026.findings-acl.4/) показують ефективність LLM як помічників, але обмеження як незалежних annotators. Використовувати для prelabel, topic name drafts, difficult-case triage і структурованого тексту, не як незалежне підтвердження.

Для stance корисні [X-Stance](https://arxiv.org/abs/2003.08385) — target як питання, transfer помірний; [VAST](https://aclanthology.org/2020.emnlp-main.717/) — нові targets/лексична варіативність; [Hardalov et al. 2022](https://aclanthology.org/2022.findings-emnlp.193/) — few-shot cross-lingual stance, де sentiment є допоміжним.

Для практичного локального benchmark додати конкретні checkpoint candidates, а не вибрати переможця наперед: `youscan/ukr-roberta-base` для українського fine-tuning; `FacebookAI/xlm-roberta-base` і `FacebookAI/xlm-roberta-large` як multilingual baselines; `intfloat/multilingual-e5-large` як embeddings + окремий classifier; `cardiffnlp/twitter-xlm-roberta-base-sentiment` лише як transfer baseline, бо його вихідний benchmark не є Social stance. Ці моделі згадані/використані у відповідних українських benchmark роботах; actual Social quality треба виміряти локально. Для GPT/Claude/Gemini не знайдено зіставного опублікованого порівняння на цих самих UA/RU comments і targets. Якщо додавати API LLMs, фіксувати доступний model snapshot, prompt, temperature, дату, latency/cost і відповідь на однакових прикладах; не оголошувати переможця за vendor claims або unrelated benchmarks.

---

## 11. Архітектура Audience Response Intelligence Engine

~~~text
Collectors
  → platform receipts, raw snapshots, completeness/missingness
  → normalize, privacy transform, language, duplicate clusters
  → reconstruct comment/reply graph + reaction snapshots
  → resolve targets/claims from existing claim graph
  → topic + stance + sentiment + emotion + incivility classifiers
  → calibration, abstention, disagreement and drift checks
  → aggregate per comment / author / thread / channel / platform
  → temporal, polarization/diversity, manipulation sensitivity
  → evidence tables and cited examples → report/dashboard
~~~

| Тип компоненту | Використання |
|---|---|
| Deterministic | Parsing, normalization, timestamps, duplicates, reaction counts, pagination, aggregation, schema. |
| Statistical | Cluster bootstrap, hierarchical models, age adjustment, bounds, stability, change points. |
| ML | Language/topic/stance/emotion/sentiment/toxicity predictions. |
| LLM | Topic-name drafts, annotation assistance, difficult-case triage, prose from structured findings. |
| Human | Gold benchmark and periodic audits during development; not each new incident. |

**Наявні integration points:** src/tg_comments_collect.py, src/tiktok_public_collect.py, src/youtube_collect.py, src/instagram_collect.py, src/analysis/tg_comment_signals.py, src/analysis/coordination_null_models.py, src/analysis/information_dynamics.py, src/analysis/offline_case_runner.py, src/analysis/incident_orchestrator.py, src/analysis/report_generator.py.

**Нові запропоновані файли (не знайдені в поточному коді):**
- src/analysis/audience_context.py
- src/analysis/audience_targets.py
- src/analysis/audience_classification.py
- src/analysis/audience_topics.py
- src/analysis/reaction_metrics.py
- src/analysis/discussion_dynamics.py
- src/analysis/audience_aggregation.py
- src/analysis/audience_quality.py
- schemas/audience_*.schema.json

Audience stage має бути downstream read-only, з власним receipt, без неявного запуску collection.

---

## 12. Data models and interfaces

Спільні правила:
- Stable local IDs; platform IDs scoped by platform/source.
- Зберігати content_created_at, collected_at, observed_at і reaction_snapshot_at окремо.
- 0, null, missing, hidden, unavailable, not_collected, partial, redacted — різні стани.
- Не з’єднувати HMAC author IDs між платформами без незалежного обґрунтування.
- Model scores не називати імовірністю істини.

~~~json
{
  "Comment": {
    "comment_id": "platform:local_id",
    "platform": "telegram|youtube|tiktok|instagram",
    "post_id": "string|null",
    "thread_id": "string|null",
    "parent_comment_id": "string|null",
    "author_pseudonym": "string|null",
    "text_original": "string|null",
    "text_normalized": "string|null",
    "language": {"label": "uk|ru|mixed|other|unknown", "method": "string"},
    "content_created_at": "ISO-8601|null",
    "content_updated_at": "ISO-8601|null",
    "collected_at": "ISO-8601",
    "availability": {
      "text": "available|redacted|hidden|unavailable|not_collected",
      "author": "available|unavailable|not_collected"
    },
    "source_receipt_id": "string",
    "schema_version": "1.0"
  },
  "CommentReactionSnapshot": {
    "snapshot_id": "string",
    "comment_id": "platform:local_id",
    "reaction_type": "like|emoji_unicode|custom_emoji_id|paid|unknown",
    "count": 0,
    "count_state": "observed|hidden|unavailable|not_collected|partial",
    "is_aggregate": true,
    "observed_at": "ISO-8601",
    "source_endpoint": "string",
    "access_scope": "public_api|research_api|owner_auth|browser_snapshot|telegram_admin_bot",
    "completeness": "complete|partial|unknown"
  },
  "CommentStance": {
    "annotation_id": "string",
    "comment_id": "platform:local_id",
    "target_id": "claim|entity|policy id",
    "label": "favor|against|neutral|no_stance|mixed|unclear|not_about_target",
    "evidence_span": {"start": 0, "end": 12, "text": "..."},
    "context_ids": ["parent_comment_id", "root_post_id"],
    "scores_raw": {"favor": 0.0, "against": 0.0, "neutral": 0.0},
    "calibration_id": "string|null",
    "abstention_reason": "string|null",
    "model_id": "string",
    "model_version": "string",
    "provenance": "string"
  },
  "CommentEmotion": {
    "annotation_id": "string",
    "comment_id": "platform:local_id",
    "target_id": "string|null",
    "emotion_labels": ["anger", "fear"],
    "label_state": "expressed|none|uncertain|insufficient_context",
    "evidence_span": {"start": 0, "end": 12, "text": "..."},
    "emotion_cause_span": null,
    "cause_state": "explicit|not_in_text|uncertain",
    "model_id": "string",
    "model_version": "string",
    "context_ids": [],
    "provenance": "string"
  },
  "AudienceAggregate": {
    "aggregate_id": "string",
    "target_id": "string|null",
    "topic_id": "string|null",
    "platform": "string|all_observed",
    "window_start": "ISO-8601|null",
    "window_end": "ISO-8601|null",
    "unit": "comment|author|thread|channel",
    "label": "string",
    "numerator": 0,
    "denominator": 0,
    "estimate": 0.0,
    "uncertainty_type": "cluster_bootstrap|posterior|scenario_bound|none",
    "interval": [0.0, 0.0],
    "coverage": {"comments": 0, "authors": 0, "threads": 0, "unclear": 0},
    "selection_description": "string",
    "model_versions": [],
    "provenance": "string"
  }
}
~~~

Додаткові об’єкти та мінімальні обов’язкові поля:

| Об’єкт | Обов’язкові поля | Перевірка цілісності |
|---|---|---|
| `CommentThread` | `thread_id`, `platform`, `root_post_id`, `comment_ids`, `reported_reply_count` + state, `collected_count`, `pagination_state`, `selection_rule`, `captured_at`, `receipt_id` | Звірити reported та collected counts; недоступне/обмежене позначати state, не нулем. |
| `CommentTopic` | `annotation_id`, `comment_id`, `topic_id`, `assignment_state`, `evidence_span` (nullable), `raw_score`, `topic_model_id/version`, `stability_id`, `provenance` | Outlier/no-topic зберігається явно; не створювати тему лише з LLM назви. |
| `CommentClaim` | `annotation_id`, `comment_id`, `claim_id` або `candidate_claim_id`, `speech_relation` (assert/deny/quote/question/unclear), `span`, `context_ids`, `model/version`, `provenance` | Цитата не стає позицією автора; контекст чужого повідомлення не додається до тексту автора. |
| `SentimentTarget` | `target_id`, `target_type`, `canonical_label`, `aliases`, `linked_claim_ids`, `source_graph_id`, `provenance` | Target має посилатися на claim/entity/policy у стабільному графі або бути явно candidate. |
| `DiscussionCluster` | `cluster_id`, `thread_id`, `member_comment_ids`, `cluster_type`, `method/version`, `representative_ids`, `noise_state`, `created_at` | Один comment не рахується двічі в одному partition; cluster не називається соціальною групою без доказу. |
| `ConversationInteraction` | `edge_id`, `from_comment_id`, `to_comment_id`, `interaction_type`, `evidence_span`, `raw_score`, `model/version`, `uncertainty_state` | Reply edge із платформних IDs відділяється від inferred agree/disagree edge. |
| `EngagementMetric` | `metric_id`, `comment_id`, `metric_name`, `numerator`, `denominator` + state, `value`, `snapshot_at`, `comment_age`, `source_receipt_id`, `method/version` | Не обчислювати rate за відсутнього знаменника; нуль відрізняється від hidden/unavailable. |
| `TemporalAudienceState` | `state_id`, `window_start/end`, `platform`, `unit`, `topic/target_id`, `label_counts`, `denominators`, `coverage`, `uncertainty_id`, `model_versions` | Один frozen binning definition на порівнювані серії; показувати composition/missingness. |
| `AnalysisUncertainty` | `uncertainty_id`, `scope_id`, `type` (classification/sampling/coverage/selection/measurement), `state`, `scenario`, `assumptions`, `range_or_interval`, `interval_type`, `provenance` | Сценарні межі не називати confidence interval; bootstrap не виправляє purposive sample. |
| `AudienceAnalyticalFinding` | `finding_id`, `statement`, `scope`, `estimate`, `numerator/denominator`, `evidence_ids`, `coverage`, `uncertainty_id`, `status`, `model_versions`, `generated_at` | Заборонити “населення/громадська думка” для comment sample; кожне число відтворюється з aggregate ID. |

У всіх записах `0`, `null`, `missing`, `hidden`, `unavailable`, `not_collected`, `partial` — різні стани. Платформа має бути джерелом будь-якого platform ID або лічильника; якщо поле не надається, схема зберігає його стан як unavailable/not_collected, а не синтезує значення.

Validator має відхиляти count=0 без receipt, що підтверджує observed zero; target-specific stance без target ID; finding “public opinion” із scope platform_comment_sample.

---

## 13. Експерименти E1–E11

Ручна експертна робота потрібна для замороженого benchmark та періодичних аудитів, але не в кожному incident run.

| Тест | Дизайн і метрики | Трактування негативного результату |
|---|---|---|
| **E1 Sentiment vs stance** | Один gold sample із target stance та sentiment; sentiment-only baseline проти target classifier. Per-class P/R/F1, macro-F1, confusion, risk–coverage. | Якщо stance не кращий — лишити sentiment описовим, stance обмежити або abstain. |
| **E2 Emotion models** | UA/RU/mixed окремо; lexicon, UkrRoberta/XLM-R/E5 fine-tune, один LLM. Per-label macro-F1, PR-AUC, Brier/ECE, slice CI, risk–coverage. | Не встановлювати універсальний поріг; оцінити error cost; слабку мітку відображати як невизначену або пропускати. |
| **E3 Topic discovery** | BERTopic/E5 vs NMF/LDA; repeat seeds/thread bootstrap; representative comments. CTC/NPMI, diversity, redundancy, stability, noise, blinded usefulness. | Coherence без стабільних зрозумілих examples — не проходить. |
| **E4 Reaction semantics** | Reaction type/count проти незалежно закодованих stance/targets у stratified samples; multilevel association і thread bootstrap. | Association не дозволяє конвертувати likes у support share без локальної валідації. |
| **E5 Engagement age bias** | Repeated snapshots: raw, same-age deltas, within-thread ranks, NB/GAM residual із age/platform/thread. | Без impressions не називати exposure-adjusted; нестійкі порівняння показати як raw/sensitivity. |
| **E6 Author concentration** | Comment-, author-, thread-, channel-balanced aggregates; top-author share; thread bootstrap. | Якщо відрізняються — показати всі; жоден не є “public opinion”. |
| **E7 Coordination sensitivity** | All comments vs exact/near duplicates, author cap, multi-signal clusters; прапорці зберігаються. | Авто-виключення за слабким signal — помилка; показувати deltas. |
| **E8 Temporal** | Fixed 1h/6h bins, frozen labels, event markers, adjust language/thread/platform mix. Counts, intervals, change-point stability. | Change point, що залежить від binning/composition, лишається exploratory; причинність не заявляти. |
| **E9 Sarcasm/context** | Held-out short replies, irony, quotes, negation, emoji-only, code-switch; parent context ablation. Per-slice F1, calibration, coverage. | Низька якість → abstain; не насильно змінювати polarity. |
| **E10 Cross-platform** | Leave-one-platform-out, train on A/test on B, duplicate/thread/author group splits. Per-platform macro-F1, calibration, risk–coverage. | Transfer drop вимагає platform-specific validation. |
| **E11 End-to-end report** | Frozen cases із omissions, conflicting replies, copy wave, changed snapshot. Trace every statement to aggregate/evidence. Metrics: unsupported-claim rate, denominator accuracy, evidence coverage, citation precision, contradiction retention, temporal consistency. | Report fail-closed без denominator/receipt або при conflict; допуски визначати до тесту. |

**Критерії прийняття експериментів:** універсального порога F1 для всіх класів тут немає. До прогону фіксуються витрати хибнопозитивної/хибнонегативної мітки й мінімальне потрібне покриття. E1/E2 проходять, якщо target-aware або emotion модель має кращий наперед визначений cost–coverage профіль за baseline на held-out групах (CI різниці не включає нуль); інакше лишається baseline/abstention. E3 проходить, якщо корисність і стабільність кластерів поліпшуються проти NMF/LDA baseline на відкладених підвибірках, а назви підтримуються прикладами. E4 проходить лише як локально валідований асоціативний сигнал у відповідних targets/threads; навіть тоді реакції не перетворюються на голоси. E5 проходить, якщо модель віку/часу краще калібрована на повторних snapshots; без impressions не заявляється exposure rate. E6/E7 проходять у частині прозорого розрахунку всіх сценаріїв; якщо знак/ранг висновку змінюється — результат позначається чутливим, а не вибирається зручний estimand. E8 приймає часову зміну як стійку лише коли вона не зникає за наперед заданих bin widths і sensitivity checks; це все одно не доводить причинність. E9 вимагає вимірного покращення на коротких/саркастичних/контекстних slices при відомому coverage; інакше відповідні випадки abstain. E10 не має загального pass для переносу: якість оцінюється окремо для кожної платформи, а cross-platform inference забороняється при значному незміряному drop. E11 є обов’язковим fail-closed тестом: кожен кількісний finding має коректний denominator, provenance та uncertainty state; жоден conflict/omission не маскується. Критерії і CI-метод фіксуються до запуску, щоб не підібрати правило після перегляду результату.

### Ground truth та leakage control

- Representative probability sample для prevalence плюс окремий challenge sample для рідкісних класів.
- Exact/near-copy clusters залишаються в одній partition; group split за thread та author; окремий cross-platform test.
- Два незалежні двомовні кодери маркують target, stance, emotion, sentiment, speech act, quote/sarcasm/context та incivility; третій adjudicates. Зберігати первісні та resolved labels.
- LLM може дати pre-label, але його голос не є незалежним human rater.
- Заморозити gold/challenge/OOD sets; кожна зміна моделі запускає regression tests. Нові кейси працюють автономно.

---

## 14. Мінімальний та розширений dashboard/report

### Мінімальний

1. Coverage: platforms, posts/videos, threads, comments, author IDs, capture window, snapshot, caps/pagination, selection, language.
2. Topics: 5–10 тем з denominator, top words, representative anonymized excerpts, stability/noise.
3. Target × stance: favor/against/neutral/no-stance/mixed/unclear; comment-weighted і author-balanced.
4. Emotion: multi-label by target/topic; no-discernible/unclear; “емоція, виражена текстом”.
5. Most engaged: окремо high likes, most replied, reaction-diverse; показати age/snapshot. Не називати most supported.
6. Timeline: counts і shares з N/coverage; incident event markers як час, не причина.
7. Sensitivity: all/deduped/author-balanced/multi-signal scenarios і deltas.
8. Limits: no population inference, missing/hidden reactions, selection, model validation status.

### Розширений

- Topic × emotion heatmap зі знаменниками.
- Target × stance matrix для claims/policies.
- Reply graph із типами взаємодії, не inferred ideology.
- Hostility/threat/disagreement/latency окремо.
- Polarization/diversity із формулами.
- Platform comparison із capture/missingness caveats.
- Repeated reaction snapshots/age.
- QA: model version, gold date/domain, slice metrics, drift, abstention.
- Evidence trace: aggregate → denominator → examples → sources → sensitivity.

---

## 15. Пріоритети реалізації

### P0 — коректність вимірювання

1. Розширити collectors: reaction type, snapshot time, access scope, missing states; звіряти platform reply counter із завантаженими. Файли: наявні src/tg_comments_collect.py, src/tiktok_public_collect.py, src/youtube_collect.py, src/instagram_collect.py.
2. Побудувати reply graph з parent IDs; виправити зведення всіх replies у один post URL. Точка: наявний src/analysis/tg_comment_signals.py; новий src/analysis/discussion_dynamics.py.
3. У кожному export фіксувати estimand, denominator, coverage; рахувати comment/author/thread/channel-balanced. Новий src/analysis/audience_aggregation.py.
4. Створити multilingual gold/challenge sets із split по thread/author/copy cluster.
5. Заборонити report labels “most supported” за сирим like/reply count.

### P1 — автономна надійність

1. Нові audience_context.py, audience_targets.py, audience_classification.py; target-aware labels і abstention.
2. Fine-tune/calibrate local classifiers; порівняти UkrRoberta/COSMUS, XLM-R, multilingual-E5, LLM baseline; зберігати model/hash/prompt versions.
3. Новий audience_topics.py: E5/BERTopic + NMF baseline, stability, representative comments.
4. Новий reaction_metrics.py: snapshots, age metadata, platform states, same-age deltas; exposure rate лише за реальних impressions.
5. Новий audience_quality.py: frozen benchmark, calibration/drift/regression, report provenance; інтеграція в наявні offline_case_runner.py/incident_orchestrator.py без implicit collection.
6. Відокремити impoliteness, threats, intolerance labels.

### P2 — додаткова глибина

- Hierarchical temporal models із thread/channel effects.
- Topic transition/OOD monitoring.
- Reaction semantics тільки після platform-specific validation.
- Не ідентифікувати авторів між платформами за схожістю імен.
- Dashboard із перемикачами weights/sensitivity.

Completion criteria: deterministic replay; missingness schema; знаменник кожного відсотка; leakage-free evaluation; UA/RU/mixed/platform metrics; measured risk–coverage; sensitivity scenarios не видаляють прапорцеві дані; report findings traceable до aggregates/evidence.

---

## 16. Обмеження висновків

### Можна

- теми, claims і позиції в зібраних коментарях;
- емоції, виявлені в тексті, з відомим покриттям/помилкою;
- reaction counts для зібраних коментарів на timestamp;
- часові відмінності в покритих threads/platforms;
- чутливість агрегатів до weights/dedup/coordination assumptions;
- місця з недостатнім контекстом або конфліктними позиціями.

### Не можна лише на цій підставі

- оцінювати частку населення України, що підтримує позицію;
- ототожнювати лайки зі згодою або replies із підтримкою;
- визначати внутрішні емоції, мотиви чи політичну ідентичність авторів;
- робити причинний висновок про вплив публікації;
- виводити comment impressions із views/followers;
- називати coordination flag доказом бота/операції;
- вважати недоступну реакцію нулем;
- називати суму views унікальними людьми.

---

## 17. Верифікована бібліографія та документація

### Sentiment, stance, emotion, multilingual NLP

1. Mohammad, S. M., Sobhani, P. & Kiritchenko, S. (2017). [Stance and Sentiment in Tweets](https://doi.org/10.1145/3003433). *ACM Transactions on Internet Technology*, 17(3), Article 25. DOI: 10.1145/3003433. (Preprint: arXiv:1605.01655, 2016.)
2. Rogers, A. et al. (2018). [RuSentiment: An Enriched Sentiment Analysis Dataset for Social Media in Russian](https://aclanthology.org/C18-1064/). COLING.
3. Demszky, D. et al. (2020). [GoEmotions: A Dataset of Fine-Grained Emotions](https://aclanthology.org/2020.acl-main.372/). ACL.
4. Barbieri, F. et al. (2020). [TweetEval: Unified Benchmark and Comparative Evaluation for Tweet Classification](https://aclanthology.org/2020.findings-emnlp.148/). Findings EMNLP.
5. Allaway, E. & McKeown, K. (2020). [Zero-Shot Stance Detection: A Dataset and Model using Generalized Topic Representations](https://aclanthology.org/2020.emnlp-main.717/). EMNLP.
6. Vamvas, J. & Sennrich, R. (2020). [X-Stance: A Multilingual Multi-Target Dataset for Stance Detection](https://arxiv.org/abs/2003.08385). SwissText/KONVENS 2020; CEUR Workshop Proceedings, vol. 2624.
7. Öhman, E. et al. (2020). [XED: A Multilingual Dataset for Sentiment Analysis and Emotion Detection](https://aclanthology.org/2020.coling-main.575/). COLING.
8. Sboev, A. et al. (2021). [Data-Driven Model for Emotion Detection in Russian Texts](https://doi.org/10.1016/j.procs.2021.06.075). Procedia Computer Science; CEDR.
9. Bestvater, S. & Monroe, B. (2023). [Sentiment is Not Stance](https://doi.org/10.1017/pan.2022.10). Political Analysis.
10. Shynkarov, Y. et al. (2025). [Improving Sentiment Analysis for Ukrainian Social Media Code-Switching Data](https://aclanthology.org/2025.unlp-1.18/). UNLP.
11. Dementieva, D. et al. (2025). [EmoBench-UA: A Benchmark Dataset for Emotion Detection in Ukrainian](https://aclanthology.org/2025.findings-emnlp.107/). Findings EMNLP.
12. Hardalov, M. et al. (2022). [Few-Shot Cross-Lingual Stance Detection with Sentiment-Based Pre-Training](https://aclanthology.org/2022.findings-emnlp.193/). Findings EMNLP.
13. Ghosh, D. et al. (2018). [Sarcasm Analysis Using Conversation Context](https://aclanthology.org/J18-4009/). TACL.
14. Gu, F. et al. (2026). [Large Language Models Are Effective Human Annotation Assistants, But Not Good Independent Annotators](https://aclanthology.org/2026.findings-acl.4/). Findings ACL.
15. Ziems, C. et al. (2024). [Can Large Language Models Transform Computational Social Science?](https://aclanthology.org/2024.cl-1.8/). Computational Linguistics.
16. Pendzel, S. et al. (2024). [A Closer Look at Multidimensional Online Political Incivility](https://aclanthology.org/2024.emnlp-main.827/). EMNLP.
17. Dementieva, D. et al. (2024). [Toxicity Classification in Ukrainian](https://aclanthology.org/2024.woah-1.19/). WOAH.
18. Joseph, K. et al. (2021). [(Mis)alignment Between Stance Expressed in Social Media Data and Public Opinion Surveys](https://aclanthology.org/2021.emnlp-main.27/). EMNLP.

### Topic discovery and polarization

19. Rahimi, H. et al. (2024). [Contextualized Topic Coherence Metrics](https://aclanthology.org/2024.findings-eacl.123/). Findings EACL.
20. Egger, R. & Yu, J. (2022). [A Topic Modeling Comparison Between LDA, NMF, Top2Vec, and BERTopic to Demystify Twitter Posts](https://doi.org/10.3389/fsoc.2022.886498). Frontiers in Sociology.
21. Medvecki, D. et al. (2024). [Multilingual transformer and BERTopic for short text topic modeling: The case of Serbian](https://arxiv.org/abs/2402.03067). Preprint; adjacent-language evidence, not UA validation.
22. Lerman, K., Feldman, D., He, Z. & Rao, A. (2024). [Affective Polarization and Dynamics of Information Spread in Online Networks](https://www.nature.com/articles/s44260-024-00008-w). npj Complexity.
23. Alvarez-Gonzalez, N., Kaltenbrunner, A. & Gómez, V. (2021). [Uncovering the Limits of Text-based Emotion Detection](https://aclanthology.org/2021.findings-emnlp.219/). Findings EMNLP.

### Reactions and engagement

24. Sumner, E. et al. (2018). [A Functional Approach to the Facebook Like Button](https://doi.org/10.1177/1461444817697917). New Media & Society.
25. Sumner, E. et al. (2020). [Assessing the Cognitive and Communicative Properties of Facebook Reactions and Likes](https://doi.org/10.5210/fm.v25i2.9621). First Monday.
26. Paolillo, J. (2023). [The Awkward Semantics of Facebook Reactions](https://doi.org/10.5210/fm.v28i8.13157). First Monday.
27. Muchnik, L., Aral, S. & Taylor, S. (2013). [Social Influence Bias: A Randomized Experiment](https://doi.org/10.1126/science.1240466). Science.
28. Vassio, L. et al. (2022). [Mining and Modelling Temporal Dynamics of Followers’ Engagement](https://doi.org/10.1007/s13278-022-00928-2). Social Network Analysis and Mining.
29. Barger, V. et al. (2022). [Conceptualising and Measuring Social Media Engagement: A Systematic Literature Review](https://doi.org/10.1007/s43039-021-00035-8).
30. Masullo, G. (2022). [Facebook Reactions as Heuristics](https://doi.org/10.5210/fm.v27i8.12674). First Monday.
31. Guess, A. et al. (2023). [How Do Social Media Feed Algorithms Affect Attitudes and Behavior in an Election Campaign?](https://doi.org/10.1126/science.abp9364). Science. Дивитися разом із [erratum 2026](https://doi.org/10.1126/science.aeh2575): він виправив облік carousel-контенту Instagram та деякі контентні метрики; автори повідомили, що основні експериментальні оцінки ефекту не змінилися.
32. Milli, S. et al. (2025). [Engagement, User Satisfaction, and the Amplification of Divisive Content on Social Media](https://doi.org/10.1093/pnasnexus/pgaf062). PNAS Nexus; X experiment, not direct evidence about Social’s feeds.

### Official APIs

33. Telegram [Bot API](https://core.telegram.org/bots/api), [reactions](https://core.telegram.org/api/reactions), [discussion groups](https://core.telegram.org/api/discussion).
34. YouTube Data API [comments](https://developers.google.com/youtube/data/reference/rest/v3/comments), [commentThreads](https://developers.google.com/youtube/data/reference/rest/v3/commentThreads), [video statistics](https://developers.google.com/youtube/data/reference/rest/v3/videos).
35. TikTok Research API [video comments](https://developers.tiktok.com/docs/en/research-api-specs-query-video-comments), [research access](https://developers.tiktok.com/docs/en/about-research-api), [FAQ](https://developers.tiktok.com/docs/en/research-api-faq).
36. Instagram [comment moderation docs](https://developers.facebook.com/docs/instagram-platform/instagram-api-with-instagram-login/comment-moderation/).
37. Meta [Content Library/API announcement and updates](https://about.fb.com/news/2023/11/new-tools-to-support-independent-research/).
38. Tardelli, S., Alvisi, L., Cima, L., Cresci, S. & Tesconi, M. (2025). [Emoji Reactions on Telegram: Unreliable Indicators of Emotional Resonance](https://arxiv.org/abs/2508.06349). arXiv preprint, v2, 19 December 2025; not peer-reviewed as of this review.

---

## Загальний висновок

Social уже має collectors, псевдонімізацію, parent metadata та coordination signals. Науково виправданий наступний крок — додати окремі target-aware шари topic, claim, stance, sentiment, emotion, hostility та engagement. Спершу потрібно забезпечити коректні знаменники, reply graph, reaction snapshots і frozen validation sets. Далі багатомовні моделі можуть автономно обробляти нові кейси з вимірюваним abstention. Звіт має описувати реакції відібраних цифрових аудиторій, не підміняючи ними суспільну думку.

