"""Integration tests for users API."""
import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.integration




@pytest.mark.asyncio
async def test_get_user_by_id(client: AsyncClient, test_user):
    """Test getting user by ID."""
    response = await client.get(f"/users/{test_user.id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(test_user.id)
    assert data["email"] == test_user.email
    assert "password" not in data


@pytest.mark.asyncio
async def test_get_user_not_found(client: AsyncClient):
    """Test getting non-existent user."""
    from uuid import uuid4
    fake_id = str(uuid4())
    
    response = await client.get(f"/users/{fake_id}")
    
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_profile(client: AsyncClient, test_user, auth_headers):
    """Test updating user profile."""
    response = await client.put(
        "/users/me",
        headers=auth_headers,
        json={
            "bio": "Updated bio",
            "login": "updated_login"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["bio"] == "Updated bio"
    assert data["login"] == "updated_login"


@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient, test_user, auth_headers):
    """Test deleting user."""
    response = await client.delete(
        f"/users/{test_user.id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    
    # Verify user is deleted
    get_response = await client.get(f"/users/{test_user.id}")
    assert get_response.status_code == 404


@pytest.mark.asyncio
async def test_delete_other_user(client: AsyncClient, test_user, auth_headers):
    """Test deleting another user (should fail)."""
    from uuid import uuid4
    other_user_id = str(uuid4())
    
    response = await client.delete(
        f"/users/{other_user_id}",
        headers=auth_headers
    )
    
    assert response.status_code == 403
