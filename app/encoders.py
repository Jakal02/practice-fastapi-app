"""Custom encoders.

Custom encoders for the api application.
"""
import datetime
from typing import Any

from fastapi.encoders import jsonable_encoder as old_encoder


def jsonable_encoder(obj: Any, *args, **kwargs) -> Any:
    """JSON encoder re-written for this app to minimize duplicated code.

    Why the need for this? Well, there is a bug it seems when it comes to Datetimes
    and asyncpg. I could have my SQLAlchemy models using datetime.datetime not problem,
    however when I switched from psycopg2 to asyncpg, I got a ProgrammingError that it can't
    subtract a offset-naive and offset-aware datetime. Thus, I switched datetime initializations
    to what you see in app.models.posts.

    the regular jsonable_encoder turns datetime.datetime objects to ISO-Format strings. But, requests
    returned by the API (controlled by asyncpg) are in military or something. Read this stackOverflow for more:
    https://stackoverflow.com/questions/19654578/python-utc-datetime-objects-iso-format-doesnt-include-z-zulu-or-zero-offset
    """

    def test_datetime_convert(datetim: datetime.datetime):
        return datetim.isoformat().replace("+00:00", "Z")

    cust_enc = {datetime.datetime: test_datetime_convert}
    return old_encoder(obj=obj, *args, custom_encoder=cust_enc, **kwargs)
