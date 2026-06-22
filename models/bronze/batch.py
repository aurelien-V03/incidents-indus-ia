from datetime import datetime

from sqlalchemy import BigInteger, Integer, Text, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from models.bronze.base import Base


class BronzeBatch(Base):
    __tablename__ = "bronze_batch"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[datetime] = mapped_column(TIMESTAMP)
    file_name: Mapped[str] = mapped_column(Text)
    row_count: Mapped[int] = mapped_column(BigInteger)
