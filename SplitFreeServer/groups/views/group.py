import datetime

from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from groups.views.common import get_group
from overrides.response import Response

from groups.models.group import Group, GroupSerializer


class GroupView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @get_group()
    def get(self, request: Request, group: Group, group_name: str):
        return Response(GroupSerializer(group).data)

    @get_group(required=False)
    def post(self, request: Request, group: None, group_name: str):
        serializer = GroupSerializer(data={
            'name': group_name,
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
    def delete(self, request: Request, group: Group, group_name: str):
        group.delete()
        return Response()

    @get_group(require_admin=True)
    def put(self, request: Request, group: Group, group_name: str):
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
