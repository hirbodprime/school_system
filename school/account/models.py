from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("teacher", "Teacher"),
        ("student", "Student"),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    national_id = models.CharField(max_length=10, unique=True, null=True, blank=True)
    bio = models.TextField(blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)



    def __str__(self):
        return f"{self.username} ({self.role})"



