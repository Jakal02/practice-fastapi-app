from app.crud.base import CRUDBase
from app.models import Post
from app.schemas import PostCreate, PostUpdate


class CRUDPost(CRUDBase[Post, PostCreate, PostUpdate]):
    """Subclass of CRUDBase for Posts model."""


posts = CRUDPost(Post)
