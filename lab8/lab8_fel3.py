#Generáljunk véletlenszerűen 2048 bites Diffie-Hellman publikus paramétert, 
# mentsük ki a generált értékeket egy állományba, majd ezeket felhasználva a Schnorr aláírási sémát alkalmazva 
# határozzuk meg egy tetszőleges bájtszekvencia digitális aláírását, 
# illetve ellenőrizzük le a létrehozott aláírást.

import os
import hashlib
from Crypto.PublicKey import DSA
from Crypto.Random import get_random_bytes
from Crypto.Util import number

# 1. Diffie-Hellman paraméterek generálása
def generate_dh_parameters(bits=2048):
    # Generálj egy prímszámot (p) és egy generátort (g) a Diffie-Hellman kulcscseréhez
    p = number.getPrime(bits)
    g = 2  # A generátor g gyakran 2 szokott lenni a Diffie-Hellman kulcscsere algoritmusokban

    # Mentsük el a paramétereket fájlba
    with open("dh_parameters.txt", "w") as f:
        f.write(f"p = {p}\n")
        f.write(f"g = {g}\n")

    return p, g

# 2. Schnorr aláírás generálása
def schnorr_sign(message, p, g, private_key):
    # A privát kulcsot szimmetrikus módon használjuk
    x = private_key  # Titkos kulcs
    h = hashlib.sha256(message.encode()).hexdigest()
    h_int = int(h, 16)

    # Lépés 1: Generálj egy véletlenszerű számot k, ami kisebb mint p-1
    k = get_random_bytes(32)
    k_int = int.from_bytes(k, byteorder="big") % (p - 1)

    # Lépés 2: Compute r = g^k mod p
    r = pow(g, k_int, p)

    # Lépés 3: Compute e = H(r || message), ahol '||' a konkatenációt jelenti
    e = int(hashlib.sha256(f"{r}{message}".encode()).hexdigest(), 16)

    # Lépés 4: Compute s = k + e * x mod (p-1)
    s = (k_int + e * x) % (p - 1)

    return (r, s)

# 3. Aláírás ellenőrzése
def schnorr_verify(message, p, g, public_key, signature):
    r, s = signature

    # Lépés 1: Compute e = H(r || message)
    e = int(hashlib.sha256(f"{r}{message}".encode()).hexdigest(), 16)

    # Lépés 2: Compute v = g^s * public_key^e mod p
    v = (pow(g, s, p) * pow(public_key, e, p)) % p

    # Lépés 3: Compare v with r
    return v == r

# 4. Kulcspár generálás (privát kulcs és publikus kulcs)
def generate_schnorr_keys(p, g):
    # A privát kulcs egy véletlenszerű szám
    private_key = int.from_bytes(get_random_bytes(32), byteorder="big") % (p - 1)
    
    # A publikus kulcs: public_key = g^private_key mod p
    public_key = pow(g, private_key, p)
    
    return private_key, public_key

# Fő program
if __name__ == "__main__":
    # 1. Diffie-Hellman paraméterek generálása
    p, g = generate_dh_parameters()

    # 2. Schnorr kulcspár generálása
    private_key, public_key = generate_schnorr_keys(p, g)
    print(f"Privát kulcs: {private_key}")
    print(f"Publikus kulcs: {public_key}")

    # 3. Aláírás generálása egy tetszőleges bájtszekvenciához
    message = "Ez egy tetszőleges bájtszekvencia"
    signature = schnorr_sign(message, p, g, private_key)
    print(f"Aláírás: {signature}")

    # 4. Aláírás ellenőrzése
    is_valid = schnorr_verify(message, p, g, public_key, signature)
    print(f"Aláírás érvényes: {is_valid}")
