import os
import struct
from random import randint

# TEA titkosító blokk (64 bit)
def tea_encrypt_block(plaintext, key):
    v0, v1 = struct.unpack('>II', plaintext)  # 2×32 bit
    k0, k1, k2, k3 = key
    delta = 0x9e3779b9
    sum = 0
    
    for _ in range(32):
        sum = (sum + delta) & 0xFFFFFFFF
        v0 += ((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1)
        v0 &= 0xFFFFFFFF
        v1 += ((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3)
        v1 &= 0xFFFFFFFF
    
    return struct.pack('>II', v0, v1)

# TEA visszafejtő blokk (64 bit)
def tea_decrypt_block(ciphertext, key):
    v0, v1 = struct.unpack('>II', ciphertext)
    k0, k1, k2, k3 = key
    delta = 0x9e3779b9
    sum = 0xC6EF3720  # 32 * delta
    
    for _ in range(32):
        v1 -= ((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3)
        v1 &= 0xFFFFFFFF
        v0 -= ((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1)
        v0 &= 0xFFFFFFFF
        sum -= delta
    
    return struct.pack('>II', v0, v1)

# TEA-CBC titkosítás
def tea_cbc_encrypt(plaintext, key, iv):
    encrypted = bytearray()
    prev_block = iv
    
    # Padding hozzáadása (PKCS#5/PKCS#7 stílus)
    padding_length = 8 - (len(plaintext) % 8)
    plaintext += bytes([padding_length]) * padding_length
    
    for i in range(0, len(plaintext), 8):
        block = plaintext[i:i+8]
        # XOR az előző blokkal (vagy IV-vel)
        block = bytes(a ^ b for a, b in zip(block, prev_block))
        encrypted_block = tea_encrypt_block(block, key)
        encrypted.extend(encrypted_block)
        prev_block = encrypted_block
    
    return bytes(encrypted)

# TEA-CBC visszafejtés
def tea_cbc_decrypt(ciphertext, key, iv):
    decrypted = bytearray()
    prev_block = iv
    
    for i in range(0, len(ciphertext), 8):
        block = ciphertext[i:i+8]
        decrypted_block = tea_decrypt_block(block, key)
        # XOR az előző titkosított blokkal (vagy IV-vel)
        decrypted.extend(bytes(a ^ b for a, b in zip(decrypted_block, prev_block)))
        prev_block = block
    
    # Padding eltávolítása
    padding_length = decrypted[-1]
    return bytes(decrypted[:-padding_length])

# TEA-CTR titkosítás/visszafejtés (ugyanaz, mert szimmetrikus)
def tea_ctr_encrypt_decrypt(data, key, nonce):
    result = bytearray()
    counter = 0
    
    for i in range(0, len(data), 8):
        # Nonce + számláló (64 bit)
        counter_block = nonce[:4] + struct.pack('>I', counter)
        encrypted_counter = tea_encrypt_block(counter_block, key)
        
        block = data[i:i+8]
        # XOR a kulcsfolyammal
        result.extend(bytes(a ^ b for a, b in zip(block, encrypted_counter[:len(block)])))
        counter += 1
    
    return bytes(result)

# Fő program
if __name__ == "__main__":
    input_file = "lab5\Fajlok\cryptOTP"
    
    # Véletlenszerű 128 bites kulcs generálása (4×32 bit)
    key = (
        randint(0, 0xFFFF),  # k0
        randint(0, 0xFFFF),  # k1
        randint(0, 0xFFFF),  # k2
        randint(0, 0xFFFF)   # k3
    )
    
    # Véletlenszerű IV (CBC-hez) és nonce (CTR-hez)
    iv = os.urandom(8)    # 64 bit
    nonce = os.urandom(4) # 32 bit (a másik 32 bit a számlálóé)
    
    # Eredeti fájl beolvasása
    with open(input_file, 'rb') as f:
        plaintext = f.read()
    
    # TEA-CBC titkosítás
    cbc_ciphertext = tea_cbc_encrypt(plaintext, key, iv)
    with open("lab5\Fajlok\tea_cbc_encrypted.bin", 'wb') as f:
        f.write(iv + cbc_ciphertext)
    
    # TEA-CBC visszafejtés
    with open("lab5\Fajlok\tea_cbc_encrypted.bin", 'rb') as f:
        data = f.read()
        iv, cbc_ciphertext = data[:8], data[8:]
    cbc_decrypted = tea_cbc_decrypt(cbc_ciphertext, key, iv)
    with open("tea_cbc_decrypted.bin", 'wb') as f:
        f.write(cbc_decrypted)
    
    # TEA-CTR titkosítás
    ctr_ciphertext = tea_ctr_encrypt_decrypt(plaintext, key, nonce)
    with open("lab5\Fajlok\tea_ctr_encrypted.bin", 'wb') as f:
        f.write(nonce + ctr_ciphertext)
    
    # TEA-CTR visszafejtés
    with open("lab5\Fajlok\tea_ctr_encrypted.bin", 'rb') as f:
        data = f.read()
        nonce, ctr_ciphertext = data[:4], data[4:]
    ctr_decrypted = tea_ctr_encrypt_decrypt(ctr_ciphertext, key, nonce)
    with open("tea_ctr_decrypted.bin", 'wb') as f:
        f.write(ctr_decrypted)
    
    print("TEA-CBC és TEA-CTR titkosítás/visszafejtés kész.")