def lfsr_decrypt(encrypted_data, plain_chunk, encrypted_chunk):
    # Kulcsfolyam kiszámítása: plain XOR encrypted
    key_stream = bytes(a ^ b for a, b in zip(plain_chunk, encrypted_chunk))
    
    # Teljes adat visszafejtése a kulcsfolyammal
    decrypted_data = bytearray()
    for i, byte in enumerate(encrypted_data):
        key_byte = key_stream[i % len(key_stream)]  # Ciklikusan használjuk a kulcsfolyamot
        decrypted_data.append(byte ^ key_byte)
    
    return bytes(decrypted_data)

# Adatok hexadecimális formában
plain_chunk = bytes.fromhex('e0ffd8ff464a1000')
encrypted_chunk = bytes.fromhex('880006b0de683e80')

# Titkosított fájl beolvasása
with open('lab4\Fajlok\cryptLFSR', 'rb') as f:
    encrypted_data = f.read()

# Visszafejtés
decrypted_data = lfsr_decrypt(encrypted_data, plain_chunk, encrypted_chunk)

# Eredmény kiírása
with open('lab4\Fajlok\decrypted.jpg', 'wb') as f:
    f.write(decrypted_data)