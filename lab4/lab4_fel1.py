import base64
import time
import os
from typing import List

class RC4:
    def __init__(self, key: bytes):
        self.S = list(range(256))
        self.key = key
        self._initialize()

    def _initialize(self):
        j = 0
        for i in range(256):
            j = (j + self.S[i] + self.key[i % len(self.key)]) % 256
            self.S[i], self.S[j] = self.S[j], self.S[i]

    def generate_stream(self, length: int) -> bytes:
        S = self.S.copy()
        i = j = 0
        output = bytearray()
        
        # Teljes kimenet generálása, beleértve a kihagyandó 1024 bájtot is
        for _ in range(length + 1024):
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]
            output.append(S[(S[i] + S[j]) % 256])
        
        # Az első 1024 bájt kihagyása
        return bytes(output[1024:])

def encrypt_decrypt(input_data: bytes, key: bytes) -> bytes:
    rc4 = RC4(key)
    keystream = rc4.generate_stream(len(input_data))
    return bytes(a ^ b for a, b in zip(input_data, keystream))

def read_key_from_file(key_file: str) -> bytes:
    with open(key_file, 'r') as f:
        base64_key = f.read().strip()
    key = base64.b64decode(base64_key)
    if len(key) != 16:  # 128 bit = 16 bájt
        raise ValueError("A kulcsnak 128 bitesnek (16 bájt) kell lennie!")
    return key

def process_file(input_file: str, key_file: str, output_file: str) -> float:
    # Kulcs beolvasása
    key = read_key_from_file(key_file)
    
    # Bemeneti fájl beolvasása
    with open(input_file, 'rb') as f:
        input_data = f.read()
    
    # Időmérés kezdete
    start_time = time.time()
    
    # Titkosítás/visszafejtés
    output_data = encrypt_decrypt(input_data, key)
    
    # Időmérés vége
    end_time = time.time()
    
    # Kimeneti fájl írása
    with open(output_file, 'wb') as f:
        f.write(output_data)
    
    return end_time - start_time

def main():
    # Teszt kulcs létrehozása (128 bit = 16 bájt)
    sample_key = os.urandom(16)
    base64_key = base64.b64encode(sample_key).decode('utf-8')
    
    with open('key.txt', 'w') as f:
        f.write(base64_key)
    
    # Teszt fájlok méretei (bájtban)
    test_sizes = [1024, 1024*1024, 10*1024*1024]  # 1KB, 1MB, 10MB
    
    for size in test_sizes:
        # Teszt fájl létrehozása
        with open('input.bin', 'wb') as f:
            f.write(os.urandom(size))
        
        # Titkosítás
        encrypt_time = process_file('input.bin', 'key.txt', 'encrypted.bin')
        
        # Visszafejtés
        decrypt_time = process_file('encrypted.bin', 'key.txt', 'decrypted.bin')
        
        # Eredmények kiírása
        print(f"Fájl mérete: {size/1024:.2f} KB")
        print(f"Titkosítási idő: {encrypt_time:.4f} másodperc")
        print(f"Visszafejtési idő: {decrypt_time:.4f} másodperc")
        print("-" * 50)
        
        # Ellenőrzés, hogy a visszafejtett fájl megegyezik-e az eredetivel
        with open('input.bin', 'rb') as f1, open('decrypted.bin', 'rb') as f2:
            original = f1.read()
            decrypted = f2.read()
            print(f"Visszafejtés sikeres: {original == decrypted}")

if __name__ == "__main__":
    main()