from unittest.mock import AsyncMock

import pytest
from fastapi import HTTPException

from src.application.users_service import UsersService
from src.domain.models.users import UserCreateApi, UserProfileUpdate, UserPublic


@pytest.mark.asyncio
async def test_create_user_success(
    mock_user_repository, mock_password_hasher, sample_user_public, sample_user_id
):
    service = UsersService(mock_user_repository, mock_password_hasher)

    mock_user_repository.get_by_email = AsyncMock(return_value=None)
    mock_user_repository.get_by_login = AsyncMock(return_value=None)
    mock_user_repository.create = AsyncMock(return_value=sample_user_public)
    mock_password_hasher.hash = AsyncMock(return_value="hashed_password")

    user_data = UserCreateApi(email="test@example.com", login="testuser", password="password123")

    result = await service.create_user(user_data)

    assert result.email == "test@example.com"
    assert result.login == "testuser"
    mock_user_repository.get_by_email.assert_called_once_with("test@example.com")
    mock_user_repository.get_by_login.assert_called_once_with("testuser")
    mock_user_repository.create.assert_called_once()
    mock_password_hasher.hash.assert_called_once_with("password123")


@pytest.mark.asyncio
async def test_create_user_duplicate_email(
    mock_user_repository, mock_password_hasher, sample_user_read
):
    service = UsersService(mock_user_repository, mock_password_hasher)

    mock_user_repository.get_by_email = AsyncMock(return_value=sample_user_read)

    user_data = UserCreateApi(email="test@example.com", login="testuser", password="password123")

    with pytest.raises(HTTPException) as exc_info:
        await service.create_user(user_data)

    assert exc_info.value.status_code == 400
    assert "Email уже зарегистрирован" in exc_info.value.detail


@pytest.mark.asyncio
async def test_create_user_duplicate_login(
    mock_user_repository, mock_password_hasher, sample_user_read
):
    service = UsersService(mock_user_repository, mock_password_hasher)

    mock_user_repository.get_by_email = AsyncMock(return_value=None)
    mock_user_repository.get_by_login = AsyncMock(return_value=sample_user_read)

    user_data = UserCreateApi(email="test@example.com", login="testuser", password="password123")

    with pytest.raises(HTTPException) as exc_info:
        await service.create_user(user_data)

    assert exc_info.value.status_code == 400
    assert "Логин уже занят" in exc_info.value.detail


@pytest.mark.asyncio
async def test_get_user_success(
    mock_user_repository, mock_password_hasher, sample_user_public, sample_user_id
):
    service = UsersService(mock_user_repository, mock_password_hasher)

    mock_user_repository.get_public_profile = AsyncMock(return_value=sample_user_public)

    result = await service.get_user(sample_user_id)

    assert result.id == sample_user_id
    mock_user_repository.get_public_profile.assert_called_once_with(sample_user_id)


@pytest.mark.asyncio
async def test_get_user_not_found(mock_user_repository, mock_password_hasher, sample_user_id):
    service = UsersService(mock_user_repository, mock_password_hasher)

    mock_user_repository.get_public_profile = AsyncMock(return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        await service.get_user(sample_user_id)

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_update_profile_success(
    mock_user_repository, mock_password_hasher, sample_user_public, sample_user_id
):
    service = UsersService(mock_user_repository, mock_password_hasher)

    updated_public_dict = sample_user_public.model_dump()
    updated_public_dict["bio"] = "Updated bio"
    updated_public = UserPublic(**updated_public_dict)

    mock_user_repository.get_by_email = AsyncMock(return_value=None)
    mock_user_repository.get_by_login = AsyncMock(return_value=None)
    mock_user_repository.update_profile = AsyncMock(return_value=updated_public)

    profile_update = UserProfileUpdate(bio="Updated bio")

    result = await service.update_profile(sample_user_id, profile_update)

    assert result.bio == "Updated bio"
    mock_user_repository.update_profile.assert_called_once_with(sample_user_id, profile_update)


@pytest.mark.asyncio
async def test_update_profile_duplicate_email(
    mock_user_repository, mock_password_hasher, sample_user_read, sample_user_id
):
    service = UsersService(mock_user_repository, mock_password_hasher)

    other_user_dict = sample_user_read.model_dump()
    other_user_dict["id"] = str(sample_user_read.id) + "different"
    other_user = type(sample_user_read)(**other_user_dict)

    mock_user_repository.get_by_email = AsyncMock(return_value=other_user)

    profile_update = UserProfileUpdate(email="existing@example.com")

    with pytest.raises(HTTPException) as exc_info:
        await service.update_profile(sample_user_id, profile_update)

    assert exc_info.value.status_code == 400
    assert "Email уже используется" in exc_info.value.detail


@pytest.mark.asyncio
async def test_delete_user_success(mock_user_repository, mock_password_hasher, sample_user_id):
    service = UsersService(mock_user_repository, mock_password_hasher)

    mock_user_repository.delete = AsyncMock(return_value=True)

    await service.delete_user(sample_user_id, sample_user_id)

    mock_user_repository.delete.assert_called_once_with(sample_user_id)


@pytest.mark.asyncio
async def test_delete_user_different_user(
    mock_user_repository, mock_password_hasher, sample_user_id
):
    service = UsersService(mock_user_repository, mock_password_hasher)

    other_user_id = sample_user_id + "different"

    with pytest.raises(HTTPException) as exc_info:
        await service.delete_user(sample_user_id, other_user_id)

    assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_delete_user_not_found(mock_user_repository, mock_password_hasher, sample_user_id):
    service = UsersService(mock_user_repository, mock_password_hasher)

    mock_user_repository.delete = AsyncMock(return_value=False)

    with pytest.raises(HTTPException) as exc_info:
        await service.delete_user(sample_user_id, sample_user_id)

    assert exc_info.value.status_code == 404


@pytest.mark.asyncio
async def test_search_users(mock_user_repository, mock_password_hasher, sample_user_public):
    service = UsersService(mock_user_repository, mock_password_hasher)

    mock_user_repository.search = AsyncMock(return_value=[sample_user_public])

    results = await service.search_users("test")

    assert len(results) == 1
    assert results[0].login == "testuser"
    mock_user_repository.search.assert_called_once_with("test")
