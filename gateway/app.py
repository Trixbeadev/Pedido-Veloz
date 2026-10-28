import os

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

SERVICOS = {
    "pedidos": os.getenv("PEDIDOS_URL", "http://servico-pedidos:5001"),
    "pagamentos": os.getenv("PAGAMENTOS_URL", "http://servico-pagamentos:5002"),
    "estoque": os.getenv("ESTOQUE_URL", "http://servico-estoque:5003")
}


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "servico": "gateway"}), 200


def encaminhar(servico, caminho):
    url = SERVICOS[servico] + caminho

    try:
        resposta = requests.request(
            method=request.method,
            url=url,
            json=request.get_json(silent=True),
            params=request.args,
            timeout=10
        )

        try:
            dados = resposta.json()
        except ValueError:
            dados = {"resposta": resposta.text}

        return jsonify(dados), resposta.status_code

    except requests.RequestException:
        return jsonify({
            "erro": "Não foi possível se comunicar com o microsserviço."
        }), 502


@app.route("/pedidos", methods=["GET", "POST"])
def pedidos():
    return encaminhar("pedidos", "/pedidos")


@app.route("/pagamentos", methods=["POST"])
def pagamentos():
    return encaminhar("pagamentos", "/pagamentos")


@app.route("/estoque", methods=["GET"])
@app.route("/estoque/reservas", methods=["POST"])
def estoque():
    caminho = "/estoque"

    if request.path.endswith("/reservas"):
        caminho = "/estoque/reservas"

    return encaminhar("estoque", caminho)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))