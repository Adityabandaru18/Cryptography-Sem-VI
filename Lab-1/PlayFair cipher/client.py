import socket
from threading import Thread

def create_playfair_matrix(key):
    key = key.lower().replace('j', 'i')
    matrix, used_chars = [], set()
    
    for char in key:
        if char not in used_chars and char.isalpha():
            matrix.append(char)
            used_chars.add(char)
    
    for char in "abcdefghiklmnopqrstuvwxyz":
        if char not in used_chars:
            matrix.append(char)
            used_chars.add(char)
    
    return [matrix[i:i + 5] for i in range(0, 25, 5)]

def find_position(matrix, char):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col
    return None

def playfair_encrypt_pair(matrix, pair):
    r1, c1 = find_position(matrix, pair[0])
    r2, c2 = find_position(matrix, pair[1])
    
    if r1 == r2:
        return matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5]
    elif c1 == c2:
        return matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2]
    else:
        return matrix[r1][c2] + matrix[r2][c1]

def playfair_encrypt(text, key="monarchy"):
    matrix = create_playfair_matrix(key)
    text = text.lower().replace('j', 'i')
    if len(text) % 2 != 0:
        text += 'x'
    
    encrypted_text = ""
    for i in range(0, len(text), 2):
        encrypted_text += playfair_encrypt_pair(matrix, text[i:i+2])
    
    return encrypted_text

def handle_client(connection):
    while True:
        try:
            message = input("Send data: ")
            encrypted_message = playfair_encrypt(message)
            connection.send(encrypted_message.encode())
            response = connection.recv(1024).decode()
            print(response)
        except Exception as e:
            print(f"Error: {e}")
            break

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 3000))
    server_socket.listen(5)
    print("Server is running and waiting for connections...")
    
    while True:
        client_sock, client_addr = server_socket.accept()
        print(f"Connection established with {client_addr}")
        Thread(target=handle_client, args=(client_sock,)).start()

if __name__ == "__main__":
    start_server()
