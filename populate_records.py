# populate_records.py

import os
import django
import random
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from website.models import Record

fake = Faker()
countries = {
    'USA': ['New York', 'California', 'Texas', 'Florida', 'Illinois'],
    'UE': ['Germany', 'France', 'Spain', 'Italy', 'Poland']
}

def create_records():
    for i in range(10):
        # USA
        state = random.choice(countries['USA'])
        Record.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            phone=fake.phone_number(),
            address=fake.street_address(),
            city=fake.city(),
            state=state,
            postal_code=fake.postcode()
        )
    for i in range(10):
        # UE
        state = random.choice(countries['UE'])
        Record.objects.create(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            phone=fake.phone_number(),
            address=fake.street_address(),
            city=fake.city(),
            state=state,
            postal_code=fake.postcode()
        )
    print("✅ Successfully added 20 sample records (UE + USA)")

if __name__ == '__main__':
    create_records()
