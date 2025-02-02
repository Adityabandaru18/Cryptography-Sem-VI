import socket

def decrypt_message(text, shift=1):
    decrypted_text = ""
    for character in text.lower():
        if character.isalpha():
            adjusted = (ord(character) - ord('a') - shift) % 26
            decrypted_text += chr(adjusted + ord('a'))
        else:
            decrypted_text += character
    return decrypted_text

def client_program():
    client = socket.socket()
    client.connect(("localhost", 3000))
    print("Connection successful!")
    
    while True:
        try:
            encrypted_text = client.recv(1024).decode()
            if not encrypted_text:
                break
            
            decrypted_text = decrypt_message(encrypted_text)
            print("\nEncrypted message received:", encrypted_text)
            print("Decrypted message:", decrypted_text)
            acknowledgment = "Decryption successful. Message received."
            client.send(acknowledgment.encode())
        except:
            break
    
    client.close()

if __name__ == "__main__":
    client_program()
