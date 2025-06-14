# chat/views.py

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from chat.models import Message
from chat.api.serializers import MessageSerializer
from account.models import User
from django.db.models import Q

class SendMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        recipient_id = request.data.get("recipient_id")
        content = request.data.get("content")

        if not recipient_id or not content:
            return Response({"error": "recipient_id and content are required."}, status=400)

        try:
            recipient = User.objects.get(id=recipient_id)
        except User.DoesNotExist:
            return Response({"error": "Recipient not found."}, status=404)

        message = Message.objects.create(
            sender=request.user,
            recipient=recipient,
            content=content
        )

        serializer = MessageSerializer(message)
        return Response({"message": "Message sent.", "data": serializer.data}, status=201)


class ConversationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Distinct user IDs this user has chatted with
        recipients = Message.objects.filter(sender=user).values_list('recipient', flat=True)
        senders = Message.objects.filter(recipient=user).values_list('sender', flat=True)
        partner_ids = set(list(recipients) + list(senders))

        users = User.objects.filter(id__in=partner_ids)
        data = [
            {
                "id": u.id,
                "first_name": u.first_name,
                "last_name": u.last_name,
                "username": u.username,
                "role": u.role
            } for u in users
        ]
        return Response({"data": data})
class MessageHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            partner = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)

        messages = Message.objects.filter(
            Q(sender=request.user, recipient=partner) |
            Q(sender=partner, recipient=request.user)
        ).order_by('sent_at')

        serializer = MessageSerializer(messages, many=True)
        return Response({"data": serializer.data})
