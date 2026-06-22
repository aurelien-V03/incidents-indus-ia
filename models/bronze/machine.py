from datetime import date, datetime
from typing import Optional

from sqlalchemy import Boolean, Date, Integer, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from models.bronze.base import Base


class BronzeMachine(Base):
    __tablename__ = "bronze_machine"

    machine_code: Mapped[str] = mapped_column(String(16), primary_key=True)
    commissioning_date: Mapped[Optional[date]] = mapped_column(Date)
    max_daily_capacity: Mapped[Optional[int]] = mapped_column(Integer)
    max_hourly_capacity_pieces: Mapped[Optional[int]] = mapped_column(Integer)
    model: Mapped[Optional[str]] = mapped_column(String(32))
    production_line: Mapped[Optional[str]] = mapped_column(String(16))
    location: Mapped[Optional[str]] = mapped_column(String(16))
    criticality: Mapped[Optional[str]] = mapped_column(String(8))
    is_active: Mapped[Optional[bool]] = mapped_column(Boolean)
    created_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)
