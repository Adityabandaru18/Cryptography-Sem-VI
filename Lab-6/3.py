import random

def get_private_key(p):
    return random.randint(2, p-1)

def get_public_key(g, private_key, p):
    return pow(g, private_key, p)

def get_shared_secret(other_public_key, private_key, p):
    return pow(other_public_key, private_key, p)

def diffie_hellman():
    p = 23  # Prime number
    g = 5   # Base value
    # g must be primitve root of p

    alice_private_key = get_private_key(p)
    bob_private_key = get_private_key(p)

    alice_public_key = get_public_key(g, alice_private_key, p)
    bob_public_key = get_public_key(g, bob_private_key, p)

    alice_secret = get_shared_secret(bob_public_key, alice_private_key, p)
    bob_secret = get_shared_secret(alice_public_key, bob_private_key, p)

    print("Publicly Shared Values:")
    print("Prime (p):", p)
    print("Base (g):", g)
    print()
    
    print("Private Keys:")
    print("Alice's Private Key:", alice_private_key)
    print("Bob's Private Key:", bob_private_key)
    print()
    
    print("Public Keys:")
    print("Alice's Public Key:", alice_public_key)
    print("Bob's Public Key:", bob_public_key)
    print()
    
    print("Shared Secrets:")
    print("Alice's Computed Shared Secret:", alice_secret)
    print("Bob's Computed Shared Secret:", bob_secret)
    
    if alice_secret == bob_secret:
        print("Key Exchange Successful: Shared Secret Matched")
    else:
        print("Key Exchange Failed: Shared Secret Mismatch")
    print()

diffie_hellman()
