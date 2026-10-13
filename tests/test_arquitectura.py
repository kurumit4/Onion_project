import ast
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def _imports(carpeta: str):
    for archivo in (RAIZ / carpeta).rglob("*.py"):
        arbol = ast.parse(archivo.read_text(encoding="utf-8"))
        for nodo in ast.walk(arbol):
            if isinstance(nodo, ast.Import):
                for alias in nodo.names:
                    yield archivo, alias.name
            elif isinstance(nodo, ast.ImportFrom) and nodo.module:
                yield archivo, nodo.module


def violaciones(carpeta: str, prohibidos: list[str]) -> list[str]:
    return [
        f"{archivo.relative_to(RAIZ)} importa {modulo}"
        for archivo, modulo in _imports(carpeta)
        if any(modulo == p or modulo.startswith(p + ".") for p in prohibidos)
    ]


def test_dominio_no_depende_de_frameworks_ni_infraestructura():
    assert violaciones("domain", ["flask", "sqlalchemy", "infrastructure", "applications"]) == []


def test_entry_points_no_conocen_la_persistencia():
    assert violaciones(
        "infrastructure/entry_points",
        ["sqlalchemy", "infrastructure.driven_adapters"],
    ) == []


def test_driven_adapters_no_conocen_flask_ni_entry_points():
    assert violaciones(
        "infrastructure/driven_adapters",
        ["flask", "infrastructure.entry_points"],
    ) == []


def test_web_ui_no_importa_persistencia():
    assert violaciones(
        "infrastructure/entry_points/web_ui",
        ["sqlalchemy", "infrastructure.driven_adapters", "domain"],
    ) == []
