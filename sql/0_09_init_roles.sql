-- Active: 1713084168788@@127.0.0.1@4903@DB_completed_tasks
CREATE ROLE big_boss WITH LOGIN;
ALTER ROLE big_boss WITH PASSWORD 'jumanji';
GRANT ALL ON Заявки,Личные_данные,Отделы,Типы_работ TO big_boss;

CREATE ROLE usual_worker WITH LOGIN;
ALTER ROLE usual_worker WITH PASSWORD 'jumanji_1';
GRANT USAGE ON SCHEMA public TO usual_worker;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO usual_worker;
