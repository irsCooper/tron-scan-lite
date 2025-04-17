from datetime import datetime
from typing import Optional
import uuid
from pydantic import BaseModel


class BandwidthSchema(BaseModel):
    freeNetUsed: Optional[int] = None
    freeNetLimit: Optional[int] = None
    TotalNetLimit: Optional[int] = None
    TotalNetWeight: Optional[int] = None


class EnergySchema(BaseModel):
    EnergyLimit: Optional[int] = None
    TotalEnergyLimit: Optional[int] = None
    TotalEnergyWeight: Optional[int] = None


class ResourcesSchema(BaseModel):
    bandwidth: BandwidthSchema
    energy: EnergySchema


class TronAccountInfoSchema(BaseModel):
    address: str
    balance: float
    bandwidth: BandwidthSchema
    energy: EnergySchema


class TronAccountInfoCreate(TronAccountInfoSchema):
    pass 


class TronAccountInfoUpdate(BaseModel):
    pass


class TronAccountInfoDB(TronAccountInfoSchema):
    id: uuid.UUID
    creates_at: datetime