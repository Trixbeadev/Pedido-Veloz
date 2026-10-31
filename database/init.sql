CREATE TABLE IF NOT EXISTS pedidos (
    id SERIAL PRIMARY KEY,
    produto VARCHAR(100) NOT NULL,
    quantidade INTEGER NOT NULL,
    valor_unitario NUMERIC(10, 2) NOT NULL,
    status VARCHAR(30) DEFAULT 'CRIADO',
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS estoque (
    produto VARCHAR(100) PRIMARY KEY,
    quantidade INTEGER NOT NULL CHECK (quantidade >= 0)
);

INSERT INTO estoque (produto, quantidade) VALUES
    ('Notebook', 10),
    ('Mouse', 50),
    ('Teclado', 30)
ON CONFLICT (produto) DO NOTHING;