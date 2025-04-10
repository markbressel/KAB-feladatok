#Generáljunk véletlenszerűen egy 2048 bites RSA kulcspárt, a kulcsokat mentsük ki egy-egy állományba, 
# majd ezeket a kulcsot felhasználva határozzuk meg egy tetszőleges bináris állomány digitális aláírását 
# valamely RSA aláírási sémát alkalmazva, illetve ellenőrizzük le a létrehozott aláírást.

from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes

# 1. RSA kulcspár generálása és fájlba mentés
def generate_rsa_key_pair(bits=2048):
    key = RSA.generate(bits)
    
    # Kulcsok mentése fájlba
    with open("private_key.pem", "wb") as f:
        f.write(key.export_key('PEM'))
        
    with open("public_key.pem", "wb") as f:
        f.write(key.publickey().export_key('PEM'))
    
    return key

# 2. Aláírás létrehozása
def sign_file(file_path, private_key):
    # Fájl olvasása
    with open(file_path, 'rb') as f:
        file_data = f.read()
    
    # A fájl hash értéke (SHA256)
    hash_object = SHA256.new(file_data)
    
    # RSA aláírás generálása
    signer = pkcs1_15.new(private_key)
    signature = signer.sign(hash_object)
    
    return signature

# 3. Aláírás ellenőrzése
def verify_signature(file_path, signature, public_key):
    # Fájl olvasása
    with open(file_path, 'rb') as f:
        file_data = f.read()
    
    # A fájl hash értéke (SHA256)
    hash_object = SHA256.new(file_data)
    
    # Aláírás ellenőrzése
    verifier = pkcs1_15.new(public_key)
    try:
        verifier.verify(hash_object, signature)
        print("Aláírás érvényes!")
    except (ValueError, TypeError):
        print("Aláírás érvénytelen!")

# Fő program
if __name__ == "__main__":
    # 1. RSA kulcspár generálása
    key = generate_rsa_key_pair()

    # 2. Fájl aláírása
    file_path = 'input_file.bin'  # Tetszőleges bináris fájl
    signature = sign_file(file_path, key)

    # 3. Aláírás ellenőrzése
    public_key = RSA.import_key(open('public_key.pem').read())
    verify_signature(file_path, signature, public_key)
