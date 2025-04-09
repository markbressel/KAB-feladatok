def mod_inverse(a, m):
    """Számít az 'a' moduláris inverzét 'm' alatt az extenedált Euklideszi algoritmus segítségével."""
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"{a} nem invertálható modulo {m} alatt")
    return (x % m + m) % m

def find_key(p1, c1, p2, c2, m=256):
    """Megoldja a kulcsot (a, b) az ismert párok alapján: c1 = a*p1 + b, c2 = a*p2 + b mod m."""
    # c2 = b mod m, mert p2 = 0
    b = c2
    
    # c1 = a*p1 + b mod m
    # a*p1 = c1 - b mod m
    diff = (c1 - b) % m
    inv_p1 = mod_inverse(p1, m)
    a = (diff * inv_p1) % m
    
    return a, b

def decrypt_file(input_path, output_path, a, b, m=256):
    """Dekódol egy titkosított fájlt az affin titkosításból."""
    a_inv = mod_inverse(a, m)
    
    with open(input_path, 'rb') as f_in:
        ciphertext = f_in.read()
    
    plaintext = bytearray()
    for c in ciphertext:
        p = (a_inv * (c - b)) % m
        plaintext.append(p)
    
    with open(output_path, 'wb') as f_out:
        f_out.write(plaintext)

# Ismert párok
p1, c1 = 255, 48  # 0xFF -> 0x30
p2, c2 = 0, 119   # 0x00 -> 0x77

# Kulcs kiszámítása
a, b = find_key(p1, c1, p2, c2)
print(f"Megtalált kulcs: a = {a}, b = {b}")

# Ellenőrzés: az 'a'-nak páratlannak kell lennie (invertálható modulo 256)
if a % 2 == 0:
    print("Hiba: 'a' nem invertálható modulo 256 alatt!")
else:
    # Fájl beolvasása és dekódolása
    input_file = "cryptAffin3"  # A titkosított kép fájlneve
    output_file = "decrypted_image2.jpg"  # A dekódolt kép fájlneve
    
    decrypt_file(input_file, output_file, a, b)
    print(f"A kép dekódolva: {output_file}")
    
    # Ellenőrzés: az első néhány bájt (BMP kezdete: 0x42, 0x4D)
    with open(output_file, 'rb') as f:
        decrypted_data = f.read()
        print(f"Dekódolt első két bájt: {hex(decrypted_data[0])}, {hex(decrypted_data[1])}")