import pytest
from httpx import AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.tron.dao import TronAccountInfoDAO
from src.tron.model import TronAccountInfoModel

@pytest.mark.asyncio
async def test_info_by_address_endpoint(ac: AsyncClient):
    address = "TLSgRcoeokT8mSB8Fsm9FYw3bAHmCijLkZ"
    response = await ac.post(f"/Info?address={address}")

    assert response.status_code == 200
    data = response.json()
    assert data["address"] == address

@pytest.mark.asyncio
async def test_get_list_info_by_address(ac: AsyncClient, test_session: AsyncSession, wallet_data):
    await test_session.execute(delete(TronAccountInfoModel))
    for wallet in wallet_data:
        await TronAccountInfoDAO.add(test_session, wallet)

    response = await ac.get("/Info", params={"offset": 0, "limit": 100})

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == len(wallet_data)
