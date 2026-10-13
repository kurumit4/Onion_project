from decimal import Decimal

from domain.model.alquiler.enums import EstadoVehiculo
from domain.model.alquiler.vehiculo import Vehiculo
from infrastructure.driven_adapters.sqlite_adapter.dbo.vehiculo_dbo import VehiculoDBO


class VehiculoMapper:
    @staticmethod
    def to_domain(dbo: VehiculoDBO) -> Vehiculo:
        return Vehiculo(
            id=dbo.id,
            placa=dbo.placa,
            marca=dbo.marca,
            modelo=dbo.modelo,
            tarifa_diaria=Decimal(dbo.tarifa_diaria),
            estado=EstadoVehiculo(dbo.estado),
        )

    @staticmethod
    def to_dbo(vehiculo: Vehiculo) -> VehiculoDBO:
        return VehiculoDBO(
            id=vehiculo.id,
            placa=vehiculo.placa,
            marca=vehiculo.marca,
            modelo=vehiculo.modelo,
            tarifa_diaria=str(vehiculo.tarifa_diaria),
            estado=vehiculo.estado.value,
        )
