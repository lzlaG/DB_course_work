CREATE OR REPLACE FUNCTION clear_tasks() RETURNS VOID AS
$$
DECLARE
    id_of_task iNT;
BEGIN
    SELECT Заявки.id_заявки INTO id_of_task FROM Заявки WHERE Заявки.Статус = 3;  
    DELETE FROM Выполнение WHERE Выполнение.id_заявки = id_of_task;
    DELETE FROM Заявки WHERE Заявки.id_заявки = id_of_task;
END;
$$
LANGUAGE plpgsql;