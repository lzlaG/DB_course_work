from faker import Faker
import csv
from faker.providers import *
import random

fake = Faker('ru_RU') # задаем локаль данных

def pers_data(id):
    prefix = fake.prefix()
    id +=1
    if prefix=='тов.':
        return [id,'М',fake.last_name_male(),fake.first_name_male(),fake.middle_name_male(),fake.free_email(),fake.phone_number(),fake.job(),random.randint(1,5),random.randint(1,5)]
    else:
        return [id,'Ж', fake.last_name_female(),fake.first_name_female(),fake.middle_name_female(),fake.free_email(),fake.phone_number(),fake.job(),random.randint(1,5),random.randint(1,5)]

with open('./data/pers_data.csv', 'w') as csvfile: #записываем данные  в csv файл
    writer = csv.writer(csvfile)
    writer.writerow(['Id', 'Пол', 'Фамилия', 'Имя', 'Отчество', 'email', 'телефон','Должность','Компетенция','Отдел'])
    for i in range (5):
        writer.writerow(pers_data(i))

def Tasks(id):
    task_list = [ #перечисление видов работ
        'Комплексное техническое обслуживание',
        'Диагностика и ремонт электроники автомобиля',
        'Замена масла и фильтров',
        'Ремонт тормозной системы и замена колодок',
        'Шиномонтаж и балансировка колес',
        'Диагностика и ремонт двигателя',
        'Обслуживание и ремонт системы кондиционирования',
        'Замена передач и дифференциалов',
        'Реставрация кузова и покраска',
        'Устранение шумов и вибраций',
        'Обновление системы освещения и сигнализации',
        'Регулировка подвески и рулевого управления',
        'Установка сигнализации и дополнительного оборудования',
        'Диагностика и ремонт системы вывода отработавших газов',
        'Тюнинг и модификация автомобиля'
    ]
    random_work = fake.word(ext_word_list=task_list) # выбираем рандомную работу
    return [id+1,random_work,fake.date(),random.randint(1,5),random.randint(1,3)] 


with open('./data/task_data.csv', 'w') as csvfile: #записываем заявки  в csv файл
    writer = csv.writer(csvfile)
    writer.writerow(['Id_заявки', 'Наименование', 'Дата', 'Тип_работы', 'Статус'])
    for i in range (15):
        writer.writerow(Tasks(i))
