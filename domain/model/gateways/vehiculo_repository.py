from abc import ABC, abstractmethod

from domain.model.alquiler.vehiculo import Vehiculo


class VehiculoRepository(ABC):
    @abstractmethod
    def guardar(self, vehiculo: Vehiculo) -> Vehiculo:
        """Inserta (id None) o actualiza. Devuelve la entidad con id asignado."""

    @abstractmethod
    def obtener_por_id(self, vehiculo_id: int) -> Vehiculo | None: ...

    @abstractmethod
    def obtener_por_placa(self, placa: str) -> Vehiculo | None: ...

    @abstractmethod
    def listar(self) -> list[Vehiculo]: ...
