# website/tests/test_views.py

from django.test import TestCase
from django.urls import reverse

class HomeViewTest(TestCase):
    
    def test_home_view_status_code(self):
        url = reverse("home")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_view_template_used(self):
        url = reverse("home")
        response = self.client.get(url)
        self.assertTemplateUsed(response, "home.html")

    def test_home_view_contains_title_or_keyword(self):
        """Optional: Check if key content exists in the page."""
        response = self.client.get(reverse("home"))
        self.assertContains(response, "<title>SimpCRM</title>", html=True)