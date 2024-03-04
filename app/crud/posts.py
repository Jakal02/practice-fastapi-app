from datetime import datetime

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

    async def all_posts_modified_since(self, db: AsyncSession, time: datetime):
        """Return all posts not ghost deleted modified after `time`."""
        stmt = select(Post).where(Post.is_deleted is False, Post.date_modified >= time)
        results = await db.execute(stmt)
        return results.all()


posts = CRUDPost(Post)
