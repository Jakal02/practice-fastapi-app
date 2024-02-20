from fastapi import status
from fastapi.testclient import TestClient
from pydantic import PositiveInt


def _get_test_posts(num: PositiveInt = 1) -> dict | list[dict]:
    """Return information needed to create `num` posts."""
    posts = [{"title": f"test title {i}", "body": f"test body {i}"} for i in range(num)]

    return posts[0] if num == 1 else posts


def test_create_post(client: TestClient):
    response = client.post("/posts/", json={})

    assert response.status_code == status.HTTP_201_CREATED


def test_delete_post(client: TestClient):
    id = 0
    response = client.delete(f"/posts/{id}")

    assert response.status_code == status.HTTP_202_ACCEPTED


def test_update_post(client: TestClient):
    id = 0
    response = client.put(f"/posts/{id}", json={})

    assert response.status_code == status.HTTP_200_OK


def test_read_post(client: TestClient):
    id = 0
    response = client.get(f"/posts/{id}")

    assert response.status_code == status.HTTP_200_OK
