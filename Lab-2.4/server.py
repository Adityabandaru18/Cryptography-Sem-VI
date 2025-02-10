import socket
from Crypto.Cipher import ARC4

KEY = b"12345" 
HOST="localhost"
PORT=4000

def decrypt_RC4(data, key):
    cipher = ARC4.new(key)
    return cipher.decrypt(data)

def decrypt_FILE(conn):
    encrypted_data = conn.recv(4096)  
    with open("encrypt.rc4", "wb") as f:
        f.write(encrypted_data)
    print("Received and saved encrypted file!")

    decrypted_data = decrypt_RC4(encrypted_data, KEY)
    with open("decrypt.txt", "wb") as f:
        f.write(decrypted_data)
    print("File decrypted and saved as 'decrypt.txt'")

def main():
    server_socket = socket.socket()
    server_socket.bind((HOST, PORT))
    server_socket.listen(1)
    print("Server is listening on port 4000...")

    conn, addr = server_socket.accept()
    print(f" Connection established with {addr}")

    decrypt_FILE(conn)
    conn.close()

if __name__ == "__main__":
    main()