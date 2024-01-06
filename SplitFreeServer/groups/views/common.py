from rest_framework.request import Request

from groups.models import Group
from libs.decorators import query_param_required
from libs.overrides import Response


def get_group(required=True, has_access=True, require_admin=True):
    def caller(method):
        def wrapper(self, request: Request, *args, name=None, **kwargs):
            group = Group.objects.filter(name=name).first()
            if group is None:
                if required:
                    return Response(message=f'{name} does not exist', status=404)
            else:  # group exists
                if not required:
                    return Response(message=f'{name} already exist', status=400)
                # group required and valid
                if require_admin and not group.user_is_admin(request.user):
                    Response(message=f'You are not allowed for group {name}', status=403)
                if has_access and not group.user_is_member(request.user):
                    return Response(message=f'You are not allowed for group {name}', status=403)
            return method(self, request, *args, **kwargs, group=group)

        if required:
            return query_param_required('name')(wrapper)
        return wrapper
    return caller
