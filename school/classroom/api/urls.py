from django.urls import path
from .views import TeacherClassesLessonsView,StudentClassesView,AddStudentToClassView,StudentHomeworkListView,StudentNewsListView

urlpatterns = [
    path('classes/', TeacherClassesLessonsView.as_view(), name='teacher-classes-lessons'),
    path('teacher/classes/add-student/', AddStudentToClassView.as_view(), name='add-student-to-class'),
    path('student/classes/', StudentClassesView.as_view(), name='student-classes'),
    path('student/news/', StudentNewsListView.as_view(), name='student-news'),
    path('student/homework/', StudentHomeworkListView.as_view(), name='student-homework'),
]
