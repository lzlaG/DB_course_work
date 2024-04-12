host = "127.0.0.1"
user = "admin"
password = "a1m40sdf"
db_name = "DB_completed_tasks"
#port = "4903"

'''
environment:
      POSTGRES_DB: "DB_completed_tasks"
      POSTGRES_USER: "admin"
      POSTGRES_PASSWORD: "a1m40sdf"
    volumes:
      - ./sql:/docker-entrypoint-initdb.d
      - ./data/pers_data.csv:/my_data/pers_data.csv
      - ./data/task_data.csv:/my_data/task_data.csv
      - ./data/complete_data.csv:/my_data/complete_data.csv
    ports: 
      - "4903:5432"
'''
