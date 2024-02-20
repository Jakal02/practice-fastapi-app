from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic import PositiveInt

from app.api.deps import SessionDep
from app.crud.posts import posts
from app.schemas import PostCreate, PostRetrieve

router = APIRouter()


@router.post("/", response_model=PostRetrieve, status_code=status.HTTP_201_CREATED)
async def create_post(db: SessionDep, data: PostCreate):
    """Create Post in database from provided data."""
    db_post = posts.create(db, obj_in=data)

    return jsonable_encoder(db_post)


@router.get("/{id}", response_model=PostRetrieve, status_code=status.HTTP_200_OK)
async def get_post(db: SessionDep, id: PositiveInt):
    """Retrieve existing Post object in database with given ID."""
    existing_post = posts.get(db, id)
    if not existing_post:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found."
        )

    return jsonable_encoder(existing_post)


@router.put("/{id}", response_model=PostRetrieve, status_code=status.HTTP_200_OK)
async def update_post(db: SessionDep, id: PositiveInt, update_data: PostRetrieve):
    """Update existing Post object in database with provided data."""
    existing_post = posts.get(db, id)
    if not existing_post:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found."
        )

    db_post = posts.update(db, db_obj=existing_post, obj_in=update_data)

    return jsonable_encoder(db_post)


@router.delete(
    "/{id}", response_model=PostRetrieve, status_code=status.HTTP_202_ACCEPTED
)
async def delete_post(db: SessionDep, id: PositiveInt):
    """Delete existing Post object in database with given ID."""
    existing_post = posts.get(db, id)
    if not existing_post:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, detail=f"post with id {id} not found."
        )

    db_post = posts.remove(db, id=id)

    return jsonable_encoder(db_post)
