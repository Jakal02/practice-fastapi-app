from datetime import datetime

from pydantic import BaseModel, PositiveInt

# DateTime = Annotated[
#     datetime, PlainSerializer(lambda x: x.isoformat(), return_type=str)
# ]


class PostCreate(BaseModel):
    """Pydantic model supporting post creation."""

    title: str
    body: str


class PostUpdate(PostCreate):
    """Pydantic model support post information updates."""


class PostRetrieve(PostUpdate):
    """Pydantic model supporting post information retrieval."""

    id: PositiveInt
    date_created: datetime
    date_modified: datetime
    is_deleted: bool


class PostIndexForSearch(PostCreate):
    """Pydantic model specifying which fields should be indexed for search."""

    id: PositiveInt
    date_created: datetime
    date_modified: datetime


class SearchParams(BaseModel):
    """Pydantic model displaying which options go to the search algorithm."""

    query: str
