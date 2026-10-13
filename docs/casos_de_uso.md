# Casos de uso

| CU | Caso de uso | Método del caso de uso | HTTP |
|---|---|---|---|
| CU-01 | Registrar vehículo | `VehiculoUseCase.registrar` | POST /vehiculos |
| CU-02 | Consultar vehículo | `VehiculoUseCase.obtener` | GET /vehiculos/{id} |
| CU-03 | Listar vehículos | `VehiculoUseCase.listar` | GET /vehiculos |
| CU-04 | Crear alquiler | `AlquilerUseCase.crear` | POST /alquileres |
| CU-05 | Consultar alquiler | `AlquilerUseCase.obtener` | GET /alquileres/{id} |
| CU-06 | Listar alquileres | `AlquilerUseCase.listar` | GET /alquileres |
| CU-07 | Finalizar alquiler | `AlquilerUseCase.finalizar` | PUT /alquileres/{id}/finalizar |
| CU-08 | Cancelar alquiler | `AlquilerUseCase.cancelar` | PUT /alquileres/{id}/cancelar |

## Reglas de negocio

1. Un vehículo con alquiler `ACTIVO` no puede alquilarse de nuevo.
2. `fecha_fin` debe ser posterior a `fecha_inicio`.
3. `costo_total = días × tarifa_diaria` (la tarifa queda como copia fija en el alquiler).
4. Solo un alquiler `ACTIVO` puede finalizarse o cancelarse; al hacerlo, el vehículo queda `DISPONIBLE`.
