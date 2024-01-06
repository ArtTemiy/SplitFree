from django.urls import path

from .views.split import SplitAPI

urlpatterns = [
    path('', SplitAPI.as_view()),
]
