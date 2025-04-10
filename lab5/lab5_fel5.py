import numpy as np

BLOCK_SIZE = 16  # CBC mód blokkmérete
HILL_BLOCK_SIZE = 4  # Hill titkosítás belső blokkmérete (4x4 mátrixhoz)
MOD = 256

# Mátrix beolvasása fájlból
def read_key_matrix(path):
    with open(path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    matrix = [list(map(int, line.split())) for line in lines]

    # Ellenőrzés: legyen 4x4
    if len(matrix) != 4 or any(len(row) != 4 for row in matrix):
        raise ValueError("A kulcs mátrixnak 4x4-esnek kell lennie.")
    
    return np.array(matrix, dtype=int)

# Hill kulcs inverze mod 256 alatt
def modinv_matrix(matrix, mod):
    det = int(round(np.linalg.det(matrix))) % mod
    if det == 0 or np.gcd(det, mod) != 1:
        raise ValueError("A mátrix nem invertálható modulo 256 alatt.")
    
    det_inv = pow(det, -1, mod)
    matrix_adj = np.round(det * np.linalg.inv(matrix)).astype(int) % mod
    return (det_inv * matrix_adj) % mod

# Egy 4 bájtos blokk visszafejtése Hill módszerrel
def hill_decrypt_block(block, inv_key):
    if len(block) != HILL_BLOCK_SIZE:
        raise ValueError(f"A Hill blokk mérete {len(block)} byte, de {HILL_BLOCK_SIZE} byte szükséges.")
    
    vec = np.array(list(block), dtype=int).reshape(4, 1)  # 4x1 vektor
    res = np.dot(inv_key, vec) % MOD
    return res.flatten().astype(np.uint8).tobytes()

# CBC mód visszafejtés 16 bájtos blokkokkal, Hill 4 bájtos alblokkjaival
def decrypt_hill_cbc(ciphertext, key_matrix, iv):
    if len(iv) != BLOCK_SIZE:
        raise ValueError(f"Az IV hossza {len(iv)} byte, de {BLOCK_SIZE} byte szükséges.")
    
    inv_key = modinv_matrix(key_matrix, MOD)
    decrypted = b''

    prev = iv
    for i in range(0, len(ciphertext), BLOCK_SIZE):
        block = ciphertext[i:i+BLOCK_SIZE]
        if len(block) < BLOCK_SIZE:
            block += b'\x00' * (BLOCK_SIZE - len(block))  # Padding, ha szükséges
        
        decrypted_block = b''
        # 16 bájtos blokkot 4 db 4 bájtos alblokkra bontunk
        for j in range(0, BLOCK_SIZE, HILL_BLOCK_SIZE):
            sub_block = block[j:j+HILL_BLOCK_SIZE]
            decrypted_sub_block = hill_decrypt_block(sub_block, inv_key)
            decrypted_block += decrypted_sub_block
        
        # XOR az előző blokkal (CBC mód)
        plain_block = bytes(a ^ b for a, b in zip(decrypted_block, prev))
        decrypted += plain_block
        prev = block
    
    return decrypted

# Főprogram
def main():
    try:
        # Kulcs beolvasása
        key_matrix = read_key_matrix(r"lab5\Fajlok\keyHillCBC.txt")
        
        # Titkosított fájl beolvasása
        with open(r"lab5\Fajlok\cryptHillCBC_Ikrek", "rb") as f:
            data = f.read()

        # IV az utolsó BLOCK_SIZE bájt
        iv = data[-BLOCK_SIZE:]
        ciphertext = data[:-BLOCK_SIZE]

        # Visszafejtés
        plaintext = decrypt_hill_cbc(ciphertext, key_matrix, iv)

        # Eredmény mentése
        with open("visszafejtett.jpg", "wb") as f:
            f.write(plaintext)
        
        print("A visszafejtés sikeresen megtörtént, az eredmény 'visszafejtett.jpg' néven mentve.")
    
    except Exception as e:
        print(f"Hiba történt: {str(e)}")

if __name__ == "__main__":
    main()