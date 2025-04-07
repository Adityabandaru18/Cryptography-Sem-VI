a = 182841384165841685416854134135
b = 135481653441354138548413384135
m = 10**9 + 7 

if pow(b, -1, m):
    result = (a * pow(b, -1, m)) % m
    print("Modular Division Result:", result)
else:
    print("Modular inverse does not exist.")
