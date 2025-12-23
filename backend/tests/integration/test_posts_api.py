import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.integration


@pytest.mark.asyncio
async def test_create_post(client: AsyncClient, test_user, auth_headers):
    response = await client.post(
        "/posts",
        headers=auth_headers,
        json={"title": "Test Post", "content": "This is a test post content"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Post"
    assert data["content"] == "This is a test post content"
    assert data["authorId"] == str(test_user.id)
    assert "id" in data


@pytest.mark.asyncio
async def test_create_post_unauthorized(client: AsyncClient):
    response = await client.post("/posts", json={"title": "Test Post", "content": "Content"})

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_all_posts(client: AsyncClient, test_user, auth_headers):
    # Create a post first
    await client.post(
        "/posts", headers=auth_headers, json={"title": "Test Post", "content": "Content"}
    )

    response = await client.get("/posts")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_get_post_by_id(client: AsyncClient, test_user, auth_headers):
    # Create a post first
    create_response = await client.post(
        "/posts", headers=auth_headers, json={"title": "Test Post", "content": "Content"}
    )
    post_id = create_response.json()["id"]

    # Get the post
    response = await client.get(f"/posts/{post_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == post_id
    assert data["title"] == "Test Post"


@pytest.mark.asyncio
async def test_update_post(client: AsyncClient, test_user, auth_headers):
    # Create a post first
    create_response = await client.post(
        "/posts",
        headers=auth_headers,
        json={"title": "Original Title", "content": "Original content"},
    )
    post_id = create_response.json()["id"]

    # Update the post
    response = await client.put(
        f"/posts/{post_id}",
        headers=auth_headers,
        json={"title": "Updated Title", "content": "Updated content"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["content"] == "Updated content"


@pytest.mark.asyncio
async def test_delete_post(client: AsyncClient, test_user, auth_headers):
    # Create a post first
    create_response = await client.post(
        "/posts", headers=auth_headers, json={"title": "To Delete", "content": "Content"}
    )
    post_id = create_response.json()["id"]

    # Delete the post
    response = await client.delete(f"/posts/{post_id}", headers=auth_headers)

    assert response.status_code == 200

    # Verify post is deleted
    get_response = await client.get(f"/posts/{post_id}")
    assert get_response.status_code == 404
