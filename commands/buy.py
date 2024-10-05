from vkbottle.bot import Bot, Message
from commands import db, keyboards, cfg, vkc, qiwi
import math


config = cfg.update()
token = config["token"]
bot = Bot(token)


# Подключаемся к БД
conn = db.connect_to_db()
cursor = conn.cursor()


# Функция покупки VKC location_id = 1
async def buy_vkc(message: Message):
    config = cfg.update()
    if config["market_config"]["buy_is_enabled"] == True:
    
        # Парсим сумму
        amount = message.text
        amount = amount.replace(" ", "")
        amount = amount.replace(".", "")
        amount = amount.replace(",", "")
        
        # Проверяем содержит ли строка только числа
        if amount.isdigit():
            vkc_amount = int(amount)
            min_amount = config["market_config"]["coin_amount"] / (config["market_config"]["buy_price"] / 100)
            
            # Округляем число в меньшую сторону
            min_amount = math.floor(min_amount)

            # Минимальная транзакция на 1 рубль
            if vkc_amount < min_amount:
                min_amount = "{:,}".format(min_amount).replace(",", ".")
                await message.answer("Минимальная сумма покупки: " + str(min_amount) + " VKCoin")
                return

            # Проверяем хватает ли VKCoin в резерве
            max_amount = vkc.get_shop_balance()
            if vkc_amount > max_amount:
                await message.answer("В наличии недостаточно VKCoin")
                return

        else:
            await message.answer("Некорректная сумма")
            return

        rub_amount = vkc_amount / config["market_config"]["coin_amount"] * config["market_config"]["buy_price"]

        # Округляем число в большую сторону с точностью до 2 знаков после запятой
        rub_amount = math.ceil(rub_amount)

        temp = "insert into transactions (user_id, vkc_amount, rub_amount, type, status) values (" + str(message.from_id) + ", " + str(vkc_amount) + ", " + str(rub_amount) + ", \'buy\', \'pending\');"
        temp += "update users set location_id = 3 where user_id = " + str(message.from_id) + ";"
        cursor.execute(temp)
        conn.commit()

        vkc_amount = "{:,}".format(vkc_amount).replace(",", ".")
        text = "Покупка VKCoin\n"
        text += "Сумма: " + str(vkc_amount) + " VKCoin\n"
        text += "Стоимость: " + str(rub_amount/100) + " руб.\n"
        text += "Ссылка оплаты действительна в течение 10 минут: "
        text += str(qiwi.get_payment_link(rub_amount/100, message.from_id) + "\n\n")
        text += "После подтветждения платежа нажмите кнопку \"Я оплатил\"\n"
        text += "Если хотите отменить покупку нажмите кнопку \"Отменить покупку\""
        await message.answer(text, keyboard=keyboards.KEYBOARD_CANCEL_PURCHASE)

    else:
        temp = "select is_admin from users where user_id = " + str(message.from_id)
        cursor.execute(temp)
        is_admin = cursor.fetchall()[0][0]
        text = "К сожалению, в данный момент покупка VKCoin отключена"
        if is_admin == True:
            await message.answer(text, keyboard=keyboards.KEYBOARD_ADMIN)
            temp = "update users set location_id = 10 where user_id = " + str(message.from_id)
        else:
            await message.answer(text, keyboard=keyboards.KEYBOARD_MAIN)
            temp = "update users set location_id = 0 where user_id = " + str(message.from_id)
        cursor.execute(temp)
        conn.commit()


# Функция подтверждения покупки VKC location_id = 3
async def confirm_purchase_handler(message: Message):
    temp = "select location_id from users where user_id = " + str(message.from_id)
    cursor.execute(temp)
    location_id = cursor.fetchall()[0][0]
    if location_id == 3:
        temp = "select id from transactions where user_id = " + str(message.from_id) + " and status = \'pending\'"
        cursor.execute(temp)
        transaction_id = cursor.fetchall()[0][0]
        status = qiwi.check_payment_status(transaction_id)
        if status == "PAID":
            temp = "select vkc_amount from transactions where user_id = " + str(message.from_id) + " and status = \'pending\'"
            cursor.execute(temp)
            vkc_amount = cursor.fetchall()[0][0]
            temp = "update transactions set status = \'success\' where id = " + str(transaction_id) + ";"
            temp += "update users set location_id = 0 where user_id = " + str(message.from_id)
            cursor.execute(temp)
            conn.commit()
            vkc.merchant.send_payment(message.from_id, int(vkc_amount) * 1000)
            await message.answer("Покупка успешно завершена", keyboard=keyboards.KEYBOARD_MAIN)
        else:
            await message.answer("Платеж еще не завершен, попробуйте позже")


# Функция отмены покупки VKC location_id = 3
async def cancel_purchase_handler(message: Message):
    temp = "select location_id from users where user_id = " + str(message.from_id)
    cursor.execute(temp)
    location_id = cursor.fetchall()[0][0]
    if location_id == 3:
        temp = "select id from transactions where user_id = " + str(message.from_id) + " and status = \'pending\'"
        cursor.execute(temp)
        transaction_id = cursor.fetchall()[0][0]
        status = qiwi.check_payment_status(transaction_id)
        if status == "PAID":
            temp = "select vkc_amount from transactions where user_id = " + str(message.from_id) + " and status = \'pending\'"
            cursor.execute(temp)
            vkc_amount = cursor.fetchall()[0][0]
            temp = "update transactions set status = \'success\' where id = " + str(transaction_id) + ";"
            temp += "update users set location_id = 0 where user_id = " + str(message.from_id)
            cursor.execute(temp)
            conn.commit()
            vkc.merchant.send_payment(message.from_id, int(vkc_amount) * 1000)
            await message.answer("Покупка успешно завершена", keyboard=keyboards.KEYBOARD_MAIN)
            return
        else:
            temp = "select id from transactions where user_id = " + str(message.from_id) + " and status = \'pending\'"
            cursor.execute(temp)
            transaction_id = cursor.fetchall()[0][0]
            if qiwi.cancel_payment(transaction_id):
                temp = "update users set location_id = 1 where user_id = " + str(message.from_id) + ";"
                temp += "update transactions set status = \'canceled\' where user_id = " + str(message.from_id) + " and status = \'pending\';"
                cursor.execute(temp)
                conn.commit()
                await message.answer("Покупка отменена", keyboard=keyboards.update_keyboard_buy())
            else:
                await message.answer("Ошибка отмены покупки")