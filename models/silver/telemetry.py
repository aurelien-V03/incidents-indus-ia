from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from models.silver.base import Base


class SilverTelemetry(Base):
    __tablename__ = "silver_telemetry"

    machine_id: Mapped[str] = mapped_column(Text, primary_key=True)
    date: Mapped[datetime] = mapped_column(TIMESTAMP, primary_key=True)
    temperature_c: Mapped[Optional[float]] = mapped_column()
    pressure_bar: Mapped[Optional[float]] = mapped_column()
    voltage_mean_v: Mapped[Optional[float]] = mapped_column()
    rotation_mean_rpm: Mapped[Optional[float]] = mapped_column()
    pieces_produced: Mapped[Optional[int]] = mapped_column(BigInteger)
