import socket
import json

class ComunicacaoServidores:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))

    def send_message(self, message):
        data = json.dumps(message).encode()
        self.socket.sendall(data)

    def receive_message(self):
        data = self.socket.recv(1024).decode()
        message = json.loads(data)
        return message

    def close(self):
        self.socket.close()
