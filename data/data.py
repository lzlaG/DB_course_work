from faker import Faker
import csv
from faker.providers import *
import random

fake = Faker("ru_RU") # задаем локаль данных

def pers_data(id):
    prefix = fake.prefix()
    id +=1
    if prefix=='тов.':
        return [id,'М',fake.last_name_male(),fake.first_name_male(),fake.middle_name_male(),fake.free_email(),fake.phone_number(),fake.job(),random.randint(1,5),random.randint(1,5)]
    else:
        return [id,'Ж', fake.last_name_female(),fake.first_name_female(),fake.middle_name_female(),fake.free_email(),fake.phone_number(),fake.job(),random.randint(1,5),random.randint(1,5)]

with open('./data/pers_data.csv', 'w') as csvfile: #
    writer = csv.writer(csvfile)
    writer.writerow(['Id', 'Пол', 'Фамилия', 'Имя', 'Отчество', 'email', 'телефон','Должность','Компетенция','Отдел'])
    for i in range (5):
        writer.writerow(pers_data(i))

