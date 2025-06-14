from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework import status
from news.models import News
from .serializers import NewsSerializer,NewsUpdateSerializer
from account.api.validators import IsActiveTeacher

class NewsUpdateView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated, IsActiveTeacher]
    queryset = News.objects.all()

    def get_serializer_class(self):
        return NewsUpdateSerializer if self.request.method == "PATCH" else NewsSerializer

    def get_queryset(self):
        print("GET called from NewsUpdateView ✅")

        return self.queryset.filter(teacher=self.request.user)

    def get(self, request, *args, **kwargs):
        print("GET called from NewsUpdateView ✅")

        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"data": serializer.data}, status=status.HTTP_200_OK)
    

class NewsListCreateView(APIView):
    permission_classes = [IsAuthenticated, IsActiveTeacher]

    def get(self, request):
        news = News.objects.filter(teacher=request.user).order_by('-created_at')
        serializer = NewsSerializer(news, many=True)
        return Response({"data": serializer.data})

    def post(self, request):
        serializer = NewsSerializer(data=request.data)
        if serializer.is_valid():
            classroom = serializer.validated_data['classroom']
            if classroom.teacher != request.user:
                return Response({"error": "You can only add news to your own class."}, status=403)

            serializer.save(teacher=request.user)
            return Response({"message": "News created", "data": serializer.data}, status=201)

        return Response(serializer.errors, status=400)

