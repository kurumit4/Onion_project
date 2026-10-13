from dataclasses import dataclass

from domain.usecase.alquiler_usecase import AlquilerUseCase
from domain.usecase.vehiculo_usecase import VehiculoUseCase
from infrastructure.driven_adapters.sqlite_adapter.database import (
    crear_engine,
    crear_session_factory,
    crear_tablas,
)
from infrastructure.driven_adapters.sqlite_adapter.repositories.sqlite_alquiler_repository import (
    SqliteAlquilerRepository,
)
from infrastructure.driven_adapters.sqlite_adapter.repositories.sqlite_vehiculo_repository import (
    SqliteVehiculoRepository,
)


@dataclass
class Container:
    vehiculo_usecase: VehiculoUseCase
    alquiler_usecase: AlquilerUseCase


def construir_container(database_url: str) -> Container:
    engine = crear_engine(database_url)
    crear_tablas(engine)
    session_factory = crear_session_factory(engine)

    repo_vehiculos = SqliteVehiculoRepository(session_factory)
    repo_alquileres = SqliteAlquilerRepository(session_factory)

    return Container(
        vehiculo_usecase=VehiculoUseCase(repo_vehiculos),
        alquiler_usecase=AlquilerUseCase(repo_alquileres, repo_vehiculos),
    )
