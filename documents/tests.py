import os

from django.core import mail
from django.test import TestCase
from django.urls import reverse
from django.utils import translation
from rest_framework import status
from rest_framework.test import APITestCase

from config import settings
from documents.models import Document
from documents.services import send_email_message
from users.models import User

ROOT_DIR = os.path.dirname(__file__)


class EducationTestCase(APITestCase):

    def setUp(self) -> None:

        super().setUp()
        self.user = User.objects.create(email="new_email@list.ru", password="qwe123")
        self.client.force_authenticate(user=self.user)

        with open(os.path.join(ROOT_DIR, "test_file", "test_file.txt"), "rb") as f:
            data = {"name": "test_file", "file": f, "owner": self.user.pk}
            self.response = self.client.post(reverse("documents:document_create"), data)

    def test_documents_list_is_true(self):
        """Проверка списка документов"""

        url = reverse("documents:document_list")
        response = self.client.get(url)
        data = response.json()
        result = [self.response.json()]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data, result)

    def test_document_create_is_true(self):
        """Проверка загрузки документа"""

        url = reverse("documents:document_create")
        with open(os.path.join(ROOT_DIR, "test_file", "test_file.txt"), "rb") as f:
            data = {"name": "test", "file": f, "owner": self.user.pk}
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(Document.objects.all().count(), 2)

    def test_document_create_is_false(self):
        """Проверка загрузки документа (с ошибкой)"""

        # без названия файла
        url = reverse("documents:document_create")
        file = os.path.join(ROOT_DIR, "test_file", "test_file.txt")
        with open(file, "rb") as f:
            data = {"file": f, "owner": self.user.pk}
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(Document.objects.all().count(), 1)

        # без файла
        url = reverse("documents:document_create")
        file = os.path.join(ROOT_DIR, "test_file", "test_file.txt")
        data = {"name": "test", "file": file, "owner": self.user.pk}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Document.objects.all().count(), 1)

        # некорректно указан владелец файла
        url = reverse("documents:document_create")
        with open(os.path.join(ROOT_DIR, "test_file", "test_file.txt"), "rb") as f:
            data = {"name": "test", "file": f, "owner": "self.user"}
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(Document.objects.all().count(), 1)

        # некорректно указан владелец файла
        url = reverse("documents:document_create")
        with open(os.path.join(ROOT_DIR, "test_file", "test_file.txt"), "rb") as f:
            data = {"name": "test", "file": f, "owner": not self.user.pk}
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(Document.objects.all().count(), 1)

        # название документа с ошибкой
        url = reverse("documents:document_create")
        file = os.path.join(ROOT_DIR, "test_file", "test_file.txt")
        with open(file, "rb") as fb:
            data = {"name": "#$%fbhdb", "file": fb, "owner": self.user.pk}
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(Document.objects.all().count(), 1)

        # не корректный наименование файла
        url = reverse("documents:document_create")
        file = os.path.join(ROOT_DIR, "test_file", "test_*&^file.txt")
        with open(file, "rb") as f:
            data = {"name": "doc", "file": f, "owner": self.user.pk}
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(Document.objects.all().count(), 1)

        # не корректный формат файла
        url = reverse("documents:document_create")
        file = os.path.join(ROOT_DIR, "test_file", "test_file2")
        with open(file, "rb") as f:
            data = {"name": "doc", "file": f, "owner": self.user.pk}
            response = self.client.post(url, data)
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(Document.objects.all().count(), 1)

    def tearDown(self):
        translation.activate(settings.LANGUAGE_CODE)
        super().tearDown()


class EmailTest(TestCase):

    def test_send_email(self):
        """Отправка сообщения"""

        # Empty the test outbox
        mail.outbox = []
        # Send message.
        send_email_message(
            "Subject here",
            "Here is the message.",
            "from@example.com",
        )
        # Test that one message has been sent.
        self.assertEqual(len(mail.outbox), 1)
        # Verify that the subject of the first message is correct.
        self.assertEqual(mail.outbox[0].subject, "Subject here")

    def tearDown(self):
        translation.activate(settings.LANGUAGE_CODE)
        super().tearDown()
