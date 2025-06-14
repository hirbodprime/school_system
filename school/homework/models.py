from django.db import models
from django.conf import settings

def homework_upload_path(instance, filename):
    return f"homeworks/{instance.teacher.id}/{filename}"


class Homework(models.Model):
    classroom = models.ForeignKey("classroom.Classroom", on_delete=models.CASCADE, related_name="homeworks", blank=True, null=True)
    lesson = models.ForeignKey("classroom.Lesson", on_delete=models.CASCADE, related_name="homeworks", null=True, blank=True)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='homeworks')
    title = models.CharField(max_length=255,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateTimeField()
    attachment = models.FileField(upload_to=homework_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # ✅ add this

    def __str__(self):
        return f"Homework by {self.teacher.username} - {self.created_at.date()}"


class HomeworkSubmission(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="submissions")
    homework = models.ForeignKey(Homework, on_delete=models.CASCADE, related_name="submissions")
    answer_text = models.TextField(blank=True)
    answer_file = models.FileField(upload_to="homework_answers/", blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'homework']  # only one submission per student per homework

    def __str__(self):
        return f"{self.student.username} -> {self.homework.title}"
