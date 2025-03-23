from django.test import TestCase
from django.urls import reverse

class HomeViewTest(TestCase):
    def test_home_view_status_code(self):
        """
        Test that the home view returns a 200 status code.
        """
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_view_uses_correct_template(self):
        """
        Test that the home view uses the 'core/index.html' template.
        """
        url = reverse('home')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'core/index.html')
