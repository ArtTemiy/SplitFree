from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
# from django.shortcuts import get_object_or_404
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView

from groups.models import Group
from groups.views.common import get_group
from overrides.response import Response


class AddMemberView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @get_group()
    def post(self, request: Request, group: Group, group_name: str):
        group.members.add(
            *User.objects.filter(username__in=request.data['members'])
        )
        group.save()
        return Response()

    @get_group(require_admin=True)
    def delete(self, request: Request, group: Group, group_name: str):
        group.members.remove(
            *User.objects.filter(username__in=request.data['members'])
        )
        group.save()
        return Response()
