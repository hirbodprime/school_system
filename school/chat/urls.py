# chat/urls.py

from django.urls import path,include

urlpatterns = [
        path('api/', include('chat.api.urls')),

]
