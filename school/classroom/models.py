from django.db import models
from django.conf import settings

class Classroom(models.Model):
    name = models.CharField(max_length=255)
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='classes')
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='enrolled_classes', limit_choices_to={'role': 'student'})
    school = models.ForeignKey("core.School", on_delete=models.CASCADE, related_name='classrooms', null=True, blank=True)

    def __str__(self):
        return f"{self.name} (by {self.teacher.username})"


class Lesson(models.Model):
    name = models.CharField(max_length=255)
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE, related_name='lessons')

    def __str__(self):
        return f"{self.name} - {self.classroom.name}"
