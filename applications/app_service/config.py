import os


def obtener_database_url() -> str:
    return os.getenv("ALQUILERES_DATABASE_URL", "sqlite:///:memory:")
