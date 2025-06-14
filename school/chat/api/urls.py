from django.urls import path
from .views import SendMessageView, ConversationListView, MessageHistoryView

urlpatterns = [
    path('send/', SendMessageView.as_view(), name='chat-send'),
    path('conversations/', ConversationListView.as_view(), name='chat-conversations'),
    path('messages/<int:user_id>/', MessageHistoryView.as_view(), name='chat-messages'),
]
