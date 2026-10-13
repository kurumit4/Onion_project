from datetime import date

from domain.model.alquiler.alquiler import Alquiler
from domain.model.alquiler.exceptions import NoEncontradoError
from domain.model.alquiler.vehiculo import Vehiculo
from domain.model.gateways.alquiler_repository import AlquilerRepository
from domain.model.gateways.vehiculo_repository import VehiculoRepository


class AlquilerUseCase:
    def __init__(self, alquileres: AlquilerRepository, vehiculos: VehiculoRepository):
        self._alquileres = alquileres
        self._vehiculos = vehiculos

    def crear(self, vehiculo_id: int, cliente: str, fecha_inicio: date, fecha_fin: date) -> Alquiler:
        vehiculo = self._vehiculo(vehiculo_id)
        alquiler = Alquiler(
            vehiculo_id=vehiculo.id,
            cliente=cliente,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            tarifa_diaria=vehiculo.tarifa_diaria,
        )
        vehiculo.marcar_alquilado()
        guardado = self._alquileres.guardar(alquiler)
        self._vehiculos.guardar(vehiculo)
        return guardado

    def obtener(self, alquiler_id: int) -> Alquiler:
        alquiler = self._alquileres.obtener_por_id(alquiler_id)
        if alquiler is None:
            raise NoEncontradoError(f"No existe el alquiler {alquiler_id}")
        return alquiler

    def listar(self) -> list[Alquiler]:
        return self._alquileres.listar()

    def finalizar(self, alquiler_id: int) -> Alquiler:
        alquiler = self.obtener(alquiler_id)
        alquiler.finalizar()
        return self._cerrar(alquiler)

    def cancelar(self, alquiler_id: int) -> Alquiler:
        alquiler = self.obtener(alquiler_id)
        alquiler.cancelar()
        return self._cerrar(alquiler)

    def _cerrar(self, alquiler: Alquiler) -> Alquiler:
        vehiculo = self._vehiculo(alquiler.vehiculo_id)
        vehiculo.marcar_disponible()
        guardado = self._alquileres.guardar(alquiler)
        self._vehiculos.guardar(vehiculo)
        return guardado

    def _vehiculo(self, vehiculo_id: int) -> Vehiculo:
        vehiculo = self._vehiculos.obtener_por_id(vehiculo_id)
        if vehiculo is None:
            raise NoEncontradoError(f"No existe el vehículo {vehiculo_id}")
        return vehiculo
