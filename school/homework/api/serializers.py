from rest_framework import serializers
from homework.models import Homework,HomeworkSubmission
from classroom.models import Classroom, Lesson
from classroom.api.serializers import ClassroomSerializer, LessonSerializer

from datetime import datetime



class HomeworkUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ['title', 'description', 'deadline', 'attachment', 'updated_at']
        read_only_fields = ['updated_at','classroom']

    def validate_attachment(self, file):
        if file:
            if not file.name.lower().endswith(('.pdf', '.zip')):
                raise serializers.ValidationError("Only PDF or ZIP files are allowed.")
        return file

    def to_internal_value(self, data):
        deadline = data.get("deadline")
        if isinstance(deadline, str) and len(deadline) == 5 and deadline.count("-") == 1:
            try:
                current_year = datetime.now().year
                deadline = f"{current_year}-{deadline}"
                data['deadline'] = deadline
            except Exception:
                pass
        return super().to_internal_value(data)


class HomeworkSerializer(serializers.ModelSerializer):
    teacher = serializers.SerializerMethodField()
    classroom = ClassroomSerializer(read_only=True)
    lesson = LessonSerializer(read_only=True)
    classroom_id = serializers.PrimaryKeyRelatedField(queryset=Classroom.objects.all(), source='classroom', write_only=True)
    lesson_id = serializers.PrimaryKeyRelatedField(queryset=Lesson.objects.all(), source='lesson', write_only=True)

    class Meta:
        model = Homework
        fields = [
            'id', 'title', 'description', 'deadline', 'attachment',
            'created_at', 'updated_at',
            'classroom', 'lesson',
            'classroom_id', 'lesson_id',  # for write operations
            'teacher'
        ]
        read_only_fields = ['created_at', 'updated_at', 'teacher']
        extra_kwargs = {
            'title': {'required': True},
            'description': {'required': True},
            'deadline': {'required': True},
        }
    def validate(self, data):
        teacher = self.context['request'].user
        classroom = data.get('classroom')
        lesson = data.get('lesson')

        if classroom and classroom.teacher != teacher:
            raise serializers.ValidationError("You can only assign homework to your own classrooms.")

        if lesson and lesson.classroom != classroom:
            raise serializers.ValidationError("Selected lesson does not belong to the selected classroom.")

        return data

    def get_teacher(self, obj):
        return {
            "username": obj.teacher.username,
            "first_name": obj.teacher.first_name,
            "last_name": obj.teacher.last_name,
            "id": obj.teacher.id
        }


    def to_internal_value(self, data):
        deadline = data.get("deadline")
        if isinstance(deadline, str) and len(deadline) == 5 and deadline.count("-") == 1:
            try:
                current_year = datetime.now().year
                deadline = f"{current_year}-{deadline}"
                data['deadline'] = deadline
            except Exception:
                pass  
        return super().to_internal_value(data)

    def validate_attachment(self, file):
        if file:
            if not file.name.lower().endswith(('.pdf', '.zip')):
                raise serializers.ValidationError("Only PDF or ZIP files are allowed.")
        return file



class HomeworkSubmissionSerializer(serializers.ModelSerializer):
    homework_id = serializers.PrimaryKeyRelatedField(
        queryset=Homework.objects.all(), source='homework', write_only=True
    )

    class Meta:
        model = HomeworkSubmission
        fields = [
            'id', 'homework_id', 'answer_text', 'answer_file',
            'submitted_at', 'updated_at'
        ]
        read_only_fields = ['submitted_at', 'updated_at']

    def validate(self, data):
        user = self.context['request'].user
        homework = data['homework']

        if homework.classroom not in user.enrolled_classes.all():
            raise serializers.ValidationError("You are not enrolled in this class.")

        answer_text = data.get("answer_text")
        answer_file = data.get("answer_file")

        if not answer_text and not answer_file:
            raise serializers.ValidationError({
                "non_field_errors": ["You must provide either answer text or answer file."]
            })

        return data

    def validate_answer_file(self, file):
        if file and not file.name.lower().endswith(('.pdf', '.zip')):
            raise serializers.ValidationError("Only PDF or ZIP files are allowed.")
        return file

    def update(self, instance, validated_data):
        # Check deadline
        if instance.homework.deadline and datetime.now() > instance.homework.deadline:
            raise serializers.ValidationError("The deadline has passed. You cannot update your submission.")

        return super().update(instance, validated_data)
