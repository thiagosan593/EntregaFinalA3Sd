
import socket
import json
import sqlite3
import sales_data

HOST = "localhost"
PORT = 12345

DATABASE_NAME = "dados_venda.db"

def validar_venda(message):
    nome_vendedor = message["nome_vendedor"]
    loja_id = message["loja_id"]
    data_venda = message["data_venda"]
    valor_venda = message["valor_venda"]

    # Validar os dados da venda
    if not all([nome_vendedor, loja_id, data_venda, valor_venda]):
        return "ERRO: Dados de venda inválidos"

    # Inserir a venda no banco de dados
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO venda (nome_vendedor, loja_id, data_venda, valor_venda)
            VALUES (?, ?, ?, ?)
        """, (nome_vendedor, loja_id, data_venda, valor_venda))
        conn.commit()
    except Exception as e:
        return f"ERRO: Falha ao inserir a venda - {str(e)}"
    finally:
        conn.close()

    return "Venda registrada com sucesso"

def msg_consulta_bd(message):
    cod_operacao = message["cod_operacao"]
    data = message["data"]

    # Realizar a consulta no banco de dados
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    if cod_operacao == 2:  # Total de vendas de um vendedor
        nome_vendedor = data["nome_vendedor"]
        cursor.execute("""
            SELECT SUM(valor_venda)
            FROM venda
            WHERE nome_vendedor = ?
        """, (nome_vendedor,))
        total_venda = cursor.fetchone()[0]

        if total_venda is None:
            resposta = "Nenhum dado encontrado para o vendedor especificado"
        else:
            resposta = f"Total de vendas do vendedor {nome_vendedor}: {total_venda}"
    elif cod_operacao == 3:  # Total de vendas de uma loja
        loja_id = data["loja_id"]
        cursor.execute("""
            SELECT SUM(valor_venda)
            FROM venda
            WHERE loja_id = ?
        """, (loja_id,))
        total_venda = cursor.fetchone()[0]

        if total_venda is None:
            resposta = "Nenhum dado encontrado para a loja especificada"
        else:
            resposta = f"Total de vendas da loja {loja_id}: {total_venda}"
    elif cod_operacao == 4:  # Total de vendas da rede de lojas em um período
        data_inicio = data["data_inicio"]
        data_fim = data["data_fim"]
        cursor.execute("""
            SELECT SUM(valor_venda)
            FROM venda
            WHERE data_venda >= ? AND data_venda <= ?
        """, (data_inicio, data_fim))
        total_venda = cursor.fetchone()[0]

        if total_venda is None:
            resposta = "Nenhum dado encontrado para o período especificado"
        else:
            resposta = f"Total de vendas da rede de lojas no período de {data_inicio} a {data_fim}: {total_venda}"
    elif cod_operacao == 5:  # Melhor vendedor
        cursor.execute("""
            SELECT nome_vendedor, SUM(valor_venda) as total_venda
            FROM venda
            GROUP BY nome_vendedor
            ORDER BY total_venda DESC
            LIMIT 1
        """)
        result = cursor.fetchone()

        if result is None:
            resposta = "Nenhum dado encontrado"
        else:
            nome_vendedor, total_venda = result
            resposta = f"Melhor vendedor: {nome_vendedor} (Total de vendas: {total_venda})"
    elif cod_operacao == 6:  # Melhor loja
        cursor.execute("""
            SELECT loja_id, SUM(valor_venda) as total_venda
            FROM venda
            GROUP BY loja_id
            ORDER BY total_venda DESC
            LIMIT 1
        """)
        result = cursor.fetchone()

        if result is None:
            resposta = "Nenhum dado encontrado"
        else:
            loja_id, total_venda = result
            resposta = f" Loja: {loja_id} (Total de vendas: {total_venda})"
    else:
        resposta = "ERRO: Operação não suportada"

    conn.close()

    return resposta


def cnx_cliente(client_socket):
    data = client_socket.recv(1024).decode()
    message = json.loads(data)

    cod_operacao = message.get("cod_operacao")

    if cod_operacao == 1:  # Informe de venda
        resposta = validar_venda(message)
    elif cod_operacao == 2 or cod_operacao == 3 or cod_operacao == 4 or cod_operacao == 5 or cod_operacao == 6:  # Consulta
        resposta = msg_consulta_bd(message)
    else:
        resposta = "ERRO: Operação inválida"

    client_socket.sendall(resposta.encode())

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)

    print("Servidor iniciado. Aguardando conexões...")

    while True:
        client_socket, addr = server_socket.accept()
        print("Conexão estabelecida com", addr)

        cnx_cliente(client_socket)

        client_socket.close()

start_server()
