from datetime import datetime

from sqlalchemy import ColumnOperators as co
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Post
from app.schemas import PostCreate, PostUpdate


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    """Subclass of CRUDBase for Posts model."""

    def __init__(self, *args, **kwargs):
        """Initialize the class."""
        super().__init__(*args, **kwargs)
        off_limits_fields = []
        self.update_excluded_fields.update(off_limits_fields)

    async def all_posts_modified_since(
        self, db: AsyncSession, time: datetime
    ) -> list[Post]:
        """Return all posts not ghost deleted modified after `time`."""
        stmt = (
            select(Post)
            .where(co.__eq__(Post.is_deleted, False))
            .where(co.__gt__(Post.date_modified, time))
        )
        results = await db.execute(stmt)
        return [item.tuple()[0] for item in results.all()]

    async def all_posts(
        self, db: AsyncSession, exclude_ghost: bool = True
    ) -> list[Post]:
        """Return all posts.

        By defualt, exclude ghost deleted posts.
        """
        stmt = select(Post)
        if not exclude_ghost:
            stmt = stmt.where(co.__eq__(Post.is_deleted, False))
        results = await db.execute(stmt)
        return [item.tuple()[0] for item in results.all()]


posts = CRUDPost(Post)
