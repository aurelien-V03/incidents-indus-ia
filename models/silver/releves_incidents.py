from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from models.silver.base import Base


class SilverRelevesIncidents(Base):
    __tablename__ = "silver_releves_incidents"

    incident_id: Mapped[str] = mapped_column(Text, primary_key=True)
    date: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP)
    operator_name: Mapped[Optional[str]] = mapped_column(Text)
    machine_id: Mapped[Optional[str]] = mapped_column(Text)
    severity: Mapped[Optional[int]] = mapped_column(BigInteger)
    operator_badge: Mapped[Optional[str]] = mapped_column(Text)
    comment: Mapped[Optional[str]] = mapped_column(Text)
    shift: Mapped[Optional[str]] = mapped_column(Text)
    type_surchauffe: Mapped[Optional[int]] = mapped_column(BigInteger)
    type_baisse_pression: Mapped[Optional[int]] = mapped_column(BigInteger)
    type_vibration: Mapped[Optional[int]] = mapped_column(BigInteger)
    type_bruit_mecanique: Mapped[Optional[int]] = mapped_column(BigInteger)
    type_surconsommation: Mapped[Optional[int]] = mapped_column(BigInteger)
    type_blocage_mecanique: Mapped[Optional[int]] = mapped_column(BigInteger)
    type_alarme_capteur: Mapped[Optional[int]] = mapped_column(BigInteger)
    type_arret_urgence: Mapped[Optional[int]] = mapped_column(BigInteger)
    type_defaut_qualite: Mapped[Optional[int]] = mapped_column(BigInteger)
