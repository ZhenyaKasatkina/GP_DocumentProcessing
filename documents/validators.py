import os

from rest_framework import serializers


def validate_size(file):
    """Валидация размера загружаемого документа
    (не может быть более 50 Гб)"""
    size_50_gb = 1024 ** 3 * 50
    size_file = file.size
    if size_file > size_50_gb:
        raise serializers.ValidationError(
            f"Размер Вашего файла: {size_file}, что больше 50 Гб"
        )
