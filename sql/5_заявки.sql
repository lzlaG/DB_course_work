CREATE TABLE Заявки
(
    Id SERIAL PRIMARY KEY,
    Наименование VARCHAR(30),
    Дата DATE,
    Исполнитель INTEGER NOT NULL REFERENCES Личные_данные(Id),
    Отвественный INTEGER NOT NULL REFERENCES Личные_данные(Id),
    Статус INTEGER NOT NULL REFERENCES Статус(Id),
    Тип_работы INTEGER NOT NULL REFERENCES Типы_работ(Id)
);