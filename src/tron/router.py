import uuid
from fastapi import APIRouter, Depends, status

from requests import session
from sqlalchemy.ext.asyncio import AsyncSession

from src.tron.schemas import TronAccountInfoDB
from src.tron.service import TronAccountInfoService
from src.core.db_helper import db


router = APIRouter(
    prefix="/Info",
    tags=["Info"],
)

@router.post("", response_model_exclude=TronAccountInfoDB)
async def info_by_address(
    address: str,
    session: AsyncSession = Depends(db.session_dependency)
):
    return await TronAccountInfoService.info_by_address(
        address=address, session=session
    )

@router.get("", response_model_exclude=list[TronAccountInfoDB])
async def get_list_info_by_address(
    offset: int,
    limit: int,
    session: AsyncSession = Depends(db.session_dependency)
):
    return await TronAccountInfoService.get_list_info_by_address(
        session=session,
        offset=offset,
        limit=limit
    )