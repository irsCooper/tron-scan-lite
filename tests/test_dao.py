import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from src.tron.dao import TronAccountInfoDAO
from src.tron.model import TronAccountInfoModel

@pytest.mark.asyncio
async def test_add_wallet_query(test_session: AsyncSession, wallet_data):
    for wallet in wallet_data:
        result = await TronAccountInfoDAO.add(test_session, wallet)
        
        assert isinstance(result, TronAccountInfoModel)
        assert result.address == wallet.address
