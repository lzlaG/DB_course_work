-- Active: 1712897215912@@127.0.0.1@4903@DB_completed_tasks
CREATE OR REPLACE PROCEDURE change_status(
    new_id_status INT,
    task_id INT
)
LANGUAGE SQL
AS $$
UPDATE Заявки
SET Статус = new_id_status
WHERE id_заявки = task_id;
$$;

--CALL change_status(3,1);