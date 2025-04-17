from sqlalchemy import desc, select
from fastapi import HTTPException, status

from src.tron.schemas import TronAccountInfoCreate, TronAccountInfoUpdate
from src.tron.model import TronAccountInfoModel
from src.base_dao import BaseDAO
from sqlalchemy.ext.asyncio import AsyncSession


class TronAccountInfoDAO(BaseDAO[TronAccountInfoModel, TronAccountInfoCreate, TronAccountInfoUpdate]):
    model = TronAccountInfoModel

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
            .order_by(desc(cls.model.creates_at))
        ) 
        result = await session.execute(stmt)
        res = result.scalars().all()
        return res