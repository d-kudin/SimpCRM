# website/tests/test_models.py

from django.test import TestCase
from website.models import Record

class RecordModelTest(TestCase):

    def setUp(self):
        self.record = Record.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
            phone="123456789",
            address="123 Main St",
            city="Warsaw",
            state="Masovian",
            postal_code="00-001"
        )

    def test_record_creation(self):
        self.assertEqual(self.record.first_name, "John")
        self.assertEqual(self.record.last_name, "Doe")
        self.assertEqual(self.record.email, "john.doe@example.com")
        self.assertEqual(self.record.phone, "123456789")
        self.assertEqual(self.record.address, "123 Main St")
        self.assertEqual(self.record.city, "Warsaw")
        self.assertEqual(self.record.state, "Masovian")
        self.assertEqual(self.record.postal_code, "00-001")