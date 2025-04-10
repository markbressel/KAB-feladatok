from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

def verify_chacha20_poly1305(key, nonce, ciphertext, tag):
    try:
        # ChaCha20-Poly1305 objektum létrehozása a kulccsal
        chacha = ChaCha20Poly1305(key)
        # Hitelesítés: ha a tag nem egyezik, kivételt dob
        chacha.decrypt(nonce, ciphertext + tag, None)
        return True
    except Exception:
        return False

def process_poly1305_file(filename):
    with open(filename, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    # Négyesével dolgozzuk fel a sorokat
    for i in range(0, len(lines), 4):
        if i + 3 >= len(lines):
            print(f"Hiba: Hiányos adat a {i//4 + 1}. blokkban")
            break
        
        # Adatok beolvasása hexadecimális formátumból
        key = bytes.fromhex(lines[i])
        nonce = bytes.fromhex(lines[i + 1])
        ciphertext = bytes.fromhex(lines[i + 2])
        tag = bytes.fromhex(lines[i + 3])
        
        # Ellenőrzés
        is_authentic = verify_chacha20_poly1305(key, nonce, ciphertext, tag)
        print(f"Blokk {i//4 + 1}: {'Hiteles' if is_authentic else 'Nem hiteles'}")

# Fájl feldolgozása
if __name__ == "__main__":
    filename = "lab4\Fajlok\poly1305.txt"
    process_poly1305_file(filename)