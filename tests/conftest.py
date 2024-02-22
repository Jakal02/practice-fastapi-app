from typing import AsyncGenerator
import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import func, select, event
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session, SessionTransaction

from app.schemas import PostCreate
from app.main import PracticeAPI
from app.config import settings
from app.database import get_db_session
from app.models import Post


@pytest.fixture
def anyio_backend() -> str:
    return "asyncio"


# Provide Database connection
# copied from: https://github.com/rhoboro/async-fastapi-sqlalchemy/blob/main/app/tests/conftest.py
@pytest.fixture
async def session() -> AsyncGenerator:
    # https://github.com/sqlalchemy/sqlalchemy/issues/5811#issuecomment-756269881
    async_engine = create_async_engine(settings.get_db_uri_string())
    async with async_engine.connect() as conn:
        await conn.begin()
        await conn.begin_nested()
        AsyncSessionLocal = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=conn,
            future=True,
        )

        async_session = AsyncSessionLocal()

        @event.listens_for(async_session.sync_session, "after_transaction_end")
        def end_savepoint(session: Session, transaction: SessionTransaction) -> None:
            if conn.closed:
                return
            if not conn.in_nested_transaction():
                if conn.sync_connection:
                    conn.sync_connection.begin_nested()

        async def test_get_session() -> AsyncGenerator:
            try:
                yield AsyncSessionLocal()
            except SQLAlchemyError:
                pass

        PracticeAPI.dependency_overrides[get_db_session] = test_get_session

        yield async_session
        await async_session.close()
        await conn.rollback()

    await async_engine.dispose()


@pytest.fixture(scope="function")
async def client() -> AsyncGenerator:
    async with AsyncClient(
        transport=ASGITransport(app=PracticeAPI), base_url="https://test/"
    ) as c:
        yield c


# PracticeAPI.dependency_overrides[get_db_session] =


"""Helper functions for tests."""


def _get_test_post_data() -> PostCreate:
    """
    Return information for a test post.
    """
    return PostCreate(title="test title.", body="test_body.")


async def num_rows_in_tbl(db: AsyncSession, table):
    """
    Return number of rows in passed in table.
    """
    num_rows = -1
    num_rows = await db.execute(select(func.count()).select_from(Post))
    return num_rows.scalar()
