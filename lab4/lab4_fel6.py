import time
import os

# LFSR generátor 16 bites kulccsal
def lfsr_16(seed, length):
    # 16 bites LFSR tap pozíciók: x^16 + x^14 + x^13 + x^11 + 1 (0xD801)
    state = seed & 0xFFFF  # Biztosítjuk, hogy 16 bit legyen
    output = bytearray()
    
    for _ in range(length):
        # Következő bájt generálása (8 bitenként)
        byte = 0
        for i in range(8):
            bit = state & 1  # Legalsó bit
            byte |= (bit << i)
            # Visszacsatolás: x^16 + x^14 + x^13 + x^11
            feedback = ((state >> 0) ^ (state >> 2) ^ (state >> 3) ^ (state >> 5)) & 1
            state = (state >> 1) | (feedback << 15)
        output.append(byte)
    
    return bytes(output)

# Titkosítás és visszafejtés XOR-ral
def encrypt_decrypt(data, key_stream):
    return bytes(a ^ b for a, b in zip(data, key_stream))

# Kulcs beolvasása szövegfájlból
def read_key_from_file(filename):
    with open(filename, 'r') as f:
        hex_key = f.read().strip()
    return int(hex_key, 16)

# Fő program
def process_file(input_file, key_file, output_encrypted, output_decrypted):
    # Kulcs beolvasása
    seed = read_key_from_file(key_file)
    
    # Bemeneti fájl beolvasása
    with open(input_file, 'rb') as f:
        plaintext = f.read()
    
    # Kulcsfolyam generálása az input méretének megfelelően
    key_stream = lfsr_16(seed, len(plaintext))
    
    # Titkosítás időmérése
    start_time = time.time()
    encrypted_data = encrypt_decrypt(plaintext, key_stream)
    encrypt_time = time.time() - start_time
    
    # Titkosított fájl mentése
    with open(output_encrypted, 'wb') as f:
        f.write(encrypted_data)
    
    # Visszafejtés (ugyanazzal a kulcsfolyammal)
    decrypted_data = encrypt_decrypt(encrypted_data, key_stream)
    
    # Visszafejtett fájl mentése
    with open(output_decrypted, 'wb') as f:
        f.write(decrypted_data)
    
    # Fájlméret és idő kiírása
    file_size = os.path.getsize(input_file) / 1024  # KB-ban
    print(f"Fájl: {input_file}, Méret: {file_size:.2f} KB, Titkosítási idő: {encrypt_time:.6f} másodperc")

# Tesztelés különböző méretű fájlokkal
if __name__ == "__main__":
    key_file = "lab4\Fajlok\key.txt"  # A kulcsot tartalmazó szövegfájl (pl. "ABCD")
    
    # Példa fájlok (cseréld ki a saját tesztfájljaidra!)
    test_files = [
        ("lab4\Fajlok\cryptHB", "small_encrypted.bin", "small_decrypted.bin"),  # Kis fájl
        ("lab4\Fajlok\cryptLFSR", "medium_encrypted.bin", "medium_decrypted.bin"),  # Közepes fájl
        ("lab4\Fajlok\cryptOTP", "large_encrypted.bin", "large_decrypted.bin"),  # Nagy fájl
    ]
    
    for input_file, enc_file, dec_file in test_files:
        if os.path.exists(input_file):
            process_file(input_file, key_file, enc_file, dec_file)
        else:
            print(f"Hiba: {input_file} nem található!")
