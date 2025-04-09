import sympy as sp

def hill_decrypt(ciphertext, key_inv, mod):
    """Visszafejt egy Hill-titkosított szöveget."""
    n = key_inv.rows  # Blokk méret (2)
    plaintext = ""
    
    # Szöveg páronkénti feldolgozása
    for i in range(0, len(ciphertext), n):
        block = ciphertext[i:i+n]
        # Betűk kódokká alakítása (A=0, ..., Z=25)
        c_vector = sp.Matrix([ord(c) - ord('A') for c in block])
        # Visszafejtés: P = K^-1 * C mod 26
        p_vector = (key_inv * c_vector) % mod
        # Visszaalakítás betűkké
        plaintext += ''.join(chr(int(p) + ord('A')) for p in p_vector)
    
    return plaintext

# Paraméterek
mod = 26  # Angol ábécé mérete
ciphertext = "AOGWEPOFKHSVRWYUKDAZKVYYNGYPQFKAWROZIEATIYROLMYYOSNRLIACOFJAGIUT"

# Kulcsmátrix inverze (kézzel kiszámítva)
key_inv = sp.Matrix([[24, 13], [5, 18]])

# Visszafejtés
plaintext = hill_decrypt(ciphertext, key_inv, mod)
print(f"Titkosított szöveg: {ciphertext}")
print(f"Eredeti szöveg: {plaintext}")