from django.contrib import admin
from .models import Classroom, Lesson

@admin.register(Classroom)
class ClassroomAdmin(admin.ModelAdmin):
    list_display = ['name', 'teacher']
    search_fields = ['name']
    list_filter = ['teacher']

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['name', 'classroom']
    search_fields = ['name']
    list_filter = ['classroom']
