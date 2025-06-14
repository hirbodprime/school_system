from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from account.models import User
from chat.models import Message
from rest_framework.authtoken.models import Token


class TestChatViews(APITestCase):
    def setUp(self):
        self.teacher = User.objects.create_user(
            username="teacher1",
            password="pass1234",
            role="teacher",
            is_active=True
        )
        self.student = User.objects.create_user(
            username="student1",
            password="pass1234",
            role="student",
            is_active=True
        )

        self.teacher_token, _ = Token.objects.get_or_create(user=self.teacher)
        self.student_token, _ = Token.objects.get_or_create(user=self.student)

        self.client = APIClient()
    def test_send_message_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.teacher_token.key}")
        url = reverse('chat-send')
        data = {"recipient_id": self.student.id, "content": "Hello student!"}

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 201)
        self.assertIn("data", response.data)
        self.assertEqual(response.data["data"]["content"], "Hello student!")
    def test_conversation_list(self):
        # Create some messages
        Message.objects.create(sender=self.teacher, recipient=self.student, content="Hi there!")
        Message.objects.create(sender=self.student, recipient=self.teacher, content="Hi teacher!")

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.teacher_token.key}")
        url = reverse('chat-conversations')

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["data"]), 1)
        self.assertEqual(response.data["data"][0]["id"], self.student.id)
    def test_message_history(self):
        Message.objects.create(sender=self.teacher, recipient=self.student, content="First")
        Message.objects.create(sender=self.student, recipient=self.teacher, content="Second")

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.teacher_token.key}")
        url = reverse('chat-messages', args=[self.student.id])

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["data"]), 2)
        self.assertEqual(response.data["data"][0]["content"], "First")
