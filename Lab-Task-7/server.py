import socket
import hashlib
import random
import base64
from Crypto.Cipher import AES  # type: ignore
from Crypto.Util.Padding import pad, unpad # type: ignore

def dh_key():
    p, g = 23, 5
    priv = random.randint(1, p - 1)
    pub = pow(g, priv, p)
    return priv, pub, p, g

def shared_key(priv, pub, p):
    return hashlib.sha512(str(pow(pub, priv, p)).encode()).digest()[:32]

def hash_msg(msg):
    return hashlib.sha512(msg.encode()).digest()

def encrypt(msg, key):
    cipher = AES.new(key, AES.MODE_CBC)
    data = msg.encode() + b"*" + hash_msg(msg)
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
    s_priv, s_pub, p, g = dh_key()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("localhost", 4000))
    sock.listen(1)
    print("Server listening on port 4000...")

    client, addr = sock.accept()
    print(f"Client {addr} connected")

    client.send(f"{s_pub},{p},{g}".encode())
    c_pub = int(client.recv(1024).decode())
    print(f"Client pub key: {c_pub}")

    key = shared_key(s_priv, c_pub, p)
    print("Shared key set")

    enc_msg = client.recv(1024).decode()
    dec_msg, ok = decrypt(enc_msg, key)

    print("\nReceived Message:")
    print(f"Content: {dec_msg}")
    print(f"Integrity: {'Yes' if ok else 'No'}")

    response = "Message received with integrity verification"
    client.send(encrypt(response, key).encode())

    client.close()
    sock.close()

if __name__ == "__main__":
    main()