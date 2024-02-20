from app.crud.base import CRUDBase
from app.models import Post
from app.schemas import PostCreate, PostRetrieve


class CRUDPost(CRUDBase[Post, PostCreate, PostRetrieve]):
    """Subclass of CRUDBase for Posts model."""

    pass


posts = CRUDPost()

posts.remove()
posts.update()
