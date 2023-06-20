import socket
import json

HOST = "localhost"
PORT = 12345

def consulta_bd(cod_operacao, data):
    message = {
        "cod_operacao": cod_operacao,
        "data": data
    }
    json_message = json.dumps(message)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        client_socket.sendall(json_message.encode())

        resposta = client_socket.recv(1024).decode()
        print("Server resposta:", resposta)

def menu():
    print("")
    print("=================== Gerente =====================")
    print("1. Total de vendas de um vendedor")
    print("2. Total de vendas de uma loja")
    print("3. Total de vendas da rede de lojas em um período")
    print("4. Melhor vendedor")
    print("5. Melhor loja")
    print("0. Sair")
    print("=================================================")
    print("")
    print("Nome dos Vendedores: Vendedor_1 ==== Vendedor_2 ==== Vendedor_3 ==== Vendedor_4 ==== Vendedor_5")
    print("IDs das lojas: loja 1 id: 1 ==== Loja 2 id: 2 ==== Loja 3 id: 3")
    print("")

def tot_venda_vendedor():
    nome_vendedor = input("Nome do vendedor: ")
    data = {"nome_vendedor": nome_vendedor}
    consulta_bd(2, data)
    
def tot_venda_loja():
    loja_id = input("ID da loja: ")
    data = {"loja_id": loja_id}
    consulta_bd(3, data)

def tot_venda_periodo():
    data_inicio = input("Data inicial (DD/MM/AAAA): ")
    data_fim = input("Data final (DD/MM/AAAA): ")
    data = {"data_inicio": data_inicio, "data_fim": data_fim}
    consulta_bd(4, data)

def melhor_vendedor():
    consulta_bd(5, {})

def melhor_loja():
    consulta_bd(6, {})

while True:
    menu()
    print("")
    choice = input("Escolha uma opção: ")
    print("")
    
    if choice == "1":
       tot_venda_vendedor()
    elif choice == "2":
        tot_venda_loja()
    elif choice == "3":
        tot_venda_periodo()
    elif choice == "4":
        melhor_vendedor()
    elif choice == "5":
        melhor_loja()
    elif choice == "0":
        break
    else:
        print("Opção inválida. Tente novamente.")

print("Encerrando o cliente/gerente.")
