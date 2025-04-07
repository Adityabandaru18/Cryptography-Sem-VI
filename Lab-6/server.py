import socket
import random

p = 23
g = 5

def get_private_key(p):
    return random.randint(2, p - 1)

def get_public_key(g, private_key, p):
    return pow(g, private_key, p)

def get_shared_secret(other_public_key, private_key, p):
    return pow(other_public_key, private_key, p)

def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():  
            shift_amount = shift % 26
            new_char = chr(((ord(char.lower()) - 97 + shift_amount) % 26) + 97)
            result += new_char.upper() if char.isupper() else new_char
        elif char.isdigit():  
            shift_amount = shift % 10
            new_char = chr(((ord(char) - 48 + shift_amount) % 10) + 48)
            result += new_char
        else:
            result += char  
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)


server = socket.socket()
server.bind(("0.0.0.0", 12345))
server.listen(1)
print("Waiting for client to connect...")
conn, addr = server.accept()
print(f"Connected to client: {addr}")

server_private_key = get_private_key(p)
server_public_key = get_public_key(g, server_private_key, p)

conn.send(str(server_public_key).encode())
client_public_key = int(conn.recv(1024).decode())

shared_secret = get_shared_secret(client_public_key, server_private_key, p)
shift = shared_secret % 26

print("\n--- Key Exchange ---")
print(f"Prime (p): {p}, Base (g): {g}")
print(f"Server Private Key: {server_private_key}")
print(f"Server Public Key: {server_public_key}")
print(f"Client Public Key: {client_public_key}")
print(f"Shared Secret Key: {shared_secret}")
print(f"Caesar Cipher Shift Value: {shift}\n")

while True:
    encrypted_message = conn.recv(1024).decode()
    decrypted_message = caesar_decrypt(encrypted_message, shift)
    
    print("\n--- Message Received ---")
    print(f"Encrypted Message: {encrypted_message}")
    print(f"Decrypted Message: {decrypted_message}")
    
    message = input("Server: ")
    encrypted_message = caesar_encrypt(message, shift)
    
    print("\n--- Message Sent ---")
    print(f"Original Message: {message}")
    print(f"Encrypted Message: {encrypted_message}")
    
    conn.send(encrypted_message.encode())
