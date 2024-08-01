from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER, SERVER_HOST
from documents.models import Document


def send_email_message(subject, message, email):
    """Направляет письмо адресату"""

    send_mail(
        subject=subject,
        message=message,
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False,
    )


def create_letter_new_document(pk):
    """Создает письмо (новый документ)"""

    new_document = Document.objects.filter(pk=pk).first()
    message = (
        f"Пользователь {new_document.owner} загрузил новый документ: "
        f"\n{new_document}."
        f"\nПрошу проверить и изменить статус документа по ссылке: "
        f"http://{SERVER_HOST}/admin/documents"
        f"/document/?o=7&status__exact=%D0%97%D0%B0%D0%B3%D1%80%D1%83%D0%B6%D0%B5%D0%BD"
    )
    subject = f"Загружен новый документ: {new_document.name}"
    send_email_message(subject, message, EMAIL_HOST_USER)


def create_letter_document_status_changed(pk):
    """Создает письмо (статус документа изменен)"""

    new_document = Document.objects.filter(pk=pk).first()
    message = f"Документ {new_document.name}: {new_document.status}"
    subject = f"Изменился статус документа {new_document.name}"
    send_email_message(subject, message, new_document.owner.email)
