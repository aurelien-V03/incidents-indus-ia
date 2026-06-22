from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, Boolean, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from models.bronze.base import Base


class BronzeTelemetry(Base):
    __tablename__ = "bronze_telemetry"

    # Clé composite machine_id + date car pas de clé primaire naturelle unique
    machine_id: Mapped[str] = mapped_column(Text, primary_key=True)
    date: Mapped[datetime] = mapped_column(TIMESTAMP, primary_key=True)
    temperature_c: Mapped[Optional[float]] = mapped_column()
    pressure_bar: Mapped[Optional[float]] = mapped_column()
    voltage_mean_v: Mapped[Optional[float]] = mapped_column()
    rotation_mean_rpm: Mapped[Optional[float]] = mapped_column()
    pieces_produced: Mapped[Optional[int]] = mapped_column(BigInteger)
    valid_parsing: Mapped[bool] = mapped_column(Boolean, default=True)
    valid_error_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
