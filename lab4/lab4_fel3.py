def recover_otp_key(ciphertext_file, known_plaintext_start):
    with open(ciphertext_file, 'rb') as f:
        ciphertext = f.read()
    
    # Az első 16 bájt kulcsot ad, mert key = ciphertext XOR plaintext
    key = bytes([c ^ p for c, p in zip(ciphertext[:16], known_plaintext_start)])
    return key

def decrypt_otp_repeating_key(ciphertext_file, output_file, key):
    with open(ciphertext_file, 'rb') as f:
        ciphertext = f.read()
    
    decrypted = bytes([c ^ key[i % len(key)] for i, c in enumerate(ciphertext)])
    
    with open(output_file, 'wb') as f:
        f.write(decrypted)

# Ismert plaintext kezdet: "<!DOCTYPE html>\n" (16 bájt)
known_start = b'<!DOCTYPE html>\n'

# Kulcs visszanyerése
key = recover_otp_key('lab4\Fajlok\cryptOTP', known_start)

# Fájl visszafejtése
decrypt_otp_repeating_key('lab4\Fajlok\cryptOTP', 'lab4\Fajlok\decrypted.html', key)