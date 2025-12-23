"""Integration tests for ratings API."""
import pytest

from httpx import AsyncClient

pytestmark = pytest.mark.integration



@pytest.mark.asyncio
async def test_rate_post_positive(client: AsyncClient, test_user, auth_headers):
    """Test rating a post positively."""
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
    
    # Rate the post
    response = await client.post(
        f"/posts/{post_id}/rate",
        headers=auth_headers,
        json={
            "value": 1
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "rated"
    assert data["value"] == 1


@pytest.mark.asyncio
async def test_rate_post_negative(client: AsyncClient, test_user, auth_headers):
    """Test rating a post negatively."""
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
    
    # Rate the post
    response = await client.post(
        f"/posts/{post_id}/rate",
        headers=auth_headers,
        json={
            "value": -1
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "rated"
    assert data["value"] == -1


@pytest.mark.asyncio
async def test_remove_rating(client: AsyncClient, test_user, auth_headers):
    """Test removing a rating."""
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
    
    # Rate the post first
    await client.post(
        f"/posts/{post_id}/rate",
        headers=auth_headers,
        json={
            "value": 1
        }
    )
    
    # Remove rating
    response = await client.post(
        f"/posts/{post_id}/rate",
        headers=auth_headers,
        json={
            "value": 0
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "removed"
    assert data["value"] == 0

