from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView

from rest_framework import status
from homework.models import Homework,HomeworkSubmission
from .serializers import HomeworkSerializer,HomeworkUpdateSerializer,HomeworkSubmissionSerializer
from account.api.validators import IsActiveTeacher,IsStudent
from django.utils import timezone



class SubmitHomeworkView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def post(self, request):
        homework_id = request.data.get("homework_id")
        if not homework_id:
            return Response({"error": "homework_id is required."}, status=400)

        try:
            homework = Homework.objects.get(id=homework_id)
        except Homework.DoesNotExist:
            return Response({"error": "Homework not found."}, status=404)

        # Check if the student is in the class
        if homework.classroom not in request.user.enrolled_classes.all():
            return Response({"error": "You are not enrolled in this class."}, status=403)

        # Check deadline
        if timezone.now() > homework.deadline:
            return Response({"error": "The deadline for this homework has passed."}, status=403)

        # Find or create submission
        submission, created = HomeworkSubmission.objects.get_or_create(
            student=request.user,
            homework=homework,
            defaults={
                "answer_text": request.data.get("answer_text", ""),
                "answer_file": request.FILES.get("answer_file"),
            }
        )

        if not created:
            # Update existing
            submission.answer_text = request.data.get("answer_text", submission.answer_text)
            if request.FILES.get("answer_file"):
                submission.answer_file = request.FILES["answer_file"]
            submission.save()

        serializer = HomeworkSubmissionSerializer(submission)
        return Response({
            "message": "Homework submitted." if created else "Homework updated.",
            "data": serializer.data
        }, status=201)


class HomeworkUpdateView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsActiveTeacher]
    queryset = Homework.objects.all()

    def get_serializer_class(self):
        return HomeworkUpdateSerializer if self.request.method == "PATCH" else HomeworkSerializer

    def get_queryset(self):
        return self.queryset.filter(teacher=self.request.user)

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)


class HomeworkListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsActiveTeacher]

    def get(self, request):
        homeworks = Homework.objects.filter(teacher=request.user).order_by('-created_at')
        serializer = HomeworkSerializer(homeworks, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        serializer = HomeworkSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(teacher=request.user)
            return Response({"message": "Homework created", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
