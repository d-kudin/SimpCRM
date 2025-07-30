# website/tests/test_authentication.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthenticationTest(TestCase):

    def setUp(self):
        self.credentials = {
            'username': 'john',
            'password': 'secret123'
        }
        User.objects.create_user(**self.credentials)

    def test_login_valid_user(self):
        response = self.client.post(reverse('home'), self.credentials, follow=True)
        self.assertTrue(response.context['user'].is_authenticated)
        self.assertContains(response, "Logout")

    def test_login_invalid_user(self):
        response = self.client.post(reverse('home'), {
            'username': 'john',
            'password': 'wrongpass'
        }, follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_logout(self):
        self.client.login(**self.credentials)
        response = self.client.get(reverse('logout'), follow=True)
        self.assertFalse(response.context['user'].is_authenticated)

    def test_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'anna',
            'first_name': 'Anna',
            'last_name': 'Nowak',
            'email': 'anna@example.com',
            'password1': 'SuperSecret123',
            'password2': 'SuperSecret123',
        }, follow=True)
        self.assertTrue(User.objects.filter(username='anna').exists())
        self.assertTrue(response.context['user'].is_authenticated)
