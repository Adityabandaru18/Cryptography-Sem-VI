import socket
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

key = b'mysecretkey12345mysecretkey12345'  

def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_message = cipher.encrypt(pad(message.encode(), AES.block_size))
    return encrypted_message

def decrypt_message(encrypted_message, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_message = unpad(cipher.decrypt(encrypted_message), AES.block_size)
    return decrypted_message.decode()

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))

    while True:
        message = input("Enter message to send (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break

        encrypted_message = encrypt_message(message, key)
        client_socket.send(encrypted_message)

        encrypted_response = client_socket.recv(1024)
        if not encrypted_response:
            break

        decrypted_response = decrypt_message(encrypted_response, key)
        print(f"Received from server: {decrypted_response}")

    client_socket.close()

if __name__ == "__main__":
    start_client()