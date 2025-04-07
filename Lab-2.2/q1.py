from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

KEY_LENGTH = 32
BLOCK_SIZE = 16

def encrypt_data(input_text, secret_key):
    aes_cipher = AES.new(secret_key, AES.MODE_CBC)
    iv_bytes = aes_cipher.iv
    encrypted_content = aes_cipher.encrypt(pad(input_text.encode('utf-8'), BLOCK_SIZE))
    return iv_bytes + encrypted_content

def decrypt_data(encrypted_blob, secret_key):
    iv_bytes = encrypted_blob[:BLOCK_SIZE]
    actual_encrypted_data = encrypted_blob[BLOCK_SIZE:]
    aes_cipher = AES.new(secret_key, AES.MODE_CBC, iv_bytes)
    decrypted_content = unpad(aes_cipher.decrypt(actual_encrypted_data), BLOCK_SIZE)
    return decrypted_content.decode('utf-8')

key = get_random_bytes(KEY_LENGTH)
message = "Confidential data for encryption"

cipher_text = encrypt_data(message, key)
original_message = decrypt_data(cipher_text, key)

print("Original Message:", message)
print("Cipher Text:", cipher_text)
print("Decrypted Message:", original_message)
