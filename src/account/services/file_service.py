import aiofiles
import os
import uuid
import base64
from fastapi import HTTPException, status


class FileService:
    def __init__(self, upload_dir: str = "uploads"):
        self.upload_dir = upload_dir
        os.makedirs(upload_dir, exist_ok=True)

    async def save_base64_file(self, file_data: str, folder: str) -> str:
        """Сохраняет base64 файл и возвращает путь."""
        try:
            if not file_data.startswith("data:"):
                return file_data

            header, data = file_data.split(",", 1)
            mime_type = header.split(";")[0].split(":")[1]

            extension = self._get_extension_from_mime(mime_type)
            filename = f"{uuid.uuid4()}{extension}"
            filepath = os.path.join(self.upload_dir, folder, filename)

            os.makedirs(os.path.dirname(filepath), exist_ok=True)

            file_bytes = base64.b64decode(data)

            async with aiofiles.open(filepath, "wb") as f:
                await f.write(file_bytes)

            return filepath

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid file data: {str(e)}",
            )

    def _get_extension_from_mime(self, mime_type: str) -> str:
        """Определяет расширение файла по MIME типу."""
        extensions = {
            "image/jpeg": ".jpg",
            "image/png": ".png",
            "image/gif": ".gif",
            "image/webp": ".webp",
            "application/pdf": ".pdf",
            "application/msword": ".doc",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": ".docx",
        }
        return extensions.get(mime_type, ".bin")

    async def delete_file(self, filepath: str) -> None:
        """Удаляет файл."""
        try:
            if os.path.exists(filepath):
                os.remove(filepath)
        except Exception:
            pass
