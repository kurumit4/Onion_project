from datetime import date

from domain.model.alquiler.alquiler import Alquiler
from domain.model.alquiler.exceptions import ValidacionError
from infrastructure.entry_points.rest_flask.dto.comun import exigir_campos


def _fecha(valor, campo: str) -> date:
    if not isinstance(valor, str):
        raise ValidacionError(f"{campo} debe ser una fecha con formato YYYY-MM-DD")
    try:
        return date.fromisoformat(valor)
    except ValueError as exc:
        raise ValidacionError(
            f"{campo} debe ser una fecha con formato YYYY-MM-DD"
        ) from exc


def parse_creacion(cuerpo) -> dict:
    datos = exigir_campos(
        cuerpo, ["vehiculo_id", "cliente", "fecha_inicio", "fecha_fin"]
    )
    vehiculo_id = datos["vehiculo_id"]
    if isinstance(vehiculo_id, bool) or not isinstance(vehiculo_id, int):
        raise ValidacionError("vehiculo_id debe ser un entero")
    return {
        "vehiculo_id": vehiculo_id,
        "cliente": datos["cliente"],
        "fecha_inicio": _fecha(datos["fecha_inicio"], "fecha_inicio"),
        "fecha_fin": _fecha(datos["fecha_fin"], "fecha_fin"),
    }


def a_dict(alquiler: Alquiler) -> dict:
    return {
        "id": alquiler.id,
        "vehiculo_id": alquiler.vehiculo_id,
        "cliente": alquiler.cliente,
        "fecha_inicio": alquiler.fecha_inicio.isoformat(),
        "fecha_fin": alquiler.fecha_fin.isoformat(),
        "dias": alquiler.dias,
        "tarifa_diaria": str(alquiler.tarifa_diaria),
        "costo_total": str(alquiler.costo_total),
        "estado": alquiler.estado.value,
    }
