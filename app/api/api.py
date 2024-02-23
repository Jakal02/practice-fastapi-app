from fastapi import APIRouter

from app.api.endpoints import meilisearch, posts

api_router = APIRouter()

api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(
    meilisearch.router, prefix="/meilisearch", tags=["meilisearch"]
)
