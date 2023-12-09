from django.contrib.auth import login
from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


# Create your views here.
class RegisterView(APIView):
    def post(self, request: Request):
        username = request.data.get('username')
        password = request.data.get('password')
        if username is None or password is None:
            return Response(status=400, data={'message': 'Username or password is invalid'})
        if User.objects.filter(username=username).count() > 0:
            return Response(status=400, data={'message': 'Already exists'})
        user = User(username=username)
        user.set_password(password)
        user.save()
        return Response()
