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
        """
        self.model = model

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
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        update_data.pop("id", None)

        update_dict = {}
        for field in self.model.__table__.c.keys():
            if field in update_data:
                update_dict[field] = update_data.get(field)

        update_stmt = (
            update(self.model).where(self.model.id == id).values(**update_dict)
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
