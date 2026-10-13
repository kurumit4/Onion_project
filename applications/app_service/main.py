from flask import Flask, jsonify

from applications.app_service.config import obtener_database_url
from applications.app_service.container import construir_container
from infrastructure.entry_points.rest_flask.api import registrar_api
from infrastructure.entry_points.web_ui.blueprint import crear_blueprint_web_ui


def create_app(database_url: str | None = None) -> Flask:
    app = Flask(__name__)
    container = construir_container(database_url or obtener_database_url())

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    registrar_api(app, container.vehiculo_usecase, container.alquiler_usecase)
    app.register_blueprint(crear_blueprint_web_ui())
    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5000, debug=False, threaded=False)
