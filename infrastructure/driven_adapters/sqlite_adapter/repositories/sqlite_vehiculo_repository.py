from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker

from domain.model.alquiler.exceptions import PlacaDuplicadaError
from domain.model.alquiler.vehiculo import Vehiculo
from domain.model.gateways.vehiculo_repository import VehiculoRepository
from infrastructure.driven_adapters.sqlite_adapter.dbo.vehiculo_dbo import VehiculoDBO
from infrastructure.driven_adapters.sqlite_adapter.mappers.vehiculo_mapper import VehiculoMapper


class SqliteVehiculoRepository(VehiculoRepository):
    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory

    def guardar(self, vehiculo: Vehiculo) -> Vehiculo:
        with self._session_factory() as session:
            try:
                dbo = session.merge(VehiculoMapper.to_dbo(vehiculo))
                session.commit()
            except IntegrityError as exc:
                session.rollback()
                raise PlacaDuplicadaError(f"Ya existe un vehículo con placa {vehiculo.placa}") from exc
            return VehiculoMapper.to_domain(dbo)

    def obtener_por_id(self, vehiculo_id: int) -> Vehiculo | None:
        with self._session_factory() as session:
            dbo = session.get(VehiculoDBO, vehiculo_id)
            return VehiculoMapper.to_domain(dbo) if dbo else None

    def obtener_por_placa(self, placa: str) -> Vehiculo | None:
        with self._session_factory() as session:
            dbo = session.scalars(select(VehiculoDBO).where(VehiculoDBO.placa == placa)).first()
            return VehiculoMapper.to_domain(dbo) if dbo else None

    def listar(self) -> list[Vehiculo]:
        with self._session_factory() as session:
            filas = session.scalars(select(VehiculoDBO).order_by(VehiculoDBO.id)).all()
            return [VehiculoMapper.to_domain(f) for f in filas]
