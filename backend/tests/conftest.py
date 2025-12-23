"""Pytest configuration and fixtures."""
import os
import pytest
from unittest.mock import AsyncMock
from datetime import datetime
from uuid import uuid4

# Устанавливаем переменные окружения ДО импорта любых модулей src
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///:memory:")
os.environ.setdefault("SERVER_ADDRESS", "0.0.0.0:8000")
os.environ.setdefault("SECRET_KEY", "test-secret-key-for-testing-only")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("ACCESS_TOKEN_EXPIRE_MINUTES", "30")

# Теперь можно импортировать модели
from src.domain.models.users import UserRead, UserPublic, UserCreate
from src.domain.models.posts import PostRead, CommentRead


@pytest.fixture
def mock_user_repository():
    """Mock UserRepository."""
    return AsyncMock()


@pytest.fixture
def mock_post_repository():
    """Mock PostRepository."""
    return AsyncMock()


@pytest.fixture
def mock_comment_repository():
    """Mock CommentRepository."""
    return AsyncMock()


@pytest.fixture
def mock_favorite_repository():
    """Mock FavoriteRepository."""
    return AsyncMock()


@pytest.fixture
def mock_rating_repository():
    """Mock RatingRepository."""
    return AsyncMock()


@pytest.fixture
def mock_password_hasher():
    """Mock PasswordHasher."""
    hasher = AsyncMock()
    hasher.hash = AsyncMock(return_value="hashed_password")
    hasher.verify = AsyncMock(return_value=True)
    return hasher


@pytest.fixture
def sample_user_id():
    """Sample user ID."""
    return str(uuid4())


@pytest.fixture
def sample_post_id():
    """Sample post ID."""
    return str(uuid4())


@pytest.fixture
def sample_user_read(sample_user_id):
    """Sample UserRead object."""
    return UserRead(
        id=sample_user_id,
        email="test@example.com",
        login="testuser",
        password="hashed_password",
        createdAt=datetime.utcnow(),
        updatedAt=datetime.utcnow(),
    )


@pytest.fixture
def sample_user_public(sample_user_id):
    """Sample UserPublic object."""
    return UserPublic(
        id=sample_user_id,
        email="test@example.com",
        login="testuser",
        avatar_url=None,
        bio=None,
        createdAt=datetime.utcnow(),
        updatedAt=datetime.utcnow(),
    )


@pytest.fixture
def sample_post_read(sample_user_id, sample_post_id):
    """Sample PostRead object."""
    return PostRead(
        id=sample_post_id,
        authorId=sample_user_id,
        authorLogin="testuser",
        authorAvatar=None,
        title="Test Post",
        content="Test content",
        image_url=None,
        rating=0,
        user_rating=None,
        is_favorited=False,
        comments_count=0,
        createdAt=datetime.utcnow(),
        updatedAt=datetime.utcnow(),
    )


@pytest.fixture
def sample_comment_read(sample_user_id, sample_post_id):
    """Sample CommentRead object."""
    comment_id = str(uuid4())
    return CommentRead(
        id=comment_id,
        postId=sample_post_id,
        authorId=sample_user_id,
        authorLogin="testuser",
        authorAvatar=None,
        content="Test comment",
        createdAt=datetime.utcnow(),
        updatedAt=datetime.utcnow(),
    )
