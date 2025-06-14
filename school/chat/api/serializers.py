from rest_framework import serializers
from chat.models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'sent_at', 'read']
        read_only_fields = ['sender', 'sent_at', 'read']