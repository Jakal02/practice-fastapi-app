"""Sync changes to the database to the search index.

Async process which regularly runs.
"""

import asyncio

from pydantic import PositiveInt


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
        self.updated_at = None
        self.delay = delay_in_seconds

    async def begin_indexing(self):
        """Run the syncing process."""
        while self.running:
            await asyncio.sleep(self.delay)
            print("Sync Process Running.")  # noqa T201
