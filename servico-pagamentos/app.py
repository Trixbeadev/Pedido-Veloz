import os

from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
PrometheusMetrics(app)


@app.route("/health", methods=["GET"])
@app.route("/health/ready", methods=["GET"])
def health():
    return jsonify({"status": "ok", "servico": "pagamentos"}), 200


@app.route("/pagamentos", methods=["POST"])
def realizar_pagamento():
    dados = request.get_json(silent=True) or {}

    pedido_id = dados.get("pedido_id")
    valor = dados.get("valor")

    if isinstance(pedido_id, bool) or not isinstance(pedido_id, int) or pedido_id <= 0:
        return jsonify({"erro": "Informe um ID de pedido válido."}), 400

    try:
        if isinstance(valor, bool):
            raise ValueError()
        valor = float(valor)
        if valor <= 0:
            raise ValueError()
    except (TypeError, ValueError):
        return jsonify({"erro": "Informe um valor positivo."}), 400

    return jsonify({
        "pedido_id": pedido_id,
        "valor": valor,
        "status": "APROVADO",
        "mensagem": "Pagamento simulado com sucesso."
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5002)))