# Gestión de alquileres de vehículos

Aplicación de ejemplo para administrar vehículos y alquileres con arquitectura
hexagonal (Clean / Puertos y Adaptadores). El backend usa Flask, SQLite y
SQLAlchemy; una página HTML estática consume la API REST y permite verificar
el flujo completo.

## Requisitos

- Python 3.12 o compatible
- pip

## Instalación

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Ejecutar pruebas

```powershell
pytest -q
```

## Iniciar la aplicación

```powershell
python -m applications.app_service.main
```

Abre [http://127.0.0.1:5000/](http://127.0.0.1:5000/) para usar el panel.
El API está disponible en `/vehiculos` y `/alquileres`.

## Persistencia en disco

Por defecto la aplicación usa una base SQLite en memoria, que se pierde al
reiniciar el proceso. Para conservar los datos en un archivo, configura la
variable de entorno antes de arrancar:

```powershell
$env:ALQUILERES_DATABASE_URL = "sqlite:///alquileres.db"
python -m applications.app_service.main
```

## Limitaciones conocidas

- La base de datos predeterminada es volátil porque reside en memoria.
- Las operaciones de alquiler coordinan persistencias separadas para alquiler y
  vehículo; una mejora futura es implementar Unit of Work para transacciones
  atómicas.
- El servidor de desarrollo se ejecuta con `threaded=False`, requerido para el
  uso seguro de la conexión SQLite compartida en memoria.

## Trazabilidad

| Criterio | Dónde se cumple |
|---|---|
| Servicio funcional (gestión de alquileres) | `domain/usecase/`, `infrastructure/entry_points/rest_flask/` |
| Base de datos local (H2 o equivalente) | SQLite en memoria: `infrastructure/driven_adapters/sqlite_adapter/database.py` |
| DBO | `infrastructure/driven_adapters/sqlite_adapter/dbo/` |
| Mappers | `infrastructure/driven_adapters/sqlite_adapter/mappers/` |
| Scaffold Bancolombia (Clean / Puertos y Adaptadores) | Estructura `domain/` · `infrastructure/` · `applications/` |
| Interfaces de abstracción | `domain/model/gateways/` (ABC) implementadas en `infrastructure/driven_adapters/sqlite_adapter/repositories/` |
| Dependencias controladas | `tests/test_arquitectura.py` |
| Verificación visual | `infrastructure/entry_points/web_ui/static/index.html` servida en `/` |

## Diagramas

- [Arquitectura](docs/diagrama_arquitectura.md)
- [Clases](docs/diagrama_clases.md)
- [Casos de uso](docs/casos_de_uso.md)
