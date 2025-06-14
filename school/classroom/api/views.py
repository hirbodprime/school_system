from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from classroom.models import Classroom, Lesson
from classroom.api.serializers import ClassroomSerializer, LessonSerializer,AddStudentToClassSerializer
from account.api.validators import IsActiveTeacher, IsStudent
from homework.api.serializers import HomeworkSerializer
from homework.models import Homework
from news.api.serializers import NewsSerializer
from news.models import News,NewsView

class TeacherClassesLessonsView(APIView):
    permission_classes = [IsAuthenticated, IsActiveTeacher]

    def get(self, request):
        classrooms = Classroom.objects.filter(teacher=request.user)
        data = []
        for classroom in classrooms:
            lessons = Lesson.objects.filter(classroom=classroom)
            data.append({
                "classroom": ClassroomSerializer(classroom).data,
                "lessons": LessonSerializer(lessons, many=True).data
            })
        return Response({"data": data})

class AddStudentToClassView(APIView):
    permission_classes = [IsAuthenticated, IsActiveTeacher]

    def post(self, request):
        serializer = AddStudentToClassSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            student = serializer.save()
            return Response({
                "message": "Student added to class.",
                "student": {
                    "id": student.id,
                    "first_name": student.first_name,
                    "last_name": student.last_name,
                    "national_id": student.national_id
                }
            }, status=201)
        return Response(serializer.errors, status=400)
    

class StudentNewsListView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        student = request.user

        news_items = News.objects.filter(
            classroom__students=student
        ).select_related('teacher', 'classroom').order_by('-created_at')

        # Track news views (first-time view)
        for news in news_items:
            NewsView.objects.get_or_create(student=student, news=news)

        serializer = NewsSerializer(news_items, many=True, context={'request': request})
        return Response({"data": serializer.data}, status=200)

    
class StudentHomeworkListView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        student = request.user

        # Get all homeworks related to any class the student is in
        homeworks = Homework.objects.filter(
            classroom__students=student
        ).select_related('teacher', 'classroom', 'lesson').order_by('-created_at')

        serializer = HomeworkSerializer(homeworks, many=True)
        return Response({"data": serializer.data}, status=200)

class StudentClassesView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        student = request.user
        classes = Classroom.objects.filter(students=student).prefetch_related('lessons')
        data = []

        for classroom in classes:
            lessons = Lesson.objects.filter(classroom=classroom)
            data.append({
                "classroom_id": classroom.id,
                "classroom_name": classroom.name,
                "teacher": {
                    "id": classroom.teacher.id,
                    "first_name": classroom.teacher.first_name,
                    "last_name": classroom.teacher.last_name,
                },
                "lessons": [
                    {"id": lesson.id, "name": lesson.name}
                    for lesson in lessons
                ]
            })

        return Response({"data": data}, status=200)
