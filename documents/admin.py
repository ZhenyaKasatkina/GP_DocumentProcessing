from django.contrib import admin

from documents.models import Document
from documents.tasks import send_email_about_changes_in_document_status


@admin.action(description="Изменить статус документа на Принято")
def is_accepted(modeladmin, request, queryset):
    queryset.update(status="Принят")
    for document in queryset:
        send_email_about_changes_in_document_status.delay(document.pk)


@admin.action(description="Изменить статус документа на Отклонен")
def is_rejected(modeladmin, request, queryset):
    queryset.update(status="Отклонен")
    for document in queryset:
        send_email_about_changes_in_document_status.delay(document.pk)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "owner",
        "file",
        "description",
        "created_at",
        "status",
    )
    list_filter = (
        "status",
        "created_at",
        "owner",
    )
    search_fields = (
        "name",
        "description",
    )
    actions = [is_accepted, is_rejected]
    readonly_fields = (
        "name",
        "owner",
        "file",
        "description",
        "created_at",
        "status",
    )
