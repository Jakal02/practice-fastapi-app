"""Sync changes to the database to the search index.

Async process which regularly runs.
"""

import asyncio
import datetime

from fastapi.encoders import jsonable_encoder
from meilisearch_python_sdk import AsyncIndex
from pydantic import PositiveInt

from app.crud.posts import posts
from app.database import INDEX_NAME, get_db_session, get_meilisearch_client


class BackgroundSearchSyncer:
    """Sync search index with recent database changes.

    Behavior:
    Application Startup:
    - index the entire Posts table.

    Application Lifespan:
    - awaken every `SEARCH_SYNCER_DELAY_SECONDS` seconds
    - gather changes made to the database since last run
    - apply those changes to the index
    - a ghost delete or real delete to the database will remove
        that post from the search index.
    """

    def __init__(self, delay_in_seconds: PositiveInt = 3):
        """Initialize BackgroundSearchSyncer."""
        self.running = True
        self.updated_at = datetime.datetime.utcnow()
        self.delay = delay_in_seconds

    async def begin_indexing(self):
        """Run the syncing process."""
        while self.running:
            await asyncio.sleep(self.delay)

            # Gather Changes
            async for db in get_db_session():
                posts_modded = await posts.all_posts_modified_since(db, self.updated_at)
                data_of_posts_modded = [jsonable_encoder(p) for p in posts_modded]
                posts_deleted = await posts.all_posts_modified_since(
                    db, self.updated_at, ghost_deleted=True
                )
                ids_of_ghost_deleted = [p.id for p in posts_deleted]
                print("Posts Modified: ", [p.id for p in posts_modded])  # noqa T201
                print("Posts Deleted: ", [p.id for p in posts_deleted])  # noqa T201

            # Grab index and make changes to it
            async for client in get_meilisearch_client():
                index: AsyncIndex = client.index(uid=INDEX_NAME)
                await index.add_documents(data_of_posts_modded)
                await index.delete_documents(ids_of_ghost_deleted)
                # update self.updated_at
                index_info = await client.get_raw_index(INDEX_NAME)
                self.updated_at = index_info.updated_at
