import datetime

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.types import TIMESTAMP

from app.models import Base


class Post(Base):
    """Posts table definition."""

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    date_created = Column(
        type_=TIMESTAMP(timezone=True), default=datetime.datetime.utcnow()
    )
    date_modified = Column(
        type_=TIMESTAMP(timezone=True), default=datetime.datetime.utcnow()
    )
    is_deleted = Column(Boolean, default=False)

    # Required on Creation
    title = Column(String)
    body = Column(String)
