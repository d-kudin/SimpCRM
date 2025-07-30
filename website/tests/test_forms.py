# website/tests/test_forms.py

from django.test import TestCase
from website.forms import SignUpForm

class SignUpFormTest(TestCase):
    
    def test_signup_form_valid_data(self):
        form = SignUpForm(data={
            "username": "jan_kowalski",
            "first_name": "Jan",
            "last_name": "Kowalski",
            "email": "jan.kowalski@example.com",
            "password1": "SuperSecret123",
            "password2": "SuperSecret123"
        })
        self.assertTrue(form.is_valid(), msg=form.errors)

    def test_signup_form_invalid_data(self):
        form = SignUpForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 6)