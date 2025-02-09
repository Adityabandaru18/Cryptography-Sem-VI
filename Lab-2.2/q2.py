from cryptography.fernet import Fernet

def generate_key(key_file='key.key'):
    key = Fernet.generate_key()
    with open(key_file, 'wb') as f:
        f.write(key)

def load_key(key_file='key.key'):
    return open(key_file, 'rb').read()

def encrypt_text_file(input_file, output_file, key_file='key.key'):
    generate_key(key_file)
    key = load_key(key_file)
    fernet = Fernet(key)
    
    with open(input_file, 'r') as f:
        text_data = f.read()
    bytes_data = text_data.encode()
    
    encrypted_data = fernet.encrypt(bytes_data)
    
    # Save encrypted bytes to a file
    with open(output_file, 'wb') as f:
        f.write(encrypted_data)

def decrypt_text_file(input_file, output_file, key_file='key.key'):
    """Decrypt an encrypted text file back to plain text."""
    key = load_key(key_file)
    fernet = Fernet(key)
    
    # Read encrypted bytes
    with open(input_file, 'rb') as f:
        encrypted_data = f.read()
    
    decrypted_data = fernet.decrypt(encrypted_data).decode()
    
    # Save decrypted text
    with open(output_file, 'w') as f:
        f.write(decrypted_data)

if __name__ == '__main__':
    # Encrypt the text file
    encrypt_text_file('plaintext.txt', 'encrypted_text.enc')
    print("Text file encrypted.")
    
    # Decrypt the text file
    decrypt_text_file('encrypted_text.enc', 'decrypted_text.txt')
    print("Text file decrypted.")