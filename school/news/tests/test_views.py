from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse
from account.models import User
from classroom.models import Classroom
from news.models import News


class NewsAPITests(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username="teacher01", password="pass1234", role="teacher", is_active=True
        )
        self.other_teacher = User.objects.create_user(
            username="teacher02", password="pass1234", role="teacher", is_active=True
        )
        self.student = User.objects.create_user(
            username="student01", password="pass1234", role="student", is_active=True
        )
        self.classroom = Classroom.objects.create(name="Math", teacher=self.teacher)

        self.news = News.objects.create(
            teacher=self.teacher,
            classroom=self.classroom,
            title="Exam Notice",
            description="There will be an exam tomorrow."
        )

        self.client = APIClient()
        self.teacher_token, _ = Token.objects.get_or_create(user=self.teacher)
        self.student_token, _ = Token.objects.get_or_create(user=self.student)
        self.other_teacher_token, _ = Token.objects.get_or_create(user=self.other_teacher)

    def test_list_news(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.teacher_token.key}")
        url = reverse('teacher-news')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["data"]), 1)

    def test_create_news(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.teacher_token.key}")
        url = reverse('teacher-news')
        data = {
            "title": "Class Cancelled",
            "description": "No class tomorrow",
            "classroom_id": self.classroom.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["data"]["title"], "Class Cancelled")

    def test_create_news_wrong_teacher(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.other_teacher_token.key}")
        url = reverse('teacher-news')
        data = {
            "title": "Invalid News",
            "description": "Wrong classroom",
            "classroom_id": self.classroom.id  # not owned by this teacher
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)

    def test_update_news_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.teacher_token.key}")
        url = reverse('update-news', kwargs={'pk': self.news.id})
        response = self.client.patch(url, {"title": "Updated Title"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["title"], "Updated Title")

    def test_update_news_not_owner(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.other_teacher_token.key}")
        url = reverse('update-news', kwargs={'pk': self.news.id})
        response = self.client.patch(url, {"title": "Hacked"})
        self.assertEqual(response.status_code, 404)  # filtered out in get_queryset()

    def test_student_cannot_access_news_api(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.student_token.key}")
        url = reverse('teacher-news')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
