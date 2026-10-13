from datetime import date
from decimal import Decimal

import pytest

from domain.model.alquiler.enums import EstadoAlquiler, EstadoVehiculo
from domain.model.alquiler.exceptions import (
    AlquilerNoActivoError,
    NoEncontradoError,
    PlacaDuplicadaError,
    ValidacionError,
    VehiculoNoDisponibleError,
)
from domain.usecase.alquiler_usecase import AlquilerUseCase
from domain.usecase.vehiculo_usecase import VehiculoUseCase
from tests.fakes import FakeAlquilerRepository, FakeVehiculoRepository

INICIO, FIN = date(2030, 1, 1), date(2030, 1, 4)


@pytest.fixture
def servicios():
    vehiculos = FakeVehiculoRepository()
    alquileres = FakeAlquilerRepository()
    return VehiculoUseCase(vehiculos), AlquilerUseCase(alquileres, vehiculos)


@pytest.fixture
def vehiculo(servicios):
    uc_vehiculo, _ = servicios
    return uc_vehiculo.registrar("ABC123", "Mazda", "3", Decimal("100000"))


# ---- Vehículos ----
def test_registrar_vehiculo_asigna_id(vehiculo):
    assert vehiculo.id == 1
    assert vehiculo.estado == EstadoVehiculo.DISPONIBLE


def test_placa_duplicada(servicios, vehiculo):
    uc_vehiculo, _ = servicios
    with pytest.raises(PlacaDuplicadaError):
        uc_vehiculo.registrar("abc123", "Kia", "Rio", Decimal("90000"))


def test_obtener_vehiculo_inexistente(servicios):
    uc_vehiculo, _ = servicios
    with pytest.raises(NoEncontradoError):
        uc_vehiculo.obtener(999)


def test_listar_vehiculos(servicios, vehiculo):
    uc_vehiculo, _ = servicios
    assert [v.placa for v in uc_vehiculo.listar()] == ["ABC123"]


# ---- Alquileres ----
def test_crear_alquiler_calcula_costo_y_marca_vehiculo(servicios, vehiculo):
    uc_vehiculo, uc_alquiler = servicios
    alquiler = uc_alquiler.crear(vehiculo.id, "Ana", INICIO, FIN)

    assert alquiler.id == 1
    assert alquiler.costo_total == Decimal("300000.00")
    assert alquiler.estado == EstadoAlquiler.ACTIVO
    assert uc_vehiculo.obtener(vehiculo.id).estado == EstadoVehiculo.ALQUILADO


def test_crear_alquiler_vehiculo_inexistente(servicios):
    _, uc_alquiler = servicios
    with pytest.raises(NoEncontradoError):
        uc_alquiler.crear(999, "Ana", INICIO, FIN)


def test_no_se_alquila_un_vehiculo_ya_alquilado(servicios, vehiculo):
    _, uc_alquiler = servicios
    uc_alquiler.crear(vehiculo.id, "Ana", INICIO, FIN)
    with pytest.raises(VehiculoNoDisponibleError):
        uc_alquiler.crear(vehiculo.id, "Luis", INICIO, FIN)


def test_fechas_invalidas_no_dejan_el_vehiculo_alquilado(servicios, vehiculo):
    uc_vehiculo, uc_alquiler = servicios
    with pytest.raises(ValidacionError):
        uc_alquiler.crear(vehiculo.id, "Ana", FIN, INICIO)
    assert uc_vehiculo.obtener(vehiculo.id).estado == EstadoVehiculo.DISPONIBLE


def test_finalizar_libera_el_vehiculo(servicios, vehiculo):
    uc_vehiculo, uc_alquiler = servicios
    alquiler = uc_alquiler.crear(vehiculo.id, "Ana", INICIO, FIN)

    finalizado = uc_alquiler.finalizar(alquiler.id)

    assert finalizado.estado == EstadoAlquiler.FINALIZADO
    assert uc_vehiculo.obtener(vehiculo.id).estado == EstadoVehiculo.DISPONIBLE


def test_cancelar_libera_el_vehiculo(servicios, vehiculo):
    uc_vehiculo, uc_alquiler = servicios
    alquiler = uc_alquiler.crear(vehiculo.id, "Ana", INICIO, FIN)

    cancelado = uc_alquiler.cancelar(alquiler.id)

    assert cancelado.estado == EstadoAlquiler.CANCELADO
    assert uc_vehiculo.obtener(vehiculo.id).estado == EstadoVehiculo.DISPONIBLE


def test_no_se_finaliza_dos_veces(servicios, vehiculo):
    _, uc_alquiler = servicios
    alquiler = uc_alquiler.crear(vehiculo.id, "Ana", INICIO, FIN)
    uc_alquiler.finalizar(alquiler.id)
    with pytest.raises(AlquilerNoActivoError):
        uc_alquiler.finalizar(alquiler.id)


def test_se_puede_alquilar_de_nuevo_tras_finalizar(servicios, vehiculo):
    _, uc_alquiler = servicios
    primero = uc_alquiler.crear(vehiculo.id, "Ana", INICIO, FIN)
    uc_alquiler.finalizar(primero.id)
    segundo = uc_alquiler.crear(vehiculo.id, "Luis", INICIO, FIN)
    assert segundo.id == 2


def test_obtener_y_listar_alquileres(servicios, vehiculo):
    _, uc_alquiler = servicios
    creado = uc_alquiler.crear(vehiculo.id, "Ana", INICIO, FIN)
    assert uc_alquiler.obtener(creado.id).cliente == "Ana"
    assert len(uc_alquiler.listar()) == 1
    with pytest.raises(NoEncontradoError):
        uc_alquiler.obtener(999)
