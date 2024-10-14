CREATE USER repl_user REPLICATION LOGIN PASSWORD '1234';

-- Создание базы данных
CREATE DATABASE bot;


\connect bot;


CREATE TABLE IF NOT EXISTS phone_nubers (
    id SERIAL PRIMARY KEY,
    phone_number VARCHAR(20) NOT NULL
);


CREATE TABLE IF NOT EXISTS emails (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) NOT NULL
);


INSERT INTO emails (email) 
VALUES ('aboba@gmail.com'), ('bibka@yandex.ru');

INSERT INTO phone_numbers (phone_number) 
VALUES ('88005553535'), ('+78888888888');

