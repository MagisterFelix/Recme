from collections import OrderedDict

from django.contrib.auth.models import AbstractBaseUser
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from core.server.models import User
from core.server.serializers.user import UserSerializer


class AuthorizationSerializer(TokenObtainPairSerializer):

    def validate(self, attrs: dict) -> dict:
        email = attrs["email"]
        password = attrs.get("password", "")

        self.user = User.objects.get_or_none(email=email)

        if self.user is None or not self.user.check_password(password):
            raise AuthenticationFailed("No user was found with these credentials.")

        return super().validate(attrs)

    def to_representation(self, tokens: dict) -> OrderedDict:
        data = OrderedDict(tokens)

        if self.user is None:
            return data

        data["user"] = UserSerializer(self.user, context=self.context).data

        return data


class RegistrationSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ("name", "email", "password",)
        extra_kwargs = {
            "password": {
                "write_only": True
            },
        }

    def validate(self, attrs: dict) -> dict:
        if attrs["name"] == "admin":
            raise ValidationError({"name": "Forbidden name."})

        return super().validate(attrs)

    def create(self, validated_data: dict) -> AbstractBaseUser:
        user = User.objects.create_user(**validated_data)

        return user

    def to_representation(self, user: User) -> OrderedDict:
        data = OrderedDict(super().to_representation(user))
        return data
