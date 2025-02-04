import socket
from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
import base64

def _pad_text(text):
    padding_size = 8 - (len(text) % 8)
    return text + chr(padding_size) * padding_size

def _unpad_text(text):
    padding_size = ord(text[-1])
    return text[:-padding_size]

class _TripleDesClient:
    def __init__(self, _host='localhost', _port=8000):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((_host, _port))
        self._key = DES3.adjust_key_parity(get_random_bytes(24))
        self._socket.sendall(self._key)
        print("Connected to server and key exchanged")

    def _encrypt_data(self, message):
        _cipher = DES3.new(self._key, DES3.MODE_ECB)
        _padded_text = _pad_text(message)
        _encrypted_text = _cipher.encrypt(_padded_text.encode('utf-8'))
        _encoded_encrypted_text = base64.b64encode(_encrypted_text).decode('utf-8')
        print(f"Encrypted Message (Base64): {_encoded_encrypted_text}")
        return _encoded_encrypted_text

    def _decrypt_data(self, encrypted_message):
        _cipher = DES3.new(self._key, DES3.MODE_ECB)
        _decrypted_text = _cipher.decrypt(base64.b64decode(encrypted_message))
        return _unpad_text(_decrypted_text.decode('utf-8'))

    def _send_data(self):
        try:
            while True:
                message = input("Enter message: ")
                if message.lower() == 'quit':
                    break
                encrypted_message = self._encrypt_data(message)
                self._socket.sendall(encrypted_message.encode('utf-8'))
                response = self._socket.recv(1024).decode('utf-8')
                print(f"Received Encrypted Response (Base64): {response}")
                decrypted_response = self._decrypt_data(response)
                print(f"Server response (decrypted): {decrypted_response}")
        finally:
            self._socket.close()

if __name__ == "__main__":
    client = _TripleDesClient()
    client._send_data()