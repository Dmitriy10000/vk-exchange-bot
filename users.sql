-- Создать таблицу users
create table if not exists users (
    user_id         integer primary key not null,
    qiwi            text                            default null,
    is_admin        boolean             not null    default false,
    location_id     integer             not null    default 0,
    first_name      text                not null,
    last_name       text                not null
);

-- Вывести список админов
select * from users where is_admin = true;

-- Назначить админом
update users set is_admin = true where user_id = 216738936;

-- Получаем location_id
select location_id from users where user_id = 216738936;

-- Устанавливаем location_id
update users set location_id = 1 where user_id = 216738936;

-- Назначаем админом и устанавливаем location_id = 10
update users set is_admin = true, location_id = 10 where user_id = 216738936;

-- Добавить пользователя если его нет
insert into users (user_id, first_name, last_name) values (216738936, 'А', 'Б') on conflict do nothing;

-- Получить количество пользователей
select count(*) from users;

-- Добавить vkc_buy
update users set vkc_buy = vkc_buy + 1 where user_id = 216738936;

-- Создать таблицу transactions
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

-- Добавить транзакцию покупки
insert into transactions (user_id, vkc_amount, rub_amount, type, status) values (216738936, 1, 100, 'buy', 'success');

-- Добавить транзакцию продажи
insert into transactions (user_id, vkc_amount, rub_amount, type, status) values (216738936, 1, 100, 'sell', 'success');

-- Получить кол-во транзакций пользователя
select count(*) from transactions where user_id = 216738936;

-- Общий оборот VKC
select sum(vkc_amount) from transactions;

-- Общий оборот RUB
select sum(rub_amount) from transactions;

-- Получить общее кол-во транзакций
select count(*) from transactions;

-- Обнуляем все данные в таблице users, кроме столбца user_id
update users set is_admin = false, location_id = 0, vkc_sell = 0, vkc_buy = 0;

-- Проверка существования таблицы users
select exists(select * from information_schema.tables where table_name = 'users');

-- Проверка существования таблицы transactions
select exists(select * from information_schema.tables where table_name = 'transactions');

-- Удалить таблицу users
drop table users;

-- Удалить таблицу transactions
drop table transactions;

-- Вывести id транзакции, где user_id = 216738936 и status = 'pending'
select id from transactions where user_id = 216738936 and status = 'pending';

-- Проверка существования пользователя
select exists(select * from users where user_id = 216738936);

-- Отменяем транзакцию
update transactions set status = 'canceled' where user_id = 216738936 and status = 'pending';

-- Получить кол-во успешных транзакций пользователя
select count(*) from transactions where user_id = 216738936 and status = 'success';

-- Получить кол-во купленных VKC пользователя
select sum(vkc_amount) from transactions where user_id = 216738936 and type = 'buy' and status = 'success';

-- Получить кол-во проданных VKC пользователя
select sum(vkc_amount) from transactions where user_id = 216738936 and type = 'sell' and status = 'success';

-- Получить id транзакции по user_id и status = 'pending'
select id from transactions where user_id = 216738936 and status = 'pending';

-- Получить дату и время последней транзакции пользователя по user_id
select date, time from transactions where user_id = 216738936 order by id desc limit 1;