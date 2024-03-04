"""Sync changes to the database to the search index.

Async process which regularly runs.
"""

import asyncio
import datetime

from pydantic import PositiveInt

from app.crud.posts import posts
from app.database import get_db_session


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
            async for db in get_db_session():
                posts_modded = await posts.all_posts_modified_since(db, self.updated_at)
                print("Posts Modified: ", [p.id for p in posts_modded])  # noqa T201
