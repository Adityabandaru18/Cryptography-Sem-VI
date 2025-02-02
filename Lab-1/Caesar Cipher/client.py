import socket
from threading import Thread

class ClientHandler(Thread):
    def __init__(self, client_socket, client_address):
        Thread.__init__(self)
        self.sock = client_socket
        self.addr = client_address
        self.start()
    
    def encrypt_data(self, data, shift=1):
        encrypted_text = ""
        for char in data.lower():
            if char.isalpha():
                shifted = (ord(char) - ord('a') + shift) % 26
                encrypted_text += chr(shifted + ord('a'))
            else:
                encrypted_text += char
        return encrypted_text
    
    def run(self):
        while True:
            try:
                message = input("Send data: ")
                encrypted_message = self.encrypt_data(message)
                self.sock.send(encrypted_message.encode())
                response = self.sock.recv(1024).decode()
                print(response)
            except Exception as error:
                print(f"Error: {error}")
                break

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 3000))
    server_socket.listen(5)
    print("Server is running and awaiting connections...")
    
    while True:
        client_sock, client_addr = server_socket.accept()
        print(f"Connection established with {client_addr}")
        ClientHandler(client_sock, client_addr)

if __name__ == "__main__":
    start_server()
