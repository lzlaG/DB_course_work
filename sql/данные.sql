-- Active: 1710951336829@@127.0.0.1@4903@DB_completed_tasks
CREATE TABLE Личные_данные
(
    Id SERIAL PRIMARY KEY,
    Пол VARCHAR(1) NOT NULL,
    Имя VARCHAR(30) NOT NULL,
    Фамилия VARCHAR(30) NOT NULL,
    Отчество VARCHAR(30),
    Email VARCHAR(30),
    Телефон VARCHAR(10)
);