from rest_framework import serializers

from documents.models import Document
from users.serializers import UserSerializer


class DocumentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    def validate(self, attrs):

        my_file_format = str(attrs["file"])
        file_name = str(attrs["name"])

        file_format = [
            "txt",
            "doc",
            "docx",
            "bmp",
            "jpg",
            "jpeg",
            "png",
            "tif",
            "tiff",
            "zip",
            "7z",
            "rar",
            "odt",
            "pdf",
            "ods",
        ]
        if my_file_format.rsplit(".")[-1] not in file_format:
            raise serializers.ValidationError(
                'Вы можете добавить файлы в формате: ".txt", ".doc", '
                '".docx", ".bmp", ".jpg", ".jpeg", ".png", ".tif", '
                '".tiff", ".zip", ".7z", ".rar", ".odt", ".pdf", ".ods".'
            )

        symbols = (";", "%", ":", "?", "*", "&", "^", "$", "#", "№")
        for symbol in symbols:
            if symbol in my_file_format:
                raise serializers.ValidationError(
                    "В наименовании файла не могут содержаться символы: "
                    "';', '%', ':', '?', '*', '&', '^', '$', '#', '№'."
                )

            if symbol in file_name:
                raise serializers.ValidationError(
                    "В названии файла не могут содержаться символы: "
                    "';', '%', ':', '?', '*', '&', '^', '$', '#', '№'."
                )

        return attrs

    class Meta:
        model = Document
        fields = "__all__"
