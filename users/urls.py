from django.urls import path
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.permissions import IsRealUser
from users.views import (UserCreateAPIView, UserUpdateAPIView,
                         UserDestroyAPIView, UserRetrieveAPIView)

app_name = UsersConfig.name


urlpatterns = [
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path(
        "create/",
        UserCreateAPIView.as_view(permission_classes=(AllowAny,)),
        name="user_create"
    ),
    path(
        "update/<int:pk>/",
        UserUpdateAPIView.as_view(permission_classes=(IsRealUser,)),
        name="user_update",
    ),
    path(
        "delete/<int:pk>/",
        UserDestroyAPIView.as_view(permission_classes=(IsAdminUser | IsRealUser,)),
        name="user_delete",
    ),
    path(
        "view/<int:pk>/",
        UserRetrieveAPIView.as_view(permission_classes=(IsRealUser,)),
        name="user_view",
    ),
]
