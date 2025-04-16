from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession

from src.blockchain.dao import TronAccountInfoDAO
from src.blockchain.schemas import TronAccountInfoCreate, TronAccountInfoDB, ResourcesSchema
from src.blockchain.client import tron_client
from src.exceptions.BlockchainException import AddressNotFoundException

class TronAccountInfoService:
    @classmethod
    async def info_by_address(
        cls,
        address: str,
        session: AsyncSession
    ) -> Optional[TronAccountInfoDB]:
        if tron_client.client.is_address(address):
            balance: float = await tron_client.get_balance(address)
            info: ResourcesSchema = await tron_client.get_resources(address)

            return await TronAccountInfoDAO.add(
                session=session,
                obj_in=TronAccountInfoCreate(
                    address=address,
                    balance=balance,
                    bandwidth=info.bandwidth,
                    energy=info.energy
                )
            )
        
        raise AddressNotFoundException(address)
    

    @classmethod
    async def get_list_info_by_address(
        cls,
        session: AsyncSession,
        offset: int,
        limit: int
    ):
        return await TronAccountInfoDAO.find_all(
            session,
            offset=offset,
            limit=limit
        )