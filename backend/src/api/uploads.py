from fastapi import APIRouter, Depends, UploadFile, File

from src.api.dependencies import get_current_user, get_uploads_service
from src.application.uploads_service import UploadsService
from src.domain.models.users import UserRead

router = APIRouter()


@router.post("/avatar", summary="Загрузить аватар")
async def upload_avatar(
    file: UploadFile = File(...),
    service: UploadsService = Depends(get_uploads_service),
    current_user: UserRead = Depends(get_current_user),
):
    url = await service.upload_avatar(current_user.id, file)
    return {"url": url}


@router.post("/image", summary="Загрузить изображение")
async def upload_image(
    file: UploadFile = File(...),
    service: UploadsService = Depends(get_uploads_service),
    current_user: UserRead = Depends(get_current_user),
):
    url = await service.upload_image(file)
    return {"url": url}
