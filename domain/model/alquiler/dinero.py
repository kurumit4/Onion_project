from decimal import Decimal, InvalidOperation

from domain.model.alquiler.exceptions import ValidacionError

_CENTAVOS = Decimal("0.01")


def a_dinero_positivo(valor, campo: str) -> Decimal:
    """Convierte a Decimal con 2 decimales y exige que sea > 0."""
    try:
        dinero = Decimal(str(valor)).quantize(_CENTAVOS)
    except (InvalidOperation, ValueError):
        raise ValidacionError(f"{campo} no es un número válido")
    if dinero <= 0:
        raise ValidacionError(f"{campo} debe ser mayor que cero")
    return dinero
