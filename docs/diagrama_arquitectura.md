# Arquitectura (Puertos y Adaptadores)

```mermaid
flowchart LR
    subgraph EP[entry_points]
        REST[rest_flask<br/>controllers + DTO]
        UI[web_ui<br/>index.html]
    end
    subgraph DOM[domain]
        UC[usecase]
        GW[[gateways ABC]]
        MOD[model: entidades]
    end
    subgraph DA[driven_adapters]
        REPO[sqlite_adapter<br/>repositories + mappers + DBO]
    end
    UI -->|fetch| REST
    REST --> UC
    UC --> MOD
    UC --> GW
    REPO -.implementa.-> GW
    REPO --> DB[(SQLite en memoria)]
    APP[applications/app_service<br/>composition root] -.ensambla.-> REST
    APP -.ensambla.-> REPO
```

Regla: las flechas de dependencia del código apuntan hacia `domain`. El dominio no conoce ni Flask ni infraestructura; la composición se hace desde `applications`.
