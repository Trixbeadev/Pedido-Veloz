import os
import threading

from flask import Flask, jsonify, request

app = Flask(__name__)

estoque = {
    "Notebook": 10,
    "Mouse": 50,
    "Teclado": 30
}

bloqueio = threading.Lock()


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "servico": "estoque"}), 200


@app.route("/estoque", methods=["GET"])
def consultar_estoque():
    with bloqueio:
        return jsonify(estoque), 200


@app.route("/estoque/reservas", methods=["POST"])
def reservar_estoque():
    dados = request.get_json(silent=True) or {}

    produto = dados.get("produto")
    quantidade = dados.get("quantidade")

    if not isinstance(produto, str) or not produto:
        return jsonify({"erro": "Informe o produto."}), 400

    if isinstance(quantidade, bool) or not isinstance(quantidade, int) or quantidade <= 0:
        return jsonify({"erro": "A quantidade deve ser um inteiro positivo."}), 400

    with bloqueio:
        if produto not in estoque:
            return jsonify({"erro": "Produto não encontrado."}), 404

        if estoque[produto] < quantidade:
            return jsonify({"erro": "Estoque insuficiente."}), 409

        estoque[produto] -= quantidade

        return jsonify({
            "produto": produto,
            "quantidade_reservada": quantidade,
            "estoque_disponivel": estoque[produto]
        }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5003)))