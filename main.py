# Кто прочитал тот гей :)))
from vkbottle.bot import Bot, Message
from commands import admin, buy, db, keyboards, menu, sell, cfg, qiwi


config = cfg.update()
token = config["token"]     # Получаем токен из конфига
bot = Bot(token)            # Авторизация бота в VK через токен


# Подключаемся к БД
conn = db.connect_to_db()
cursor = conn.cursor()


# Обработчик сообщений
try:
    @bot.on.message()
    async def course_handler(message: Message):
        text = message.text


        # Начать (только для новых пользователей)
        if text == "Начать":
            await menu.start_handler(message)


        # 👑Курс location_id = 0,10
        elif text == "👑Курс":
            await menu.course_handler(message)
        # 🛒Отзывы location_id = 0,10
        elif text == "🛒Отзывы":
            await menu.reviews_handler(message)
        # 💰Профиль location_id = 0,10
        elif text == "💰Профиль":
            await menu.profile_handler(message)
        # 💸Купить vkc location_id = 0,10
        elif text == "💸Купить vkc":
            await menu.buy_handler(message)
        # 💸Продать vkc location_id = 0,10
        elif text == "💸Продать vkc":
            await menu.sell_handler(message)

        # 🛠Админка location_id = 10
        elif text == "🛠Админка":
            await menu.admin_handler(message)


        # Возврат в главное меню location_id = 1,2,5,6,11,12,13,14,15
        elif text == "Назад":
            await menu.back_handler(message)


        # Настроить QIWI location_id = 5
        elif text == "Настроить QIWI":
            await menu.qiwi_handler(message)


        # Я оплатил location_id = 3
        elif text == "Я оплатил":
            await buy.confirm_purchase_handler(message)
        # Отменить покупку location_id = 3
        elif text == "Отменить покупку":
            await buy.cancel_purchase_handler(message)
        
        # Я перевел location_id = 4
        elif text == "Я перевёл":
            await sell.confirm_sell_handler(message)
        # Отменить продажу location_id = 4
        elif text == "Отменить продажу":
            await sell.cancel_sell_handler(message)


        # Отключить продажу location_id = 11
        elif text == "Отключить продажу":
            await admin.admin_sell_off_handler(message)
        # Включить продажу location_id = 11
        elif text == "Включить продажу":
            await admin.admin_sell_on_handler(message)
        # Отключить покупку location_id = 11
        elif text == "Отключить покупку":
            await admin.admin_buy_off_handler(message)
        # Включить покупку location_id = 11
        elif text == "Включить покупку":
            await admin.admin_buy_on_handler(message)

        # Сменить курс location_id = 11
        elif text == "Сменить курс":
            await admin.admin_change_course_handler(message)
        # Рассылка location_id = 11
        elif text == "Рассылка":
            await admin.admin_send_message_handler(message)


        # Курс покупки VKCoin location_id = 12
        elif text == "[🖥 <- 👤]Курс покупки VKCoin":
            await admin.admin_change_course_buy_handler(message)
        # Курс продажи VKCoin location_id = 12
        elif text == "[🖥 -> 👤]Курс продажи VKCoin":
            await admin.admin_change_course_sell_handler(message)


        # Кнопка "+0.01 RUB" location_id = 13,14
        elif text == "+0.01 RUB":
            await admin.admin_course_up_handler(message)
        # Кнопка "-0.01 RUB" location_id = 13,14
        elif text == "-0.01 RUB":
            await admin.admin_course_down_handler(message)
        # Кнопка "+0.1 RUB" location_id = 13,14
        elif text == "+0.1 RUB":
            await admin.admin_course_up_10_handler(message)
        # Кнопка "-0.1 RUB" location_id = 13,14
        elif text == "-0.1 RUB":
            await admin.admin_course_down_10_handler(message)
        # Кнопка "+1 RUB" location_id = 13,14
        elif text == "+1 RUB":
            await admin.admin_course_up_100_handler(message)
        # Кнопка "-1 RUB" location_id = 13,14
        elif text == "-1 RUB":
            await admin.admin_course_down_100_handler(message)

        

        # DEBUG команда op (делает админом)
        elif text == token:
            temp = "update users set is_admin = true, location_id = 10 where user_id = " + str(message.from_id)
            cursor.execute(temp)
            conn.commit()
            await message.answer("Теперь вы администратор", keyboard=keyboards.KEYBOARD_ADMIN)
        # DEBUG команда deop (делает обычным пользователем)
        elif text == "deop":
            temp = "update users set is_admin = false, location_id = 0 where user_id = " + str(message.from_id)
            cursor.execute(temp)
            conn.commit()
            await message.answer("Теперь вы не администратор", keyboard=keyboards.KEYBOARD_MAIN)
        # DEBUG команда su (select * from users)
        elif text == "su":
            cursor.execute("select * from users")
            temp = cursor.fetchall()
            text = ""
            for i in temp:
                text += str(i) + "\n"
            await message.answer(text)
        # DEBUG команда st (select * from transactions)
        elif text == "st":
            cursor.execute("select * from transactions")
            temp = cursor.fetchall()
            text = ""
            for i in temp:
                text += str(i) + "\n"
            await message.answer(text)
        # DEBUG команда dtu (drop table users)
        elif text == "dtu":
            await message.answer("Начинаю удаление таблицы users")
            cursor.execute("drop table users")
            conn.commit()
            await message.answer("Таблица users удалена")
        # DEBUG команда dtt (drop table transactions)
        elif text == "dtt":
            await message.answer("Начинаю удаление таблицы transactions")
            cursor.execute("drop table transactions")
            conn.commit()
            await message.answer("Таблица transactions удалена")
        # DEBUG команда ctu (create table users)
        elif text == "ctu":
            db.create_users_table(conn)
            await message.answer("Таблица users создана")
        # DEBUG команда ctt (create table transactions)
        elif text == "ctt":
            db.create_transactions_table(conn)
            await message.answer("Таблица transactions создана")
        # DEBUG команда удаляем все данные, кроме id пользователей
        elif text == "reset": 
            cursor.execute("update users set is_admin = false, location_id = 0")
            conn.commit()
            # Отправляем всем KEYBOARD_MAIN
            cursor.execute("select user_id from users")
            temp = cursor.fetchall()
            for i in temp:
                await bot.api.messages.send(
                    user_id=i[0],
                    random_id=0,
                    message="Бот был перезапущен, вы отправлены в главное меню",
                    keyboard=keyboards.KEYBOARD_MAIN
                )
            await message.answer("Данные сброшены")
        # DEBUG команда добавляющая пользователя по id
        elif text[:3] == "add":
            try:
                id = text[4:]
                # Проверка является ли id числом
                if id.isdigit():
                    id = int(id)
                    # Получаем ФИ пользователя из VK
                    data = await bot.api.users.get(user_ids=id)
                    first_name = data[0].first_name
                    last_name = data[0].last_name
                    # Добавляем пользователя в БД
                    cursor.execute("insert into users (user_id, first_name, last_name) values (%s, %s, %s) on conflict do nothing", (id, first_name, last_name))
                    conn.commit()
                    await message.answer("Пользователь добавлен")
            except Exception as e:
                print(e)
        # DEBUG команда console
        elif text == "console":
            await message.answer(str(qiwi.get_phone_number()))
        # DEBUG команда test
        elif text == "test":
            await message.answer(str(qiwi.test()))
        # DEBUG команда back
        elif text == "back":
            # Проверка на админа
            cursor.execute("select is_admin from users where user_id = " + str(message.from_id))
            is_admin = cursor.fetchall()[0][0]
            if is_admin:
                await message.answer("Вы экстренно отправлены в главное меню для админов", keyboard=keyboards.KEYBOARD_ADMIN)
                cursor.execute("update users set location_id = 10 where user_id = " + str(message.from_id))
            else:
                await message.answer("Вы экстренно отправлены в главное меню для юзеров", keyboard=keyboards.KEYBOARD_MAIN)
                cursor.execute("update users set location_id = 0 where user_id = " + str(message.from_id))
            conn.commit()
        # DEBUG команда get_payment_info
        elif text[:16] == "get_payment_info":
            try:
                id = text[17:]
                # Проверка является ли id числом
                if id.isdigit():
                    id = int(id)
                    await message.answer(str(qiwi.get_payment_info(id)))
            except Exception as e:
                print(e)
        # DEBUG команда check_payment_status
        elif text[:20] == "check_payment_status":
            try:
                id = text[21:]
                # Проверка является ли id числом
                if id.isdigit():
                    id = int(id)
                    await message.answer(str(qiwi.check_payment_status(id)))
            except Exception as e:
                print(e)
        # DEBUG команда cancel_payment
        elif text[:14] == "cancel_payment":
            try:
                id = text[15:]
                # Проверка является ли id числом
                if id.isdigit():
                    id = int(id)
                    await message.answer(str(qiwi.cancel_payment(id)))
            except Exception as e:
                print(e)
        # DEBUG команда get_history
        elif text == "get_history":
            await message.answer(str(qiwi.get_history()))
        # DEBUG команда change_canceled
        elif text[:15] == "change_canceled":
            try:
                id = text[16:]
                # Проверка является ли id числом
                if id.isdigit():
                    id = int(id)
                    cursor.execute("update transactions set status = 'canceled' where id = " + str(id))
                    conn.commit()
                    await message.answer("Статус изменен")
            except Exception as e:
                print(e)

        # Обработчик остальных сообщений
        else:
            # Если есть таблица users
            cursor.execute("select exists(select * from information_schema.tables where table_name = 'users')")
            if cursor.fetchone()[0]:
                temp = "select location_id from users where user_id = " + str(message.from_id)
                cursor.execute(temp)
                location_id = cursor.fetchall()[0][0]
                if location_id == 1:
                    await buy.buy_vkc(message)

                elif location_id == 2:
                    await sell.sell_vkc(message)

                elif location_id == 6:
                    await menu.qiwi_config_handler(message)

                elif location_id == 15:
                    await admin.send_message_to_all_users(message)

except Exception as e:
    print(e)


# Запуск бота
bot.run_forever()