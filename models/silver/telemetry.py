from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, Integer, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from models.silver.base import Base


class SilverTelemetry(Base):
    __tablename__ = "silver_telemetry"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    machine_id: Mapped[str] = mapped_column(Text)
    date: Mapped[datetime] = mapped_column(TIMESTAMP)
    temperature_c: Mapped[Optional[float]] = mapped_column()
    pressure_bar: Mapped[Optional[float]] = mapped_column()
    voltage_mean_v: Mapped[Optional[float]] = mapped_column()
    rotation_mean_rpm: Mapped[Optional[float]] = mapped_column()
    pieces_produced: Mapped[Optional[int]] = mapped_column(BigInteger)
