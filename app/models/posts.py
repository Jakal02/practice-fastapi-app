import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.models import Base


class Post(Base):
    """Posts table definition."""

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    date_created = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
    date_modified = Column(DateTime, default=datetime.datetime.utcnow(), nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)

    # Required on Creation
    title = Column(String, nullable=False)
    body = Column(String, nullable=False)
