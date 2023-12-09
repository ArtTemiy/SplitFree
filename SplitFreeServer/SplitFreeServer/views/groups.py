from django.views import View
from django.contrib import auth

class GroupView(auth.mixins.LoginRequiredMixin, View):
    def get(self, request):
        user = auth.get_user(request)
