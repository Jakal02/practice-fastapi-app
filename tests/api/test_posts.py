import datetime
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status
from fastapi.encoders import jsonable_encoder
from httpx import AsyncClient
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


@pytest.mark.anyio
async def test_create_post(client: AsyncClient, session: AsyncSession):
    post_data = _get_test_post_data()
    rows = await num_rows_in_tbl(session, Post)
    response = await client.post("/posts/", json=post_data.model_dump())

    assert response.status_code == status.HTTP_201_CREATED
    assert await num_rows_in_tbl(session, Post) == 1 + rows


@pytest.mark.anyio
async def test_true_delete_post(client: AsyncClient, session: AsyncSession):
    post_data = _get_test_post_data()
    made_post = await posts.create(session, obj_in=post_data)
    rows = await num_rows_in_tbl(session, Post)

    id = made_post.id
    response = await client.delete(f"/posts/true_delete/{id}")

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert await num_rows_in_tbl(session, Post) == rows - 1
    assert response.json() == jsonable_encoder(made_post)


@pytest.mark.anyio
async def test_update_post(client: AsyncClient, session: AsyncSession):
    post_data = _get_test_post_data()
    date_begun = datetime.datetime.utcnow()
    made_post = await posts.create(session, obj_in=post_data)
    rows = await num_rows_in_tbl(session, Post)

    id = made_post.id
    update_data = jsonable_encoder(made_post)
    update_data["body"] = "new body."
    update_data.pop("date_modified")

    response = await client.put(f"/posts/{id}", json=update_data)
    date_done = datetime.datetime.utcnow()
    result: dict = dict(response.json())
    date_modified = datetime.datetime.fromisoformat(result.pop("date_modified"))

    assert response.status_code == status.HTTP_200_OK
    assert await num_rows_in_tbl(session, Post) == rows
    assert result == update_data
    assert date_modified > date_begun and date_modified < date_done


@pytest.mark.anyio
async def test_read_post(client: AsyncClient, session: AsyncSession):
    post_data = _get_test_post_data()
    made_post = await posts.create(session, obj_in=post_data)
    rows = await num_rows_in_tbl(session, Post)

    id = made_post.id
    response = await client.get(f"/posts/{id}")

    assert response.status_code == status.HTTP_200_OK

    assert response.json() == jsonable_encoder(made_post)
    assert await num_rows_in_tbl(session, Post) == rows


@pytest.mark.anyio
async def test_ghost_delete_post(client: AsyncClient, session: AsyncSession):
    post_data = _get_test_post_data()
    date_started = datetime.datetime.utcnow()
    made_post = await posts.create(session, obj_in=post_data)
    rows = await num_rows_in_tbl(session, Post)

    id = made_post.id
    response = await client.delete(f"/posts/{id}")
    date_stopped = datetime.datetime.utcnow()
    result: dict = dict(response.json())
    date_modified = datetime.datetime.fromisoformat(result.pop("date_modified"))

    deleted_data = jsonable_encoder(made_post)
    deleted_data.pop("date_modified")
    deleted_data["is_deleted"] = True

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert await num_rows_in_tbl(session, Post) == rows
    assert result == deleted_data
    assert date_modified > date_started and date_modified < date_stopped


## Edge Case Tests


@pytest.mark.anyio
async def test_no_read_when_ghost_deleted(client: AsyncClient, session: AsyncSession):
    post_data = _get_test_post_data()
    made_post = await posts.create(session, obj_in=post_data)
    await posts.update(session, id=made_post.id, obj_in={"is_deleted": True})

    id = made_post.id
    response = await client.get(f"/posts/{id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_no_update_when_ghost_deleted(client: AsyncClient, session: AsyncSession):
    post_data = _get_test_post_data()
    made_post = await posts.create(session, obj_in=post_data)
    await posts.update(session, id=made_post.id, obj_in={"is_deleted": True})

    id = made_post.id
    update_data = PostUpdate(**jsonable_encoder(made_post))
    update_data.body = "new body."

    response = await client.put(f"/posts/{id}", json=jsonable_encoder(update_data))

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_no_ghost_delete_when_ghost_deleted(
    client: AsyncClient, session: AsyncSession
):
    post_data = _get_test_post_data()
    made_post = await posts.create(session, obj_in=post_data)
    await posts.update(session, id=made_post.id, obj_in={"is_deleted": True})

    id = made_post.id
    response = await client.delete(f"/posts/{id}")

    assert response.status_code == status.HTTP_404_NOT_FOUND
