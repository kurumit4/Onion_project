from infrastructure.entry_points.rest_flask.controllers.alquiler_controller import (
    crear_blueprint_alquileres,
)
from infrastructure.entry_points.rest_flask.controllers.vehiculo_controller import (
    crear_blueprint_vehiculos,
)

__all__ = ["crear_blueprint_vehiculos", "crear_blueprint_alquileres"]