from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from account.models import User
from rest_framework.authtoken.models import Token

class TestAccountViews(APITestCase):

    def setUp(self):
        self.teacher = User.objects.create_user(
            username="teacher001",
            password="pass1234",
            first_name="Ali",
            last_name="Karimi",
            role="teacher",
            national_id="1234567890",
            is_active=True
        )

        self.student = User.objects.create_user(
            username="student001",
            password="pass1234",
            first_name="Sara",
            last_name="Ahmadi",
            role="student",
            national_id="0084575948",
            is_active=True
        )

        self.teacher_token, _ = Token.objects.get_or_create(user=self.teacher)
        self.student_token, _ = Token.objects.get_or_create(user=self.student)

        self.client = APIClient()
    def test_login_teacher_success(self):
        response = self.client.post(reverse('login'), {
            "username": "teacher001",
            "password": "pass1234"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.data["data"])

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('login'), {
            "username": "teacher001",
            "password": "wrongpass"
        })
        self.assertEqual(response.status_code, 401)
    def test_logout(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.teacher_token.key}")
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], "Successfully logged out.")

    def test_get_student_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.student_token.key}")
        response = self.client.get(reverse('student-profile'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["first_name"], "Sara")

    def test_update_student_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.student_token.key}")
        response = self.client.patch(reverse('student-profile'), {
            "first_name": "Fatemeh",
            "latitude": 35.6,
            "longitude": 51.3
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["first_name"], "Fatemeh")

    def test_get_teacher_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.teacher_token.key}")
        response = self.client.get(reverse('teacher-profile'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["username"], "teacher001")
