from domain.model.alquiler.exceptions import ValidacionError


def exigir_campos(cuerpo, campos: list[str]) -> dict:
    if not isinstance(cuerpo, dict):
        raise ValidacionError("El cuerpo debe ser un objeto JSON")
    faltantes = [campo for campo in campos if campo not in cuerpo]
    if faltantes:
        raise ValidacionError(f"Faltan campos obligatorios: {', '.join(faltantes)}")
    return cuerpo
