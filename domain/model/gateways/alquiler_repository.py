from abc import ABC, abstractmethod

from domain.model.alquiler.alquiler import Alquiler


class AlquilerRepository(ABC):
    @abstractmethod
    def guardar(self, alquiler: Alquiler) -> Alquiler:
        """Inserta (id None) o actualiza. Devuelve la entidad con id asignado."""

    @abstractmethod
    def obtener_por_id(self, alquiler_id: int) -> Alquiler | None: ...

    @abstractmethod
    def listar(self) -> list[Alquiler]: ...
