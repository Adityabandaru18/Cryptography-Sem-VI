import socket

def create_matrix(key):
    matrix = []
    used = set()
    
    for char in key.lower():
        if char not in used and char != 'j':
            matrix.append(char)
            used.add(char)
    
    for char in "abcdefghiklmnopqrstuvwxyz":
        if char not in used:
            matrix.append(char)
            used.add(char)
    
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def get_position(char, matrix):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col
    return None

def decrypt_pair(pair, matrix):
    r1, c1 = get_position(pair[0], matrix)
    r2, c2 = get_position(pair[1], matrix)
    
    if r1 == r2:
        return matrix[r1][(c1 - 1) % 5] + matrix[r2][(c2 - 1) % 5]
    elif c1 == c2:
        return matrix[(r1 - 1) % 5][c1] + matrix[(r2 - 1) % 5][c2]
    else:
        return matrix[r1][c2] + matrix[r2][c1]

def decrypt(msg, matrix):
    result = ""
    for i in range(0, len(msg), 2):
        result += decrypt_pair(msg[i:i+2], matrix)
    
    return result.rstrip('x')

s = socket.socket()
s.connect(("localhost", 3000))
print("Connected successfully!")

key = "monarchy"
matrix = create_matrix(key)

while True:
    try:
        enc_msg = s.recv(1024).decode()
        if not enc_msg:
            break

        dec_msg = decrypt(enc_msg, matrix)
        print("\nReceived encrypted message:", enc_msg)
        print("Decrypted message:", dec_msg)
        ack = "Message received and decrypted successfully\n"
        s.send(ack.encode())
    except:
        break

s.close()
