from django.contrib import admin
from .models import News,NewsView
admin.site.register(NewsView)
@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher', 'created_at', 'updated_at']
    search_fields = ['title', 'description']
    list_filter = ['created_at']
