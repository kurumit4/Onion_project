from flask import Flask

from domain.usecase.alquiler_usecase import AlquilerUseCase
from domain.usecase.vehiculo_usecase import VehiculoUseCase
from infrastructure.entry_points.rest_flask.controllers.alquiler_controller import (
    crear_blueprint_alquileres,
)
from infrastructure.entry_points.rest_flask.controllers.vehiculo_controller import (
    crear_blueprint_vehiculos,
)
from infrastructure.entry_points.rest_flask.error_handlers import (
    registrar_error_handlers,
)


def registrar_api(
    app: Flask,
    vehiculo_usecase: VehiculoUseCase,
    alquiler_usecase: AlquilerUseCase,
) -> None:
    app.register_blueprint(crear_blueprint_vehiculos(vehiculo_usecase))
    app.register_blueprint(crear_blueprint_alquileres(alquiler_usecase))
    registrar_error_handlers(app)
