from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import TeacherRegisterSerializer, StudentRegisterSerializer,AddStudentByTeacherSerializer,TeacherProfileUpdateSerializer,StudentProfileUpdateSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model

from .validators import IsActiveTeacher,IsStudent
from .utils import generate_user_response

User = get_user_model()

class StudentProfileView(APIView):
    permission_classes = [IsAuthenticated, IsStudent]

    def get(self, request):
        serializer = StudentProfileUpdateSerializer(request.user)
        return Response({"data": serializer.data})

    def patch(self, request):
        serializer = StudentProfileUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response(
                {"detail": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(
                {"detail": "Invalid national ID or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.check_password(password):
            return Response(
                {"detail": "Invalid national ID or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {"detail": "Your account is awaiting admin approval."},
                status=status.HTTP_403_FORBIDDEN
            )

        return Response(generate_user_response(user))


class TeacherRegisterView(APIView):
    def post(self, request):
        serializer = TeacherRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(generate_user_response(user), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentRegisterView(APIView):
    def post(self, request):
        serializer = StudentRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(generate_user_response(user), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddStudentByTeacherView(APIView):
    permission_classes = [IsAuthenticated, IsActiveTeacher]

    def post(self, request):
        serializer = AddStudentByTeacherSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(generate_user_response(user), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TeacherProfileView(APIView):
    permission_classes = [IsAuthenticated, IsActiveTeacher]

    def get(self, request):
        return Response(generate_user_response(request.user))

    def patch(self, request):
        serializer = TeacherProfileUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(generate_user_response(request.user))
        return Response({"data": {"success": False, "errors": serializer.errors}}, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            request.user.auth_token.delete()
        except Token.DoesNotExist:
            pass  # Already logged out

        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)
