from django.urls import path
from .views import TeacherRegisterView, StudentRegisterView,CustomLoginView,AddStudentByTeacherView,TeacherProfileView,StudentProfileView,LogoutView
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('register/teacher/', TeacherRegisterView.as_view()),
    path('register/student/', StudentRegisterView.as_view()),
    path('teacher/add-student/', AddStudentByTeacherView.as_view()),
    path('teacher/profile/', TeacherProfileView.as_view(), name='teacher-profile'),
    path('student/profile/', StudentProfileView.as_view(), name='student-profile'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

]
