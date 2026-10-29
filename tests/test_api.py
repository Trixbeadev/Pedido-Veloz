import requests

BASE_URL = "http://localhost:5000"


def test_gateway_health():
    resposta = requests.get(f"{BASE_URL}/health", timeout=5)
    assert resposta.status_code == 200


def test_listar_estoque():
    resposta = requests.get(f"{BASE_URL}/estoque", timeout=5)
    assert resposta.status_code == 200


def test_listar_pedidos():
    resposta = requests.get(f"{BASE_URL}/pedidos", timeout=5)
    assert resposta.status_code == 200
