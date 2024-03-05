from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import PositiveInt

from app.api.deps import DBSessionDep, MeiliSessionDep
from app.crud.posts import posts
from app.database import INDEX_NAME
from app.schemas import PostCreate, PostRetrieve, PostUpdate

router = APIRouter()


@router.post("/", response_model=PostRetrieve, status_code=status.HTTP_201_CREATED)
async def create_post(db: DBSessionDep, data: PostCreate):
    """Create Post in database from provided data."""
    db_post = await posts.create(db, obj_in=data)

    return PostRetrieve(**jsonable_encoder(db_post))


@router.get("/{id}", response_model=PostRetrieve, status_code=status.HTTP_200_OK)
async def get_post(db: DBSessionDep, id: PositiveInt):
    """Retrieve existing Post object in database with given ID."""
    existing_post = await posts.get(db, id)
    if not existing_post or existing_post.is_deleted:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found."
        )

    return PostRetrieve(**jsonable_encoder(existing_post))


@router.put("/{id}", response_model=PostRetrieve, status_code=status.HTTP_200_OK)
async def update_post(db: DBSessionDep, id: PositiveInt, update_data: PostUpdate):
    """Update existing Post object in database with provided data."""
    existing_post = await posts.get(db, id)
    if not existing_post or existing_post.is_deleted:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found."
        )

    db_post = await posts.update(db, id=id, obj_in=update_data)

    return PostRetrieve(**jsonable_encoder(db_post))


@router.delete(
    "/{id}", response_model=PostRetrieve, status_code=status.HTTP_202_ACCEPTED
)
async def ghost_delete_post(db: DBSessionDep, id: PositiveInt):
    """Ghost delete existing Post object in database with given ID."""
    existing_post = await posts.get(db, id)
    if not existing_post or existing_post.is_deleted:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found."
        )

    db_post = await posts.update(db, id=id, obj_in={"is_deleted": True})

    return PostRetrieve(**jsonable_encoder(db_post))


@router.delete(
    "/true_delete/{id}",
    response_model=PostRetrieve,
    status_code=status.HTTP_202_ACCEPTED,
)
async def delete_post(db: DBSessionDep, client: MeiliSessionDep, id: PositiveInt):
    """Delete existing Post object in database with given ID.

    Also remove it from the search index if it exists.
    """
    existing_post = await posts.get(db, id)
    if not existing_post:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found."
        )

    try:
        await client.index(INDEX_NAME).delete_document(str(id))
    except Exception:
        print(f"post with id {id} not found in search index.")  # noqa T201

    db_post = await posts.remove(db, id=id)
    return PostRetrieve(**jsonable_encoder(db_post))
