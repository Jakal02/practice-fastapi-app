import pytest
from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from tests.conftest import _get_test_post_data, num_rows_in_tbl

from app.crud.posts import posts
from app.models import Post
from app.schemas import PostUpdate


@pytest.mark.anyio
async def test_create_post(session: AsyncSession):
    post_data = _get_test_post_data()

    rows = await num_rows_in_tbl(session, Post)

    db_post = await posts.create(session, obj_in=post_data)

    assert db_post.title == post_data.title
    assert db_post.body == post_data.body

    assert await num_rows_in_tbl(session, Post) == 1 + rows


@pytest.mark.anyio
async def test_read_post(session: AsyncSession):
    post_data = _get_test_post_data()

    db_post = await posts.create(session, obj_in=post_data)

    db_read = await posts.get(session, db_post.id)
    assert db_read == db_post


@pytest.mark.anyio
async def test_update_post(session: AsyncSession):
    post_data = _get_test_post_data()

    db_created = await posts.create(session, obj_in=post_data)

    update_data = PostUpdate(**jsonable_encoder(db_created))
    update_data.title = "bob"

    db_read = await posts.update(session, id=db_created.id, obj_in=update_data)

    assert db_read.title != post_data.title
    assert db_read.title == update_data.title
    assert db_read.body == post_data.body
    assert db_read.id == db_created.id


@pytest.mark.anyio
async def test_delete_post(session: AsyncSession):
    post_data = _get_test_post_data()

    rows = await num_rows_in_tbl(session, Post)

    db_post = await posts.create(session, obj_in=post_data)

    assert await num_rows_in_tbl(session, Post) == 1 + rows

    await posts.remove(session, id=db_post.id)

    assert await num_rows_in_tbl(session, Post) == rows
