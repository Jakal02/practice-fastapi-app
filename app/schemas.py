from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, PlainSerializer, PositiveInt

DateTime = Annotated[
    datetime, PlainSerializer(lambda x: x.isoformat(), return_type=str)
]


class PostCreate(BaseModel):
    """Pydantic model supporting post creation."""

    title: str
    body: str


class PostRetrieve(PostCreate):
    """Pydantic model supporting post information retrieval."""

    id: PositiveInt
    date_created: DateTime
    date_modified: DateTime
    is_deleted: bool
