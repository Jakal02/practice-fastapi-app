import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.api import api_router
from app.database import sessionmanager
from app.search_sync.indexer import BackgroundSearchSyncer

indexer = BackgroundSearchSyncer()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events.

    To understand more, read https://fastapi.tiangolo.com/advanced/events/
    """
    syncer = asyncio.create_task(indexer.begin_indexing())
    yield
    print(syncer.cancel())  # noqa T201
    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()


PracticeAPI = FastAPI(lifespan=lifespan)


@PracticeAPI.get("/")
def home_route():
    """Return basic Hello World message."""
    return {"Hello": "World"}


PracticeAPI.include_router(api_router)
