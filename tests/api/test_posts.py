from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from fastapi import status
from fastapi.testclient import TestClient
from pydantic import PositiveInt
from tests.conftest import _get_test_post_data, num_rows_in_tbl

from app.schemas import PostRetrieve, PostUpdate
from app.crud.posts import posts
from app.models import Post


def _get_test_posts(num: PositiveInt = 1) -> dict | list[dict]:
    """Return information needed to create `num` posts."""
    posts = [{"title": f"test title {i}", "body": f"test body {i}"} for i in range(num)]

    return posts[0] if num == 1 else posts


## Intended use case tests


def test_create_post(client: TestClient, db: Session):
    post_data = _get_test_post_data()
    response = client.post("/posts/", json=post_data.model_dump())

    assert response.status_code == status.HTTP_201_CREATED
    assert num_rows_in_tbl(db, Post) == 1
    assert False


def test_true_delete_post(client: TestClient, db: Session):
    post_data = _get_test_post_data()
    made_post = posts.create(db, obj_in=post_data)
    assert num_rows_in_tbl(db, Post) == 1

    id = made_post.id
    response = client.delete(f"/posts/true_delete/{id}")

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert num_rows_in_tbl(db, Post) == 0
    assert response.json() == jsonable_encoder(made_post)


def test_update_post(client: TestClient, db: Session):
    post_data = _get_test_post_data()
    made_post = posts.create(db, obj_in=post_data)
    assert num_rows_in_tbl(db, Post) == 1

    id = made_post.id
    update_data = PostUpdate(**jsonable_encoder(made_post))
    update_data.body = "new body."

    response = client.put(f"/posts/{id}", json=jsonable_encoder(update_data))

    assert response.status_code == status.HTTP_200_OK
    assert num_rows_in_tbl(db, Post) == 1
    assert response.json() == jsonable_encoder(update_data)


def test_read_post(client: TestClient, db: Session):
    post_data = _get_test_post_data()
    made_post = posts.create(db, obj_in=post_data)
    assert num_rows_in_tbl(db, Post) == 1

    id = made_post.id
    response = client.get(f"/posts/{id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == jsonable_encoder(made_post)


def test_ghost_delete_post(client: TestClient, db: Session):
    post_data = _get_test_post_data()
    made_post = posts.create(db, obj_in=post_data)
    assert num_rows_in_tbl(db, Post) == 1

    id = made_post.id
    response = client.delete(f"/posts/{id}")

    deleted_data = jsonable_encoder(made_post)
    deleted_data["is_deleted"] = True

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert num_rows_in_tbl(db, Post) == 1
    assert response.json() == deleted_data


## Edge Case Tests


def test_no_read_when_ghost_deleted(client: TestClient, db: Session):
    post_data = _get_test_post_data()
    made_post = posts.create(db, obj_in=post_data)
    posts.update(db, db_obj=made_post, obj_in={"is_deleted": True})

    id = made_post.id
    response = client.get(f"/posts/{id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_no_update_when_ghost_deleted(client: TestClient, db: Session):
    post_data = _get_test_post_data()
    made_post = posts.create(db, obj_in=post_data)
    posts.update(db, db_obj=made_post, obj_in={"is_deleted": True})

    id = made_post.id
    update_data = PostUpdate(**jsonable_encoder(made_post))
    update_data.body = "new body."

    response = client.put(f"/posts/{id}", json=jsonable_encoder(update_data))

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_no_ghost_delete_when_ghost_deleted(client: TestClient, db: Session):
    post_data = _get_test_post_data()
    made_post = posts.create(db, obj_in=post_data)
    posts.update(db, db_obj=made_post, obj_in={"is_deleted": True})

    id = made_post.id
    response = client.delete(f"/posts/{id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
