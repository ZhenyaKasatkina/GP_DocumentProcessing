from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Document(models.Model):
    """Документ"""

    owner = models.ForeignKey(
        User,
        related_name="document",
        verbose_name="владелец документа",
        on_delete=models.SET_NULL,
        **NULLABLE,
    )
    name = models.CharField(
        max_length=50,
        verbose_name="Название документа"
    )
    file = models.FileField(
        upload_to="documents/",
        max_length=300,
        verbose_name="файл"
    )
    description = models.TextField(
        verbose_name="описание",
        help_text="краткий комментарий к документу",
        **NULLABLE
    )
    created_at = models.DateField(
        auto_now_add=True,
        verbose_name="Дата создания (записи в БД)"
    )

    LOADED = "Загружен"
    ADOPTED = "Принят"
    REJECTED = "Отклонен"
    STATUS = {
        LOADED: "Загружен",
        ADOPTED: "Принят",
        REJECTED: "Отклонен",
    }
    status = models.CharField(
        choices=STATUS,
        max_length=10,
        verbose_name="Статус",
        default=LOADED,
    )

    def __str__(self):
        # Строковое отображение объекта
        return (
            f"{self.name} ({self.description}), статус: {self.status} "
            f"(дата загрузки {self.created_at}.)"
        )

    class Meta:
        # Настройка для наименования одного объекта
        verbose_name = "документ"
        # Настройка для наименования набора объектов
        verbose_name_plural = "документы"
        # Сортировка по id
        ordering = ["-pk"]
