from django.urls import path
from .views import NewsListCreateView,NewsUpdateView

urlpatterns = [
    path('', NewsListCreateView.as_view(), name='teacher-news'),
    path('update/<int:pk>/', NewsUpdateView.as_view(), name='update-news'),

]
