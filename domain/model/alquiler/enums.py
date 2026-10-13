from enum import Enum


class EstadoVehiculo(str, Enum):
    DISPONIBLE = "DISPONIBLE"
    ALQUILADO = "ALQUILADO"


class EstadoAlquiler(str, Enum):
    ACTIVO = "ACTIVO"
    FINALIZADO = "FINALIZADO"
    CANCELADO = "CANCELADO"

