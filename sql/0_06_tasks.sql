CREATE TABLE Заявки
(
    Id_заявки INTEGER PRIMARY KEY,
    Наименование VARCHAR(60),
    Дата DATE,
    Тип_работы INTEGER NOT NULL REFERENCES Типы_работ(Id_типа_работ),
    Статус INTEGER NOT NULL REFERENCES Статус(Id_статуса)
);