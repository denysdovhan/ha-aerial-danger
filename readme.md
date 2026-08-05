[![SWUbanner](https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-direct-single.svg)](https://stand-with-ukraine.pp.ua/)

<!-- markdownlint-disable no-inline-html -->
<h1 align="center">
  <img alt="Логотип HA Aerial Danger" src="./assets/logo.png" width="250px">
  <br />
  💥 HA Aerial Danger
</h1>
<!-- markdownlint-enable no-inline-html -->

[![GitHub Release][gh-release-image]][gh-release-url]
[![GitHub Downloads][gh-downloads-image]][gh-downloads-url]
[![hacs][hacs-image]][hacs-url]
[![GitHub Sponsors][gh-sponsors-image]][gh-sponsors-url]
[![Buy Me A Coffee][buymeacoffee-image]][buymeacoffee-url]
[![Twitter][twitter-image]][twitter-url]

[**Українською**](./readme.md) | [English](./readme.en.md)

> [!NOTE]
> Інтеграція [Home Assistant][home-assistant] для виявлення повітряних загроз, що стосуються вибраних регіонів і місцевостей України.

## Про інтеграцію

**Aerial Danger** аналізує повідомлення про повітряні загрози та визначає, чи стосуються вони вибраних регіонів або місцевостей.

Інтеграція виявляє БРСД[^1], РСЗВ[^2], КАБ[^3], балістичні й крилаті ракети, дрони та невстановлені повітряні загрози.

Aerial Danger не завантажує повідомлення самостійно. Інтеграція аналізує текстовий стан вибраних сутностей Home Assistant. Наприклад, такі сутності можна створити з публічних Telegram-каналів за допомогою інтеграції [Scrape][scrape-url].

> [!CAUTION]
> **Інтеграція може помилятися, пропускати повідомлення або виявляти їх із запізненням.**
>
> Не використовуйте її як єдине чи офіційне джерело сповіщень.
>
> Завжди стежте за офіційними сповіщеннями та виконуйте їхні вказівки. Під час повітряної тривоги негайно прямуйте до найближчого укриття та залишайтеся там до офіційного відбою.
>
> Інтеграція надається «як є». Автор не гарантує точність, повноту чи своєчасність даних і не несе відповідальності за безпеку користувачів, ухвалені рішення чи наслідки використання інтеграції.

## Підтримати проєкт

Ваша підтримка допомагає розвивати цей та інші українські проєкти для Home Assistant.

- 💖 [GitHub Sponsors][gh-sponsors-url]
- ☕️ [Buy Me A Coffee][buymeacoffee-url]
- Bitcoin: `bc1q7lfx6de8jrqt8mcds974l6nrsguhd6u30c6sg8`
- Ethereum: `0x6aF39C917359897ae6969Ad682C14110afe1a0a1`

## Встановлення

Найпростіший спосіб встановити інтеграцію — через [HACS][hacs-url]:

[![Додати до HACS через My Home Assistant][hacs-install-image]][hacs-install-url]

<details>
  <summary>Якщо кнопка не працює, додайте репозиторій вручну</summary>

1. Відкрийте **HACS → Інтеграції**.
2. Відкрийте меню **⋮ → Користувацькі репозиторії**.
3. Вставте `https://github.com/denysdovhan/ha-aerial-danger`.
4. Виберіть категорію **Integration** і натисніть **Add**.
5. Знайдіть **Aerial Danger**, встановіть інтеграцію та перезапустіть Home Assistant.

</details>

## Налаштування джерел повідомлень

Для роботи Aerial Danger потрібне щонайменше одне джерело повідомлень з актуальним текстом повідомлення про загрозу.

Інтеграція підтримує сутності доменів `sensor`, `text` та `input_text`. Вона аналізує лише стан сутності, тому він має містити текст самого повідомлення.

> [!WARNING]
> Користувачі самостійно обирають джерела повідомлень. Інтеграція не перевіряє достовірність або повноту даних і не гарантує своєчасність сповіщень.

Як джерела повідомлень можна використовувати публічні моніторингові Telegram-канали, наприклад:

| Канал                                                             | Адреса                              |
| ----------------------------------------------------------------- | ----------------------------------- |
| [Повітряні Сили ЗСУ](https://telegram.me/s/kpszsu)                | `https://telegram.me/s/kpszsu`      |
| [War Monitor](https://telegram.me/s/war_monitor)                  | `https://telegram.me/s/war_monitor` |
| [Aeris Rimor](https://telegram.me/s/AerisRimor)                   | `https://telegram.me/s/AerisRimor`  |
| [Оперативний інформ](https://telegram.me/s/operinform)            | `https://telegram.me/s/operinform`  |
| [Kyiv Air Defence](https://telegram.me/s/kyiv_airdef) (лише Київ) | `https://telegram.me/s/kyiv_airdef` |

Читати повідомлення з Telegram-каналів можна за допомогою інтеграції [Scrape][scrape-url].

### Створіть Scrape-сенсор для Telegram-каналу

Створіть окремий запис інтеграції [Scrape][scrape-url] для кожного потрібного каналу:

[![Додати інтеграцію Scrape][scrape-install-image]][scrape-install-url]

<details>
  <summary>Якщо кнопка не працює, налаштуйте запис вручну</summary>

1. Відкрийте **Налаштування → Пристрої та служби → Додати інтеграцію**.
2. Виберіть **Scrape**.
3. Вкажіть URL каналу у форматі `https://telegram.me/s/CHANNEL`.

</details>

Для каналу Повітряних сил ЗСУ заповніть основні параметри так:

| Параметр | Значення                       |
| -------- | ------------------------------ |
| Ресурс   | `https://telegram.me/s/kpszsu` |
| Метод    | `GET`                          |

На наступному кроці додайте сенсор:

| Параметр                                 | Значення                                                 |
| ---------------------------------------- | -------------------------------------------------------- |
| Назва                                    | `Повітряні Сили ЗСУ Telegram`                            |
| CSS-селектор                             | `.js-widget_message_wrap:last-child .js-message_text`    |
| Додаткові налаштування → Шаблон значення | `{{ value \| trim \| truncate(255, end='', leeway=0) }}` |

Шаблон прибирає зайві пробіли та обмежує стан сенсора до 255 символів — максимальної довжини стану сутності Home Assistant.

Повторіть ці кроки для кожного потрібного каналу.

### Оновлюйте дані створених сенсорів частіше

Scrape за замовчуванням опитує ресурс кожні 600 секунд (10 хвилин). Для сповіщень про повітряні загрози цей інтервал може бути надто довгим.

Імпортуйте готовий шаблон автоматизації, а потім виберіть створені Scrape-сенсори та інтервал оновлення — 5 або 10 секунд:

[![Імпортувати автоматизацію для Telegram-сенсорів][blueprint-install-image]][telegram-scrape-blueprint-install-url]

<details>
  <summary>Якщо кнопка не працює, створіть автоматизацію вручну</summary>

```yaml
alias: Оновлення Telegram-сенсорів кожні 5 секунд
description: Примусово оновлює джерела повідомлень для Aerial Danger
triggers:
  - trigger: time_pattern
    seconds: "/5"
conditions: []
actions:
  - action: homeassistant.update_entity
    target:
      entity_id:
        - sensor.telegram_kpszsu
mode: single
max_exceeded: silent
```

> [!IMPORTANT]
> Замініть `sensor.telegram_kpszsu` на фактичний ідентифікатор свого сенсора. Для кількох каналів додайте всі сутності до списку `entity_id`.

> [!TIP]
> Щоб зменшити кількість запитів, оновлюйте сенсори лише під час активної повітряної тривоги. У готовому шаблоні для цього можна вибрати сенсори безпеки **Повітряна тривога** з інтеграції [Ukraine Alarm][ukraine-alarm-url]. Якщо створюєте автоматизацію вручну, додайте відповідну перевірку до блоку `conditions`.

</details>

## Налаштування Aerial Danger

Додайте запис інтеграції **Aerial Danger (Повітряна загроза)**:

[![Налаштувати Aerial Danger][aerial-danger-install-image]][aerial-danger-install-url]

<details>
  <summary>Якщо кнопка не працює, налаштуйте інтеграцію вручну</summary>

1. Відкрийте **Налаштування → Пристрої та служби → Додати інтеграцію**.
2. Знайдіть і виберіть **Aerial Danger**.

</details>

1. Задайте назву запису. За замовчуванням використовується назва вашого дому.
2. Оберіть одне або кілька джерел повідомлень про загрози.
3. Оберіть готові регіони й місцевості або додайте власні регулярні вирази.

### Налаштування регіонів та місцевостей

**Регіони** використовуються для виявлення балістичних і крилатих ракет та інших швидких загроз.

**Місцевості** потрібні для виявлення РСЗВ[^2], КАБ[^3] і дронів. Вони також використовуються для всіх інших типів загроз.

Готові регіони та місцевості можна поєднувати з власними [регулярними виразами Python][python-regex-url] у форматі списку YAML:

```yaml
- (до|на) нас
- наш(у|ої) област(ь|і)?
```

> [!IMPORTANT]
> Оберіть щонайменше одне джерело повідомлень та щонайменше один регіон або одну місцевість.

> [!TIP]
> Рекомендуємо обрати свою та сусідні місцевості, щоб отримувати повідомлення про наближення цілей.

Створіть кілька незалежних записів інтеграції, якщо для різних територій потрібні різні джерела або правила виявлення.

## Створені сутності

Кожен запис інтеграції створює такі сутності:

| Сенсори небезпек              | Діагностичні сенсори               |
| ----------------------------- | ---------------------------------- |
| ![](./assets/danger-demo.png) | ![](./assets/diagnostics-demo.png) |

Як працюють ці сутності:

| Тип                  | Сутності                                                                               | Призначення                                       |
| -------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------- |
| Сенсори небезпеки    | БРСД[^1], РСЗВ[^2], КАБ[^3], балістика, крилаті ракети, дрони, невстановлена небезпека | Показують активну загрозу відповідного типу       |
| Загальний сенсор     | **Небезпека**                                                                          | Увімкнений, доки активний хоча б один тип загрози |
| Діагностичні сенсори | Виявлене повідомлення, територія, тип загрози та джерело повідомлень                   | Показують дані останнього активного виявлення     |
| Сутність подій       | **Виявлена небезпека**                                                                 | Реєструє кожне нове виявлення для автоматизацій   |

Усі бінарні сенсори мають стабільні атрибути:

| Атрибут            | Значення                                                             |
| ------------------ | -------------------------------------------------------------------- |
| `matched_message`  | Повний текст повідомлення, у якому виявлено загрозу                  |
| `matched_area`     | Частина повідомлення, що збіглася з вибраним регіоном або місцевістю |
| `matched_danger`   | Частина повідомлення, що вказує на тип загрози                       |
| `source_entity_id` | Ідентифікатор сутності, з якої надійшло повідомлення                 |

Для загрози БРСД[^1] сенсор території показує **Вся країна**, оскільки такі повідомлення вважаються загальнонаціональними.

## Автоматизації та сповіщення

Основне призначення інтеграції — запускати автоматизації та критичні сповіщення після виявлення загрози.

### Критичні сповіщення

Імпортуйте готовий шаблон і створіть із нього автоматизацію критичних сповіщень:

[![Імпортувати шаблон для критичних сповіщень][blueprint-install-image]][critical-notification-blueprint-install-url]

Під час створення автоматизації:

1. Оберіть пристрій **Повітряної загрози**.
2. Оберіть мобільний пристрій із застосунком Home Assistant.
3. Задайте затримку між повторними сповіщеннями.

Шаблон надсилає критичні сповіщення на iOS та сповіщення з високим пріоритетом на Android. Текст містить виявлену територію та повне повідомлення про загрозу.

### Вбудовані тригери

Щоб створити власну автоматизацію, додайте тригер, оберіть пристрій **Aerial Danger**, а потім потрібний тип виявлення:

- **Виявлено будь-яку небезпеку**
- **Виявлено небезпеку БРСД**
- **Виявлено небезпеку РСЗВ**
- **Виявлено небезпеку КАБ**
- **Виявлено балістичну небезпеку**
- **Виявлено небезпеку крилатих ракет**
- **Виявлено небезпеку дронів**
- **Виявлено невстановлену небезпеку**

> [!IMPORTANT]
> Тригери спрацьовують для кожного відповідного виявлення, зокрема для повторних повідомлень того самого типу.

## Як працює виявлення

1. Інтеграція реагує на зміну текстового стану кожної вибраної сутності та не опитує зовнішні джерела самостійно.
2. У кожному повідомленні інтеграція шукає ключові слова загроз і згадки вибраних регіонів або місцевостей.
3. Для кожного джерела зберігається перший знайдений тип небезпеки.
   1. БРСД[^1] не потребує згадки місцевості чи регіону.
   2. РСЗВ[^2], КАБ[^3] і дрони потребують назви місцевості.
   3. Решта типів загроз — або регіону, або місцевості.
4. Стан залишається активним, доки з того самого джерела не надійде нове повідомлення без загрози.
5. Джерела обробляються незалежно: повідомлення без загрози очищає стан лише свого джерела.
6. Кожне нове виявлення, зокрема повторне повідомлення того самого типу, оновлює сутність подій і діагностичні сенсори.

## Часті питання

### Чому інтеграція не отримує повідомлення самостійно?

Джерела для різних регіонів і місцевостей відрізняються. Ви самі обираєте потрібні джерела, а Aerial Danger лише аналізує текст їхніх станів.

### Чому для аналізу не використовується штучний інтелект?

ШІ-моделі можуть пропустити небезпеку, помилково відреагувати на безпечне повідомлення або затримати результат. Регулярні вирази та ключові слова простіші, але працюють передбачувано й майже миттєво.

### Як додати відсутній регіон або місцевість?

1. Створіть [регулярний вираз][python-regex-url], який враховує різні форми назви. Наприклад: `київ`, `києва`, `києві`, `києвом`.
2. Перевірте вираз у [пісочниці для регулярних виразів](https://regexr.com/).
3. Додайте вираз до налаштувань інтеграції.
4. Щоб поділитися ним з іншими користувачами, додайте його до [переліку місцевостей][presets] і надішліть [пул-реквест][contributing].

## Вирішення проблем

- **Джерело порожнє або має стан `unavailable`.** Перевірте URL, CSS-селектор і доступність публічного каналу без авторизації.
- **Загроза не виявляється.** Переконайтеся, що вибрана сутність містить текст повідомлення, а повідомлення згадує налаштований регіон або місцевість. Для БРСД згадка території не потрібна.
- **Оновлення каналів створює надто багато запитів.** Виберіть у шаблоні інтервал 10 секунд, залиште лише потрібні канали або обмежте оновлення часом активної тривоги через Ukraine Alarm.
- **Потрібно змінити джерела або території.** Відкрийте **Налаштування → Пристрої та служби → Aerial Danger → Налаштувати**.

## Видалення

Щоб видалити запис Aerial Danger:

1. Відкрийте **Налаштування → Пристрої та служби → Aerial Danger**.
2. Відкрийте меню **⋮** біля потрібного запису та виберіть **Видалити**.

Запис інтеграції видаляється разом зі своїми сутностями. Scrape-сенсори, автоматизації та файли інтеграції в HACS потрібно видалити окремо, якщо вони більше не потрібні.

## Розробка

Хочете допомогти проєкту? Дякуємо! Перегляньте [настанови для учасників][contributing].

## Ліцензія

[Ліцензія MIT](./license.md) © [Денис Довгань][denysdovhan].

<!-- Footnotes -->

[^1]: БРСД — балістична ракета середньої дальності (англ. IRBM — intermediate-range ballistic missile)

[^2]: РСЗВ — реактивна система залпового вогню (англ. MLRS — multiple launch rocket system)

[^3]: КАБ — керована авіаційна бомба (англ. GAB — guided aerial bomb)

<!-- Badges -->

[gh-release-url]: https://github.com/denysdovhan/ha-aerial-danger/releases/latest
[gh-release-image]: https://img.shields.io/github/v/release/denysdovhan/ha-aerial-danger?style=flat-square
[gh-downloads-url]: https://github.com/denysdovhan/ha-aerial-danger/releases
[gh-downloads-image]: https://img.shields.io/github/downloads/denysdovhan/ha-aerial-danger/total?style=flat-square
[hacs-url]: https://github.com/hacs/integration
[hacs-image]: https://img.shields.io/badge/hacs-custom-orange.svg?style=flat-square
[gh-sponsors-url]: https://github.com/sponsors/denysdovhan
[gh-sponsors-image]: https://img.shields.io/github/sponsors/denysdovhan?style=flat-square
[buymeacoffee-url]: https://buymeacoffee.com/denysdovhan
[buymeacoffee-image]: https://img.shields.io/badge/support-buymeacoffee-222222.svg?style=flat-square
[twitter-url]: https://x.com/denysdovhan
[twitter-image]: https://img.shields.io/badge/follow-%40denysdovhan-000000.svg?style=flat-square

<!-- References -->

[home-assistant]: https://www.home-assistant.io/
[denysdovhan]: https://github.com/denysdovhan
[hacs-install-url]: https://my.home-assistant.io/redirect/hacs_repository/?owner=denysdovhan&repository=ha-aerial-danger&category=integration
[hacs-install-image]: https://my.home-assistant.io/badges/hacs_repository.svg
[scrape-url]: https://www.home-assistant.io/integrations/scrape/
[scrape-install-url]: https://my.home-assistant.io/redirect/config_flow_start?domain=scrape
[scrape-install-image]: https://my.home-assistant.io/badges/config_flow_start.svg
[ukraine-alarm-url]: https://www.home-assistant.io/integrations/ukraine_alarm/
[aerial-danger-install-image]: https://my.home-assistant.io/badges/config_flow_start.svg
[aerial-danger-install-url]: https://my.home-assistant.io/redirect/config_flow_start/?domain=aerial_danger
[blueprint-install-image]: https://my.home-assistant.io/badges/blueprint_import.svg
[telegram-scrape-blueprint-install-url]: https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdenysdovhan%2Fha-aerial-danger%2Fblob%2Fmain%2Fblueprints%2Ftelegram_scrape_refresh.yaml
[critical-notification-blueprint-install-url]: https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fdenysdovhan%2Fha-aerial-danger%2Fblob%2Fmain%2Fblueprints%2Faerial_danger_critical_notification.yaml
[python-regex-url]: https://docs.python.org/3/library/re.html
[contributing]: ./contributing.md
[presets]: https://github.com/denysdovhan/ha-aerial-danger/blob/main/custom_components/aerial_danger/danger/presets.py
