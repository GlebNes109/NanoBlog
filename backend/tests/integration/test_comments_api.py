import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.integration


@pytest.mark.asyncio
async def test_create_comment(client: AsyncClient, test_user, auth_headers):
    # Create a post first
    post_response = await client.post(
        "/posts", headers=auth_headers, json={"title": "Test Post", "content": "Content"}
    )
    post_id = post_response.json()["id"]

    # Create a comment
    response = await client.post(
        f"/posts/{post_id}/comments",
        headers=auth_headers,
        json={"content": "This is a test comment"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "This is a test comment"
    assert data["postId"] == post_id
    assert data["authorId"] == str(test_user.id)


@pytest.mark.asyncio
async def test_get_comments(client: AsyncClient, test_user, auth_headers):
    # Create a post first
    post_response = await client.post(
        "/posts", headers=auth_headers, json={"title": "Test Post", "content": "Content"}
    )
    post_id = post_response.json()["id"]

    # Create a comment
    await client.post(
        f"/posts/{post_id}/comments", headers=auth_headers, json={"content": "Comment 1"}
    )

    # Get comments
    response = await client.get(f"/posts/{post_id}/comments")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_delete_comment(client: AsyncClient, test_user, auth_headers):
    # Create a post first
    post_response = await client.post(
        "/posts", headers=auth_headers, json={"title": "Test Post", "content": "Content"}
    )
    post_id = post_response.json()["id"]

    # Create a comment
    comment_response = await client.post(
        f"/posts/{post_id}/comments", headers=auth_headers, json={"content": "To Delete"}
    )
    comment_id = comment_response.json()["id"]

    # Delete the comment
    response = await client.delete(f"/posts/{post_id}/comments/{comment_id}", headers=auth_headers)

    assert response.status_code == 200
