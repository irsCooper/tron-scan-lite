from datetime import datetime
import uuid
from sqlalchemy import JSON, TIMESTAMP, UUID, Float, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.base_model import BaseModel


class TronAccountInfoModel(BaseModel):
    __tablename__ = 'tron_account_info'
    
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    address: Mapped[str] = mapped_column(String, nullable=False)
    balance: Mapped[float] = mapped_column(Float, nullable=False)
    bandwidth: Mapped[dict] = mapped_column(JSON, nullable=False)
    energy: Mapped[dict] = mapped_column(JSON, nullable=False)
    creates_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False, default=func.now())