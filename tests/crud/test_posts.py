from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from tests.conftest import _get_test_post_data, num_rows_in_tbl

from app.crud.posts import posts
from app.models import Post
from app.schemas import PostRetrieve


def test_create_post(db: Session):
    post_data = _get_test_post_data()

    assert num_rows_in_tbl(db, Post) == 0

    db_post = posts.create(db, obj_in=post_data)

    assert db_post.title == post_data.title
    assert db_post.body == post_data.body

    assert num_rows_in_tbl(db, Post) == 1


def test_read_post(db: Session):
    post_data = _get_test_post_data()

    posts.create(db, obj_in=post_data)

    db_read = posts.get(db, 1)
    assert db_read.title == post_data.title
    assert db_read.body == post_data.body
    assert db_read.id == 1


def test_update_post(db: Session):
    post_data = _get_test_post_data()

    db_created = posts.create(db, obj_in=post_data)

    update_data = PostRetrieve(**jsonable_encoder(db_created))
    update_data.title = "bob"

    db_read = posts.update(db, db_obj=db_created, obj_in=update_data)

    assert db_read.title != post_data.title
    assert db_read.title == update_data.title
    assert db_read.body == post_data.body
    assert db_read.id == 1


def test_delete_post(db: Session):
    post_data = _get_test_post_data()

    assert num_rows_in_tbl(db, Post) == 0

    db_post = posts.create(db, obj_in=post_data)

    assert num_rows_in_tbl(db, Post) == 1

    posts.remove(db, id=db_post.id)

    assert num_rows_in_tbl(db, Post) == 0
