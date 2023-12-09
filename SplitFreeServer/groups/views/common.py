from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from rest_framework.exceptions import PermissionDenied
from rest_framework.request import Request

from decorators.query_param_required import query_param_required
from groups.models import Group
from overrides.response import Response

NAME_KEY = 'name'


def get_group(required=True, has_access=True, require_admin=True):
    def caller(method):
        def wrapper(self, request: Request, *args, **kwargs):
            name = request.query_params.get(NAME_KEY)
            group = None
            if name is None:
                if required:
                    return Response(message='Require group name', status=400)
            else:
                group = Group.objects.filter(name=name).first()
                if group is None:
                    if required:
                        return Response(message=f'Group {name} does not exist', status=404)
                else: # group exists
                    if not required:
                        return Response(message=f'Group {name} already exist', status=400)
                    # group required and valid
                    if require_admin and group.admin != request.user:
                        Response(message=f'You are not allowed for group {name}', status=403)
                    if has_access and (not group.members.contains(request.user) and group.admin != request.user):
                        return Response(message=f'You are not allowed for group {name}', status=403)
            return method(self, request, *args, **kwargs, group=group, group_name=name)

        return wrapper
    return caller
