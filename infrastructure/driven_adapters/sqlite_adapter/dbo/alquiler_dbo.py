from datetime import date

from sqlalchemy import Date, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.driven_adapters.sqlite_adapter.base import Base


class AlquilerDBO(Base):
    __tablename__ = "alquileres"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    vehiculo_id: Mapped[int] = mapped_column(ForeignKey("vehiculos.id"), nullable=False)
    cliente: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha_inicio: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_fin: Mapped[date] = mapped_column(Date, nullable=False)
    tarifa_diaria: Mapped[str] = mapped_column(String(20), nullable=False)
    costo_total: Mapped[str] = mapped_column(String(20), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False)
