import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile

from src.domain.repositories.user_repository import UserRepository

UPLOAD_DIR = Path("/app/static/uploads")
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


class UploadsService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def upload_avatar(self, user_id: str, file: UploadFile) -> str:
        url = await self._upload_file(file, f"avatar_{user_id}")
        await self.user_repository.update_avatar(user_id, url)
        return url

    async def upload_image(self, file: UploadFile) -> str:
        return await self._upload_file(file, "post")

    async def _upload_file(self, file: UploadFile, prefix: str) -> str:
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

        ext = Path(file.filename).suffix.lower() if file.filename else ""
        if ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail="Invalid file type")

        content = await file.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large (max 5MB)")

        filename = f"{prefix}_{uuid.uuid4().hex[:8]}{ext}"
        filepath = UPLOAD_DIR / filename

        with open(filepath, "wb") as f:
            f.write(content)

        return f"/static/uploads/{filename}"
