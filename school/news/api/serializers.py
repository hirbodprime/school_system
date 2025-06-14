from rest_framework import serializers
from news.models import News
from classroom.api.serializers import ClassroomSerializer
from classroom.models import Classroom

class NewsUpdateSerializer(serializers.ModelSerializer):
    classroom_id = serializers.PrimaryKeyRelatedField(
        queryset=Classroom.objects.all(), source='classroom', required=False
    )

    class Meta:
        model = News
        fields = ['title', 'description', 'updated_at', 'classroom_id']
        read_only_fields = ['updated_at']

        
class NewsSerializer(serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField()
    classroom = ClassroomSerializer(read_only=True)
    classroom_id = serializers.PrimaryKeyRelatedField(
        queryset=Classroom.objects.all(), source='classroom', write_only=True
    )
    views_count = serializers.SerializerMethodField()
    seen = serializers.SerializerMethodField() 

    class Meta:
        model = News
        fields = [
            'id', 'title', 'description', 'created_at', 'updated_at', 'views_count', 'seen',
            'teacher', 'classroom', 'classroom_id'
        ]
        read_only_fields = ['created_at', 'updated_at', 'teacher']

    def get_teacher(self, obj):
        return {
            "username": obj.teacher.username,
            "first_name": obj.teacher.first_name,
            "last_name": obj.teacher.last_name,
            "id": obj.teacher.id,
        }
    def get_views_count(self, obj):
        return obj.views.count()
    def get_seen(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated and request.user.role == 'student':
            return obj.views.filter(student=request.user).exists()
        return False