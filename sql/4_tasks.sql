CREATE TABLE Заявки
(
    Id_заявки INTEGER PRIMARY KEY,
    Наименование VARCHAR(30),
    Дата DATE,
    Исполнитель INTEGER NOT NULL REFERENCES Личные_данные(Id_сотрудника),
    Отвественный INTEGER NOT NULL REFERENCES Личные_данные(Id_сотрудника),
    Тип_работы INTEGER NOT NULL REFERENCES Типы_работ(Id_типа_работ)
);