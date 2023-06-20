import socket
import json

HOST = "localhost"
PORT = 12345

def enviar_venda(nome_vendedor, loja_id, data_venda, valor_venda):
    message = {
        "cod_operacao": 1,
        "nome_vendedor": nome_vendedor,
        "loja_id": loja_id,
        "data_venda": data_venda,
        "valor_venda": valor_venda
    }
    json_message = json.dumps(message)

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            try:
                client_socket.connect((HOST, PORT))
                client_socket.sendall(json_message.encode())

                resposta = client_socket.recv(1024).decode()
                print("Server resposta:", resposta)
                break
            except ConnectionRefusedError:
                print("Servidor principal não está respondendo. Iniciando processo de eleição...")
                from op_eleicao import Eleicao
                break
                


def menu():
    print("")
    print("======= Vendedor 1 =======")
    print("1. Registrar venda")
    print("0. Sair")
    print("==========================")
    print("")

def registrar_venda():
    nome_vendedor = "Vendedor_1"
    loja_id = 1
    data_venda = input("Data da venda (DD/MM/AAAA): ")
    valor_venda = float(input("Valor da venda: ").replace(",", "."))

    enviar_venda(nome_vendedor, loja_id, data_venda, valor_venda)

while True:
    menu()
    choice = input("Escolha uma opção: ")

    if choice == "1":
        registrar_venda()
    elif choice == "0":
        break
    else:
        print("Opção inválida. Tente novamente.")

print("Encerrando o cliente/vendedor 1.")

