def gcd(a, b):
    """Legnagyobb közös osztó kiszámítása"""
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    """Moduláris inverz kiszámítása (ha létezik)"""
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    g, x, _ = extended_gcd(a, m)
    if g != 1:
        return None  # Nincs inverz, ha nem relatív prím
    return x % m

def affine_decrypt(ciphertext, a, b):
    """Affin titkosítás visszafejtése"""
    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        return None
    
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            # Nagybetűs karakter visszafejtése
            C = ord(char) - ord('A')
            P = (a_inv * (C - b)) % 26
            plaintext += chr(P + ord('A'))
        else:
            # Írásjelek változatlanul
            plaintext += char
    return plaintext

def find_possible_keys(ciphertext, required_word="AZ"):
    """Az összes lehetséges kulcs kipróbálása"""
    valid_a = [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]  # Relatív prímek 26-hoz
    results = []

    for a in valid_a:
        for b in range(26):
            decrypted = affine_decrypt(ciphertext, a, b)
            if decrypted and required_word in decrypted:
                results.append((a, b, decrypted))
    
    return results

# A titkosított szöveg
ciphertext = "EX GKLGTGWRGW BE HGDPGAODRG KIRZEX EKIH WIVERREW, RGK VEDRE E PEVOWTE. BGTEWDGIHYAX"

# Kulcsok keresése
possible_solutions = find_possible_keys(ciphertext)

# Eredmények kiírása
print("Lehetséges megoldások (a, b, dekódolt szöveg):")
for a, b, decrypted in possible_solutions:
    print(f"a = {a}, b = {b}: {decrypted}")

# Az előző megfejtés ellenőrzése (a=7, b=4)
specific_decryption = affine_decrypt(ciphertext, 7, 4)
print(f"\nEllenőrzés a=7, b=4 esetén: {specific_decryption}")