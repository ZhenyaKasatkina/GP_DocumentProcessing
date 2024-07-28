from celery import shared_task

from config.settings import EMAIL_HOST_USER, SERVER_HOST
from documents.models import Document
from documents.services import send_email_message


@shared_task
def send_email_about_new_document(pk):
    """Направляет письмо о загрузке нового документа"""

    new_document = Document.objects.filter(pk=pk).first()
    message = (
        f"Пользователь {new_document.owner} загрузил новый документ: "
        f"\n{new_document}."
        f"\nПрошу проверить и изменить статус документа по ссылке: "
        f"http://{SERVER_HOST}/admin/documents"
        f"/document/?o=7&status__exact=%D0%97%D0%B0%D0%B3%D1%80%D1%83%D0%B6%D0%B5%D0%BD"
    )
    print(message)
    subject = f"Загружен новый документ: {new_document.name}"
    send_email_message(subject, message, EMAIL_HOST_USER)


@shared_task
def send_email_about_changes_in_document_status(pk):
    """Направляет письмо об изменении статуса документа"""

    new_document = Document.objects.filter(pk=pk).first()
    message = f"Документ {new_document.name}: {new_document.status}"
    subject = f"Изменился статус документа {new_document.name}"
    send_email_message(subject, message, new_document.owner.email)
