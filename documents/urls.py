from django.urls import path
from rest_framework.permissions import IsAdminUser

from documents.apps import DocumentsConfig
from documents.permissions import IsOwner
from documents.views import DocumentCreateAPIView, DocumentListAPIView

app_name = DocumentsConfig.name


urlpatterns = [
    path(
        "documents/",
        DocumentListAPIView.as_view(permission_classes=(IsAdminUser | IsOwner,)),
        name="document_list",
    ),
    path(
        "documents/create/",
        DocumentCreateAPIView.as_view(),
        name="document_create"
    ),
]
