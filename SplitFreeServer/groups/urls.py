from django.urls import path

from .views.group import GroupView
from .views.additional import AddMemberView

urlpatterns = [
    path('', GroupView.as_view()),
    path('/members', AddMemberView.as_view()),
]
