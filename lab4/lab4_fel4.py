import time
from A51 import A51  # Feltételezzük, hogy van egy A51 implementáció

def encrypt_decrypt_file(input_file, output_file, key, encrypt=True):
    a51 = A51(key)
    
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        while True:
            chunk = f_in.read(1024)
            if not chunk:
                break
            processed = bytes([b ^ next(a51.keystream) for b in chunk])
            f_out.write(processed)

def measure_time(file_sizes):
    key = b'secret_key_12345'  # 16 bájtos kulcs
    results = {}
    
    for size in file_sizes:
        # Tesztfájl generálása
        test_file = f'test_{size}.bin'
        with open(test_file, 'wb') as f:
            f.write(bytes([i % 256 for i in range(size)]))
        
        # Titkosítás időmérése
        encrypted_file = f'encrypted_{size}.bin'
        start = time.time()
        encrypt_decrypt_file(test_file, encrypted_file, key, encrypt=True)
        encrypt_time = time.time() - start
        
        # Visszafejtés időmérése
        decrypted_file = f'decrypted_{size}.bin'
        start = time.time()
        encrypt_decrypt_file(encrypted_file, decrypted_file, key, encrypt=False)
        decrypt_time = time.time() - start
        
        results[size] = (encrypt_time, decrypt_time)
        
        # Tisztítás
        import os
        os.remove(test_file)
        os.remove(encrypted_file)
        os.remove(decrypted_file)
    
    return results

# Példa használat
file_sizes = [1024, 10240, 102400, 1048576]  # 1KB, 10KB, 100KB, 1MB
timings = measure_time(file_sizes)

for size, (enc_time, dec_time) in timings.items():
    print(f"Size: {size} bytes - Encrypt: {enc_time:.4f}s, Decrypt: {dec_time:.4f}s")