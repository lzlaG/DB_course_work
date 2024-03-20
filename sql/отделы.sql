CREATE TABLE Отделы
(
    Id SERIAL PRIMARY KEY,
    ID_Сотрудника INTEGER NOT NULL REFERENCES Личные_данные(Id),
    Должность VARCHAR(30),
    Компетенция VARCHAR(20),
    Название_отдела VARCHAR(30)
);