from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse
from account.models import User
from core.models import School

class ClosestSchoolsViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            national_id="1234567890",
            role="student",
            is_active=True,
            latitude=35.7000,  # Near Tehran
            longitude=51.4000
        )
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Nearby schools
        School.objects.create(name="School A", latitude=35.7010, longitude=51.4010)
        School.objects.create(name="School B", latitude=35.7020, longitude=51.4020)
        School.objects.create(name="School C", latitude=35.7030, longitude=51.4030)

        # Far schools
        School.objects.create(name="School D", latitude=32.0000, longitude=51.0000)
        School.objects.create(name="School E", latitude=29.0000, longitude=52.0000)

    def test_closest_schools_returns_top_3(self):
        response = self.client.get(reverse("closest-schools"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("closest_schools", response.data)
        self.assertEqual(len(response.data["closest_schools"]), 3)
        school_names = [school["name"] for school in response.data["closest_schools"]]
        self.assertIn("School A", school_names)
        self.assertIn("School B", school_names)
        self.assertIn("School C", school_names)

    def test_closest_schools_location_not_set(self):
        self.user.latitude = None
        self.user.longitude = None
        self.user.save()

        response = self.client.get(reverse("closest-schools"))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data["error"], "Your location is not set.")
