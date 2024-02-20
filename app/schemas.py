from datetime import datetime

from pydantic import BaseModel, PositiveInt

# DateTime = Annotated[
#     datetime, PlainSerializer(lambda x: x.isoformat(), return_type=str)
# ]


class PostCreate(BaseModel):
    """Pydantic model supporting post creation."""

    title: str
    body: str


class PostRetrieve(PostCreate):
    """Pydantic model supporting post information retrieval."""

    id: PositiveInt
    date_created: datetime
    date_modified: datetime
    is_deleted: bool
