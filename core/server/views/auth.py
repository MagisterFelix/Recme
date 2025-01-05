from django.middleware.csrf import rotate_token
from rest_framework import status
from rest_framework.fields import empty
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.views import APIView

from core.server.serializers import AuthorizationSerializer, RegistrationSerializer
from core.server.utils import AuthorizationUtils


class AuthorizationView(APIView):

    serializer_class = AuthorizationSerializer
    permission_classes = (AllowAny,)

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data, context={"request": self.request})
        serializer.is_valid(raise_exception=True)

        rotate_token(request._request)

        data = serializer.data

        if isinstance(data, ReturnDict):
            data.pop("refresh")

        response = Response(data=data, status=status.HTTP_200_OK)

        if serializer.validated_data is not None and not isinstance(serializer.validated_data, empty):
            AuthorizationUtils.set_access_cookie(response, token=serializer.validated_data["access"], httponly=False)
            AuthorizationUtils.set_refresh_cookie(response, token=serializer.validated_data["refresh"], httponly=True)

        return response


class RegistrationView(APIView):

    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return response
