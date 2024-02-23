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


posts = CRUDPost(Post)
