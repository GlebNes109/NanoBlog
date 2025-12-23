from unittest.mock import AsyncMock, patch

import pytest
from fastapi import HTTPException

from src.application.auth_service import AuthService


@pytest.mark.asyncio
async def test_login_success(mock_user_repository, mock_password_hasher, sample_user_read):
    service = AuthService(mock_user_repository, mock_password_hasher)

    mock_user_repository.get_by_login = AsyncMock(return_value=sample_user_read)
    mock_password_hasher.verify = AsyncMock(return_value=True)

    with patch("src.application.auth_service.create_access_token") as mock_token:
        mock_token.return_value = "test_token"

        result = await service.login("testuser", "password123")

        assert result["access_token"] == "test_token"
        assert result["token_type"] == "bearer"
        mock_user_repository.get_by_login.assert_called_once_with("testuser")
        mock_password_hasher.verify.assert_called_once_with(
            "password123", sample_user_read.password
        )


@pytest.mark.asyncio
async def test_login_user_not_found(mock_user_repository, mock_password_hasher):
    service = AuthService(mock_user_repository, mock_password_hasher)

    mock_user_repository.get_by_login = AsyncMock(return_value=None)

    with pytest.raises(HTTPException) as exc_info:
        await service.login("nonexistent", "password123")

    assert exc_info.value.status_code == 400
    assert "Incorrect username or password" in exc_info.value.detail


@pytest.mark.asyncio
async def test_login_incorrect_password(
    mock_user_repository, mock_password_hasher, sample_user_read
):
    service = AuthService(mock_user_repository, mock_password_hasher)

    mock_user_repository.get_by_login = AsyncMock(return_value=sample_user_read)
    mock_password_hasher.verify = AsyncMock(return_value=False)

    with pytest.raises(HTTPException) as exc_info:
        await service.login("testuser", "wrong_password")

    assert exc_info.value.status_code == 400
    assert "Incorrect username or password" in exc_info.value.detail
    mock_password_hasher.verify.assert_called_once_with("wrong_password", sample_user_read.password)
