import socket
from Crypto.Cipher import ARC4

KEY = b"12345" 
HOST="localhost"
PORT=4000

def encrypt_RC4(data, key):
    cipher = ARC4.new(key)
    return cipher.encrypt(data)

def encrypt_FILE(filename, client_socket):
    with open(filename, "rb") as f:
        plaintext = f.read()

    encrypted_data = encrypt_RC4(plaintext, KEY)
    
    print(f"Encrypted {filename} ({len(encrypted_data)} bytes)")
    client_socket.sendall(encrypted_data)  

def main():
    client_socket = socket.socket()
    client_socket.connect((HOST, PORT))
    print("Connected to server successfully!")

    filename = "input.txt"  
    encrypt_FILE(filename, client_socket)

    print("File sent successfully!")
    client_socket.close()

if __name__ == "__main__":
    main()