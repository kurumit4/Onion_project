from datetime import date
from decimal import Decimal

import pytest

from domain.model.alquiler.alquiler import Alquiler
from domain.model.alquiler.enums import EstadoAlquiler, EstadoVehiculo
from domain.model.alquiler.exceptions import PlacaDuplicadaError
from domain.model.alquiler.vehiculo import Vehiculo
from domain.usecase.alquiler_usecase import AlquilerUseCase
from domain.usecase.vehiculo_usecase import VehiculoUseCase
from infrastructure.driven_adapters.sqlite_adapter.database import (
    crear_engine,
    crear_session_factory,
    crear_tablas,
)
from infrastructure.driven_adapters.sqlite_adapter.mappers.alquiler_mapper import AlquilerMapper
from infrastructure.driven_adapters.sqlite_adapter.mappers.vehiculo_mapper import VehiculoMapper
from infrastructure.driven_adapters.sqlite_adapter.repositories.sqlite_alquiler_repository import (
    SqliteAlquilerRepository,
)
from infrastructure.driven_adapters.sqlite_adapter.repositories.sqlite_vehiculo_repository import (
    SqliteVehiculoRepository,
)


@pytest.fixture
def session_factory():
    engine = crear_engine("sqlite:///:memory:")
    crear_tablas(engine)
    return crear_session_factory(engine)


@pytest.fixture
def repos(session_factory):
    return SqliteVehiculoRepository(session_factory), SqliteAlquilerRepository(session_factory)


def _vehiculo(placa="ABC123"):
    return Vehiculo(placa=placa, marca="Mazda", modelo="3", tarifa_diaria=Decimal("100000.50"))


# ---- Mappers ----
def test_mapper_vehiculo_ida_y_vuelta():
    original = _vehiculo()
    original.id = 7
    dbo = VehiculoMapper.to_dbo(original)
    assert dbo.tarifa_diaria == "100000.50"
    assert dbo.estado == "DISPONIBLE"
    assert VehiculoMapper.to_domain(dbo) == original


def test_mapper_alquiler_ida_y_vuelta():
    original = Alquiler(
        id=3,
        vehiculo_id=1,
        cliente="Ana",
        fecha_inicio=date(2030, 1, 1),
        fecha_fin=date(2030, 1, 4),
        tarifa_diaria=Decimal("100000"),
    )
    dbo = AlquilerMapper.to_dbo(original)
    assert dbo.costo_total == "300000.00"
    assert AlquilerMapper.to_domain(dbo) == original


# ---- Repositorio de vehículos ----
def test_guardar_vehiculo_asigna_id_y_lo_recupera(repos):
    repo_v, _ = repos
    guardado = repo_v.guardar(_vehiculo())
    assert guardado.id is not None
    assert repo_v.obtener_por_id(guardado.id) == guardado
    assert repo_v.obtener_por_placa("ABC123") == guardado


def test_actualizar_vehiculo_persiste_el_cambio(repos):
    repo_v, _ = repos
    v = repo_v.guardar(_vehiculo())
    v.marcar_alquilado()
    repo_v.guardar(v)
    assert repo_v.obtener_por_id(v.id).estado == EstadoVehiculo.ALQUILADO
    assert len(repo_v.listar()) == 1


def test_placa_duplicada_a_nivel_de_bd(repos):
    repo_v, _ = repos
    repo_v.guardar(_vehiculo())
    with pytest.raises(PlacaDuplicadaError):
        repo_v.guardar(_vehiculo())


def test_obtener_inexistente_devuelve_none(repos):
    repo_v, repo_a = repos
    assert repo_v.obtener_por_id(99) is None
    assert repo_v.obtener_por_placa("ZZZ999") is None
    assert repo_a.obtener_por_id(99) is None


def test_listar_ordenado_por_id(repos):
    repo_v, _ = repos
    repo_v.guardar(_vehiculo("AAA111"))
    repo_v.guardar(_vehiculo("BBB222"))
    assert [v.placa for v in repo_v.listar()] == ["AAA111", "BBB222"]


# ---- Repositorio de alquileres ----
def test_guardar_y_actualizar_alquiler(repos):
    repo_v, repo_a = repos
    v = repo_v.guardar(_vehiculo())
    a = repo_a.guardar(
        Alquiler(
            vehiculo_id=v.id,
            cliente="Ana",
            fecha_inicio=date(2030, 1, 1),
            fecha_fin=date(2030, 1, 4),
            tarifa_diaria=v.tarifa_diaria,
        )
    )
    assert a.id is not None
    assert a.costo_total == Decimal("300001.50")

    a.finalizar()
    repo_a.guardar(a)
    leido = repo_a.obtener_por_id(a.id)
    assert leido.estado == EstadoAlquiler.FINALIZADO
    assert len(repo_a.listar()) == 1


# ---- Integración: casos de uso + repositorios reales ----
def test_flujo_completo_con_bd_real(repos):
    repo_v, repo_a = repos
    uc_v, uc_a = VehiculoUseCase(repo_v), AlquilerUseCase(repo_a, repo_v)

    v = uc_v.registrar("XYZ789", "Kia", "Rio", Decimal("80000"))
    a = uc_a.crear(v.id, "Luis", date(2030, 2, 1), date(2030, 2, 3))

    assert a.costo_total == Decimal("160000.00")
    assert uc_v.obtener(v.id).estado == EstadoVehiculo.ALQUILADO

    uc_a.finalizar(a.id)
    assert uc_v.obtener(v.id).estado == EstadoVehiculo.DISPONIBLE
