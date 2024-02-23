from typing import Annotated

from fastapi import Depends
from meilisearch_python_sdk import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session, get_meilisearch_client

DBSessionDep = Annotated[AsyncSession, Depends(get_db_session)]

MeiliSessionDep = Annotated[AsyncClient, Depends(get_meilisearch_client)]
