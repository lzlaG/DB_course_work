from faker import Faker
import csv
from faker.providers import *

fake = Faker("ru_RU") # задаем локаль данных

def pers_data(id):
    prefix = fake.prefix()
    id +=1
    if prefix=='тов.':
        return [id,'М',fake.last_name_male(),fake.first_name_male(),fake.middle_name_male(),fake.free_email(),fake.phone_number()]
    else:
        return [id,'Ж', fake.last_name_female(),fake.first_name_female(),fake.middle_name_female(),fake.free_email(),fake.phone_number()]

with open('pers_data.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Id', 'Пол', 'Фамилия', 'Имя', 'Отчество', 'email', 'телефон'])
    for i in range (15):
        writer.writerow(pers_data(i))
