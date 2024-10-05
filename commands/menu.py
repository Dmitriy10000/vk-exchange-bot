from vkbottle.bot import Bot, Message
from commands import db, keyboards, vkc, cfg, qiwi


config = cfg.update()
token = config["token"]
bot = Bot(token)


# Подключаемся к БД
conn = db.connect_to_db()
cursor = conn.cursor()


# Кнопка "Начать"
async def start_handler(message: Message):
    # Проверка существования пользователя в БД
    temp = "select exists(select * from users where user_id = " + str(message.from_id) + ")"
    cursor.execute(temp)
    is_user = cursor.fetchall()[0][0]
    if is_user == False:
        users_info = await bot.api.users.get(message.from_id)
        # Добавляем пользователя в БД
        try:
            temp = "insert into users (user_id, first_name, last_name) values (" + str(message.from_id) + ", '" + users_info[0].first_name + "', '" + users_info[0].last_name + "') on conflict do nothing"
            cursor.execute(temp)
            conn.commit()
            print("Пользователь {} {} успешно добавлен в базу данных".format(users_info[0].first_name, users_info[0].last_name))
        except Exception as e:
            print("Ошибка добавления пользователя в базу данных: " + str(e))
    await message.answer("Привет, {}!".format(users_info[0].first_name), keyboard=keyboards.KEYBOARD_MAIN)


# Кнопка "Курс"
async def course_handler(message: Message):
    config = cfg.update()
    temp = "select location_id from users where user_id = " + str(message.from_id)
    cursor.execute(temp)
    location_id = cursor.fetchall()[0][0]

    if location_id == 0 or location_id == 10:
        # Кол-во пользователей бота
        cursor.execute("select count(*) from users")
        user_count = cursor.fetchall()[0][0]
        
        # Приводим число config["market_config"]["coin_amount"] к формату 1.000.000
        coin_amount = "{:,}".format(config["market_config"]["coin_amount"]).replace(",", ".")
        
        # Общий оборот VKC и RUB
        cursor.execute("select * from transactions where status = 'success'")
        transactions = cursor.fetchall()
        vkc_turnover = 0
        rub_turnover = 0
        if len(transactions) != 0:
            for transaction in transactions:
                vkc_turnover += transaction[2]
                rub_turnover += transaction[3]
            vkc_turnover = "{:,}".format(vkc_turnover).replace(",", ".")
            rub_turnover /= 100
            rub_turnover = "{:,}".format(rub_turnover).replace(",", ".")
        
        # Общее кол-во транзакций
        transactions_count = len(transactions)

        # Получаем резерв VKC
        reserve_vkc = vkc.get_shop_balance()
        reserve_vkc = "{:,}".format(reserve_vkc).replace(",", ".")  # Приводим число reserve_vkc к формату 1.000.000

        # Получаем резерв RUB
        reserve_rub = qiwi.get_balance()
        # Приводим число reserve_rub к формату 1 000 000 и округляем до целого в меньшую сторону
        reserve_rub = "{:,}".format(round(reserve_rub)).replace(",", " ")

        text = (
            "[ 📊 ] Информация:\n\n" +

            "[ 👥 ] Пользователей: " + str(user_count) + " \n\n" +

            "📥Продаем: " + str(config["market_config"]["buy_price"]/100) + " RUB за " + str(coin_amount) + " VkCoin\n" +
            "📥Скупаем: " + str(config["market_config"]["sell_price"]/100) + " RUB за " + str(coin_amount) + " VkCoin\n\n" +

            "💰Резерв: " + str(reserve_rub) + " RUB\n" +
            "💰Резерв VKCOIN: " + str(reserve_vkc) + " VKC\n\n" +

            "Другие Способы оплаты - " + str(config["market_config"]["seller"]) + "\n\n" +

            "🚀Оборот: " + str(vkc_turnover) + " VKCOIN (" + str(rub_turnover) + " RUB)\n" +
            "Всего сделок: " + str(transactions_count) + "\n\n" +
            
            "Разработчик: @id258714686")
        
        # Проверка на админа
        temp = "select is_admin from users where user_id = " + str(message.from_id)
        cursor.execute(temp)
        is_admin = cursor.fetchall()[0][0]
        if is_admin == True:
            await message.answer(text, keyboard=keyboards.KEYBOARD_ADMIN)
        else:
            await message.answer(text, keyboard=keyboards.KEYBOARD_MAIN)


# Кнопка "Отзывы"
async def reviews_handler(message: Message):
    temp = "select location_id from users where user_id = " + str(message.from_id)
    cursor.execute(temp)
    location_id = cursor.fetchall()[0][0]
    if location_id == 0 or location_id == 10:
        text = (
            """
            😧 Сомневаетесь в нашей честности?
            Тогда посмотрите на отзывы наших клиентов!
            - https://vk.com/topic-216221455_49070217
            """)
        
        # Проверка на админа
        temp = "select is_admin from users where user_id = " + str(message.from_id)
        cursor.execute(temp)
        is_admin = cursor.fetchall()[0][0]
        if is_admin == True:
            await message.answer(text, keyboard=keyboards.KEYBOARD_ADMIN)
        else:
            await message.answer(text, keyboard=keyboards.KEYBOARD_MAIN)


# Кнопка "Профиль"
async def profile_handler(message: Message):
    temp = "select location_id from users where user_id = " + str(message.from_id)
    cursor.execute(temp)
    location_id = cursor.fetchall()[0][0]
    if location_id == 0 or location_id == 10:
        users_info = await bot.api.users.get(message.from_id)
        # select sum(vkc_amount) from transactions where user_id = 216738936 and type = 'buy' and status = 'success';
        temp = "select sum(vkc_amount) from transactions where user_id = " + str(message.from_id) + " and type = 'buy' and status = 'success'"
        cursor.execute(temp)
        vkc_buy = cursor.fetchall()[0][0]
        if vkc_buy == None:
            vkc_buy = 0
        else:
            # Приводим число vkc_buy к формату 1.000.000
            vkc_buy = "{:,}".format(vkc_buy).replace(",", ".")
        # select sum(vkc_amount) from transactions where user_id = 216738936 and type = 'sell' and status = 'success';
        temp = "select sum(vkc_amount) from transactions where user_id = " + str(message.from_id) + " and type = 'sell' and status = 'success'"
        cursor.execute(temp)
        vkc_sell = cursor.fetchall()[0][0]
        if vkc_sell == None:
            vkc_sell = 0
        else:
            # Приводим число vkc_sell к формату 1.000.000
            vkc_sell = "{:,}".format(vkc_sell).replace(",", ".")
        # select count(*) from transactions where user_id = 216738936 and status = 'success';
        temp = "select count(*) from transactions where user_id = " + str(message.from_id) + " and status = 'success'"
        cursor.execute(temp)
        transaction_count = cursor.fetchall()[0][0]
        # qiwi number
        temp = "select qiwi from users where user_id = " + str(message.from_id)
        cursor.execute(temp)
        qiwi = cursor.fetchall()[0][0]
        text = (
            "[ 💰 ] Ваш профиль:\n" +
            "[ 🤑 ] Всего вы купили: " + str(vkc_buy) + " VKCoin\n" + 
            "[ 🤑 ] Всего вы продали: " + str(vkc_sell) + " VKCoin\n\n" +
            "Сделок: " + str(transaction_count) + "\n" +
            "Qiwi: "
        )
        if qiwi == None:
            text += "Не указан"
        else:
            text += "+" + str(qiwi)
        temp = "update users set location_id = 5 where user_id = " + str(message.from_id)
        cursor.execute(temp)
        conn.commit()
        await message.answer(text, keyboard=keyboards.KEYBOARD_PROFILE)


# Кнопка "Купить VKC"
async def buy_handler(message: Message):
    config = cfg.update()
    temp = "select location_id from users where user_id = " + str(message.from_id)
    cursor.execute(temp)
    location_id = cursor.fetchall()[0][0]
    if location_id == 0 or location_id == 10:
        if config["market_config"]["buy_is_enabled"] == True:
            temp = "update users set location_id = 1 where user_id = " + str(message.from_id)
            cursor.execute(temp)
            conn.commit()
            await message.answer("Введите сумму, которую хотите купить", keyboard=keyboards.update_keyboard_buy())
        else:
            await message.answer("К сожалению, в данный момент покупка VKCoin отключена")


# Кнопка "Продать VKC"
async def sell_handler(message: Message):
    config = cfg.update()
    temp = "select location_id from users where user_id = " + str(message.from_id)
    cursor.execute(temp)
    location_id = cursor.fetchall()[0][0]
    if location_id == 0 or location_id == 10:
        if config["market_config"]["sell_is_enabled"] == True:
            temp = "update users set location_id = 2 where user_id = " + str(message.from_id)
            cursor.execute(temp)
            conn.commit()
            await message.answer("Введите сумму, которую хотите продать", keyboard=keyboards.update_keyboard_sell(message.from_id))
        else:
            await message.answer("К сожалению, в данный момент продажа VKCoin отключена")


# Кнопка "Админка"
async def admin_handler(message: Message):
    temp = "select location_id from users where user_id = " + str(message.from_id)
    cursor.execute(temp)
    location_id = cursor.fetchall()[0][0]
    if location_id == 10:
        temp = "select is_admin from users where user_id = " + str(message.from_id) + ";"
        cursor.execute(temp)
    
        is_admin = cursor.fetchall()[0][0]
        if is_admin == True:

            temp = "update users set location_id = " + str(11) + " where user_id = " + str(message.from_id)
            cursor.execute(temp)
            conn.commit()

            await message.answer("Админка", keyboard=keyboards.update_keyboard_admin_panel())


# Кнопка "Назад"
async def back_handler(message: Message):
    temp = "select location_id from users where user_id = " + str(message.from_id)
    cursor.execute(temp)
    location_id = cursor.fetchall()[0][0]
    if location_id == 1 or location_id == 2 or location_id == 5 or location_id == 6 or (location_id >= 11 and location_id <= 15):
        temp = "select is_admin from users where user_id = " + str(message.from_id)
        cursor.execute(temp)
        is_admin = cursor.fetchall()[0][0]
        if is_admin == 1:
            await message.answer("Вы перемещены в главное меню!", keyboard=keyboards.KEYBOARD_ADMIN)
            temp = "update users set location_id = 10 where user_id = " + str(message.from_id)
        else:
            await message.answer("Вы перемещены в главное меню!", keyboard=keyboards.KEYBOARD_MAIN)
            temp = "update users set location_id = 0 where user_id = " + str(message.from_id)
        cursor.execute(temp)
        conn.commit()


# Кнопка "Настроить QIWI"
async def qiwi_handler(message: Message):
    temp = "select location_id from users where user_id = " + str(message.from_id)
    cursor.execute(temp)
    location_id = cursor.fetchall()[0][0]
    if location_id == 5:
        temp = "update users set location_id = 6 where user_id = " + str(message.from_id)
        cursor.execute(temp)
        conn.commit()
        text = "Введите номер QIWI, на который будут приходить деньги"
        await message.answer(text, keyboard=keyboards.KEYBOARD_BACK)


# Функция настройки QIWI
async def qiwi_config_handler(message: Message):
    try:
        text = message.text
        # Удаляем пробелы, скобки и тире
        text = text.replace(" ", "")
        text = text.replace("(", "")
        text = text.replace(")", "")
        text = text.replace("-", "")
        qiwi_number = "7"
        # Проверка на то, что введенный номер является номером QIWI
        if text[0] == "+" and text[1] == "7" and len(text) == 12:
            for i in range(2, 12):
                if text[i].isdigit():
                    qiwi_number += text[i]
                else:
                    await message.answer("Неверный формат номера QIWI")
                    return
        elif text[0] == "7" and len(text) == 11:
            for i in range(1, 11):
                if text[i].isdigit():
                    qiwi_number += text[i]
                else:
                    await message.answer("Неверный формат номера QIWI")
                    return
        elif text[0] == "8" and len(text) == 11:
            for i in range(1, 11):
                if text[i].isdigit():
                    qiwi_number += text[i]
                else:
                    await message.answer("Неверный формат номера QIWI")
                    return
        else:
            await message.answer("Неверный формат номера QIWI")
            return

        temp = "update users set qiwi = " + str(qiwi_number) + " where user_id = " + str(message.from_id)
        cursor.execute(temp)
        conn.commit()

        # Проверка на админа
        temp = "select is_admin from users where user_id = " + str(message.from_id)
        cursor.execute(temp)
        is_admin = cursor.fetchall()[0][0]
        if is_admin == 1:
            await message.answer("Номер QIWI успешно изменен на +" + str(qiwi_number), keyboard=keyboards.KEYBOARD_ADMIN)
            temp = "update users set location_id = 10 where user_id = " + str(message.from_id)
        else:
            await message.answer("Номер QIWI успешно изменен на +" + str(qiwi_number), keyboard=keyboards.KEYBOARD_MAIN)
            temp = "update users set location_id = 0 where user_id = " + str(message.from_id)
        cursor.execute(temp)
        conn.commit()
    except:
        await message.answer("Номер QIWI должен состоять из цифр!")