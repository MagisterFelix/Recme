from collections import OrderedDict

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from core.server.models import User


class UserSerializer(ModelSerializer):

    new_password = serializers.CharField(max_length=128, required=False, write_only=True)

    class Meta:
        model = User
        exclude = ("last_login",)
        extra_kwargs = {
            "username": {
                "required": False
            },
            "email": {
                "required": False
            },
            "password": {
                "required": False,
                "write_only": True
            },
        }

    def validate(self, attrs: dict) -> dict:
        if not isinstance(self.instance, User):
            return super().validate(attrs)

        user = self.instance

        password = attrs.get("password")
        new_password = attrs.get("new_password")

        if password is None and new_password is None:
            return super().validate(attrs)

        if password is None and new_password is not None:
            raise ValidationError({"password": "This field is required."})

        if password is not None and new_password is None:
            raise ValidationError({"new_password": "This field is required."})

        if password is not None and not user.check_password(password):
            raise ValidationError({"password": "Password mismatch."})

        return super().validate(attrs)

    def update(self, user: User, validated_data: dict) -> User:
        if validated_data.get("new_password") is None:
            return super().update(user, validated_data)

        user.set_password(validated_data["new_password"])
        user.save()

        return user

    def to_representation(self, user: User) -> OrderedDict:
        data = OrderedDict(super().to_representation(user))
        return data
