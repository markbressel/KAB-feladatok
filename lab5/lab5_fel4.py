def mod_inverse(a, m):
    """Moduláris inverz kiszámítása"""
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Nincs moduláris inverz")
    return (x % m + m) % m

def affine_decrypt(cipher_byte, a_inv, b, m=256):
    """Affin visszafejtés egy bájtra: P = a_inv * (C - b) mod 256"""
    return (a_inv * (cipher_byte - b)) % m

def decrypt_cbc_affine(ciphertext, iv, a, b):
    """CBC módú affin titkosítás visszafejtése"""
    a_inv = mod_inverse(a, 256)  # a inverze mod 256
    plaintext = bytearray()
    prev_block = iv  # Az első blokkhoz az IV-t használjuk
    
    for i in range(0, len(ciphertext)):
        cipher_byte = ciphertext[i]
        # Visszafejtés: P = a_inv * (C - b) mod 256, majd XOR az előző blokkal
        decrypted_byte = affine_decrypt(cipher_byte, a_inv, b)
        plain_byte = decrypted_byte ^ prev_block
        plaintext.append(plain_byte)
        # Az előző blokk a titkosított bájt (CBC mód)
        prev_block = cipher_byte
    
    return bytes(plaintext)

# Fő program
if __name__ == "__main__":
    # Adatok
    iv = 19
    a, b = 157, 45  # Kulcs: (a, b)
    input_file = "lab5\Fajlok\cryptAffine256_Tanacs"
    output_file = "lab5\Fajlok\decrypted.jpg"
    
    # Titkosított fájl beolvasása
    with open(input_file, 'rb') as f:
        ciphertext = f.read()
    
    # Visszafejtés
    plaintext = decrypt_cbc_affine(ciphertext, iv, a, b)
    
    # Visszafejtett fájl mentése
    with open(output_file, 'wb') as f:
        f.write(plaintext)
    
    print("A visszafejtett JPG fájl mentve: decrypted.jpg")