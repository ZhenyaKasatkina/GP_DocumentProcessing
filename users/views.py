from rest_framework.generics import (DestroyAPIView, UpdateAPIView,
                                     CreateAPIView, RetrieveAPIView)

from users.models import User
from users.serializers import UserSerializer, UserFullSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserFullSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()
