from rest_framework import serializers
from classroom.models import Classroom, Lesson
from django.contrib.auth import get_user_model
User = get_user_model()

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'name']

class ClassroomSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = ['id', 'name', 'lessons']


class AddStudentToClassSerializer(serializers.Serializer):
    classroom_id = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all())
    student_national_id = serializers.CharField()

    def validate(self, data):
        teacher = self.context['request'].user
        classroom = data['classroom_id']
        if classroom.teacher != teacher:
            raise serializers.ValidationError("You can only modify your own classes.")
        return data

    def save(self):
        classroom = self.validated_data['classroom_id']
        national_id = self.validated_data['student_national_id']

        try:
            student = User.objects.get(national_id=national_id, role='student', is_active=True)
        except User.DoesNotExist:
            raise serializers.ValidationError("Student not found or not active.")

        if classroom.students.filter(id=student.id).exists():
            raise serializers.ValidationError("This student is already in the class.")

        classroom.students.add(student)
        return student

