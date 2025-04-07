import socket
from Crypto.Cipher import DES3
import base64

def _pad_data(text):
    padding_len = 8 - (len(text) % 8)
    return text + chr(padding_len) * padding_len

def _unpad_data(text):
    padding_len = ord(text[-1])
    return text[:-padding_len]

class _TripleDesServer:
    def __init__(self, _host='localhost', _port=8000):
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.bind((_host, _port))
        self._server_socket.listen(1)
        print("Server is listening...")

    def _handle_client(self, _client_socket):
        _key = _client_socket.recv(24)

        def _encrypt_data(message):
            _cipher = DES3.new(_key, DES3.MODE_ECB)
            _padded_text = _pad_data(message)
            _encrypted_text = _cipher.encrypt(_padded_text.encode('utf-8'))
            _encoded_encrypted_text = base64.b64encode(_encrypted_text).decode('utf-8')
            print(f"Encrypted Response (Base64): {_encoded_encrypted_text}")
            return _encoded_encrypted_text

        def _decrypt_data(encrypted_message):
            _cipher = DES3.new(_key, DES3.MODE_ECB)
            _decrypted_text = _cipher.decrypt(base64.b64decode(encrypted_message))
            return _unpad_data(_decrypted_text.decode('utf-8'))

        try:
            while True:
                _encrypted_message = _client_socket.recv(1024).decode('utf-8')
                if not _encrypted_message:
                    break
                print(f"Received Encrypted Message (Base64): {_encrypted_message}")
                _decrypted_message = _decrypt_data(_encrypted_message)
                print(f"Received (decrypted): {_decrypted_message}")
                _response = f"Server received: {_decrypted_message}"
                _encrypted_response = _encrypt_data(_response)
                _client_socket.sendall(_encrypted_response.encode('utf-8'))
        finally:
            _client_socket.close()

    def _start_server(self):
        try:
            while True:
                _client_socket, _addr = self._server_socket.accept()
                print(f"Client connected from {_addr}")
                self._handle_client(_client_socket)
        finally:
            self._server_socket.close()

if __name__ == "__main__":
    _server = _TripleDesServer()
    _server._start_server()