import socket
import hashlib
import random
import base64
from Crypto.Cipher import AES  # type: ignore
from Crypto.Util.Padding import pad, unpad #type: ignore 

def dh_key():
    p, g = 23, 5  
    priv = random.randint(1, p - 1)
    pub = pow(g, priv, p)
    return priv, pub, p, g

def sec_key(priv, pub, p):
    sec = pow(pub, priv, p)
    return hashlib.sha512(str(sec).encode()).digest()[:32]

def hash_msg(msg):
    return hashlib.sha512(msg.encode()).digest()

def encrypt(msg, key):
    cipher = AES.new(key, AES.MODE_CBC)
    hsh = hash_msg(msg)
    data = msg.encode() + b"*" + hsh
    enc = cipher.encrypt(pad(data, AES.block_size))
    return base64.b64encode(cipher.iv + enc).decode()

def decrypt(enc_data, key):
    raw = base64.b64decode(enc_data)
    iv, cipher_text = raw[:16], raw[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    dec = unpad(cipher.decrypt(cipher_text), AES.block_size)
    msg, hsh_recv = dec.split(b"*")
    return msg.decode(), hash_msg(msg.decode()) == hsh_recv

def main():
    sock = socket.socket()
    sock.connect(("localhost", 4000))
    print("Connected to server!")

    c_priv, c_pub, p, g = dh_key()
    print(f"Client pub: {c_pub}")

    srv_pub, p, g = map(int, sock.recv(1024).decode().split(','))
    print(f"Server pub: {srv_pub}")

    sock.send(str(c_pub).encode())
    key = sec_key(c_priv, srv_pub, p)
    print("Shared key set")

    msg = input("Enter message: ")
    enc_msg = encrypt(msg, key)
    print(f"Encrypted: {enc_msg}")

    sock.send(enc_msg.encode())
    enc_resp = sock.recv(1024).decode()
    dec_resp, ok = decrypt(enc_resp, key)

    print("\nResults:")
    print(f"Decrypted: {dec_resp}")
    print(f"Integrity: {'Yes' if ok else 'No'}")
    sock.close()

if __name__ == "__main__":
    main()