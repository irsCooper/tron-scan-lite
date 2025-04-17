# import pytest_asyncio
# from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
# from src.base_model import BaseModel  
# from src.core.config import settings

# DATABASE_URL = settings.db_url

# engine_test = create_async_engine(DATABASE_URL, echo=True)
# TestSessionLocal = async_sessionmaker(engine_test, expire_on_commit=False)

# @pytest_asyncio.fixture(scope="session", autouse=True)
# async def prepare_database():
#     async with engine_test.begin() as conn:
#         await conn.run_sync(BaseModel.metadata.create_all)
#     yield
#     async with engine_test.begin() as conn:
#         await conn.run_sync(BaseModel.metadata.drop_all)

# @pytest_asyncio.fixture()
# async def test_session() -> AsyncSession:
#     async with TestSessionLocal() as session:
#         yield session

import asyncio
import uuid
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport
import pytest_asyncio
from sqlalchemy import NullPool, text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from src.core.db_helper import db
from src.base_model import BaseModel
from src.core.config import settings
from main import app
from src.tron.schemas import TronAccountInfoCreate

engine_test = create_async_engine(settings.db_url_test, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_test, expire_on_commit=False)
BaseModel.metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
        await session.commit()


app.dependency_overrides[db.session_dependency] = override_get_async_session


@pytest_asyncio.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture
async def test_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
        await session.commit()

@pytest_asyncio.fixture
async def wallet_data():
    wallets = []
    addresses = [
        "TLSgRcoeokT8mSB8Fsm9FYw3bAHmCijLkZ",
        "TGAsYqmz2DF41tqSmHzRpJe4frgnkmTSCw",
        "TPPJeMAL38vnGyA7okhEv6QEg6VPvYVK6z",
        "TJwoFcjbwyoExajXjwktUEatLdkaVaTSDe",
        "TGeUXHdW5946LoiCkVxb57R6cx1MvcvQiu",
        "TK1tznW9vaL6WEzkjn5y1zGbvjvor1mN9g",
        "TLSgRcoeokT8mSB8Fsm9FYw3bAHmCijLkZ",
        "TK1tznW9vaL6WEzkjn5y1zGbvjvor1mN9g",
        "TNy7RXWEcKEs8qRnXLHhcgcjxFkS4DiUzw",
        "TUNfXYmHh8GDRyqP4rqohsoHYGrLbv6kj7",
    ]
    for i in range(10):
        address = addresses[i]
        balance = 100.0 + i * 100  
        bandwidth = {'freeNetUsed': 100 + i, 'freeNetLimit': 200, 'energyUsed': 50 + i, 'energyLimit': 100}
        energy = {'EnergyLimit': 1000, 'TotalEnergyLimit': 180000000000, 'TotalEnergyWeight': 564766467306}
        
        obj_in = TronAccountInfoCreate(
            address=address,
            balance=balance,
            bandwidth=bandwidth,
            energy=energy
        )

        wallets.append(obj_in)

    return wallets