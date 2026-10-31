import os
import time

import psycopg
from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
PrometheusMetrics(app)

DATABASE_URL = os.getenv("DATABASE_URL")


def conectar_banco():
    return psycopg.connect(DATABASE_URL)


def iniciar_banco():
    for _ in range(10):
        try:
            with conectar_banco() as conexao:
                conexao.execute("""
                    CREATE TABLE IF NOT EXISTS estoque (
                        produto VARCHAR(100) PRIMARY KEY,
                        quantidade INTEGER NOT NULL CHECK (quantidade >= 0)
                    )
                """)
                conexao.execute("""
                    INSERT INTO estoque (produto, quantidade) VALUES
                        ('Notebook', 10),
                        ('Mouse', 50),
                        ('Teclado', 30)
                    ON CONFLICT (produto) DO NOTHING
                """)
            return
        except psycopg.OperationalError:
            time.sleep(3)

    raise RuntimeError("Nao foi possivel conectar ao banco de dados do estoque.")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "servico": "estoque"}), 200


@app.route("/health/ready", methods=["GET"])
def health_ready():
    try:
        with conectar_banco() as conexao:
            conexao.execute("SELECT 1")
        return jsonify({"status": "ready"}), 200
    except psycopg.Error:
        return jsonify({"status": "unavailable"}), 503


@app.route("/estoque", methods=["GET"])
def consultar_estoque():
    with conectar_banco() as conexao:
        itens = conexao.execute(
            "SELECT produto, quantidade FROM estoque ORDER BY produto"
        ).fetchall()
    return jsonify({produto: quantidade for produto, quantidade in itens}), 200


@app.route("/estoque/reservas", methods=["POST"])
def reservar_estoque():
    dados = request.get_json(silent=True) or {}

    produto = dados.get("produto")
    quantidade = dados.get("quantidade")

    if not isinstance(produto, str) or not produto:
        return jsonify({"erro": "Informe o produto."}), 400

    if isinstance(quantidade, bool) or not isinstance(quantidade, int) or quantidade <= 0:
        return jsonify({"erro": "A quantidade deve ser um inteiro positivo."}), 400

    with conectar_banco() as conexao:
        item = conexao.execute(
            """
            UPDATE estoque
            SET quantidade = quantidade - %s
            WHERE produto = %s AND quantidade >= %s
            RETURNING quantidade
            """,
            (quantidade, produto, quantidade),
        ).fetchone()

        if item is None:
            atual = conexao.execute(
                "SELECT quantidade FROM estoque WHERE produto = %s", (produto,)
            ).fetchone()
            if atual is None:
                return jsonify({"erro": "Produto não encontrado."}), 404
            return jsonify({"erro": "Estoque insuficiente."}), 409

    return jsonify({
        "produto": produto,
        "quantidade_reservada": quantidade,
        "estoque_disponivel": item[0]
    }), 200


if __name__ == "__main__":
    iniciar_banco()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5003)))
