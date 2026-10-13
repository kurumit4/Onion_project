from flask import Blueprint, jsonify, request

from domain.usecase.alquiler_usecase import AlquilerUseCase
from infrastructure.entry_points.rest_flask.dto import alquiler_dto


def crear_blueprint_alquileres(usecase: AlquilerUseCase) -> Blueprint:
    bp = Blueprint("alquileres", __name__, url_prefix="/alquileres")

    @bp.post("")
    def crear():
        datos = alquiler_dto.parse_creacion(request.get_json(silent=True))
        return jsonify(alquiler_dto.a_dict(usecase.crear(**datos))), 201

    @bp.get("")
    def listar():
        return jsonify([alquiler_dto.a_dict(a) for a in usecase.listar()]), 200

    @bp.get("/<int:alquiler_id>")
    def obtener(alquiler_id: int):
        return jsonify(alquiler_dto.a_dict(usecase.obtener(alquiler_id))), 200

    @bp.put("/<int:alquiler_id>/finalizar")
    def finalizar(alquiler_id: int):
        return jsonify(alquiler_dto.a_dict(usecase.finalizar(alquiler_id))), 200

    @bp.put("/<int:alquiler_id>/cancelar")
    def cancelar(alquiler_id: int):
        return jsonify(alquiler_dto.a_dict(usecase.cancelar(alquiler_id))), 200

    return bp
