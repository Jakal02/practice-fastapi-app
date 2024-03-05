from fastapi import APIRouter
from meilisearch_python_sdk.models.health import Health

from app.api.deps import MeiliSessionDep
from app.database import INDEX_NAME

router = APIRouter()


@router.get("/health", response_model=Health)
async def get_meili_health(client: MeiliSessionDep):
    """Display health information of meilisearch."""
    return await client.health()


@router.get("/search")
async def search_for_posts(client: MeiliSessionDep):
    """Search for posts that have been made."""
    return await client.index(uid=INDEX_NAME).search()
