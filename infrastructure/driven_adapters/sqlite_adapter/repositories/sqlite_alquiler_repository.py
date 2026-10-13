from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from domain.model.alquiler.alquiler import Alquiler
from domain.model.gateways.alquiler_repository import AlquilerRepository
from infrastructure.driven_adapters.sqlite_adapter.dbo.alquiler_dbo import AlquilerDBO
from infrastructure.driven_adapters.sqlite_adapter.mappers.alquiler_mapper import AlquilerMapper


class SqliteAlquilerRepository(AlquilerRepository):
    def __init__(self, session_factory: sessionmaker):
        self._session_factory = session_factory

    def guardar(self, alquiler: Alquiler) -> Alquiler:
        with self._session_factory() as session:
            dbo = session.merge(AlquilerMapper.to_dbo(alquiler))
            session.commit()
            return AlquilerMapper.to_domain(dbo)

    def obtener_por_id(self, alquiler_id: int) -> Alquiler | None:
        with self._session_factory() as session:
            dbo = session.get(AlquilerDBO, alquiler_id)
            return AlquilerMapper.to_domain(dbo) if dbo else None

    def listar(self) -> list[Alquiler]:
        with self._session_factory() as session:
            filas = session.scalars(select(AlquilerDBO).order_by(AlquilerDBO.id)).all()
            return [AlquilerMapper.to_domain(f) for f in filas]
