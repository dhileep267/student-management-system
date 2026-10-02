from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient


class DashboardAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="dashboarduser",
            password="testpassword"
        )

        response = self.client.post(
            "/api/token/",
            {
                "username": "dashboarduser",
                "password": "testpassword"
            },
            format="json"
        )

        access_token = response.data["access"]

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

    def test_dashboard_api(self):

        response = self.client.get("/api/dashboard/")

        self.assertEqual(response.status_code, 200)

        self.assertIn("total_students", response.data)
        self.assertIn("total_departments", response.data)
        self.assertIn("average_age", response.data)