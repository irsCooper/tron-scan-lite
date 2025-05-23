from typing import Any, Dict, Generic, Optional, TypeVar, Union
from fastapi import HTTPException, status
from pydantic import BaseModel

from sqlalchemy import delete, func, insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.base_model import BaseModel
from src.exceptions.DatabaseException import DatabaseException, UnknowanDatabaseException


ModelType = TypeVar('ModelType', bound=BaseModel)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)

class BaseDAO(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    model = None 


    @classmethod
    async def add(
        cls,
        session: AsyncSession,
        obj_in: Union[CreateSchemaType, Dict[str, Any]],
    ) -> Optional[ModelType]:
        if isinstance(obj_in, dict):
            create_data = obj_in
        else:
            create_data = obj_in.model_dump(exclude_unset=True)

        try:
            stmt = (
                insert(cls.model)
                .values(**create_data)
                .returning(cls.model)
            )
            result = await session.execute(stmt)
            await session.commit()
            return result.scalars().first()
        except SQLAlchemyError:
            raise DatabaseException
        except Exception as e:
            print(e)
            raise UnknowanDatabaseException


    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        *where,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> Optional[ModelType]:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        
        stmt = (
            update(cls.model)
            .where(*where)
            .values(**update_data)
            .returning(cls.model)
        )

        result = await session.execute(stmt)
        return result.scalars().one_or_none()


    @classmethod
    async def delete(
        cls,
        session: AsyncSession,
        *filters,
        **filter_by
    ) -> None:
        stmt = (
            delete(cls.model)
            .filter(*filters)
            .filter_by(**filter_by)
        )
        await session.execute(stmt)
        await session.commit()


    @classmethod
    async def count(
        cls,
        session: AsyncSession,
        *filters,
        **filter_by
    ):
        stmt = (
            select(func.count())
            .select_from(cls.model)
            .filter(*filters)
            .filter_by(**filter_by)
        ) 

        result = await session.execute(stmt)
        return result.scalar()


    @classmethod
    async def find_all(
        cls, 
        session: AsyncSession,
        *filters,
        offset: int = 0,
        limit: int = 100,
        **filter_by
    ):
        if offset < 0 or limit <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Offset must be >= 0 and limit must be > 0"
            )
        
        stmt = (
            select(cls.model)
            .filter(*filters)
            .filter_by(**filter_by)
            .offset(offset)
            .limit(limit)
        )

        result = await session.execute(stmt)
        return result.scalars().all()
    

    @classmethod
    async def find_one_or_none(
        cls,
        session: AsyncSession,
        *filters,
        **filter_by
    ) -> Optional[ModelType]:
        stmt = (
            select(cls.model)
            .filter(*filters)
            .filter_by(**filter_by)
        )

        result = await session.execute(stmt)
        return result.scalars().one_or_none()