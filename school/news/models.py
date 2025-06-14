from django.db import models
from django.conf import settings

class News(models.Model):
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='news')
    classroom = models.ForeignKey("classroom.Classroom", on_delete=models.CASCADE, related_name='news',null=True,blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class NewsView(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="views")
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'news') 

    def __str__(self):
        return f"{self.student.username} viewed {self.news.title}"
