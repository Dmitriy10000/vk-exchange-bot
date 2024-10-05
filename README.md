# VKCoin бот на языке python

## Инструкция к файлу config.json
* `token` - токен сообщества вк
* `DB` - данные для подключения к базе данных
    * `user` (string) - пользователь базы данных
    * `host` (string) - хост базы данных
    * `name` (string) - название базы данных
    * `pass` (string) - пароль базы данных
    * `port` (string) - порт базы данных
* `market_config` - настройки магазина
    * `sell_is_enabled` (boolean) - включена ли продажа vkc
    * `buy_is_enabled` (boolean) - включена ли покупка vkc
    * `sell_price` (int) - цена продажи vkc (указана в копейках)
    * `buy_price` (int) - цена покупки vkc (указана в копейках)
    * `coin_amount` (int) - количество vkc, которое вы хотите купить/продать за указанные выше суммы
    * `seller` (string) - ник продавца
* `merchant_config` - настройки аккаунта с резервом vkc
    * `merchant_id` (int) - id аккаунта на котором хранится резерв vkc
    * `merchant_key` (string) - [токен для платежного API VKCoin](https://vk.com/coin#create_merchant)
* `qiwi` - настройки qiwi
    * `token` (string) - [токен qiwi кошелька](https://qiwi.com/api)
    * `secret_key` (string) - секретный ключ qiwi кошелька
    * `public_key` (string) - публичный ключ qiwi кошелька

Ключи создаются в личном кабинете после регистрации и подключения на kassa.qiwi.com или p2p.qiwi.com.