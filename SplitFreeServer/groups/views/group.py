import datetime

from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from .common import get_group
from libs.overrides import Response

from groups.models.group import Group, GroupSerializer


class GroupView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @get_group()
    def get(self, request: Request, group: Group):
        return Response(GroupSerializer(group).data)

    def post(self, request: Request):
        serializer = GroupSerializer(data={
            **request.data,
            'created': datetime.datetime.now(),
            'admin': request.user.username,
            'members': [],
        })
        if serializer.is_valid():
            g = serializer.save()
            return Response(GroupSerializer(instance=g).data)
        return Response(serializer.errors, status=400)

    @get_group(require_admin=True)
    def delete(self, request: Request, group: Group):
        group.delete()
        return Response()

    @get_group()
    def put(self, request: Request, group: Group):
        serializer = GroupSerializer(
            instance=group,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

        '''loveannamefidechkA
        hihihihih
        utemybolshayappisya
        voooooooottakayabolshayapisya
        inogdaonsampisay
        chinaaaaaazessssss
        and zakluchitelnaya sedimaya strochka 
        xoxo'''
