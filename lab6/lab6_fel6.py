import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
import base64

def generate_key():
    """Generál egy véletlenszerű 256 bites AES kulcsot és elmenti base64-ként"""
    key = os.urandom(32)  # AES-256
    with open('aes_key.txt', 'wb') as f:
        f.write(base64.b64encode(key))
    return key

def encrypt_file(input_file, output_file, key):
    """Titkosítja a fájlt AES-GCM módban, nonce az elején, tag a végén"""
    nonce = os.urandom(12)  # GCM-hez ajánlott 12 byte nonce
    
    # Inicializáljuk az encryptort
    cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    
    with open(input_file, 'rb') as fin, open(output_file, 'wb') as fout:
        # Nonce írása a fájl elejére
        fout.write(nonce)
        
        # Adatok titkosítása darabonként
        chunk_size = 64 * 1024  # 64KB
        while True:
            chunk = fin.read(chunk_size)
            if not chunk:
                break
            encrypted_chunk = encryptor.update(chunk)
            fout.write(encrypted_chunk)
        
        # Titkosítás befejezése és tag lekérése
        encryptor.finalize()
        tag = encryptor.tag
        
        # Tag írása a fájl végére
        fout.write(tag)

def decrypt_file(input_file, output_file, key):
    """Visszafejti a fájlt és ellenőrzi a tag-et"""
    with open(input_file, 'rb') as fin, open(output_file, 'wb') as fout:
        # Nonce kiolvasása a fájl elejéről
        nonce = fin.read(12)
        
        # Tag meghatározása - az utolsó 16 byte
        fin.seek(0, 2)  # Ugrás a fájl végére
        file_size = fin.tell()
        tag_position = file_size - 16
        fin.seek(tag_position)
        tag = fin.read(16)
        
        # Vissza az adatokhoz (nonce után)
        fin.seek(12)
        
        # Inicializáljuk a decryptort
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        
        # Adatok visszafejtése darabonként
        chunk_size = 64 * 1024  # 64KB
        remaining = tag_position - 12  # Nonce után kezdődik, tag előtt végződik
        
        while remaining > 0:
            read_size = min(chunk_size, remaining)
            chunk = fin.read(read_size)
            if not chunk:
                break
            decrypted_chunk = decryptor.update(chunk)
            fout.write(decrypted_chunk)
            remaining -= len(chunk)
        
        # Visszafejtés befejezése és tag ellenőrzése
        try:
            decryptor.finalize()
            print("A fájl hitelesítése sikeres, nem módosították.")
        except Exception as e:
            print("Hiba: A fájl hitelesítése sikertelen!", str(e))
            os.remove(output_file)  # Töröljük a részlegesen létrejött fájlt
            raise

# Példa használat
if __name__ == "__main__":
    # Kulcs generálása és mentése
    key = generate_key()
    
    # Titkosítás
    encrypt_file("input.bin", "encrypted.bin", key)
    print("Titkosítás kész.")
    
    # Visszafejtés
    decrypt_file("encrypted.bin", "decrypted.bin", key)
    print("Visszafejtés kész.")