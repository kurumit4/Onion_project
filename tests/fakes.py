import copy

from domain.model.gateways.alquiler_repository import AlquilerRepository
from domain.model.gateways.vehiculo_repository import VehiculoRepository


class _FakeBase:
    def __init__(self):
        self._datos = {}
        self._siguiente_id = 1

    def guardar(self, entidad):
        if entidad.id is None:
            entidad.id = self._siguiente_id
            self._siguiente_id += 1
        self._datos[entidad.id] = copy.deepcopy(entidad)
        return copy.deepcopy(entidad)

    def obtener_por_id(self, entidad_id):
        entidad = self._datos.get(entidad_id)
        return copy.deepcopy(entidad) if entidad is not None else None

    def listar(self):
        return [copy.deepcopy(e) for e in self._datos.values()]


class FakeVehiculoRepository(_FakeBase, VehiculoRepository):
    def obtener_por_placa(self, placa):
        for vehiculo in self._datos.values():
            if vehiculo.placa == placa:
                return copy.deepcopy(vehiculo)
        return None


class FakeAlquilerRepository(_FakeBase, AlquilerRepository):
    pass
