from tinyec import registry
import secrets

def mod_inverse(a, p):
    for i in range(1, p):
        if (a * i) % p == 1:
            return i
    return None

def add_points(x1, y1, x2, y2, a, p):
    if x1 == 0 and y1 == 0:
        return x2, y2
    if x2 == 0 and y2 == 0:
        return x1, y1
    if x1 == x2 and y1 != y2:
        return 0, 0
    
    if x1 == x2:
        slope = ((3 * x1 * x1 + a) * mod_inverse(2 * y1, p)) % p
    else:
        slope = ((y2 - y1) * mod_inverse(x2 - x1, p)) % p
    
    x3 = (slope * slope - x1 - x2) % p
    y3 = (slope * (x1 - x3) - y1) % p
    
    return x3, y3

def multiply_point(x, y, k, a, p):
    result_x, result_y = 0, 0
    temp_x, temp_y = x, y
    
    while k:
        if k & 1:
            result_x, result_y = add_points(result_x, result_y, temp_x, temp_y, a, p)
        temp_x, temp_y = add_points(temp_x, temp_y, temp_x, temp_y, a, p)
        k >>= 1
    
    return result_x, result_y

def key_exchange():
    p = 17 
    a = 2   
    b = 3   
    gx, gy = 1, 6 
    
   
    alice_private = 5
    bob_private = 7
    
    
    alice_pub_x, alice_pub_y = multiply_point(gx, gy, alice_private, a, p)
    bob_pub_x, bob_pub_y = multiply_point(gx, gy, bob_private, a, p)
    
    
    alice_shared_x, alice_shared_y = multiply_point(bob_pub_x, bob_pub_y, alice_private, a, p)
    bob_shared_x, bob_shared_y = multiply_point(alice_pub_x, alice_pub_y, bob_private, a, p)
    
   
    print("Curve: y² = x³ + 2x + 3 over F_17")
    print("\nAlice's Private Key:", alice_private)
    print("Bob's Private Key:", bob_private)
    print("\nAlice's Public Key Point:", (alice_pub_x, alice_pub_y))
    print("Bob's Public Key Point:", (bob_pub_x, bob_pub_y))
    print("\nAlice's Shared Key Point:", (alice_shared_x, alice_shared_y))
    print("Bob's Shared Key Point:", (bob_shared_x, bob_shared_y))
    
    
    if alice_shared_x == bob_shared_x and alice_shared_y == bob_shared_y:
        print("\nKey exchange successful!")
    else:
        print("\nKey exchange failed! Keys do not match.")

if __name__ == "__main__":
    print("Performing Simple ECC Key Exchange...")
    key_exchange()
 