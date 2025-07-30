# website/tests/test_crud_customers.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from website.models import Record

class CustomerCRUDTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='user1', password='pass12345')
        self.client.login(username='user1', password='pass12345')
        self.record = Record.objects.create(
            first_name="Jan",
            last_name="Kowalski",
            email="jan@example.com",
            phone="123456789",
            address="ul. Testowa 1",
            city="Warszawa",
            state="Mazowieckie",
            postal_code="00-001"
        )

    def test_add_customer(self):
        response = self.client.post(reverse('add_record'), {
            "first_name": "Anna",
            "last_name": "Nowak",
            "email": "anna@example.com",
            "phone": "987654321",
            "address": "ul. Kwiatowa 2",
            "city": "Kraków",
            "state": "Małopolskie",
            "postal_code": "30-002"
        })
        self.assertEqual(Record.objects.count(), 2)
        self.assertRedirects(response, reverse('home'))

    def test_update_customer(self):
        response = self.client.post(reverse('update_record', args=[self.record.id]), {
            "first_name": "Janek",
            "last_name": "Kowalski",
            "email": "jan@example.com",
            "phone": "123456789",
            "address": "ul. Zmieniona",
            "city": "Warszawa",
            "state": "Mazowieckie",
            "postal_code": "00-001"
        })
        self.record.refresh_from_db()
        self.assertEqual(self.record.first_name, "Janek")
        self.assertRedirects(response, reverse('home'))

    def test_delete_customer(self):
        response = self.client.get(reverse('delete_record', args=[self.record.id]))
        self.assertEqual(Record.objects.count(), 0)
        self.assertRedirects(response, reverse('home'))
