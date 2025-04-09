import math
import random
import sympy as sp

def keyGen(n, MOD):
    """Generál egy n x n-es kulcsmátrixot és annak inverzét modulo MOD alatt."""
    while True:
        # Új n x n-es mátrix generálása
        key = sp.Matrix([[random.randint(0, MOD-1) for _ in range(n)] for _ in range(n)])
        det = key.det() % MOD
        # Ellenőrzi, hogy a determináns és a MOD kölcsönösen prímek
        if math.gcd(det, MOD) == 1:  # Ellenőrzi, hogy invertálható-e
            try:
                keyInv = key.inv_mod(MOD)
                return key, keyInv
            except sp.polys.polyerrors.NotInvertible:
                # Ha nem invertálható, próbálkozz új kulcsmátrix generálásával
                continue

def text_to_vector(text, n, MOD):
    """Szöveget n-es vektorokká alakít."""
    vectors = []
    for i in range(0, len(text), n):
        block = text[i:i+n]
        # Ha az utolsó blokk rövidebb, padding 0-val
        if len(block) < n:
            block += b'\x00' * (n - len(block))
        vector = sp.Matrix([int(b) for b in block])
        vectors.append(vector)
    return vectors

def vector_to_text(vectors, MOD):
    """Vektorokból szöveget állít elő."""
    text = bytearray()
    for v in vectors:
        for i in range(v.rows):
            text.append(v[i] % MOD)
    return bytes(text)

def encrypt_file(input_path, output_path, key, n, MOD):
    """Titkosít egy fájlt Hill-módszerrel."""
    with open(input_path, 'rb') as f:
        plaintext = f.read()
    
    # Szöveg vektorokká alakítása
    plain_vectors = text_to_vector(plaintext, n, MOD)
    
    # Titkosítás
    encrypted_vectors = [(key * pv) % MOD for pv in plain_vectors]
    
    # Visszaalakítás bájtokká
    ciphertext = vector_to_text(encrypted_vectors, MOD)
    
    with open(output_path, 'wb') as f:
        f.write(ciphertext)

def decrypt_file(input_path, output_path, key_inv, n, MOD):
    """Visszafejt egy titkosított fájlt Hill-módszerrel."""
    with open(input_path, 'rb') as f:
        ciphertext = f.read()
    
    # Szöveg vektorokká alakítása
    cipher_vectors = text_to_vector(ciphertext, n, MOD)
    
    # Visszafejtés
    decrypted_vectors = [(key_inv * cv) % MOD for cv in cipher_vectors]
    
    # Visszaalakítás bájtokká
    plaintext = vector_to_text(decrypted_vectors, MOD)
    
    # Padding eltávolítása
    plaintext = plaintext.rstrip(b'\x00')
    
    with open(output_path, 'wb') as f:
        f.write(plaintext)

# Paraméterek
n = 5      # Mátrix méret
MOD = 128  # Modulo (ASCII vagy bájt alapú)

# Kulcs generálása
key, keyInv = keyGen(n, MOD)
print("Kulcsmátrix:")
print(key)
print("Inverz kulcsmátrix:")
print(keyInv)
print("Ellenőrzés (K * K^-1 mod 128):")
print((key * keyInv) % MOD)

# Fájlok titkosítása és visszafejtése
input_file = "input.txt"         # Bemeneti fájl
encrypted_file = "encrypted.txt" # Titkosított fájl
decrypted_file = "decrypted.txt" # Visszafejtett fájl

# Példa szöveg létrehozása, ha nincs bemeneti fájl
with open(input_file, 'wb') as f:
    f.write(b"Hello, this is a test message for Hill cipher!")

# Titkosítás
encrypt_file(input_file, encrypted_file, key, n, MOD)
print(f"Titkosított fájl létrehozva: {encrypted_file}")

# Visszafejtés
decrypt_file(encrypted_file, decrypted_file, keyInv, n, MOD)
print(f"Visszafejtett fájl létrehozva: {decrypted_file}")

# Ellenőrzés
with open(input_file, 'rb') as f:
    original = f.read()
with open(decrypted_file, 'rb') as f:
    decrypted = f.read()
print(f"Eredeti szöveg: {original}")
print(f"Visszafejtett szöveg: {decrypted}")
print(f"Ellenőrzés sikeres: {original == decrypted}")
