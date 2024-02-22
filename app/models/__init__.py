from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models.posts import Post  # noqa
