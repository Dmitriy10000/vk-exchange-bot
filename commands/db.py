from dotenv import load_dotenv
import psycopg2
from psycopg2._psycopg import connection
import os


# Создаем таблицу пользователей в БД
def create_users_table(conn: connection):
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            create table if not exists users (
                user_id         integer primary key not null,
                qiwi            text                            default null,
                is_admin        boolean             not null    default false,
                location_id     integer             not null    default 0,
                first_name      text                not null,
                last_name       text                not null
            );
            """
        )
        conn.commit()
        print("Таблица пользователей успешно создана")
    except Exception as e:
        print("Ошибка при создании таблицы пользователей: ", e)


# Создаем таблицу транзакций в БД
def create_transactions_table(conn: connection):
    try:
        cursor = conn.cursor()
        cursor.execute(
            """
            create table if not exists transactions (
                id              bigserial primary key   not null,
                user_id         integer                 not null,
                vkc_amount      bigint                  not null,
                rub_amount      bigint                  not null,
                type            text                    not null,
                status          text                    not null,
                date            date                    not null    default current_date,
                time            time                    not null    default current_time
            );
            """
        )
        conn.commit()
        print("Таблица транзакций успешно создана")
    except Exception as e:
        print("Ошибка при создании таблицы транзакций: ", e)


# Подключение к БД
def connect_to_db():
    try:
        load_dotenv()
        conn = psycopg2.connect(
            user=os.environ.get("USER"),
            host=os.environ.get("HOST"),
            database=os.environ.get("DATABASE"),
            password=os.environ.get("PASSWORD"),
            # port=os.environ.get("PORT")
            port=5432
        )
        create_users_table(conn)
        create_transactions_table(conn)
        print("База данных успешно подключена")
        return conn
    except:
        print("Ошибка подключения к базе данных")