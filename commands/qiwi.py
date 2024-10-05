import time
import requests
from commands import cfg, db
from datetime import datetime, timedelta


config = cfg.update()
token = config["qiwi"]["token"]
public_key = config["qiwi"]["public_key"]
secret_key = config["qiwi"]["secret_key"]



# Подключаемся к БД
conn = db.connect_to_db()
cursor = conn.cursor()


# Получаем номер телефона магазина
def get_phone_number():
    url = "https://edge.qiwi.com/person-profile/v1/profile/current"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }
    r = requests.get(url, headers=headers)
    phone_number = r.json()["contractInfo"]["contractId"]
    if r.status_code == 200:
        return phone_number
    else:
        return False


phone_number = get_phone_number()


# Получение баланса
def get_balance():
    url = "https://edge.qiwi.com/funding-sources/v2/persons/" + str(phone_number) + "/accounts"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json()["accounts"][0]["balance"]["amount"]
    else:
        return False


# Генерируем ссылку на форму оплаты для пользователя
def get_payment_link(amount, vk_id):
    # Получаем номер транзакции
    temp = "select id from transactions where user_id = " + str(vk_id) + " and status = 'pending'"
    cursor.execute(temp)
    bill_id = cursor.fetchone()[0]


    # Генерируем ссылку
    url = "https://api.qiwi.com/partner/bill/v1/bills/" + str(bill_id)
    headers = {
        "Authorization": "Bearer " + secret_key,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    # Время жизни 10 минут
    expirationDateTime = datetime.now() + timedelta(minutes=10)
    expirationDateTime = expirationDateTime.strftime("%Y-%m-%dT%H:%M:%S+00:00")
    params = {
        "amount": {
            "value": amount,
            "currency": "RUB"
        },
        "expirationDateTime": expirationDateTime,
        "customFields": {
            "vk_id": vk_id
        }
    }
    # PUT запрос
    r = requests.put(url, headers=headers, json=params)
    if r.status_code == 200:
        return (r.json()["payUrl"])
    else:
        return "Ошибка при создании ссылки на оплату, попробуйте позже"


# Получаем информацию о платеже
def get_payment_info(bill_id):
    url = "https://api.qiwi.com/partner/bill/v1/bills/" + str(bill_id)
    headers = {
        "Authorization": "Bearer " + secret_key,
        "Accept": "application/json"
    }
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        return r.json()
    else:
        return False


# Проверяем статус платежа
def check_payment_status(bill_id):
    # Получаем информацию о платеже
    payment_info = get_payment_info(bill_id)
    # Если платеж не найден
    if payment_info == False:
        return "Платеж не найден"
    # Если платеж найден
    else:
        # Если платеж не оплачен
        if payment_info["status"]["value"] == "WAITING":
            return "WAITING"
        # Если платеж оплачен
        elif payment_info["status"]["value"] == "PAID":
            return "PAID"
        # Если платеж отменен
        elif payment_info["status"]["value"] == "REJECTED":
            return "REJECTED"
        # Если платеж не оплачен
        else:
            return "WAITING"


# Отменяем платеж
def cancel_payment(bill_id):
    url = "https://api.qiwi.com/partner/bill/v1/bills/" + str(bill_id) + "/reject"
    headers = {
        "Authorization": "Bearer " + secret_key,
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    r = requests.post(url, headers=headers)
    if r.status_code == 200:
        return True
    else:
        return False


# Получаем историю платежей за последние 30 минут
def get_history():
    url = "https://edge.qiwi.com/payment-history/v2/persons/" + str(phone_number) + "/payments"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }
    start_date = datetime.now() - timedelta(minutes=30)
    start_date = start_date.strftime("%Y-%m-%dT%H:%M:%S+00:00")
    end_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S+00:00")
    params = {
        "rows": "50",
        "operation": "IN",
        "sources[0]": "QW_RUB",
        "startDate": start_date,
        "endDate": end_date
    }
    r = requests.get(url, headers=headers, params=params)
    return r.json()


# Делаем перевод на QIWI кошелек
def transfer_to_qiwi(amount, phone_number):
    url = "https://edge.qiwi.com/sinap/api/v2/terms/99/payments"
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer " + token
    }
    params = {
        # 1000*(Standard Unix time в секундах)
        "id": str(int(time.time() * 1000)),
        "sum": {
            "amount": amount,
            "currency": "643"
        },
        "paymentMethod": {
            "type": "Account",
            "accountId": "643"
        },
        "fields": {
            "account": str(phone_number)
        }
    }
    r = requests.post(url, headers=headers, json=params)
    if r.status_code == 200:
        return True
    else:
        return False












def test():
    return 0
    # return transfer_to_qiwi(1, "79220027221")
