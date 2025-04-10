import numpy as np
import sys
import os
from pathlib import Path

def read_key_matrix(key_file):
    """Beolvassa a mátrix méretét és elemeit a fájlból"""
    with open(key_file, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
        
        # Első sor tartalmazza a mátrix méretét
        n = int(lines[0].split()[0])
        
        # Mátrix elemek beolvasása
        matrix = []
        for line in lines[1:n+1]:
            row = list(map(int, line.split()))
            matrix.append(row)
            
        return np.array(matrix)

def modinv_matrix(matrix, mod=256):
    """Kiszámolja a mátrix inverzét modulo 256"""
    det = int(round(np.linalg.det(matrix)))
    try:
        det_inv = pow(det, -1, mod)
    except ValueError:
        raise ValueError("A mátrix nem invertálható mod 256")
    
    adjugate = np.round(det * np.linalg.inv(matrix)).astype(int)
    return (det_inv * adjugate) % mod

def hill_decrypt_block(cipher_block, inv_key_matrix):
    """Egy blokk visszafejtése Hill titkosítással"""
    cipher_vec = np.array([byte for byte in cipher_block])
    plain_vec = np.dot(inv_key_matrix, cipher_vec) % 256
    return bytes([int(x) for x in plain_vec])

def cbc_hill_decrypt(input_file, output_file, key_file):
    """Fő visszafejtő függvény CBC módban"""
    try:
        # Mátrix beolvasása
        key_matrix = read_key_matrix(key_file)
        block_size = len(key_matrix)
        
        # Mátrix inverz kiszámolása
        inv_key_matrix = modinv_matrix(key_matrix)
        
        # Titkosított fájl beolvasása
        with open(input_file, 'rb') as f:
            cipher_data = f.read()
        
        # IV kivonása az utolsó blokkból
        iv = cipher_data[-block_size:]
        cipher_blocks = cipher_data[:-block_size]
        
        # Blokkokra bontás
        blocks = [cipher_blocks[i:i+block_size] for i in range(0, len(cipher_blocks), block_size)]
        
        # CBC visszafejtés
        decrypted_data = bytearray()
        prev_block = iv
        
        for block in reversed(blocks):
            if len(block) < block_size:
                block = block.ljust(block_size, b'\x00')
            
            decrypted_block = hill_decrypt_block(block, inv_key_matrix)
            plain_block = bytes([d ^ p for d, p in zip(decrypted_block, prev_block)])
            decrypted_data.extend(plain_block)
            prev_block = block
        
        # Eredeti sorrend visszaállítása és fájlba írás
        with open(output_file, 'wb') as f:
            f.write(bytes(reversed(decrypted_data)))
            
        print(f"Sikeres visszafejtés! Eredmény mentve ide: {output_file}")
        
        # Ellenőrizzük, hogy JPG-e a kimenet
        with open(output_file, 'rb') as f:
            magic = f.read(3)
            if magic != b'\xff\xd8\xff':
                print("Figyelem: A kimenet nem tűnik érvényes JPG fájlnak!")
            else:
                print("A kimenet érvényes JPG fájlnak tűnik.")
                
    except Exception as e:
        print(f"Hiba történt: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    # Elérési utak kezelése
    base_dir = Path('lab5/Fajlok')
    
    input_file = base_dir / 'cryptHillCBC_Ikrek'
    output_file = base_dir / 'decrypted.jpg'
    key_file = base_dir / 'keyHillCBC.txt'
    
    # Ellenőrizzük a fájlokat
    if not input_file.exists():
        print(f"Hiba: A bemeneti fájl nem található: {input_file}")
        sys.exit(1)
        
    if not key_file.exists():
        print(f"Hiba: A kulcsfájl nem található: {key_file}")
        sys.exit(1)
    
    # Visszafejtés indítása
    print("Visszafejtés indítása...")
    cbc_hill_decrypt(str(input_file), str(output_file), str(key_file))