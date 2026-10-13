class DominioError(Exception):
    """Base de todos los errores de negocio."""


class ValidacionError(DominioError):
    """Datos inválidos (se traducirá a HTTP 400)."""


class NoEncontradoError(DominioError):
    """Recurso inexistente (HTTP 404)."""


class ConflictoError(DominioError):
    """Regla de negocio violada por el estado actual (HTTP 409)."""


class PlacaDuplicadaError(ConflictoError):
    pass


class VehiculoNoDisponibleError(ConflictoError):
    pass


class AlquilerNoActivoError(ConflictoError):
    pass
