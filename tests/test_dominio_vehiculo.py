from decimal import Decimal

import pytest

from domain.model.alquiler.enums import EstadoVehiculo
from domain.model.alquiler.exceptions import ValidacionError, VehiculoNoDisponibleError
from domain.model.alquiler.vehiculo import Vehiculo


def _vehiculo(**cambios):
    datos = dict(placa="abc123", marca="Mazda", modelo="3", tarifa_diaria=100000)
    datos.update(cambios)
    return Vehiculo(**datos)


def test_normaliza_placa_y_tarifa():
    v = _vehiculo(placa=" abc123 ")
    assert v.placa == "ABC123"
    assert v.tarifa_diaria == Decimal("100000.00")
    assert v.estado == EstadoVehiculo.DISPONIBLE


@pytest.mark.parametrize("campo", ["placa", "marca", "modelo"])
def test_campos_obligatorios(campo):
    with pytest.raises(ValidacionError):
        _vehiculo(**{campo: "  "})


@pytest.mark.parametrize("tarifa", [0, -1, "abc", None])
def test_tarifa_invalida(tarifa):
    with pytest.raises(ValidacionError):
        _vehiculo(tarifa_diaria=tarifa)


def test_marcar_alquilado_y_disponible():
    v = _vehiculo()
    v.marcar_alquilado()
    assert v.estado == EstadoVehiculo.ALQUILADO
    v.marcar_disponible()
    assert v.estado == EstadoVehiculo.DISPONIBLE


def test_no_se_puede_alquilar_un_vehiculo_alquilado():
    v = _vehiculo()
    v.marcar_alquilado()
    with pytest.raises(VehiculoNoDisponibleError):
        v.marcar_alquilado()
