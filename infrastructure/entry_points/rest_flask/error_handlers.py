from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from domain.model.alquiler.exceptions import (
    ConflictoError,
    DominioError,
    NoEncontradoError,
    ValidacionError,
)


def _respuesta(tipo: str, mensaje: str, status: int):
    return jsonify({"error": {"tipo": tipo, "mensaje": mensaje}}), status


def registrar_error_handlers(app: Flask) -> None:
    @app.errorhandler(DominioError)
    def _dominio(exc: DominioError):
        if isinstance(exc, ValidacionError):
            status = 400
        elif isinstance(exc, NoEncontradoError):
            status = 404
        elif isinstance(exc, ConflictoError):
            status = 409
        else:
            status = 400
        return _respuesta(type(exc).__name__, str(exc), status)

    @app.errorhandler(HTTPException)
    def _http(exc: HTTPException):
        return _respuesta(exc.name.replace(" ", ""), exc.description, exc.code)
