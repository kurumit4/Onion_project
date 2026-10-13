from decimal import Decimal

from domain.model.alquiler.exceptions import NoEncontradoError, PlacaDuplicadaError
from domain.model.alquiler.vehiculo import Vehiculo
from domain.model.gateways.vehiculo_repository import VehiculoRepository


class VehiculoUseCase:
    def __init__(self, vehiculos: VehiculoRepository):
        self._vehiculos = vehiculos

    def registrar(self, placa: str, marca: str, modelo: str, tarifa_diaria: Decimal) -> Vehiculo:
        vehiculo = Vehiculo(placa=placa, marca=marca, modelo=modelo, tarifa_diaria=tarifa_diaria)
        if self._vehiculos.obtener_por_placa(vehiculo.placa) is not None:
            raise PlacaDuplicadaError(f"Ya existe un vehículo con placa {vehiculo.placa}")
        return self._vehiculos.guardar(vehiculo)

    def obtener(self, vehiculo_id: int) -> Vehiculo:
        vehiculo = self._vehiculos.obtener_por_id(vehiculo_id)
        if vehiculo is None:
            raise NoEncontradoError(f"No existe el vehículo {vehiculo_id}")
        return vehiculo

    def listar(self) -> list[Vehiculo]:
        return self._vehiculos.listar()
