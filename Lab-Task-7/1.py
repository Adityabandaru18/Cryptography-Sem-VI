import hashlib

def sha512_hash(text):
    text = text.encode('utf-8') 
    hashobj = hashlib.sha512(text)  
    hashhex = hashobj.hexdigest()  
    return hashhex

if __name__ == "__main__":
    txt = input("Enter text to hash: ")
    res = sha512_hash(txt)
    print(f"SHA-512 Hash: {res}")
