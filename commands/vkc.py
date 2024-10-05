import vkcoin
from commands import cfg
import math


config = cfg.update()
merchant_id = config["merchant_config"]["merchant_id"]
merchant_key = config["merchant_config"]["merchant_key"]
merchant = vkcoin.VKCoin(merchant_id, merchant_key)
merchant.set_shop_name(name="VKCoin Shop")                      # Устанавливаем название магазина


# Функция получения баланса VKCoin магазина
def get_shop_balance():
    balance = merchant.get_balance(merchant_id)                 # Запрос на получение баланса
    balance = balance[str(merchant_id)]/1000                    # Достаем из словаря баланс (целую часть) пользователя
    balance = math.floor(balance)                               # Округляем в меньшую сторону
    return balance


# Функция получения баланса VKCoin пользователя
def get_balance(user_id):
    balance = merchant.get_balance(user_id)                     # Запрос на получение баланса
    balance = balance[str(user_id)]/1000                        # Достаем из словаря баланс (целую часть) пользователя
    balance = math.floor(balance)                               # Округляем в меньшую сторону
    return balance


# Функция, отслеживающая входящие платежи
def check_payments(user_id, vkc_amount, unix):
    payments = merchant.get_transactions(tx=[1])                # Запрос на получение списка транзакций
    for payment in payments:                                    # Перебираем все транзакции
        if payment["from_id"] == user_id:                       # Если транзакция была отправлена пользователем
            if payment["amount"] == str(vkc_amount):            # Если сумма транзакции равна сумме покупки
                if payment["created_at"] >= unix:               # Если транзакция была создана после начала покупки
                    return True                                 # Возвращаем True
    return False                                                # Возвращаем False
