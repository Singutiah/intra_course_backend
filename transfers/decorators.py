from rest_framework.response import Response
from rest_framework.views import status


def validate_transfer_data(fn):
    def decorated(*args, **kwargs):
        # args[0] == GenericView Object
        # name = args[0].request.data.get("FIRSTNAME", "")
        # artist = args[0].request.data.get("artist", "")
        # if not name:
        #     return Response(
        #         data={
        #             "message": "Name required for transfer"
        #         },
        #         status=status.HTTP_400_BAD_REQUEST
        #     )
        return fn(*args, **kwargs)

    return decorated
