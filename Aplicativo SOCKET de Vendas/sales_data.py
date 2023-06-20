import sqlite3
conn = sqlite3.connect('dados_venda.db')
cursor = conn.cursor()

# Criando a tabela de venda
cursor.execute('''
    CREATE TABLE IF NOT EXISTS venda (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_vendedor TEXT,
    loja_id TEXT,
    data_venda TEXT,
    valor_venda REAL
);
''')
def validar_venda(message):
    nome_vendedor = message["nome_vendedor"]
    loja_id = message["loja_id"]
    data_venda = message["data_venda"]
    valor_venda = message["valor_venda"]

    # Validação dos dados
    if not nome_vendedor or not loja_id or not data_venda or not valor_venda:
        return "ERRO: Dados de venda inválidos."

    try:
        conn = sqlite3.connect("dados_venda.db")
        cursor = conn.cursor()

        # Inserção dos dados no banco de dados
        cursor.execute(
            "INSERT INTO venda (nome_vendedor, loja_id, data_venda, valor_venda) VALUES (?, ?, ?, ?)",
            (nome_vendedor, loja_id, data_venda, valor_venda)
        )
        conn.commit()

        cursor.close()
        conn.close()

        return "OK: Venda registrada com sucesso."

    except sqlite3.Error as e:
        return "ERRO: Falha ao registrar venda no banco de dados - " + str(e)
