-- Active: 1712897215912@@127.0.0.1@4903@DB_completed_tasks
CREATE OR REPLACE VIEW deps AS
SELECT Личные_данные.Фамилия, Личные_данные.Имя, Личные_данные.Отчество, Отделы.Название_отдела
FROM Личные_данные
JOIN Отделы ON Личные_данные.id_отдела = Отделы.id_отдела;

--SELECT * FROM deps;