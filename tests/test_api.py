import pytest

from applications.app_service.main import create_app


@pytest.fixture
def client():
    app = create_app("sqlite:///:memory:")
    app.config["TESTING"] = True
    return app.test_client()


def _registrar_vehiculo(client, placa="ABC123", tarifa="100000"):
    response = client.post(
        "/vehiculos",
        json={
            "placa": placa,
            "marca": "Mazda",
            "modelo": "3",
            "tarifa_diaria": tarifa,
        },
    )
    assert response.status_code == 201
    return response.get_json()


def _payload_alquiler(vehiculo_id, inicio="2030-01-01", fin="2030-01-04"):
    return {
        "vehiculo_id": vehiculo_id,
        "cliente": "Ana",
        "fecha_inicio": inicio,
        "fecha_fin": fin,
    }


def test_registrar_vehiculo_201(client):
    vehiculo = _registrar_vehiculo(client, placa="abc123")
    assert vehiculo["id"] == 1
    assert vehiculo["placa"] == "ABC123"
    assert vehiculo["tarifa_diaria"] == "100000.00"
    assert vehiculo["estado"] == "DISPONIBLE"


def test_placa_duplicada_409(client):
    _registrar_vehiculo(client)
    response = client.post(
        "/vehiculos",
        json={
            "placa": "ABC123",
            "marca": "Kia",
            "modelo": "Rio",
            "tarifa_diaria": "50000",
        },
    )
    assert response.status_code == 409
    assert response.get_json()["error"]["tipo"] == "PlacaDuplicadaError"


@pytest.mark.parametrize(
    "cuerpo",
    [
        {},
        {"placa": "A1", "marca": "x", "modelo": "y"},
        {"placa": "A1", "marca": "x", "modelo": "y", "tarifa_diaria": "-5"},
        {"placa": "A1", "marca": "x", "modelo": "y", "tarifa_diaria": "abc"},
    ],
)
def test_registrar_vehiculo_invalido_400(client, cuerpo):
    response = client.post("/vehiculos", json=cuerpo)
    assert response.status_code == 400
    assert "mensaje" in response.get_json()["error"]


def test_json_invalido_400(client):
    response = client.post(
        "/vehiculos", data="no es json", content_type="application/json"
    )
    assert response.status_code == 400


def test_obtener_y_listar_vehiculos(client):
    _registrar_vehiculo(client)
    assert client.get("/vehiculos/1").status_code == 200
    assert len(client.get("/vehiculos").get_json()) == 1


def test_vehiculo_inexistente_404(client):
    response = client.get("/vehiculos/999")
    assert response.status_code == 404
    assert response.get_json()["error"]["tipo"] == "NoEncontradoError"


def test_ruta_desconocida_devuelve_json_404(client):
    response = client.get("/no-existe")
    assert response.status_code == 404
    assert "error" in response.get_json()


def test_crear_alquiler_201_con_costo_y_vehiculo_alquilado(client):
    vehiculo = _registrar_vehiculo(client)
    response = client.post(
        "/alquileres", json=_payload_alquiler(vehiculo["id"])
    )
    assert response.status_code == 201
    alquiler = response.get_json()
    assert alquiler["dias"] == 3
    assert alquiler["costo_total"] == "300000.00"
    assert alquiler["estado"] == "ACTIVO"
    assert client.get(f"/vehiculos/{vehiculo['id']}").get_json()["estado"] == "ALQUILADO"


def test_alquilar_vehiculo_ya_alquilado_409(client):
    vehiculo = _registrar_vehiculo(client)
    client.post("/alquileres", json=_payload_alquiler(vehiculo["id"]))
    response = client.post(
        "/alquileres", json=_payload_alquiler(vehiculo["id"])
    )
    assert response.status_code == 409


def test_fechas_invalidas_400_y_vehiculo_sigue_disponible(client):
    vehiculo = _registrar_vehiculo(client)
    response = client.post(
        "/alquileres",
        json=_payload_alquiler(vehiculo["id"], "2030-01-04", "2030-01-01"),
    )
    assert response.status_code == 400
    assert client.get(f"/vehiculos/{vehiculo['id']}").get_json()["estado"] == "DISPONIBLE"


def test_formato_de_fecha_invalido_400(client):
    vehiculo = _registrar_vehiculo(client)
    response = client.post(
        "/alquileres",
        json=_payload_alquiler(vehiculo["id"], "01/01/2030", "04/01/2030"),
    )
    assert response.status_code == 400


def test_alquiler_con_vehiculo_inexistente_404(client):
    response = client.post("/alquileres", json=_payload_alquiler(999))
    assert response.status_code == 404


def test_finalizar_alquiler_libera_vehiculo(client):
    vehiculo = _registrar_vehiculo(client)
    alquiler = client.post(
        "/alquileres", json=_payload_alquiler(vehiculo["id"])
    ).get_json()

    response = client.put(f"/alquileres/{alquiler['id']}/finalizar")

    assert response.status_code == 200
    assert response.get_json()["estado"] == "FINALIZADO"
    assert client.get(f"/vehiculos/{vehiculo['id']}").get_json()["estado"] == "DISPONIBLE"


def test_finalizar_dos_veces_409(client):
    vehiculo = _registrar_vehiculo(client)
    alquiler = client.post(
        "/alquileres", json=_payload_alquiler(vehiculo["id"])
    ).get_json()
    client.put(f"/alquileres/{alquiler['id']}/finalizar")
    assert client.put(f"/alquileres/{alquiler['id']}/finalizar").status_code == 409


def test_cancelar_alquiler_libera_vehiculo(client):
    vehiculo = _registrar_vehiculo(client)
    alquiler = client.post(
        "/alquileres", json=_payload_alquiler(vehiculo["id"])
    ).get_json()

    response = client.put(f"/alquileres/{alquiler['id']}/cancelar")

    assert response.status_code == 200
    assert response.get_json()["estado"] == "CANCELADO"
    assert client.get(f"/vehiculos/{vehiculo['id']}").get_json()["estado"] == "DISPONIBLE"


def test_obtener_y_listar_alquileres(client):
    vehiculo = _registrar_vehiculo(client)
    alquiler = client.post(
        "/alquileres", json=_payload_alquiler(vehiculo["id"])
    ).get_json()
    assert client.get(f"/alquileres/{alquiler['id']}").status_code == 200
    assert len(client.get("/alquileres").get_json()) == 1
    assert client.get("/alquileres/999").status_code == 404


def test_cada_app_tiene_su_propia_bd():
    app1 = create_app("sqlite:///:memory:")
    app2 = create_app("sqlite:///:memory:")
    app1.test_client().post(
        "/vehiculos",
        json={
            "placa": "AAA111",
            "marca": "x",
            "modelo": "y",
            "tarifa_diaria": "1",
        },
    )
    assert app2.test_client().get("/vehiculos").get_json() == []
