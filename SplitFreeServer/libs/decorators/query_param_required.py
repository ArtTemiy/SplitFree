from rest_framework.request import Request
from rest_framework.response import Response


def query_param_required(key: str, required=True, func_kwarg_name=None):
    if func_kwarg_name is None:
        func_kwarg_name = key

    def decorator(function):
        def wrapper(self, request: Request, *args, **kwargs):
            val = request.query_params.get(key)
            if required and val is None:
                return Response(status=400, data={'message': f'Require query param: "{key}"'})
            return function(
                self,
                request,
                *args,
                **kwargs,
                **{func_kwarg_name: request.query_params[key]}
            )

        return wrapper

    return decorator
