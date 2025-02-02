import socket
from threading import Thread

def client_function():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 4000))
    sock.listen(5)
    print("Server is running and waiting for connections...")
    
    while True:
        conn, addr = sock.accept()
        print(f"Connected to {addr}")
        
        def handle_client(connection):
            while True:
                try:
                    msg = input("Type message: ")
                    connection.send(msg.encode())
                    response = connection.recv(1024).decode()
                    print(response)
                except Exception as e:
                    print(f"Error: {e}")
                    break
        
        Thread(target=handle_client, args=(conn,)).start()

if __name__ == "__main__":
    client_function()
