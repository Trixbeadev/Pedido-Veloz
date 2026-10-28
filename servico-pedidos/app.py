import os
import time

import psycopg
from flask import Flask, jsonify, request
from psycopg.rows import dict_row

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")


def conectar_banco():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


def iniciar_banco():
    for tentativa in range(10):
        try:
            with conectar_banco() as conexao:
                conexao.execute("""
                    CREATE TABLE IF NOT EXISTS pedidos (
                        id SERIAL PRIMARY KEY,
                        produto VARCHAR(100) NOT NULL,
                        quantidade INTEGER NOT NULL,
                        valor_unitario NUMERIC(10, 2) NOT NULL,
                        status VARCHAR(30) DEFAULT 'CRIADO',
                        criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
            print("Conexão com o banco realizada!")
            return
        except psycopg.OperationalError:
            print("Aguardando o banco de dados...")
            time.sleep(3)

    raise RuntimeError("Não foi possível conectar ao banco de dados.")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "servico": "pedidos"}), 200


@app.route("/health/ready", methods=["GET"])
def health_ready():
    try:
        with conectar_banco() as conexao:
            conexao.execute("SELECT 1")
        return jsonify({"status": "ready"}), 200
    except Exception:
        return jsonify({"status": "unavailable"}), 503


@app.route("/pedidos", methods=["POST"])
def criar_pedido():
    dados = request.get_json(silent=True) or {}

    produto = dados.get("produto")
    quantidade = dados.get("quantidade")
    valor_unitario = dados.get("valor_unitario")

    if not produto or not isinstance(produto, str):
        return jsonify({"erro": "Informe o produto."}), 400

    if isinstance(quantidade, bool) or not isinstance(quantidade, int) or quantidade <= 0:
        return jsonify({"erro": "A quantidade deve ser um inteiro positivo."}), 400

    try:
        valor_unitario = float(valor_unitario)
        if valor_unitario <= 0:
            raise ValueError()
    except (TypeError, ValueError):
        return jsonify({"erro": "Informe um valor unitário positivo."}), 400

    with conectar_banco() as conexao:
        pedido = conexao.execute("""
            INSERT INTO pedidos (produto, quantidade, valor_unitario)
            VALUES (%s, %s, %s)
            RETURNING id, produto, quantidade, valor_unitario, status, criado_em
        """, (produto, quantidade, valor_unitario)).fetchone()

    pedido["valor_unitario"] = float(pedido["valor_unitario"])
    pedido["criado_em"] = pedido["criado_em"].isoformat()

    return jsonify(pedido), 201


@app.route("/pedidos", methods=["GET"])
def listar_pedidos():
    with conectar_banco() as conexao:
        pedidos = conexao.execute("""
            SELECT id, produto, quantidade, valor_unitario, status, criado_em
            FROM pedidos
            ORDER BY id DESC
        """).fetchall()

    resultado = []

    for pedido in pedidos:
        pedido["valor_unitario"] = float(pedido["valor_unitario"])
        pedido["criado_em"] = pedido["criado_em"].isoformat()
        resultado.append(pedido)

    return jsonify(resultado), 200


if __name__ == "__main__":
    iniciar_banco()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5001)))