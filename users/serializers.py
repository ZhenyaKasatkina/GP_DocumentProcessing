from rest_framework.serializers import ModelSerializer

from users.models import User


class UserFullSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "password",
            "email",
            "phone",
            "town",
            "avatar",
        ]


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        read_only_fields = ("email",)
        fields = [
            "id",
            "email",
            "phone",
            "town",
            "avatar",
        ]
