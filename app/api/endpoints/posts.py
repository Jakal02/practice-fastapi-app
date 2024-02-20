from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def home_posts():
    """Hello world for post."""
    return {"table": "posts"}
