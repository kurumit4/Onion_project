from decimal import Decimal

from domain.model.alquiler.alquiler import Alquiler
from domain.model.alquiler.enums import EstadoAlquiler
from infrastructure.driven_adapters.sqlite_adapter.dbo.alquiler_dbo import AlquilerDBO


class AlquilerMapper:
    @staticmethod
    def to_domain(dbo: AlquilerDBO) -> Alquiler:
        return Alquiler(
            id=dbo.id,
            vehiculo_id=dbo.vehiculo_id,
            cliente=dbo.cliente,
            fecha_inicio=dbo.fecha_inicio,
            fecha_fin=dbo.fecha_fin,
            tarifa_diaria=Decimal(dbo.tarifa_diaria),
            costo_total=Decimal(dbo.costo_total),
            estado=EstadoAlquiler(dbo.estado),
        )

    @staticmethod
    def to_dbo(alquiler: Alquiler) -> AlquilerDBO:
        return AlquilerDBO(
            id=alquiler.id,
            vehiculo_id=alquiler.vehiculo_id,
            cliente=alquiler.cliente,
            fecha_inicio=alquiler.fecha_inicio,
            fecha_fin=alquiler.fecha_fin,
            tarifa_diaria=str(alquiler.tarifa_diaria),
            costo_total=str(alquiler.costo_total),
            estado=alquiler.estado.value,
        )
