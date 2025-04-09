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

def find_key(c1, c2, p1=255, p2=216, m=256):
    """Megoldja a kulcsot (a, b) az ismert bájtok alapján: c1 = a*p1 + b, c2 = a*p2 + b mod m."""
    diff_p = (p1 - p2) % m  # 255 - 216 = 39
    diff_c = (c1 - c2) % m
    
    # 'a' kiszámítása: a = (c1 - c2) * (p1 - p2)^(-1) mod m
    inv_diff_p = mod_inverse(diff_p, m)
    a = (diff_c * inv_diff_p) % m
    
    # 'b' kiszámítása: b = c1 - a*p1 mod m
    b = (c1 - a * p1) % m
    
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

# Fájl beolvasása és kulcs meghatározása
input_file = "cryptAffine"  # A titkosított kép fájlneve
output_file = "decrypted_image.jpg"  # A dekódolt kép fájlneve

with open(input_file, 'rb') as f:
    encrypted_data = f.read()
    c1 = encrypted_data[0]  # Első titkosított bájt
    c2 = encrypted_data[1]  # Második titkosított bájt

# Kulcs kiszámítása
a, b = find_key(c1, c2)
print(f"Megtalált kulcs: a = {a}, b = {b}")

# Ellenőrzés: az 'a'-nak páratlannak kell lennie (invertálható modulo 256)
if a % 2 == 0:
    print("Hiba: 'a' nem invertálható modulo 256 alatt!")
else:
    # Dekódolás
    decrypt_file(input_file, output_file, a, b)
    print(f"A kép dekódolva: {output_file}")

# Ha nincs konkrét fájl, tesztelhetjük példával
# Példa: c1 = 100, c2 = 61
# a, b = find_key(100, 61)
# print(f"Teszt kulcs: a = {a}, b = {b}")