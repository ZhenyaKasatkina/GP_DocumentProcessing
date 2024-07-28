from rest_framework.generics import CreateAPIView, ListAPIView

from documents.models import Document
from documents.serializers import DocumentSerializer
from documents.tasks import send_email_about_new_document


class DocumentListAPIView(ListAPIView):
    serializer_class = DocumentSerializer
    queryset = Document.objects.all()

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if self.request.user.is_superuser:
            return queryset
        if not self.request.user.is_anonymous:
            queryset = queryset.filter(owner=self.request.user)
            return queryset
        else:
            return []


class DocumentCreateAPIView(CreateAPIView):
    serializer_class = DocumentSerializer

    def perform_create(self, serializer):
        new_document = serializer.save()
        new_document.owner = self.request.user
        new_document.save()
        # Отправка сообщения админу для принятия решения по документу
        send_email_about_new_document.delay(new_document.pk)
