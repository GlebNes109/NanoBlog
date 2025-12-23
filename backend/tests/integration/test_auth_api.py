"""Integration tests for authentication API."""
import pytest

from httpx import AsyncClient

pytestmark = pytest.mark.integration





@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    """Test user registration."""
    response = await client.post(
        "/users",
        json={
            "email": "newuser@example.com",
            "login": "newuser",
            "password": "password123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["login"] == "newuser"
    assert "password" not in data
    assert "id" in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    """Test registration with duplicate email."""
    # First registration
    await client.post(
        "/users",
        json={
            "email": "duplicate@example.com",
            "login": "user1",
            "password": "password123"
        }
    )
    
    # Second registration with same email
    response = await client.post(
        "/users",
        json={
            "email": "duplicate@example.com",
            "login": "user2",
            "password": "password123"
        }
    )
    
    assert response.status_code == 400
    assert "Email уже зарегистрирован" in response.json()["detail"]


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, test_user):
    """Test successful login."""
    response = await client.post(
        "/auth/token",
        data={
            "username": "testuser",
            "password": "testpassword"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_invalid_credentials(client: AsyncClient):
    """Test login with invalid credentials."""
    response = await client.post(
        "/auth/token",
        data={
            "username": "nonexistent",
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == 400
    assert "Incorrect username or password" in response.json()["detail"]


@pytest.mark.asyncio
async def test_get_me(client: AsyncClient, test_user, auth_headers):
    """Test getting current user profile."""
    response = await client.get("/users/me", headers=auth_headers)
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(test_user.id)
    assert data["email"] == test_user.email
    assert data["login"] == test_user.login


@pytest.mark.asyncio
async def test_get_me_unauthorized(client: AsyncClient):
    """Test getting profile without authentication."""
    response = await client.get("/users/me")
    
    assert response.status_code == 401

