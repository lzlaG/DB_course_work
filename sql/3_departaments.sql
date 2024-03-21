CREATE TABLE Отделы
(
    Id_отдела INTEGER PRIMARY KEY,
    ID_Сотрудника INTEGER NOT NULL REFERENCES Личные_данные(Id_сотрудника),
    Должность VARCHAR(30),
    Компетенция VARCHAR(20),
    Название_отдела VARCHAR(30)
);