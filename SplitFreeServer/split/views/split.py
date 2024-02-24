from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView

from libs.overrides import Response
from split.models import SplitSerializer, Split
from split.views.common import get_split


class SplitAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @get_split
    def get(self, request: Request, split: Split):
        return Response(SplitSerializer(instance=split).data)

    def post(self, request: Request):
        serializer = SplitSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        serializer.save()
        return Response(serializer.data)

    @get_split
    def put(self, request: Request, split: Split):
        serializer = SplitSerializer(
            instance=split,
            data=request.data,
            partial=True
        )
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        serializer.save()
        return Response(serializer.data)

    @get_split
    def delete(self, request: Request, split: Split):
        split.delete()
        return Response()
