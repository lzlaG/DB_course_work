-- Active: 1713084168788@@127.0.0.1@4903@DB_completed_tasks
CREATE OR REPLACE PROCEDURE add_task(
    name_of_task VARCHAR(60),
    date_of_task DATE,
    type_of_work INT,
    status_of_task INT
)
LANGUAGE plpgsql
AS $$
DECLARE
    maxIndex INT;
BEGIN
    SELECT MAX(id_заявки) INTO maxIndex FROM Заявки;
    INSERT INTO Заявки VALUES (maxIndex + 1, name_of_task, date_of_task, type_of_work, status_of_task);
END;
$$;
SELECT * FROM Заявки;
CALL add_task('починка кузова', '2024-04-13', 4, 2);

SELECT * FROM Заявки; 