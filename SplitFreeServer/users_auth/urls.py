from django.urls import path

from rest_framework.authtoken import views
from .views import RegisterView

urlpatterns = [
    path('api-token', views.obtain_auth_token),
    path('register', RegisterView.as_view()),
]
