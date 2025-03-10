from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from accounts.models import ShieldbotUser

# Create your tests here.

class DashboardTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = ShieldbotUser.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('username', response.data)
