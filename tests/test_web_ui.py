import pytest

from applications.app_service.main import create_app


@pytest.fixture
def client():
    app = create_app("sqlite:///:memory:")
    app.config["TESTING"] = True
    return app.test_client()


def test_raiz_sirve_la_pagina_html(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.content_type
    body = response.get_data(as_text=True)
    assert "Panel de verificación" in body
    assert "btn-verificar" in body


def test_la_api_sigue_funcionando_con_la_ui_registrada(client):
    assert client.get("/health").status_code == 200
    assert client.get("/vehiculos").get_json() == []
