from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.settings import api_settings
from rest_framework_simplejwt.authentication import JWTAuthentication
import jwt
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from django.conf import settings

from .serializers import TokenSerializer, UserSerializer, LoginSerializer


# Get the JWT settings
# jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
# jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# encode_secret = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'


class LoginView(generics.CreateAPIView):
    """
    POST authentication/login/
    """

    # This permission class will override the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("username", "")
        password = request.data.get("password", "")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            print("logging in")
            login(request, user)
            print("logged in")
            access_token = AccessToken.for_user(user)
            access_token.set_exp(from_time=datetime.now() + timedelta(
                seconds=int(settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds())))
            refresh_token = RefreshToken.for_user(user)

            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                'access_token': str(access_token),
                'refresh_token': str(refresh_token)
            })
            serializer.is_valid()
            # role be Admin or User
            role = 'Admin' if user.is_staff else 'User'
            return Response({"role": role, **serializer.data})

        return Response(status=status.HTTP_401_UNAUTHORIZED)


class RegisterUsersView(generics.CreateAPIView):
    """
    POST authentication/register/
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        if not username and not password and not email:
            return Response(
                data={
                    "message": "username, password and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            username=username, password=password, email=email
        )
        return Response(
            data=UserSerializer(new_user).data,
            status=status.HTTP_201_CREATED
        )
