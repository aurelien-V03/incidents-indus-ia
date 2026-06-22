from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import Integer, Numeric, String, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from models.bronze.base import Base


class BronzeMaintenance(Base):
    __tablename__ = "bronze_maintenance"

    maintenance_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    machine_code: Mapped[Optional[str]] = mapped_column(String(16))
    maintenance_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)
    maintenance_type: Mapped[Optional[str]] = mapped_column(String(16))
    action_type: Mapped[Optional[str]] = mapped_column(String(32))
    component: Mapped[Optional[str]] = mapped_column(String(64))
    description: Mapped[Optional[str]] = mapped_column(Text)
    related_incident_id: Mapped[Optional[str]] = mapped_column(String(16))
    duration_hours: Mapped[Optional[Decimal]] = mapped_column(Numeric(6, 2))
    created_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)
    updated_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)
