from datetime import datetime
import uuid
from pydantic import BaseModel


class BandwidthSchema(BaseModel):
    freeNetUsed: int
    freeNetLimit: int
    TotalNetLimit: int
    TotalNetWeight: int


class EnergySchema(BaseModel):
    EnergyLimit: int
    TotalEnergyLimit: int
    TotalEnergyWeight: int


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