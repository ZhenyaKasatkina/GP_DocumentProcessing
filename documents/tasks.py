from celery import shared_task

from documents.services import (create_letter_new_document,
                                create_letter_document_status_changed)


@shared_task
def send_email_about_new_document(pk):
    """Направляет письмо о загрузке нового документа"""

    create_letter_new_document(pk)


@shared_task
def send_email_about_changes_in_document_status(pk):
    """Направляет письмо об изменении статуса документа"""

    create_letter_document_status_changed(pk)
