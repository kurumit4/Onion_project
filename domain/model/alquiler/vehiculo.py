from dataclasses import dataclass
from decimal import Decimal

from domain.model.alquiler.dinero import a_dinero_positivo
from domain.model.alquiler.enums import EstadoVehiculo
from domain.model.alquiler.exceptions import ValidacionError, VehiculoNoDisponibleError


@dataclass
class Vehiculo:
    placa: str
    marca: str
    modelo: str
    tarifa_diaria: Decimal
    estado: EstadoVehiculo = EstadoVehiculo.DISPONIBLE
    id: int | None = None

    def __post_init__(self):
        self.placa = (self.placa or "").strip().upper()
        self.marca = (self.marca or "").strip()
        self.modelo = (self.modelo or "").strip()
        for campo in ("placa", "marca", "modelo"):
            if not getattr(self, campo):
                raise ValidacionError(f"{campo} es obligatorio")
        self.tarifa_diaria = a_dinero_positivo(self.tarifa_diaria, "tarifa_diaria")

    @property
    def esta_disponible(self) -> bool:
        return self.estado == EstadoVehiculo.DISPONIBLE

    def marcar_alquilado(self) -> None:
        if not self.esta_disponible:
            raise VehiculoNoDisponibleError(
                f"El vehículo {self.placa} no está disponible"
            )
        self.estado = EstadoVehiculo.ALQUILADO

    def marcar_disponible(self) -> None:
        self.estado = EstadoVehiculo.DISPONIBLE
