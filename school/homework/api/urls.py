from django.urls import path
from .views import HomeworkListCreateView,HomeworkUpdateView,SubmitHomeworkView

urlpatterns = [
    path('', HomeworkListCreateView.as_view(), name='teacher-homework'),
    path('update/<int:pk>/', HomeworkUpdateView.as_view(), name='update-homework'),
    path('submit/', SubmitHomeworkView.as_view(), name='submit-homework'),
]
