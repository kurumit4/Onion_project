from datetime import date
from decimal import Decimal

import pytest

from domain.model.alquiler.alquiler import Alquiler
from domain.model.alquiler.enums import EstadoAlquiler
from domain.model.alquiler.exceptions import AlquilerNoActivoError, ValidacionError


def _alquiler(**cambios):
    datos = dict(
        vehiculo_id=1,
        cliente="Ana",
        fecha_inicio=date(2030, 1, 1),
        fecha_fin=date(2030, 1, 4),
        tarifa_diaria=Decimal("100000"),
    )
    datos.update(cambios)
    return Alquiler(**datos)


def test_calcula_costo_total_dias_por_tarifa():
    a = _alquiler()
    assert a.dias == 3
    assert a.costo_total == Decimal("300000.00")
    assert a.estado == EstadoAlquiler.ACTIVO


def test_respeta_costo_informado_al_reconstruir():
    a = _alquiler(costo_total=Decimal("123.45"))
    assert a.costo_total == Decimal("123.45")


@pytest.mark.parametrize("fin", [date(2030, 1, 1), date(2029, 12, 31)])
def test_fecha_fin_debe_ser_posterior(fin):
    with pytest.raises(ValidacionError):
        _alquiler(fecha_fin=fin)


def test_cliente_obligatorio():
    with pytest.raises(ValidacionError):
        _alquiler(cliente="   ")


def test_finalizar_y_cancelar():
    a = _alquiler()
    a.finalizar()
    assert a.estado == EstadoAlquiler.FINALIZADO

    b = _alquiler()
    b.cancelar()
    assert b.estado == EstadoAlquiler.CANCELADO


def test_solo_un_alquiler_activo_cambia_de_estado():
    a = _alquiler()
    a.finalizar()
    with pytest.raises(AlquilerNoActivoError):
        a.finalizar()
    with pytest.raises(AlquilerNoActivoError):
        a.cancelar()
