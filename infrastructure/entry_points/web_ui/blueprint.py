from pathlib import Path

from flask import Blueprint, send_from_directory

_STATIC_DIR = Path(__file__).parent / "static"


def crear_blueprint_web_ui() -> Blueprint:
    bp = Blueprint("web_ui", __name__)

    @bp.get("/")
    def index():
        return send_from_directory(_STATIC_DIR, "index.html")

    return bp
