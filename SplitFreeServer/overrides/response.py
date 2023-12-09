from rest_framework.response import Response as DRFResponse


class Response(DRFResponse):
    def __init__(self, data=None, message=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        if data is None:
            if message is not None:
                data = {
                    'message': message
                }
        super().__init__(
            data=data,
            status=status,
            template_name=template_name,
            headers=headers,
            exception=exception,
            content_type=content_type
        )
