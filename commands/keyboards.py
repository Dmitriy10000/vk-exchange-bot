from vkbottle import Keyboard, KeyboardButtonColor, Text
from commands import vkc, cfg
import math


KEYBOARD_MAIN = Keyboard(one_time=False, inline=False)
KEYBOARD_MAIN.add(Text("👑Курс"), color=KeyboardButtonColor.NEGATIVE)
KEYBOARD_MAIN.row()
KEYBOARD_MAIN.add(Text("💰Профиль"), color=KeyboardButtonColor.PRIMARY)
KEYBOARD_MAIN.row()
KEYBOARD_MAIN.add(Text("💸Купить vkc"), color=KeyboardButtonColor.POSITIVE)
KEYBOARD_MAIN.add(Text("💸Продать vkc"), color=KeyboardButtonColor.POSITIVE)
KEYBOARD_MAIN.row()
KEYBOARD_MAIN.add(Text("🛒Отзывы"), color=KeyboardButtonColor.PRIMARY)
KEYBOARD_ADMIN = KEYBOARD_MAIN
KEYBOARD_MAIN = KEYBOARD_MAIN.get_json()


KEYBOARD_ADMIN.row()
KEYBOARD_ADMIN.add(Text("🛠Админка"), color=KeyboardButtonColor.SECONDARY)
KEYBOARD_ADMIN = KEYBOARD_ADMIN.get_json()


def update_keyboard_admin_panel():
    config = cfg.update()
    KEYBOARD_ADMIN_PANEL = Keyboard(one_time=False, inline=False)
    sell = config['market_config']['sell_is_enabled']
    if sell == True:
        KEYBOARD_ADMIN_PANEL.add(Text("Отключить продажу"), color=KeyboardButtonColor.NEGATIVE)
    else:
        KEYBOARD_ADMIN_PANEL.add(Text("Включить продажу"), color=KeyboardButtonColor.POSITIVE)
    buy = config['market_config']['buy_is_enabled']
    if buy == True:
        KEYBOARD_ADMIN_PANEL.add(Text("Отключить покупку"), color=KeyboardButtonColor.NEGATIVE)
    else:
        KEYBOARD_ADMIN_PANEL.add(Text("Включить покупку"), color=KeyboardButtonColor.POSITIVE)
    KEYBOARD_ADMIN_PANEL.row()
    KEYBOARD_ADMIN_PANEL.add(Text("Сменить курс"), color=KeyboardButtonColor.PRIMARY)
    KEYBOARD_ADMIN_PANEL.row()
    KEYBOARD_ADMIN_PANEL.add(Text("Рассылка"), color=KeyboardButtonColor.SECONDARY)
    KEYBOARD_ADMIN_PANEL.row()
    KEYBOARD_ADMIN_PANEL.add(Text("Назад"), color=KeyboardButtonColor.NEGATIVE)
    KEYBOARD_ADMIN_PANEL = KEYBOARD_ADMIN_PANEL.get_json()
    return KEYBOARD_ADMIN_PANEL


KEYBOARD_CHANGE_COURSE = Keyboard(one_time=False, inline=False)
KEYBOARD_CHANGE_COURSE.add(Text("[🖥 <- 👤]Курс покупки VKCoin"), color=KeyboardButtonColor.POSITIVE)
KEYBOARD_CHANGE_COURSE.row()
KEYBOARD_CHANGE_COURSE.add(Text("[🖥 -> 👤]Курс продажи VKCoin"), color=KeyboardButtonColor.POSITIVE)
KEYBOARD_CHANGE_COURSE.row()
KEYBOARD_CHANGE_COURSE.add(Text("Назад"), color=KeyboardButtonColor.NEGATIVE)
KEYBOARD_CHANGE_COURSE = KEYBOARD_CHANGE_COURSE.get_json()


KEYBOARD_COURSE_EDITOR = Keyboard(one_time=False, inline=False)
KEYBOARD_COURSE_EDITOR.add(Text("+0.01 RUB"), color=KeyboardButtonColor.POSITIVE)
KEYBOARD_COURSE_EDITOR.add(Text("+0.1 RUB"), color=KeyboardButtonColor.POSITIVE)
KEYBOARD_COURSE_EDITOR.add(Text("+1 RUB"), color=KeyboardButtonColor.POSITIVE)
KEYBOARD_COURSE_EDITOR.row()
KEYBOARD_COURSE_EDITOR.add(Text("-0.01 RUB"), color=KeyboardButtonColor.NEGATIVE)
KEYBOARD_COURSE_EDITOR.add(Text("-0.1 RUB"), color=KeyboardButtonColor.NEGATIVE)
KEYBOARD_COURSE_EDITOR.add(Text("-1 RUB"), color=KeyboardButtonColor.NEGATIVE)
KEYBOARD_COURSE_EDITOR.row()
KEYBOARD_COURSE_EDITOR.add(Text("Назад"), color=KeyboardButtonColor.PRIMARY)
KEYBOARD_COURSE_EDITOR = KEYBOARD_COURSE_EDITOR.get_json()


def update_keyboard_buy():
    config = cfg.update()
    KEYBOARD_BUY = Keyboard(one_time=False, inline=False)

    # Первая кнопка количество VKCoin на 1 рубль
    text = config["market_config"]["coin_amount"] / (config["market_config"]["buy_price"] / 100)
    text = math.floor(text)                                             # Округляем число в меньшую сторону
    text = "{:,}".format(text).replace(",", ".")                        # Приводим числа к формату 1.000.000
    KEYBOARD_BUY.add(Text(text), color=KeyboardButtonColor.SECONDARY)
    
    # Вторая кнопка количество VKCoin на coin_amount
    text = config["market_config"]["coin_amount"]
    text = "{:,}".format(text).replace(",", ".")                        # Приводим числа к формату 1.000.000
    KEYBOARD_BUY.add(Text(text), color=KeyboardButtonColor.SECONDARY)
    
    # Третья кнопка количество VKCoin на coin_amount * 5
    text = config["market_config"]["coin_amount"] * 5
    text = "{:,}".format(text).replace(",", ".")                        # Приводим числа к формату 1.000.000
    KEYBOARD_BUY.add(Text(text), color=KeyboardButtonColor.SECONDARY)
    KEYBOARD_BUY.row()
    
    # Четвертая кнопка количество VKCoin на coin_amount * 10
    text = config["market_config"]["coin_amount"] * 10
    text = "{:,}".format(text).replace(",", ".")                        # Приводим числа к формату 1.000.000
    KEYBOARD_BUY.add(Text(text), color=KeyboardButtonColor.SECONDARY)
    
    # Пятая кнопка количество VKCoin на coin_amount * 50
    text = config["market_config"]["coin_amount"] * 50
    text = "{:,}".format(text).replace(",", ".")                        # Приводим числа к формату 1.000.000
    KEYBOARD_BUY.add(Text(text), color=KeyboardButtonColor.SECONDARY)
    
    # Шестая кнопка - максимальное количество VKCoin, которое можно купить
    text = vkc.get_shop_balance()
    text = "{:,}".format(text).replace(",", ".")                        # Приводим числа к формату 1.000.000
    KEYBOARD_BUY.add(Text(text), color=KeyboardButtonColor.SECONDARY)
    
    KEYBOARD_BUY.row()
    KEYBOARD_BUY.add(Text("Назад"), color=KeyboardButtonColor.NEGATIVE)
    KEYBOARD_BUY = KEYBOARD_BUY.get_json()
    return KEYBOARD_BUY


def update_keyboard_sell(user_id):
    config = cfg.update()
    KEYBOARD_SELL = Keyboard(one_time=False, inline=False)

    # Первая кнопка количество VKCoin на 1 рубль
    text = config["market_config"]["coin_amount"] / (config["market_config"]["sell_price"] / 100)
    text = math.ceil(text)                                              # Округляем число в большую сторону
    text = "{:,}".format(text).replace(",", ".")                        # Приводим числа к формату 1.000.000
    KEYBOARD_SELL.add(Text(text), color=KeyboardButtonColor.SECONDARY)

    # Вторая кнопка количество VKCoin на coin_amount
    text = config["market_config"]["coin_amount"]
    text = "{:,}".format(text).replace(",", ".")                        # Приводим числа к формату 1.000.000
    KEYBOARD_SELL.add(Text(text), color=KeyboardButtonColor.SECONDARY)

    # Третья кнопка количество VKCoin на coin_amount * 5
    text = config["market_config"]["coin_amount"] * 5
    text = "{:,}".format(text).replace(",", ".")                        # Приводим числа к формату 1.000.000
    KEYBOARD_SELL.add(Text(text), color=KeyboardButtonColor.SECONDARY)
    KEYBOARD_SELL.row()

    # Четвертая кнопка количество VKCoin на coin_amount * 10
    text = config["market_config"]["coin_amount"] * 10
    text = "{:,}".format(text).replace(",", ".")                        # Приводим числа к формату 1.000.000
    KEYBOARD_SELL.add(Text(text), color=KeyboardButtonColor.SECONDARY)

    # Пятая кнопка количество VKCoin на coin_amount * 50
    text = config["market_config"]["coin_amount"] * 50
    text = "{:,}".format(text).replace(",", ".")                        # Приводим числа к формату 1.000.000
    KEYBOARD_SELL.add(Text(text), color=KeyboardButtonColor.SECONDARY)

    # Шестая кнопка - максимальное количество VKCoin, которое можно продать
    text = vkc.get_balance(user_id)                                     # Запрос на получение баланса
    text = "{:,}".format(text).replace(",", ".")                        # Приводим числа к формату 1.000.000
    KEYBOARD_SELL.add(Text(text), color=KeyboardButtonColor.SECONDARY)
    KEYBOARD_SELL.row()

    # Седьмая кнопка - Назад
    KEYBOARD_SELL.add(Text("Назад"), color=KeyboardButtonColor.NEGATIVE)
    KEYBOARD_SELL = KEYBOARD_SELL.get_json()
    return KEYBOARD_SELL
    

KEYBOARD_BACK = Keyboard(one_time=False, inline=False)
KEYBOARD_BACK.add(Text("Назад"), color=KeyboardButtonColor.NEGATIVE)
KEYBOARD_BACK = KEYBOARD_BACK.get_json()


KEYBOARD_CANCEL_PURCHASE = Keyboard(one_time=False, inline=False)
KEYBOARD_CANCEL_PURCHASE.add(Text("Я оплатил"), color=KeyboardButtonColor.POSITIVE)
KEYBOARD_CANCEL_PURCHASE.row()
KEYBOARD_CANCEL_PURCHASE.add(Text("Отменить покупку"), color=KeyboardButtonColor.NEGATIVE)
KEYBOARD_CANCEL_PURCHASE = KEYBOARD_CANCEL_PURCHASE.get_json()


KEYBOARD_CANCEL_SELL = Keyboard(one_time=False, inline=False)
KEYBOARD_CANCEL_SELL.add(Text("Я перевёл"), color=KeyboardButtonColor.POSITIVE)
KEYBOARD_CANCEL_SELL.row()
KEYBOARD_CANCEL_SELL.add(Text("Отменить продажу"), color=KeyboardButtonColor.NEGATIVE)
KEYBOARD_CANCEL_SELL = KEYBOARD_CANCEL_SELL.get_json()


KEYBOARD_PROFILE = Keyboard(one_time=False, inline=False)
KEYBOARD_PROFILE.add(Text("Настроить QIWI"), color=KeyboardButtonColor.PRIMARY)
KEYBOARD_PROFILE.row()
KEYBOARD_PROFILE.add(Text("Назад"), color=KeyboardButtonColor.NEGATIVE)
KEYBOARD_PROFILE = KEYBOARD_PROFILE.get_json()