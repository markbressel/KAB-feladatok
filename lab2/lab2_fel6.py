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

# Paraméterek
input_file = "cryptAffinPA"  # A titkosított kép fájlneve
output_file = "decrypted_image.jpg"  # A dekódolt kép fájlneve
a = 113  # Kulcs: a
b = 223  # Kulcs: b
m = 256  # Modulo

# Kulcs ellenőrzése és dekódolás
print(f"Kulcs: a = {a}, b = {b}")
a_inv = mod_inverse(a, m)
print(f"a inverze modulo {m}: {a_inv}")

# Dekódolás
decrypt_file(input_file, output_file, a, b)
print(f"A kép dekódolva: {output_file}")

# Ellenőrzés: az első két bájt visszafejtése (JPG: 0xFF, 0xD8)
with open(output_file, 'rb') as f:
    decrypted_data = f.read()
    print(f"Dekódolt első két bájt: {hex(decrypted_data[0])}, {hex(decrypted_data[1])}")