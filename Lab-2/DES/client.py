import socket
from Crypto.Cipher import DES  
from Crypto.Random import get_random_bytes
import base64

def _pad_text(plain_text):
    padding_size = 8 - (len(plain_text) % 8)
    return plain_text + chr(padding_size) * padding_size

def _unpad_text(padded_text):
    padding_size = ord(padded_text[-1])
    return padded_text[:-padding_size]

class _DesClient:
    def __init__(self, _host='localhost', _port=8000):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((_host, _port))
        self._key = get_random_bytes(8)
        self._socket.sendall(self._key)
        print("Connected to server and key exchanged")

    def _encrypt_data(self, _message):
        _cipher = DES.new(self._key, DES.MODE_ECB)
        _padded_data = _pad_text(_message)
        _encrypted_data = _cipher.encrypt(_padded_data.encode('utf-8'))
        return base64.b64encode(_encrypted_data).decode('utf-8')

    def _decrypt_data(self, _encrypted_message):
        _cipher = DES.new(self._key, DES.MODE_ECB)
        _decrypted_data = _cipher.decrypt(base64.b64decode(_encrypted_message))
        return _unpad_text(_decrypted_data.decode('utf-8'))

    def _send_data(self):
        try:
            while True:
                _message = input("Enter message: ")
                if _message.lower() == 'quit':
                    break
                print(f"Original Message: {_message}")
                _encrypted_message = self._encrypt_data(_message)
                print(f"Encrypted Message: {_encrypted_message}")
                self._socket.sendall(_encrypted_message.encode('utf-8'))
                _response = self._socket.recv(1024).decode('utf-8')
                print(f"Received Encrypted Response: {_response}")
                _decrypted_response = self._decrypt_data(_response)
                print(f"Decrypted Response: {_decrypted_response}")
        finally:
            self._socket.close()

if __name__ == "__main__":
    _client = _DesClient()
    _client._send_data()