import uuid
from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from src.blockchain.client import tron_client

router = APIRouter(
    prefix="/Info",
    tags=["Info"],
)

@router.post("")
async def info_by_address(
    address: str
):
    return await tron_client.get_resources(address)