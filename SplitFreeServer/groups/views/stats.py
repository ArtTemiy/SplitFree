import dataclasses

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.views import APIView

import libs.calculations.optimization as optimization
from libs.overrides import Response
from split.models import Split
from .common import get_group
from ..models import Group


class GroupStatsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @get_group(require_admin=False)
    def get(self, request: Request, group: Group):
        return Response({
            'payouts': [
                dataclasses.asdict(p) for p in
                optimization.optimize(list(Split.objects.filter(group=group)))
            ]
        })
