import socket

def server_function():
    client_socket = socket.socket()
    client_socket.connect(("localhost", 4000))
    print("Connection established!")
    
    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            
            print("\nMessage received:", data)
            acknowledgment = "Acknowledgment: Message received successfully"
            client_socket.send(acknowledgment.encode())
        except:
            break
    
    client_socket.close()

if __name__ == "__main__":
    server_function()
