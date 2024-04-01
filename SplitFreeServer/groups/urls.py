from django.urls import path

from .views.group import GroupView
from .views.add_member import AddMemberView
from .views.stats import GroupStatsView

urlpatterns = [
    path('', GroupView.as_view()),
    path('/members', AddMemberView.as_view()),
    path('/stats', GroupStatsView.as_view()),
]
