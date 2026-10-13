from domain.model.alquiler.vehiculo import Vehiculo
from infrastructure.entry_points.rest_flask.dto.comun import exigir_campos


def parse_registro(cuerpo) -> dict:
    datos = exigir_campos(cuerpo, ["placa", "marca", "modelo", "tarifa_diaria"])
    return {
        "placa": datos["placa"],
        "marca": datos["marca"],
        "modelo": datos["modelo"],
        "tarifa_diaria": datos["tarifa_diaria"],
    }


def a_dict(vehiculo: Vehiculo) -> dict:
    return {
        "id": vehiculo.id,
        "placa": vehiculo.placa,
        "marca": vehiculo.marca,
        "modelo": vehiculo.modelo,
        "tarifa_diaria": str(vehiculo.tarifa_diaria),
        "estado": vehiculo.estado.value,
    }
