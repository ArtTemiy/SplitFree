from rest_framework.request import Request

from libs.decorators import query_param_required
from libs.overrides import Response
from split.models import Split


def get_split(method):
    @query_param_required('id', func_kwarg_name='_id')
    def wrapper(self, request: Request, *args, _id=None, **kwargs):
        split = Split.objects.filter(pk=_id).first()
        if split is None:
            return Response(message=f'Split with id {split} does not exist', status=404)
        if not split.group.user_is_member(request.user):
            return Response(status=403)
        return method(self, request, *args, split=split, **kwargs)
    return wrapper
