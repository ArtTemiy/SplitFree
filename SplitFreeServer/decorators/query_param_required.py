from django.http import HttpRequest
from rest_framework.response import Response


def query_param_required(key: str):
    def decorator(function):
        def wrapper(request: HttpRequest, *args, **kwargs):
            if key not in request.GET:
                return Response(status=400, data={'message': f'Require query param: "{key}"'})
            return function(request, *args, **kwargs)
        return wrapper
    return decorator
