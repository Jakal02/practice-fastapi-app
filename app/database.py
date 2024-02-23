"""Database configuration file.

Copied from: https://medium.com/@tclaitken/setting-up-a-fastapi-app-with-async-sqlalchemy-2-0-pydantic-v2-e6c540be4308
"""
import contextlib
from collections.abc import AsyncGenerator, AsyncIterator
from typing import Any

from meilisearch_python_sdk import AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.config import settings

# Heavily inspired by https://praciano.com.br/fastapi-and-async-sqlalchemy-20-with-pytest-done-right.html


class DatabaseSessionManager:
    """Database session manager."""

    def __init__(self, host: str, engine_kwargs: dict[str, Any] = {}):
        """Initialize async database connection."""
        self._engine = create_async_engine(host, **engine_kwargs)
        self._sessionmaker = async_sessionmaker(autocommit=False, bind=self._engine)

    async def close(self):
        """Close database connection."""
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        """Connect to the database and yield async connection."""
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        """Yield an async session."""
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(settings.get_db_uri_string(), {"echo": True})


async def get_db_session():
    """Get a database session."""
    async with sessionmanager.session() as session:
        yield session


# Meilisearch connection
# copied from: https://github.com/sanders41/meilisearch-fastapi/tree/main


async def get_meilisearch_client() -> AsyncGenerator[AsyncClient, None]:
    """Get a meilisearch client."""
    async with AsyncClient(
        url=settings.get_meili_url_string(), api_key=settings.MEILISEARCH_MASTER_KEY
    ) as client:
        yield client
