import os
import struct

BLOCK_SIZE = 8  # 64 bit

# TEA algoritmus - alapértelmezett 64 kör
def tea_encrypt_block(v, key, rounds=32):
    v0, v1 = struct.unpack(">2I", v)
    k = struct.unpack(">4I", key)
    delta = 0x9E3779B9
    sum = 0
    for _ in range(rounds):
        sum = (sum + delta) & 0xFFFFFFFF
        v0 = (v0 + (((v1 << 4) + k[0]) ^ (v1 + sum) ^ ((v1 >> 5) + k[1]))) & 0xFFFFFFFF
        v1 = (v1 + (((v0 << 4) + k[2]) ^ (v0 + sum) ^ ((v0 >> 5) + k[3]))) & 0xFFFFFFFF
    return struct.pack(">2I", v0, v1)

def tea_decrypt_block(v, key, rounds=32):
    v0, v1 = struct.unpack(">2I", v)
    k = struct.unpack(">4I", key)
    delta = 0x9E3779B9
    sum = (delta * rounds) & 0xFFFFFFFF
    for _ in range(rounds):
        v1 = (v1 - (((v0 << 4) + k[2]) ^ (v0 + sum) ^ ((v0 >> 5) + k[3]))) & 0xFFFFFFFF
        v0 = (v0 - (((v1 << 4) + k[0]) ^ (v1 + sum) ^ ((v1 >> 5) + k[1]))) & 0xFFFFFFFF
        sum = (sum - delta) & 0xFFFFFFFF
    return struct.pack(">2I", v0, v1)

# PKCS5 padding
def pad(data):
    pad_len = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + bytes([pad_len]) * pad_len

def unpad(data):
    pad_len = data[-1]
    return data[:-pad_len]

# CBC mód kézi megvalósítása
def encrypt_cbc(plaintext, key, iv):
    plaintext = pad(plaintext)
    blocks = [plaintext[i:i+BLOCK_SIZE] for i in range(0, len(plaintext), BLOCK_SIZE)]
    encrypted = b''
    prev = iv
    for block in blocks:
        xor_block = bytes(a ^ b for a, b in zip(block, prev))
        enc_block = tea_encrypt_block(xor_block, key)
        encrypted += enc_block
        prev = enc_block
    return encrypted

def decrypt_cbc(ciphertext, key, iv):
    blocks = [ciphertext[i:i+BLOCK_SIZE] for i in range(0, len(ciphertext), BLOCK_SIZE)]
    decrypted = b''
    prev = iv
    for block in blocks:
        dec_block = tea_decrypt_block(block, key)
        xor_block = bytes(a ^ b for a, b in zip(dec_block, prev))
        decrypted += xor_block
        prev = block
    return unpad(decrypted)

# Fájl titkosítás / visszafejtés
def process_file(input_file, encrypted_file, decrypted_file):
    key = os.urandom(16)  # 128-bit kulcs (4x32 bit)
    iv = os.urandom(BLOCK_SIZE)

    with open(input_file, 'rb') as f:
        plaintext = f.read()

    ciphertext = encrypt_cbc(plaintext, key, iv)

    with open(encrypted_file, 'wb') as f:
        f.write(iv + ciphertext)

    with open(encrypted_file, 'rb') as f:
        iv = f.read(BLOCK_SIZE)
        ciphertext = f.read()

    decrypted = decrypt_cbc(ciphertext, key, iv)

    with open(decrypted_file, 'wb') as f:
        f.write(decrypted)

# Példa futtatás
process_file('lab5\Fajlok\cryptOTP', 'encrypted.bin', 'decrypted.bin')