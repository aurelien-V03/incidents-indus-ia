from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, Boolean, Integer, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from models.gold.base import Base


class GoldTelemetry(Base):
    __tablename__ = "gold_telemetry"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    machine_id: Mapped[str] = mapped_column(Text)
    date: Mapped[datetime] = mapped_column(TIMESTAMP)
    temperature_c: Mapped[Optional[float]] = mapped_column()
    pressure_bar: Mapped[Optional[float]] = mapped_column()
    voltage_mean_v: Mapped[Optional[float]] = mapped_column()
    rotation_mean_rpm: Mapped[Optional[float]] = mapped_column()
    pieces_produced: Mapped[Optional[int]] = mapped_column(BigInteger)

    temperature_mean_6h: Mapped[Optional[float]] = mapped_column()
    temperature_max_6h: Mapped[Optional[float]] = mapped_column()
    temperature_std_6h: Mapped[Optional[float]] = mapped_column()
    temperature_mean_12h: Mapped[Optional[float]] = mapped_column()
    temperature_max_12h: Mapped[Optional[float]] = mapped_column()
    temperature_std_12h: Mapped[Optional[float]] = mapped_column()
    temperature_mean_24h: Mapped[Optional[float]] = mapped_column()
    temperature_max_24h: Mapped[Optional[float]] = mapped_column()
    temperature_std_24h: Mapped[Optional[float]] = mapped_column()

    pressure_mean_6h: Mapped[Optional[float]] = mapped_column()
    pressure_max_6h: Mapped[Optional[float]] = mapped_column()
    pressure_std_6h: Mapped[Optional[float]] = mapped_column()
    pressure_mean_12h: Mapped[Optional[float]] = mapped_column()
    pressure_max_12h: Mapped[Optional[float]] = mapped_column()
    pressure_std_12h: Mapped[Optional[float]] = mapped_column()
    pressure_mean_24h: Mapped[Optional[float]] = mapped_column()
    pressure_max_24h: Mapped[Optional[float]] = mapped_column()
    pressure_std_24h: Mapped[Optional[float]] = mapped_column()

    voltage_mean_6h: Mapped[Optional[float]] = mapped_column()
    voltage_max_6h: Mapped[Optional[float]] = mapped_column()
    voltage_std_6h: Mapped[Optional[float]] = mapped_column()
    voltage_mean_12h: Mapped[Optional[float]] = mapped_column()
    voltage_max_12h: Mapped[Optional[float]] = mapped_column()
    voltage_std_12h: Mapped[Optional[float]] = mapped_column()
    voltage_mean_24h: Mapped[Optional[float]] = mapped_column()
    voltage_max_24h: Mapped[Optional[float]] = mapped_column()
    voltage_std_24h: Mapped[Optional[float]] = mapped_column()

    rotation_mean_6h: Mapped[Optional[float]] = mapped_column()
    rotation_max_6h: Mapped[Optional[float]] = mapped_column()
    rotation_std_6h: Mapped[Optional[float]] = mapped_column()
    rotation_mean_12h: Mapped[Optional[float]] = mapped_column()
    rotation_max_12h: Mapped[Optional[float]] = mapped_column()
    rotation_std_12h: Mapped[Optional[float]] = mapped_column()
    rotation_mean_24h: Mapped[Optional[float]] = mapped_column()
    rotation_max_24h: Mapped[Optional[float]] = mapped_column()
    rotation_std_24h: Mapped[Optional[float]] = mapped_column()

    temperature_trend_1h: Mapped[Optional[float]] = mapped_column()
    temperature_trend_3h: Mapped[Optional[float]] = mapped_column()
    temperature_trend_6h: Mapped[Optional[float]] = mapped_column()

    temperature_zscore_machine: Mapped[Optional[float]] = mapped_column()
    pressure_zscore_machine: Mapped[Optional[float]] = mapped_column()
    voltage_zscore_machine: Mapped[Optional[float]] = mapped_column()
    rotation_zscore_machine: Mapped[Optional[float]] = mapped_column()

    label_failure_next_6h: Mapped[Optional[bool]] = mapped_column(Boolean)
    label_failure_next_12h: Mapped[Optional[bool]] = mapped_column(Boolean)
    label_failure_next_24h: Mapped[Optional[bool]] = mapped_column(Boolean)
    label_failure_next_48h: Mapped[Optional[bool]] = mapped_column(Boolean)
