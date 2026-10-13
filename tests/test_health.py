from applications.app_service.main import create_app


def test_health_responde_ok():
    cliente = create_app().test_client()
    respuesta = cliente.get("/health")

    assert respuesta.status_code == 200
    assert respuesta.get_json() == {"status": "ok"}
