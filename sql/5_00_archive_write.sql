-- Active: 1713084168788@@127.0.0.1@4903@DB_completed_tasks
CREATE OR REPLACE FUNCTION write_to_archieve() RETURNS TRIGGER AS
$$
DECLARE
    id_of_task iNT;
    date_of_create DATE;
    date_of_today DATE;
BEGIN
    SELECT CURRENT_DATE INTO date_of_today;
    SELECT OLD.id_заявки INTO id_of_task FROM Заявки;  
    SELECT OLD.Дата INTO date_of_create FROM Заявки;
    INSERT INTO История_выполненных_заявок VALUES (id_of_task, date_of_create,date_of_today);
    RETURN NEW;
END;
$$
LANGUAGE plpgsql;

