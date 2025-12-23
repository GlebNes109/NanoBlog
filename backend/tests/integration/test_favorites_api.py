"""Integration tests for favorites API."""
import pytest

from httpx import AsyncClient

pytestmark = pytest.mark.integration



@pytest.mark.asyncio
async def test_add_to_favorites(client: AsyncClient, test_user, auth_headers):
    """Test adding a post to favorites."""
    # Create a post first
    post_response = await client.post(
        "/posts",
        headers=auth_headers,
        json={
            "title": "Test Post",
            "content": "Content"
        }
    )
    post_id = post_response.json()["id"]
    
    # Add to favorites
    response = await client.post(
        f"/favorites/{post_id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_favorites(client: AsyncClient, test_user, auth_headers):
    """Test getting user favorites."""
    # Create a post first
    post_response = await client.post(
        "/posts",
        headers=auth_headers,
        json={
            "title": "Favorite Post",
            "content": "Content"
        }
    )
    post_id = post_response.json()["id"]
    
    # Add to favorites
    await client.post(
        f"/favorites/{post_id}",
        headers=auth_headers
    )
    
    # Get favorites
    response = await client.get(
        "/favorites",
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_remove_from_favorites(client: AsyncClient, test_user, auth_headers):
    """Test removing a post from favorites."""
    # Create a post first
    post_response = await client.post(
        "/posts",
        headers=auth_headers,
        json={
            "title": "Test Post",
            "content": "Content"
        }
    )
    post_id = post_response.json()["id"]
    
    # Add to favorites
    await client.post(
        f"/favorites/{post_id}",
        headers=auth_headers
    )
    
    # Remove from favorites
    response = await client.delete(
        f"/favorites/{post_id}",
        headers=auth_headers
    )
    
    assert response.status_code == 200

