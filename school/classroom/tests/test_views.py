from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse
from account.models import User
from classroom.models import Classroom, Lesson
from homework.models import Homework
from news.models import News


class TestClassroomViews(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username="teacher1", password="pass1234", role="teacher", is_active=True
        )
        self.student = User.objects.create_user(
            username="student1", password="pass1234", role="student", is_active=True
        )
        self.teacher_token, _ = Token.objects.get_or_create(user=self.teacher)
        self.student_token, _ = Token.objects.get_or_create(user=self.student)
        self.client = APIClient()

        # Create a school and classroom
        self.classroom = Classroom.objects.create(name="Math Class", teacher=self.teacher)
        self.classroom.students.add(self.student)

        # Lessons
        self.lesson1 = Lesson.objects.create(name="Algebra", classroom=self.classroom)
        self.lesson2 = Lesson.objects.create(name="Geometry", classroom=self.classroom)

        # Homework
        self.homework = Homework.objects.create(
            classroom=self.classroom,
            lesson=self.lesson1,
            teacher=self.teacher,
            title="Homework 1",
            description="Solve problems",
            deadline="2030-12-31T23:59:59Z"
        )

        # News
        self.news = News.objects.create(
            teacher=self.teacher,
            classroom=self.classroom,
            title="Exam Schedule",
            description="Exam next week"
        )
    def test_teacher_classes_lessons_view(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.teacher_token.key}")
        response = self.client.get(reverse('teacher-classes-lessons'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["classroom"]["name"], "Math Class")
    def test_add_student_to_class(self):
        new_student = User.objects.create_user(
            username="student2", password="pass1234", role="student", national_id="1111111111", is_active=True
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.teacher_token.key}")
        url = reverse('add-student-to-class')
        data = {"classroom_id": self.classroom.id, "student_national_id": "1111111111"}

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["student"]["first_name"], "")
    def test_student_classes_view(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.student_token.key}")
        response = self.client.get(reverse('student-classes'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["classroom_name"], "Math Class")
    def test_student_news_list_view(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.student_token.key}")
        response = self.client.get(reverse('student-news'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["title"], "Exam Schedule")
    def test_student_homework_list_view(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.student_token.key}")
        response = self.client.get(reverse('student-homework'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["title"], "Homework 1")
