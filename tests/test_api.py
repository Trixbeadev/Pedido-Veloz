"""Unit tests for the Flask APIs; no running Docker stack or database is needed."""

import importlib.util
import copy
from datetime import datetime
from pathlib import Path
import sys
from unittest.mock import Mock

import pytest


ROOT = Path(__file__).resolve().parents[1]


def load_app(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


gateway = load_app("gateway_app", "gateway/app.py")
pedidos = load_app("pedidos_app", "servico-pedidos/app.py")
pagamentos = load_app("pagamentos_app", "servico-pagamentos/app.py")
estoque = load_app("estoque_app", "servico-estoque/app.py")


class FakeConnection:
    """Small psycopg connection substitute returning configured query results."""

    def __init__(self, results):
        self.results = iter(results)
        self.result = None

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False

    def execute(self, *_args, **_kwargs):
        self.result = next(self.results)
        return self

    def fetchone(self):
        return copy.deepcopy(self.result)

    def fetchall(self):
        return copy.deepcopy(self.result)


@pytest.fixture
def clients():
    return {
        "gateway": gateway.app.test_client(),
        "pedidos": pedidos.app.test_client(),
        "pagamentos": pagamentos.app.test_client(),
        "estoque": estoque.app.test_client(),
    }


def test_gateway_health_and_metrics(clients):
    assert clients["gateway"].get("/health").status_code == 200
    assert clients["gateway"].get("/metrics").status_code == 200


def test_gateway_forwards_request_and_preserves_response(clients, monkeypatch):
    upstream = Mock(status_code=201)
    upstream.json.return_value = {"id": 42}
    request_mock = Mock(return_value=upstream)
    monkeypatch.setattr(gateway.requests, "request", request_mock)

    response = clients["gateway"].post(
        "/pedidos", json={"produto": "Mouse", "quantidade": 2}
    )

    assert response.status_code == 201
    assert response.get_json() == {"id": 42}
    assert request_mock.call_args.kwargs["url"] == "http://servico-pedidos:5001/pedidos"
    assert request_mock.call_args.kwargs["json"] == {
        "produto": "Mouse",
        "quantidade": 2,
    }


def test_gateway_reports_upstream_failure(clients, monkeypatch):
    monkeypatch.setattr(
        gateway.requests,
        "request",
        Mock(side_effect=gateway.requests.ConnectionError("offline")),
    )
    response = clients["gateway"].get("/estoque")
    assert response.status_code == 502
    assert "erro" in response.get_json()


def test_orders_validate_create_list_and_check_readiness(clients, monkeypatch):
    response = clients["pedidos"].post("/pedidos", json={"produto": "Mouse"})
    assert response.status_code == 400

    created = {
        "id": 7,
        "produto": "Mouse",
        "quantidade": 2,
        "valor_unitario": 25.5,
        "status": "CRIADO",
        "criado_em": datetime(2026, 10, 28, 12, 0),
    }
    monkeypatch.setattr(pedidos, "conectar_banco", lambda: FakeConnection([created]))
    response = clients["pedidos"].post(
        "/pedidos",
        json={"produto": "Mouse", "quantidade": 2, "valor_unitario": 25.5},
    )
    assert response.status_code == 201
    assert response.get_json()["id"] == 7
    assert response.get_json()["valor_unitario"] == 25.5

    monkeypatch.setattr(pedidos, "conectar_banco", lambda: FakeConnection([[created]]))
    response = clients["pedidos"].get("/pedidos")
    assert response.status_code == 200
    assert response.get_json()[0]["produto"] == "Mouse"

    monkeypatch.setattr(pedidos, "conectar_banco", lambda: FakeConnection([None]))
    assert clients["pedidos"].get("/health/ready").status_code == 200


def test_payments_validate_and_approve_simulated_payment(clients):
    invalid = clients["pagamentos"].post("/pagamentos", json={"pedido_id": 0, "valor": 5})
    assert invalid.status_code == 400

    response = clients["pagamentos"].post(
        "/pagamentos", json={"pedido_id": 7, "valor": 51.0}
    )
    assert response.status_code == 200
    assert response.get_json()["status"] == "APROVADO"
    assert clients["pagamentos"].get("/metrics").status_code == 200


def test_inventory_query_and_reserve_stock(clients, monkeypatch):
    monkeypatch.setattr(
        estoque,
        "conectar_banco",
        lambda: FakeConnection([[("Mouse", 50), ("Teclado", 30)]]),
    )
    response = clients["estoque"].get("/estoque")
    assert response.status_code == 200
    assert response.get_json() == {"Mouse": 50, "Teclado": 30}

    monkeypatch.setattr(estoque, "conectar_banco", lambda: FakeConnection([(48,)]))
    response = clients["estoque"].post(
        "/estoque/reservas", json={"produto": "Mouse", "quantidade": 2}
    )
    assert response.status_code == 200
    assert response.get_json()["estoque_disponivel"] == 48

    monkeypatch.setattr(
        estoque,
        "conectar_banco",
        lambda: FakeConnection([None, (50,)]),
    )
    response = clients["estoque"].post(
        "/estoque/reservas", json={"produto": "Mouse", "quantidade": 100}
    )
    assert response.status_code == 409

    assert clients["estoque"].get("/metrics").status_code == 200
