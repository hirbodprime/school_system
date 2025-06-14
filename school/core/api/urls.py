from django.urls import path
from .views import ClosestSchoolsView

urlpatterns = [
    path('school/closest/', ClosestSchoolsView.as_view(), name="closest-schools"),



]
