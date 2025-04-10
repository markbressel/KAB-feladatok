import struct

# TEA dekódolás egy 64 bites blokkon (ECB mód)
def tea_decrypt_block(ciphertext, key):
    v0, v1 = struct.unpack('>II', ciphertext)  # 2×32 bitre bontás
    k0, k1, k2, k3 = key
    delta = 0x9e3779b9
    sum = 0xC6EF3720  # 32 * delta
    
    for _ in range(32):  # 32 ciklus
        v1 -= ((v0 << 4) + k2) ^ (v0 + sum) ^ ((v0 >> 5) + k3)
        v1 &= 0xFFFFFFFF
        v0 -= ((v1 << 4) + k0) ^ (v1 + sum) ^ ((v1 >> 5) + k1)
        v0 &= 0xFFFFFFFF
        sum -= delta
    
    return struct.pack('>II', v0, v1)

# TEA kódolás egy 64 bites blokkon (CBC módhoz)
def tea_encrypt_block(plaintext, key):
    v0, v1 = struct.unpack('>II', plaintext)
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

# ECB visszafejtés
def decrypt_tea_ecb(ciphertext, key):
    decrypted = bytearray()
    for i in range(0, len(ciphertext), 8):
        block = ciphertext[i:i+8]
        if len(block) == 8:  # Csak teljes 64 bites blokkokat dolgozunk fel
            decrypted.extend(tea_decrypt_block(block, key))
        else:
            decrypted.extend(block)  # Padding vagy maradék
    return bytes(decrypted)

# CBC titkosítás
def encrypt_tea_cbc(plaintext, key, iv):
    encrypted = bytearray()
    prev_block = iv  # Inicializációs vektor
    
    for i in range(0, len(plaintext), 8):
        block = plaintext[i:i+8]
        if len(block) < 8:
            block = block.ljust(8, b'\x00')  # Padding nullákkal
        # XOR az előző blokkal (vagy IV-vel az első blokk esetén)
        block = bytes(a ^ b for a, b in zip(block, prev_block))
        encrypted_block = tea_encrypt_block(block, key)
        encrypted.extend(encrypted_block)
        prev_block = encrypted_block
    
    return bytes(encrypted)

# Fő program
if __name__ == "__main__":
    # Kulcs definiálása
    key = (0x0123, 0x4567, 0x89ab, 0xcdef)
    
    # Titkosított fájl beolvasása
    with open('lab5\Fajlok\crypt.bmp', 'rb') as f:
        encrypted_data = f.read()
    
    # Az első 80 bájt nem titkosított
    header = encrypted_data[:80]
    encrypted_body = encrypted_data[80:]
    
    # ECB visszafejtés
    decrypted_body = decrypt_tea_ecb(encrypted_body, key)
    decrypted_data = header + decrypted_body
    
    # Visszafejtett fájl mentése
    with open('lab5\Fajlok\decrypted.bmp', 'wb') as f:
        f.write(decrypted_data)
    
    # CBC titkosítás inicializációs vektorral (pl. 8 nullás bájt)
    iv = b'\x00' * 8
    cbc_encrypted_body = encrypt_tea_cbc(decrypted_body, key, iv)
    cbc_encrypted_data = header + cbc_encrypted_body
    
    # CBC titkosított fájl mentése
    with open('lab5\Fajlok\cbc_encrypted.bmp', 'wb') as f:
        f.write(cbc_encrypted_data)
    
    print("Visszafejtés és CBC titkosítás kész.")