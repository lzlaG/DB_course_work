#!/bin/bash
echo "Добро пожаловать!"
pers_data=./data/pers_data.csv
complete_data=./data/complete_data.csv
task_data=./data/task_data.csv
if [ -f "$pers_data" ]; then
    pers_data=1
else
    pers_data=0
fi
if [ -f "$complete_data" ]; then
    complete_data=1
else
    complete_data=0
fi
if [ -f "$task_data" ]; then
    task_data=1
else
    task_data=0
fi
if [ $task_data -eq 1 ] && [ $pers_data -eq 1 ] && [ $complete_data -eq 1 ]; then
    echo "все данные на месте, переходим к установке"
    docker compose build
    docker compose up -d
    echo "установка завершена"
else
    echo "нехватка данных"
    echo "хотите обновить или создать данные?(y/n)"
    read answer
    if [[ $answer == y ]]; then
        echo "обновляем данные"
        python3 ./data/data.py
        echo "данные обновлены, переходим к установке"
        docker compose build
        docker compose up -d
        echo "установка завершена"
    else
        echo "ошибка,для запуска необходимы данные"
    fi
fi