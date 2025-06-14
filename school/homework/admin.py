from django.contrib import admin
from .models import Homework

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher', 'classroom', 'deadline', 'created_at', 'updated_at']
    search_fields = ['title', 'description']
    list_filter = ['created_at', 'deadline']
