from vkbottle.bot import Bot, Message
import json
from commands import db, keyboards, cfg


config = cfg.update()
token = config["token"]
bot = Bot(token)



# Подключаемся к БД
conn = db.connect_to_db()
cursor = conn.cursor()


# Кнопка "Отключить продажу"
async def admin_sell_off_handler(message: Message):
    config = cfg.update()
    temp = "select location_id from users where user_id = " + str(message.from_id)
    cursor.execute(temp)
    location_id = cursor.fetchall()[0][0]
    if location_id == 11:
        temp = "select is_admin from users where user_id = " + str(message.from_id)
        cursor.execute(temp)
        is_admin = cursor.fetchall()[0][0]
        if is_admin == True:
            config['market_config']['sell_is_enabled'] = False
            json.dump(config, open("config.json", "w"), indent=4)

            await message.answer("Продажа отключена", keyboard=keyboards.update_keyboard_admin_panel())


# Кнопка "Включить продажу"
async def admin_sell_on_handler(message: Message):
    config = cfg.update()
    temp = "select location_id from users where user_id = " + str(message.from_id)
    cursor.execute(temp)
    location_id = cursor.fetchall()[0][0]
    if location_id == 11:
        temp = "select is_admin from users where user_id = " + str(message.from_id)
        cursor.execute(temp)
        is_admin = cursor.fetchall()[0][0]
        if is_admin == True:
            config['market_config']['sell_is_enabled'] = True
            json.dump(config, open("config.json", "w"), indent=4)

            await message.answer("Продажа включена", keyboard=keyboards.update_keyboard_admin_panel())


# Кнопка "Отключить покупку"
async def admin_buy_off_handler(message: Message):
    config = cfg.update()
    temp = "select location_id from users where user_id = " + str(message.from_id)
    cursor.execute(temp)
    location_id = cursor.fetchall()[0][0]
    if location_id == 11:
        temp = "select is_admin from users where user_id = " + str(message.from_id)
        cursor.execute(temp)
        is_admin = cursor.fetchall()[0][0]
        if is_admin == True:
            config['market_config']['buy_is_enabled'] = False
            json.dump(config, open("config.json", "w"), indent=4)

            await message.answer("Покупка отключена", keyboard=keyboards.update_keyboard_admin_panel())


# Кнопка "Включить покупку"
async def admin_buy_on_handler(message: Message):
    config = cfg.update()
    temp = "select location_id from users where user_id = " + str(message.from_id)
    cursor.execute(temp)
    location_id = cursor.fetchall()[0][0]
    if location_id == 11:
        temp = "select is_admin from users where user_id = " + str(message.from_id)
        cursor.execute(temp)
        temp = cursor.fetchall()[0][0]
        if temp == True:
            config['market_config']['buy_is_enabled'] = True
            json.dump(config, open("config.json", "w"), indent=4)

            await message.answer("Покупка включена", keyboard=keyboards.update_keyboard_admin_panel())

        
# Кнопка "Сменить курс"
async def admin_change_course_handler(message: Message):
    temp = "select location_id from users where user_id = " + str(message.from_id)
    cursor.execute(temp)
    location_id = cursor.fetchall()[0][0]
    if location_id == 11:
        await message.answer(
            "Выберите, какой курс сменить:",
            keyboard=keyboards.KEYBOARD_CHANGE_COURSE)
        temp = "update users set location_id = " + str(12) + " where user_id = " + str(message.from_id)
        cursor.execute(temp)
        conn.commit()


# Кнопка "Рассылка"
async def admin_send_message_handler(message: Message):
    temp = "select location_id from users where user_id = " + str(message.from_id)
    cursor.execute(temp)
    location_id = cursor.fetchall()[0][0]
    if location_id == 11:
        await message.answer(
            "Введите сообщение для рассылки:",
            keyboard=keyboards.KEYBOARD_BACK)
        temp = "update users set location_id = " + str(15) + " where user_id = " + str(message.from_id)
        cursor.execute(temp)
        conn.commit()



# Функция для отправки сообщения всем пользователям
async def send_message_to_all_users(message: Message):
    temp = "select location_id from users where user_id = " + str(message.from_id)
    cursor.execute(temp)
    location_id = cursor.fetchall()[0][0]
    if location_id == 15:
        try:
            temp = "select user_id from users"
            cursor.execute(temp)
            users = cursor.fetchall()
            for user in users:
                await send_message(message, user[0])
                    
            temp = "update users set location_id = " + str(11) + " where user_id = " + str(message.from_id)
            cursor.execute(temp)
            conn.commit()
            await message.answer("Рассылка завершена", keyboard=keyboards.update_keyboard_admin_panel())
        except Exception as e:
            print("Ошибка: " + e)


# Отправка сообщения пользователю
async def send_message(message: Message, user_id: int):
    try:
        # Если есть вложения
        if message.attachments:
            # Если в сообщении была ссылка на пост, то отправляем его
            if message.attachments[0].wall is not None:
                await bot.api.messages.send(
                    user_id=user_id,
                    message=message.text,
                    attachment="wall" + str(message.attachments[0].wall.from_id) + "_" + str(message.attachments[0].wall.id),
                    random_id=0)
        else:
            await bot.api.messages.send(
                user_id=user_id,
                message=message.text,
                random_id=0)
    except Exception as e:
        print("Ошибка при отправке сообщения пользователю: " + str(e))



# Кнопка "Курс покупки VKCoin"
async def admin_change_course_buy_handler(message: Message):
    temp = "select location_id from users where user_id = " + str(message.from_id)
    cursor.execute(temp)
    location_id = cursor.fetchall()[0][0]
    if location_id == 12:
        text = (
            "Текущий курс: " + str(config["market_config"]["sell_price"]/100) + " RUB\n" +
            "Выберите изменение курса:")
        await message.answer(text, keyboard=keyboards.KEYBOARD_COURSE_EDITOR)
        temp = "update users set location_id = " + str(13) + " where user_id = " + str(message.from_id)
        cursor.execute(temp)
        conn.commit()


# Кнопка "Курс продажи VKCoin"
async def admin_change_course_sell_handler(message: Message):
    temp = "select location_id from users where user_id = " + str(message.from_id)
    cursor.execute(temp)
    location_id = cursor.fetchall()[0][0]
    if location_id == 12:
        text = (
            "Текущий курс: " + str(config["market_config"]["buy_price"]/100) + " RUB\n" +
            "Выберите изменение курса:")
        await message.answer(text, keyboard=keyboards.KEYBOARD_COURSE_EDITOR)
        temp = "update users set location_id = " + str(14) + " where user_id = " + str(message.from_id)
        cursor.execute(temp)
        conn.commit()



# Кнопка "+0.01 RUB"
async def admin_course_up_handler(message: Message):
    config = cfg.update()
    temp = "select location_id from users where user_id = " + str(message.from_id)
    cursor.execute(temp)
    location_id = cursor.fetchall()[0][0]
    if location_id == 13:
        if config["market_config"]["sell_price"] + 1 >= config["market_config"]["buy_price"]:
            await message.answer("Цена покупки VKcoin не должна быть выше цены продажи, иначе можно обанкротиться", keyboard = keyboards.KEYBOARD_COURSE_EDITOR)
        else:
            config["market_config"]["sell_price"] += 1
            json.dump(config, open("config.json", "w"), indent=4)
            await message.answer("Курс покупки успешно изменён на " + str(config["market_config"]["sell_price"]/100) + " RUB", keyboard=keyboards.KEYBOARD_COURSE_EDITOR)
    if location_id == 14:
        if config["market_config"]["buy_price"] + 1 <= config["market_config"]["sell_price"]:
            await message.answer("Цена покупки VKcoin не должна быть выше цены продажи, иначе можно обанкротиться", keyboard = keyboards.KEYBOARD_COURSE_EDITOR)
        else:
            config["market_config"]["buy_price"] += 1
            json.dump(config, open("config.json", "w"), indent=4)
            await message.answer("Курс покупки успешно изменён на " + str(config["market_config"]["buy_price"]/100) + " RUB", keyboard=keyboards.KEYBOARD_COURSE_EDITOR)


# Кнопка "+0.1 RUB"
async def admin_course_up_10_handler(message: Message):
    config = cfg.update()
    temp = "select location_id from users where user_id = " + str(message.from_id)
    cursor.execute(temp)
    location_id = cursor.fetchall()[0][0]
    if location_id == 13:
        if config["market_config"]["sell_price"] + 10 >= config["market_config"]["buy_price"]:
            await message.answer("Цена покупки VKcoin не должна быть выше цены продажи, иначе можно обанкротиться", keyboard = keyboards.KEYBOARD_COURSE_EDITOR)
        else:
            config["market_config"]["sell_price"] += 10
            json.dump(config, open("config.json", "w"), indent=4)
            await message.answer("Курс покупки успешно изменён на " + str(config["market_config"]["sell_price"]/100) + " RUB", keyboard=keyboards.KEYBOARD_COURSE_EDITOR)
    if location_id == 14:
        if config["market_config"]["buy_price"] + 10 <= config["market_config"]["sell_price"]:
            await message.answer("Цена покупки VKcoin не должна быть выше цены продажи, иначе можно обанкротиться", keyboard = keyboards.KEYBOARD_COURSE_EDITOR)
        else:
            config["market_config"]["buy_price"] += 10
            json.dump(config, open("config.json", "w"), indent=4)
            await message.answer("Курс покупки успешно изменён на " + str(config["market_config"]["buy_price"]/100) + " RUB", keyboard=keyboards.KEYBOARD_COURSE_EDITOR)


# Кнопка "+1 RUB"
async def admin_course_up_100_handler(message: Message):
    config = cfg.update()
    temp = "select location_id from users where user_id = " + str(message.from_id)
    cursor.execute(temp)
    location_id = cursor.fetchall()[0][0]
    if location_id == 13:
        if config["market_config"]["sell_price"] + 100 >= config["market_config"]["buy_price"]:
            await message.answer("Цена покупки VKcoin не должна быть выше цены продажи, иначе можно обанкротиться", keyboard = keyboards.KEYBOARD_COURSE_EDITOR)
        else:
            config["market_config"]["sell_price"] += 100
            json.dump(config, open("config.json", "w"), indent=4)
            await message.answer("Курс покупки успешно изменён на " + str(config["market_config"]["sell_price"]/100) + " RUB", keyboard=keyboards.KEYBOARD_COURSE_EDITOR)
    if location_id == 14:
        if config["market_config"]["buy_price"] + 100 <= config["market_config"]["sell_price"]:
            await message.answer("Цена покупки VKcoin не должна быть выше цены продажи, иначе можно обанкротиться", keyboard = keyboards.KEYBOARD_COURSE_EDITOR)
        else:
            config["market_config"]["buy_price"] += 100
            json.dump(config, open("config.json", "w"), indent=4)
            await message.answer("Курс покупки успешно изменён на " + str(config["market_config"]["buy_price"]/100) + " RUB", keyboard=keyboards.KEYBOARD_COURSE_EDITOR)


# Кнопка "-0.01 RUB"
async def admin_course_down_handler(message: Message):
    config = cfg.update()
    temp = "select location_id from users where user_id = " + str(message.from_id)
    cursor.execute(temp)
    location_id = cursor.fetchall()[0][0]
    if location_id == 13:
        if config["market_config"]["sell_price"] - 1 >= config["market_config"]["buy_price"]:
            await message.answer("Цена покупки VKcoin не должна быть выше цены продаже, иначе можно обанкротиться", keyboard = keyboards.KEYBOARD_COURSE_EDITOR)
        elif config["market_config"]["sell_price"] - 1 <= 0:
            await message.answer("Нельзя опустить курс ниже нуля.", keyboard = keyboards.KEYBOARD_COURSE_EDITOR)
        else:
            config["market_config"]["sell_price"] -= 1
            json.dump(config, open("config.json", "w"), indent=4)
            await message.answer("Курс покупки успешно изменён на " + str(config["market_config"]["sell_price"]/100) + " RUB", keyboard=keyboards.KEYBOARD_COURSE_EDITOR)
    if location_id == 14:
        if config["market_config"]["buy_price"] - 1 <= config["market_config"]["sell_price"]:
            await message.answer("Цена покупки VKcoin не должна быть выше цены продаже, иначе можно обанкротиться", keyboard = keyboards.KEYBOARD_COURSE_EDITOR)
        elif config["market_config"]["sell_price"] - 1 <= 0:
            await message.answer("Нельзя опустить курс ниже нуля.", keyboard = keyboards.KEYBOARD_COURSE_EDITOR)
        else:
            config["market_config"]["buy_price"] -= 1
            json.dump(config, open("config.json", "w"), indent=4)
            await message.answer("Курс покупки успешно изменён на " + str(config["market_config"]["buy_price"]/100) + " RUB", keyboard=keyboards.KEYBOARD_COURSE_EDITOR)


# Кнопка "-0.1 RUB"
async def admin_course_down_10_handler(message: Message):
    config = cfg.update()
    temp = "select location_id from users where user_id = " + str(message.from_id)
    cursor.execute(temp)
    location_id = cursor.fetchall()[0][0]
    if location_id == 13:
        if config["market_config"]["sell_price"] - 10 >= config["market_config"]["buy_price"]:
            await message.answer("Цена покупки VKcoin не должна быть выше цены продаже, иначе можно обанкротиться", keyboard = keyboards.KEYBOARD_COURSE_EDITOR)
        elif config["market_config"]["sell_price"] - 10 <= 0:
            await message.answer("Нельзя опустить курс ниже нуля.", keyboard = keyboards.KEYBOARD_COURSE_EDITOR)
        else:
            config["market_config"]["sell_price"] -= 10
            json.dump(config, open("config.json", "w"), indent=4)
            await message.answer("Курс покупки успешно изменён на " + str(config["market_config"]["sell_price"]/100) + " RUB", keyboard=keyboards.KEYBOARD_COURSE_EDITOR)
    if location_id == 14:
        if config["market_config"]["buy_price"] - 10 <= config["market_config"]["sell_price"]:
            await message.answer("Цена покупки VKcoin не должна быть выше цены продаже, иначе можно обанкротиться", keyboard = keyboards.KEYBOARD_COURSE_EDITOR)
        elif config["market_config"]["sell_price"] - 10 <= 0:
            await message.answer("Нельзя опустить курс ниже нуля.", keyboard = keyboards.KEYBOARD_COURSE_EDITOR)
        else:
            config["market_config"]["buy_price"] -= 10
            json.dump(config, open("config.json", "w"), indent=4)
            await message.answer("Курс покупки успешно изменён на " + str(config["market_config"]["buy_price"]/100) + " RUB", keyboard=keyboards.KEYBOARD_COURSE_EDITOR)


# Кнопка "-1 RUB"
async def admin_course_down_100_handler(message: Message):
    config = cfg.update()
    temp = "select location_id from users where user_id = " + str(message.from_id)
    cursor.execute(temp)
    location_id = cursor.fetchall()[0][0]
    if location_id == 13:
        if config["market_config"]["sell_price"] - 100 >= config["market_config"]["buy_price"]:
            await message.answer("Цена покупки VKcoin не должна быть выше цены продаже, иначе можно обанкротиться", keyboard = keyboards.KEYBOARD_COURSE_EDITOR)
        elif config["market_config"]["sell_price"] - 100 <= 0:
            await message.answer("Нельзя опустить курс ниже нуля.", keyboard = keyboards.KEYBOARD_COURSE_EDITOR)
        else:
            config["market_config"]["sell_price"] -= 100
            json.dump(config, open("config.json", "w"), indent=4)
            await message.answer("Курс покупки успешно изменён на " + str(config["market_config"]["sell_price"]/100) + " RUB", keyboard=keyboards.KEYBOARD_COURSE_EDITOR)
    if location_id == 14:
        if config["market_config"]["buy_price"] - 100 <= config["market_config"]["sell_price"]:
            await message.answer("Цена покупки VKcoin не должна быть выше цены продаже, иначе можно обанкротиться", keyboard = keyboards.KEYBOARD_COURSE_EDITOR)
        elif config["market_config"]["sell_price"] - 100 <= 0:
            await message.answer("Нельзя опустить курс ниже нуля.", keyboard = keyboards.KEYBOARD_COURSE_EDITOR)
        else:
            config["market_config"]["buy_price"] -= 100
            json.dump(config, open("config.json", "w"), indent=4)
            await message.answer("Курс покупки успешно изменён на " + str(config["market_config"]["buy_price"]/100) + " RUB", keyboard=keyboards.KEYBOARD_COURSE_EDITOR)
