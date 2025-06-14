from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.utils import timezone
from account.models import User
from classroom.models import Classroom, Lesson
from homework.models import Homework, HomeworkSubmission
import tempfile
from django.core.files.uploadedfile import SimpleUploadedFile
from datetime import timedelta

class HomeworkAPITests(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username="teacher1", password="pass1234", role="teacher", is_active=True
        )
        self.student = User.objects.create_user(
            username="student1", password="pass1234", role="student", is_active=True
        )

        self.teacher_token, _ = Token.objects.get_or_create(user=self.teacher)
        self.student_token, _ = Token.objects.get_or_create(user=self.student)

        self.classroom = Classroom.objects.create(name="Math", teacher=self.teacher)
        self.classroom.students.add(self.student)
        self.lesson = Lesson.objects.create(name="Algebra", classroom=self.classroom)

        self.homework = Homework.objects.create(
            teacher=self.teacher,
            title="HW 1",
            description="Solve equations",
            deadline=timezone.now() + timedelta(days=1),
            classroom=self.classroom,
            lesson=self.lesson
        )

        self.client = APIClient()

    def test_teacher_can_list_homeworks(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.teacher_token.key}")
        url = reverse('teacher-homework')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["data"]), 1)

    def test_teacher_can_create_homework(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.teacher_token.key}")
        url = reverse('teacher-homework')
        data = {
            "title": "HW 2",
            "description": "Do the worksheet",
            "deadline": (timezone.now() + timedelta(days=2)).isoformat(),
            "classroom_id": self.classroom.id,
            "lesson_id": self.lesson.id
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["data"]["title"], "HW 2")

    def test_teacher_can_update_homework(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.teacher_token.key}")
        url = reverse('update-homework', kwargs={'pk': self.homework.id})
        response = self.client.patch(url, {"title": "Updated Title"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["data"]["title"], "Updated Title")

    def test_student_can_submit_homework_text_only(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.student_token.key}")
        url = reverse('submit-homework')
        data = {
            "homework_id": self.homework.id,
            "answer_text": "My answer"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["data"]["answer_text"], "My answer")

    def test_student_can_submit_homework_file(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.student_token.key}")
        url = reverse('submit-homework')
        file = SimpleUploadedFile("answer.pdf", b"file_content", content_type="application/pdf")
        data = {
            "homework_id": self.homework.id,
            "answer_file": file
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue("answer_file" in response.data["data"])

    def test_student_cannot_submit_after_deadline(self):
        self.homework.deadline = timezone.now() - timedelta(days=1)
        self.homework.save()

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.student_token.key}")
        url = reverse('submit-homework')
        data = {
            "homework_id": self.homework.id,
            "answer_text": "Late answer"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 403)
        self.assertIn("deadline", response.data["error"].lower())
