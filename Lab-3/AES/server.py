import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

key = b'mysecretkey12345mysecretkey12345'

def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_message = cipher.encrypt(pad(message.encode(), AES.block_size))
    return encrypted_message

def decrypt_message(encrypted_message, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_message = unpad(cipher.decrypt(encrypted_message), AES.block_size)
    return decrypted_message.decode()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 12345))
    server_socket.listen(1)
    print("Server listening on port 12345...")

    conn, addr = server_socket.accept()
    print(f"Connection from {addr} established.")

    while True:
        encrypted_message = conn.recv(1024)
        if not encrypted_message:
            break

        decrypted_message = decrypt_message(encrypted_message, key)
        print(f"Received from client: {decrypted_message}")

        response = f"Server received: {decrypted_message}"
        encrypted_response = encrypt_message(response, key)
        conn.send(encrypted_response)

    conn.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()