from rest_framework.response import Response
from rest_framework.views import status


def validate_request_data(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        name = args[0].request.data.get("name", "")
        # artist = args[0].request.data.get("artist", "")
        if not name:
            return Response(
                data={
                    "message": "Name required for tag"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)

    return decorated


def validate_intent_data(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        tag = args[0].request.data.get("Tag", "")
        pattern = args[0].request.data.get("Pattern", "")
        # artist = args[0].request.data.get("artist", "")
        if not tag:
            return Response(
                data={
                    "message": "Name required for tag"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)

    return decorated


def validate_weight_data(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        value = args[0].request.data.get("value", "")
        # artist = args[0].request.data.get("artist", "")
        if not value:
            return Response(
                data={
                    "message": "Value required for tag"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        return fn(*args, **kwargs)

    return decorated

