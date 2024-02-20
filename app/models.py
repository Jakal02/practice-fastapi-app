import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String

from app.database import Base


class Post(Base):
    """Posts table definition."""

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    date_created = Column(DateTime, default=datetime.datetime.utcnow())
    date_modified = Column(DateTime, default=datetime.datetime.utcnow())
    is_deleted = Column(Boolean, default=False)

    # Required on Creation
    title = Column(String)
    body = Column(String)
