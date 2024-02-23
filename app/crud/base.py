"""Generic CRUD interface.

Shamelessly copied from https://github.com/tiangolo/full-stack-fastapi-postgresql/blob/master/src/backend/app/app/crud/base.py.
"""
from typing import Any, Generic, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, PositiveInt
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType", bound=Any)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Generic CRUD class."""

    def __init__(self, model: type[ModelType]):
        """CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class

        **Why ever add to update_excluded_fields:**

        Prevent user injection of bad json somehow.

        Even if the update schema doesn't include them, update allows a plain dictionary.
        Therefore if a user could pass a dictionary of them and get it to work via the API, we want the database connectors to refuse.
        """
        self.model = model
        self.update_excluded_fields = set(["id", "date_modified", "date_created"])

    async def get(self, db: AsyncSession, id: PositiveInt) -> ModelType | None:
        """Retrieve the object of type ModelType given it's id."""
        return await db.get(self.model, id)

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """Create object of type ModelType in database given passed in Data."""
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        id: PositiveInt,
        obj_in: UpdateSchemaType | dict[str, Any],
    ) -> ModelType:
        """Update ModelType passed in with values from relevant fields found in `obj_in`."""
        if isinstance(obj_in, dict):
            update_data = obj_in

            bad_fields = self._get_invalid_update_fields(set(update_data.keys()))
            if bad_fields:
                raise KeyError(
                    f"Fields {bad_fields} are either manual update disallowed, or don't exist."
                )
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        update_stmt = (
            update(self.model).where(self.model.id == id).values(**update_data)
        )

        await db.execute(update_stmt)
        await db.commit()
        return await db.get(self.model, id)

    async def remove(self, db: AsyncSession, *, id: PositiveInt) -> ModelType:
        """Remove object from ModelType with id == `id`."""
        result_obj = await db.get(self.model, id)
        await db.delete(result_obj)
        await db.commit()
        return result_obj

    def _get_invalid_update_fields(self, update_fields: set) -> set:
        """Return all fields passed in that are not allowed to be updated or don't exist in the table."""
        updateable_fields = set(self.model.__table__.c.keys()).difference(
            set(self.update_excluded_fields)
        )
        return update_fields.difference(updateable_fields)
