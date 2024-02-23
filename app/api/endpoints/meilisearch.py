from fastapi import APIRouter
from meilisearch_python_sdk.models.health import Health

from app.api.deps import MeiliSessionDep

router = APIRouter()


@router.get("/health", response_model=Health)
async def get_meili_health(client: MeiliSessionDep):
    """Display health information of meilisearch."""
    return await client.health()
