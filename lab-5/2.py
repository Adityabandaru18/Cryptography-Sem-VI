import random 

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(e, phi):
    for d in range(2, phi):
        if (e * d) % phi == 1:
            return d
    return None 

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def get_prime():
    primes = [i for i in range(11, 100) if is_prime(i)]
    return random.choice(primes) 

def generate_rsa_keys():
    p = get_prime()
    q = get_prime()

    n = p * q
    phi_n = (p - 1) * (q - 1)

    e = 3  
    while gcd(e, phi_n) != 1:  # e and phi_n are coprime
        e += 2  

    d = mod_inverse(e, phi_n)  # private key

    public_key = (e, n)
    private_key = (d, n)

    return public_key, private_key

def encrypt(message, public_key):
    e, n = public_key
    return pow(message, e, n)  

def decrypt(ciphertext,private_key):
    d, n = private_key
    return pow(ciphertext, d, n)  

# Generate keys
public_key, private_key = generate_rsa_keys()

print("Public Key (e, n):", public_key)
print("Private Key (d, n):", private_key)

number = 890
encrypted_number = encrypt(number, public_key)
decrypted_number = decrypt(encrypted_number, private_key)

print("\nOriginal Number:", number)
print("Encrypted Number:", encrypted_number)
print("Decrypted Number:", decrypted_number)

letter = 'H'
ascii_value = ord(letter)  # Convert letter to ASCII
encrypted_letter = encrypt(ascii_value, public_key)
decrypted_letter_ascii = decrypt(encrypted_letter, private_key)
decrypted_letter = chr(decrypted_letter_ascii)  # Convert ASCII back to letter

print("\nOriginal Letter:", letter)
print("Encrypted Letter (ASCII):", chr(encrypted_letter%255))
print("Decrypted Letter:", decrypted_letter)
