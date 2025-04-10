import os
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import base64

def generate_key():
    """Generál egy véletlenszerű kulcsot és elmenti base64 formátumban"""
    key = ChaCha20Poly1305.generate_key()
    with open("chacha20_key.txt", "wb") as key_file:
        key_file.write(base64.b64encode(key))
    return key

def encrypt_file(input_file, output_file):
    """Titkosít egy fájlt ChaCha20-Poly1305 algoritmussal"""
    key = generate_key()
    nonce = os.urandom(12)  # ChaCha20-Poly1305 96 bites nonce-ot használ
    
    chacha = ChaCha20Poly1305(key)
    
    with open(input_file, "rb") as f_in, open(output_file, "wb") as f_out:
        # Nonce írása a fájl elejére
        f_out.write(nonce)
        
        # Adatok titkosítása 64KB-os blokkokban
        chunk_size = 64 * 1024
        while True:
            chunk = f_in.read(chunk_size)
            if not chunk:
                break
            encrypted_chunk = chacha.encrypt(nonce, chunk, None)
            f_out.write(encrypted_chunk)
        
        # Hitelesítő tag generálása és hozzáfűzése
        # (A Poly1305 automatikusan hozzáadja a tag-et az encrypt során)

def decrypt_file(input_file, output_file):
    """Visszafejt egy fájlt és ellenőrzi az integritást"""
    with open("chacha20_key.txt", "rb") as key_file:
        key = base64.b64decode(key_file.read())
    
    chacha = ChaCha20Poly1305(key)
    
    with open(input_file, "rb") as f_in, open(output_file, "wb") as f_out:
        # Nonce kiolvasása a fájl elejéről
        nonce = f_in.read(12)
        
        # Adatok visszafejtése 64KB + 16 byte-os blokkokban (16 a Poly1305 tag)
        chunk_size = 64 * 1024 + 16
        while True:
            chunk = f_in.read(chunk_size)
            if not chunk:
                break
            try:
                decrypted_chunk = chacha.decrypt(nonce, chunk, None)
                f_out.write(decrypted_chunk)
            except Exception as e:
                print("Hiba: Az állomány sérült vagy módosult!")
                os.remove(output_file)
                return False
    
    print("Visszafejtés sikeres, az állomány integritása megmaradt.")
    return True

# Példa használat
input_filename = "eredeti.bin"
encrypted_filename = "titkositott.bin"
decrypted_filename = "visszafejtett.bin"

# Titkosítás
encrypt_file(input_filename, encrypted_filename)

# Visszafejtés
decrypt_file(encrypted_filename, decrypted_filename)