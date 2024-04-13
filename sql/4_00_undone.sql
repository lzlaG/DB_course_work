CREATE OR REPLACE VIEW un_done AS
SELECT *
FROM Заявки
WHERE Статус = 1;

--SELECT * FROM un_done;