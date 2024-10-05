from vkbottle.bot import Bot, Message
from commands import db, keyboards, vkc, cfg, qiwi
import time
import math


config = cfg.update()
token = config["token"]
bot = Bot(token)


# Подключаемся к БД
conn = db.connect_to_db()
cursor = conn.cursor()


# Функция продажи VKC location_id = 2
async def sell_vkc(message: Message):
    config = cfg.update()
    if config["market_config"]["sell_is_enabled"] == True:
        temp = "select qiwi from users where user_id = " + str(message.from_id)
        cursor.execute(temp)
        qiwi_number = cursor.fetchall()[0][0]
        if qiwi_number == None:
            await message.answer("⚠️ Для продажи VKC необходимо привязать QIWI кошелек. (Это можно сделать во вкладке \"💰Профиль\")", keyboard=keyboards.main_menu)
            return
        
        # Парсим сумму
        amount = message.text
        amount = amount.replace(" ", "")
        amount = amount.replace(".", "")
        amount = amount.replace(",", "")
        
        # Проверяем содержит ли строка только числа
        if amount.isdigit():
            vkc_amount = int(amount)
            min_amount = config["market_config"]["coin_amount"] / (config["market_config"]["sell_price"] / 100)
            
            # Округляем число в большую сторону
            min_amount = math.ceil(min_amount)

            # Минимальная транзакция на 1 рубль
            if vkc_amount < min_amount:
                min_amount = "{:,}".format(min_amount).replace(",", ".")
                await message.answer("Минимальная сумма продажи: " + str(min_amount) + " VKCoin")
                return

            # Проверяем хватает ли VKCoin на балансе пользователя
            user_max_vkc = vkc.get_balance(message.from_id)
            if vkc_amount > user_max_vkc:
                await message.answer("У вас нет столько VKCoin")
                return

            # Проверяем хватает ли RUB в резерве магазина
            shop_max_rub = vkc.get_shop_balance()
            if vkc_amount / config["market_config"]["coin_amount"] * (config["market_config"]["sell_price"] / 100) > shop_max_rub:
                await message.answer("У магазина нет столько RUB")
                return

        else:
            await message.answer("Некорректная сумма")
            return
        
        rub_amount = vkc_amount / config["market_config"]["coin_amount"] * config["market_config"]["sell_price"]

        # Округляем число в меньшую сторону с точностью до 2 знаков после запятой
        rub_amount = math.floor(rub_amount)

        temp = "insert into transactions (user_id, vkc_amount, rub_amount, type, status) values (" + str(message.from_id) + ", " + str(vkc_amount) + ", " + str(rub_amount) + ", \'sell\', \'pending\');"
        temp += "update users set location_id = 4 where user_id = " + str(message.from_id) + ";"
        cursor.execute(temp)
        conn.commit()

        temp = "select id from transactions where user_id = " + str(message.from_id) + " and status = \'pending\';"
        cursor.execute(temp)
        transaction_id = cursor.fetchone()[0]

        url = "vk.com/coin#x" + str(config["merchant_config"]["merchant_id"]) + "_" + str(vkc_amount * 1000) + "_" + str(transaction_id)
        vkc_amount = "{:,}".format(vkc_amount).replace(",", ".")
        text = "Продажа VKCoin\n"
        text += "Сумма: " + str(vkc_amount) + " VKCoin\n"
        text += "Вы получите: " + str(rub_amount/100) + " рублей\n"
        text += "Ссылка для перевода: " + str(url) + "\n\n"
        text += "После перевода VKCoin'ов нажмите кнопку \"Я перевёл\"\n"
        text += "Если хотите отменить продажу нажмите кнопку \"Отменить продажу\""
        await message.answer(text, keyboard=keyboards.KEYBOARD_CANCEL_SELL)

    else:
        temp = "select is_admin from users where user_id = " + str(message.from_id)
        cursor.execute(temp)
        is_admin = cursor.fetchall()[0][0]
        text = "К сожалению, в данный момент продажа VKCoin отключена"
        if is_admin == True:
            await message.answer(text, keyboard=keyboards.KEYBOARD_ADMIN)
            temp = "update users set location_id = 10 where user_id = " + str(message.from_id)
        else:
            await message.answer(text, keyboard=keyboards.KEYBOARD_MAIN)
            temp = "update users set location_id = 0 where user_id = " + str(message.from_id)
        cursor.execute(temp)
        conn.commit()


# Функция подтверждения продажи VKC location_id = 4
async def confirm_sell_handler(message: Message):
    temp = "select location_id from users where user_id = " + str(message.from_id)
    cursor.execute(temp)
    location_id = cursor.fetchall()[0][0]
    if location_id == 4:
        temp = "select vkc_amount, rub_amount, date, time from transactions where user_id = " + str(message.from_id) + " order by id desc limit 1;"
        cursor.execute(temp)
        last_transaction = cursor.fetchall()[0]     # (datetime.date(2022, 10, 21), datetime.time(18, 45, 41, 714145))
        vkc_amount = int(last_transaction[0])
        rub_amount = int(last_transaction[1])
        # unix
        unix = int(time.mktime(last_transaction[2].timetuple())) + last_transaction[3].hour * 3600 + last_transaction[3].minute * 60 + last_transaction[3].second
        status = vkc.check_payments(message.from_id, vkc_amount*1000, unix)
        if status == True:
            temp = "update transactions set status = \'success\' where user_id = " + str(message.from_id) + " and status = \'pending\';"
            temp += "update users set location_id = 0 where user_id = " + str(message.from_id) + ";"
            cursor.execute(temp)
            conn.commit()
            await message.answer("Перевод VKCoin'ов успешно завершён. Ваша сумма будет зачислена в течении 5 минут", keyboard=keyboards.KEYBOARD_MAIN)
            temp = "select QIWI from users where user_id = " + str(message.from_id)
            cursor.execute(temp)
            QIWI = cursor.fetchall()[0][0]
            rub_amount = rub_amount/100
            qiwi.transfer_to_qiwi(rub_amount, QIWI)
        else:
            await message.answer("Вы ещё не перевели VKCoin'ы")


# Функция отмены продажи VKC location_id = 4
async def cancel_sell_handler(message: Message):
    temp = "select location_id from users where user_id = " + str(message.from_id)
    cursor.execute(temp)
    location_id = cursor.fetchall()[0][0]
    if location_id == 4:
        temp = "select vkc_amount, rub_amount, date, time from transactions where user_id = " + str(message.from_id) + " order by id desc limit 1;"
        cursor.execute(temp)
        last_transaction = cursor.fetchall()[0]     # (datetime.date(2022, 10, 21), datetime.time(18, 45, 41, 714145))
        vkc_amount = int(last_transaction[0])
        rub_amount = int(last_transaction[1])
        # unix
        unix = int(time.mktime(last_transaction[2].timetuple())) + last_transaction[3].hour * 3600 + last_transaction[3].minute * 60 + last_transaction[3].second
        status = vkc.check_payments(message.from_id, vkc_amount*1000, unix)
        if status == True:
            temp = "update transactions set status = \'success\' where user_id = " + str(message.from_id) + " and status = \'pending\';"
            temp += "update users set location_id = 0 where user_id = " + str(message.from_id) + ";"
            cursor.execute(temp)
            conn.commit()
            await message.answer("Перевод VKCoin'ов успешно завершён. Ваша сумма будет зачислена в течении 5 минут", keyboard=keyboards.KEYBOARD_MAIN)
            temp = "select QIWI from users where user_id = " + str(message.from_id)
            cursor.execute(temp)
            QIWI = cursor.fetchall()[0][0]
            rub_amount = rub_amount/100
            qiwi.transfer_to_qiwi(rub_amount, QIWI)
        else:
            temp = "update transactions set status = \'canceled\' where user_id = " + str(message.from_id) + " and status = \'pending\';"
            temp += "update users set location_id = 0 where user_id = " + str(message.from_id) + ";"
            cursor.execute(temp)
            conn.commit()
            await message.answer("Продажа VKCoin'ов отменена", keyboard=keyboards.KEYBOARD_MAIN)