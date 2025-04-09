import string

def preprocess_text(text):
    """Szöveg előfeldolgozása: nagybetűsítés és csak angol ábécé megtartása."""
    return ''.join(c for c in text.upper() if c in string.ascii_uppercase)

def char_to_num(char):
    """Betű átalakítása számkóddá (A=0, B=1, ..., Z=25)."""
    return ord(char) - ord('A')

def num_to_char(num):
    """Számkód átalakítása betűvé (0=A, 1=B, ..., 25=Z)."""
    return chr(num + ord('A'))

def gcd(a, b):
    """Legnagyobb közös osztó kiszámítása."""
    while b:
        a, b = b, a % b
    return a

def extended_gcd(a, b):
    """Kiterjesztett Eukleidészi algoritmus: ax + by = gcd(a, b)."""
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y

def mod_inverse(a, m):
    """Multiplikatív inverz kiszámítása modulo m szerint."""
    g, x, _ = extended_gcd(a, m)
    if g != 1:
        raise ValueError("Nincs multiplikatív inverz, mert a és m nem relatív prímek.")
    return x % m

def affine_encrypt(text, a, b):
    """Affin titkosítás: E(x) = (a * x + b) mod 26."""
    if gcd(a, 26) != 1:
        raise ValueError("Az 'a' paraméternek relatív prímnek kell lennie 26-tal.")
    processed_text = preprocess_text(text)
    encrypted = ""
    for char in processed_text:
        x = char_to_num(char)
        encrypted_char = num_to_char((a * x + b) % 26)
        encrypted += encrypted_char
    return encrypted

def affine_decrypt(ciphertext, a, b):
    """Affin visszafejtés: D(y) = a_inv * (y - b) mod 26."""
    if gcd(a, 26) != 1:
        raise ValueError("Az 'a' paraméternek relatív prímnek kell lennie 26-tal.")
    a_inv = mod_inverse(a, 26)
    decrypted = ""
    for char in ciphertext:
        y = char_to_num(char)
        decrypted_char = num_to_char((a_inv * (y - b)) % 26)
        decrypted += decrypted_char
    return decrypted

def main():
    # Fájlnevek és kulcsok
    input_file = "input.txt"
    encrypted_file = "encrypted.txt"
    decrypted_file = "decrypted.txt"
    a, b = 5, 8  # Példa kulcsok (a relatív prím 26-tal)

    # Szöveg beolvasása fájlból
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            original_text = f.read()
    except FileNotFoundError:
        print(f"Hiba: A {input_file} fájl nem található!")
        return

    # Titkosítás
    try:
        encrypted_text = affine_encrypt(original_text, a, b)
        with open(encrypted_file, 'w', encoding='utf-8') as f:
            f.write(encrypted_text)
        print(f"Titkosított szöveg mentve a {encrypted_file} fájlba.")
    except ValueError as e:
        print(f"Titkosítási hiba: {e}")
        return

    # Visszafejtés
    try:
        decrypted_text = affine_decrypt(encrypted_text, a, b)
        with open(decrypted_file, 'w', encoding='utf-8') as f:
            f.write(decrypted_text)
        print(f"Visszafejtett szöveg mentve a {decrypted_file} fájlba.")
    except ValueError as e:
        print(f"Visszafejtési hiba: {e}")
        return

    # Ellenőrzés a konzolon
    print(f"\nEredeti szöveg (előfeldolgozva): {preprocess_text(original_text)}")
    print(f"Titkosított szöveg: {encrypted_text}")
    print(f"Visszafejtett szöveg: {decrypted_text}")

if __name__ == "__main__":
    main()