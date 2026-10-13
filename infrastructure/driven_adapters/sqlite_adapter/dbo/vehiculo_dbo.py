from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.driven_adapters.sqlite_adapter.base import Base


class VehiculoDBO(Base):
    __tablename__ = "vehiculos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    placa: Mapped[str] = mapped_column(String(15), unique=True, nullable=False)
    marca: Mapped[str] = mapped_column(String(50), nullable=False)
    modelo: Mapped[str] = mapped_column(String(50), nullable=False)
    tarifa_diaria: Mapped[str] = mapped_column(String(20), nullable=False)
    estado: Mapped[str] = mapped_column(String(20), nullable=False)
