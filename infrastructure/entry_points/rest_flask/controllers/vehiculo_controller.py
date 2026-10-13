from flask import Blueprint, jsonify, request

from domain.usecase.vehiculo_usecase import VehiculoUseCase
from infrastructure.entry_points.rest_flask.dto import vehiculo_dto


def crear_blueprint_vehiculos(usecase: VehiculoUseCase) -> Blueprint:
    bp = Blueprint("vehiculos", __name__, url_prefix="/vehiculos")

    @bp.post("")
    def registrar():
        datos = vehiculo_dto.parse_registro(request.get_json(silent=True))
        return jsonify(vehiculo_dto.a_dict(usecase.registrar(**datos))), 201

    @bp.get("")
    def listar():
        return jsonify([vehiculo_dto.a_dict(v) for v in usecase.listar()]), 200

    @bp.get("/<int:vehiculo_id>")
    def obtener(vehiculo_id: int):
        return jsonify(vehiculo_dto.a_dict(usecase.obtener(vehiculo_id))), 200

    return bp
