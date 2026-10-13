from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from domain.model.alquiler.dinero import a_dinero_positivo
from domain.model.alquiler.enums import EstadoAlquiler
from domain.model.alquiler.exceptions import AlquilerNoActivoError, ValidacionError


@dataclass
class Alquiler:
    vehiculo_id: int
    cliente: str
    fecha_inicio: date
    fecha_fin: date
    tarifa_diaria: Decimal
    costo_total: Decimal | None = None
    estado: EstadoAlquiler = EstadoAlquiler.ACTIVO
    id: int | None = None

    def __post_init__(self):
        self.cliente = (self.cliente or "").strip()
        if not self.cliente:
            raise ValidacionError("cliente es obligatorio")
        if not isinstance(self.fecha_inicio, date) or not isinstance(self.fecha_fin, date):
            raise ValidacionError("Las fechas deben ser válidas")
        if self.fecha_fin <= self.fecha_inicio:
            raise ValidacionError("fecha_fin debe ser posterior a fecha_inicio")

        self.tarifa_diaria = a_dinero_positivo(self.tarifa_diaria, "tarifa_diaria")
        if self.costo_total is None:
            self.costo_total = self.dias * self.tarifa_diaria
        self.costo_total = a_dinero_positivo(self.costo_total, "costo_total")

    @property
    def dias(self) -> int:
        return (self.fecha_fin - self.fecha_inicio).days

    def finalizar(self) -> None:
        self._exigir_activo()
        self.estado = EstadoAlquiler.FINALIZADO

    def cancelar(self) -> None:
        self._exigir_activo()
        self.estado = EstadoAlquiler.CANCELADO

    def _exigir_activo(self) -> None:
        if self.estado != EstadoAlquiler.ACTIVO:
            raise AlquilerNoActivoError(
                f"El alquiler {self.id} está {self.estado.value}; solo un alquiler ACTIVO puede cambiar de estado"
            )
