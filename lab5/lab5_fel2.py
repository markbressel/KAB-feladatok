from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def encrypt_file(input_file, output_file, key, iv_or_nonce, algorithm, mode):
    with open(input_file, 'rb') as f:
        plaintext = f.read()
    
    # Cipher objektum létrehozása
    cipher = Cipher(algorithm, mode(iv_or_nonce), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Padding hozzáadása, ha szükséges (CBC módhoz)
    if isinstance(mode, type(modes.CBC)):
        padding_length = 8 - (len(plaintext) % 8) if algorithm == algorithms.TripleDES else 16 - (len(plaintext) % 16)
        plaintext += bytes([padding_length]) * padding_length
    
    # Titkosítás
    ciphertext = encryptor.update(plaintext) + encryptor.finalize()
    
    # Mentés fájlba (IV/nonce + titkosított adat)
    with open(output_file, 'wb') as f:
        f.write(iv_or_nonce + ciphertext)

def decrypt_file(input_file, output_file, key, algorithm, mode):
    with open(input_file, 'rb') as f:
        data = f.read()
    
    # IV vagy nonce kivétele az elejéről
    iv_or_nonce_length = 8 if algorithm == algorithms.TripleDES else 16
    iv_or_nonce = data[:iv_or_nonce_length]
    ciphertext = data[iv_or_nonce_length:]
    
    # Cipher objektum létrehozása
    cipher = Cipher(algorithm, mode(iv_or_nonce), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Visszafejtés
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    
    # Padding eltávolítása, ha szükséges (CBC módhoz)
    if isinstance(mode, type(modes.CBC)):
        padding_length = plaintext[-1]
        plaintext = plaintext[:-padding_length]
    
    # Mentés fájlba
    with open(output_file, 'wb') as f:
        f.write(plaintext)

# Tesztelés
if __name__ == "__main__":
    input_file = "lab5\Fajlok\cryptOTP"
    
    # Kulcsok és IV/nonce generálása
    des3_key = os.urandom(24)  # 192 bit (24 bájt) DES3-hoz
    aes_key = os.urandom(32)   # 256 bit AES-hez
    iv = os.urandom(8)        # DES3 CBC-hez (8 bájt)
    nonce = os.urandom(8)     # DES3 CTR-hez (8 bájt)
    aes_iv = os.urandom(16)   # AES CBC-hez (16 bájt)
    aes_nonce = os.urandom(8) # AES CTR-hez (8 bájt)
    
    # Módok definiálása
    modes_list = [
        ("DES3-CBC", algorithms.TripleDES(des3_key), modes.CBC, iv, "des3_cbc_encrypted.bin", "des3_cbc_decrypted.bin"),
        ("DES3-CTR", algorithms.TripleDES(des3_key), modes.CTR, nonce, "des3_ctr_encrypted.bin", "des3_ctr_decrypted.bin"),
        ("AES-CBC", algorithms.AES(aes_key), modes.CBC, aes_iv, "aes_cbc_encrypted.bin", "aes_cbc_decrypted.bin"),
        ("AES-CTR", algorithms.AES(aes_key), modes.CTR, aes_nonce, "aes_ctr_encrypted.bin", "aes_ctr_decrypted.bin")
    ]
    
    for mode_name, algo, mode_type, iv_or_nonce, enc_file, dec_file in modes_list:
        print(f"{mode_name} titkosítás...")
        encrypt_file(input_file, enc_file, algo.key, iv_or_nonce, algo, mode_type)
        print(f"{mode_name} visszafejtés...")
        decrypt_file(enc_file, dec_file, algo.key, algo, mode_type)
        print(f"{mode_name} kész.")
