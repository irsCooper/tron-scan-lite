from sqlalchemy import desc, select
from src.blockchain.schemas import TronAccountInfoCreate, TronAccountInfoUpdate
from src.blockchain.model import TronAccountInfoModel
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