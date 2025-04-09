def mod_inverse(a, m):
    """Számít az 'a' moduláris inverzét 'm' alatt az extenedált Euklideszi algoritmus segítségével."""
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError(f"{a} nem invertálható modulo {m} alatt")
    return (x % m + m) % m

def find_key(x1, y1, x2, y2, m):
    """Megoldja a kulcsot (a, b) az ismert párok alapján: x1*a + b = y1 mod m, x2*a + b = y2 mod m."""
    # x1*a + b = y1
    # x2*a + b = y2
    # Kivonás: (x1 - x2)*a = y1 - y2 mod m
    diff_x = (x1 - x2) % m
    diff_y = (y1 - y2) % m
    
    # 'a' kiszámítása: a = (y1 - y2) * (x1 - x2)^(-1) mod m
    inv_diff_x = mod_inverse(diff_x, m)
    a = (diff_y * inv_diff_x) % m
    
    # 'b' kiszámítása: b = y1 - x1*a mod m
    b = (y1 - x1 * a) % m
    
    return a, b

def decrypt(ciphertext, a, b, m, alphabet):
    """Dekódol egy titkosított szöveget az affin titkosításból."""
    a_inv = mod_inverse(a, m)
    plaintext = ""
    for c in ciphertext:
        if c in alphabet:
            c_num = alphabet.index(c)
            p_num = (a_inv * (c_num - b)) % m
            plaintext += alphabet[p_num]
        else:
            plaintext += c  # Ha nem része az alfabetumnak, változatlanul hagyjuk
    return plaintext

# Alfabetum definiálása
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ,. "
M = 29  # Az alfabetum mérete

# 1. szöveg: A (0) → K (10), O (14) → D (3)
x1_1, y1_1 = 0, 10   # A → K
x2_1, y2_1 = 14, 3   # O → D
a1, b1 = find_key(x1_1, y1_1, x2_1, y2_1, M)
print(f"Első szöveg kulcsa: a = {a1}, b = {b1}")

# 2. szöveg: I (8) → K (10), O (14) → J (9)
x1_2, y1_2 = 8, 10   # I → K
x2_2, y2_2 = 14, 9  # O → J
a2, b2 = find_key(x1_2, y1_2, x2_2, y2_2, M)
print(f"Második szöveg kulcsa: a = {a2}, b = {b2}")

# Példa dekódolás (ha lenne titkosított szöveg)
ciphertext1 = "KZRGQKEGBDFZEKHKBBKHKSKFZFGBMKEGPKBKQKZBMDTHKTDZEDXBMIQPZKZEGTIPDBMGZPVKTIBMZWIXIMPIZWIT,ZEIHRIXGHZAH.,ZVDH.ZEIHEIQPIZKQS.IFAFKPZKYYKSZKMZGXDRDSPYKS,ZKEGFDQZKQS.IFASFZVDBBMKZIH.ISTDZPIBPASFZEKHKBBKHKOKTLLL"
plaintext1 = decrypt(ciphertext1, a1, b1, M, alphabet)
print(f"Első szöveg dekódolva: {plaintext1}")
#
ciphertext2 = "QKMJORJS,GJYUJA,PVNVYTIOAQVO,DVOOVAH,TVS,GJYUJA,OKOLSBOBACNJYIOA,ZIUU,V,DBYBTBORIOAH,VM,JSMNJOJS,DVURIOAH,V,NJXBADBSIOA,BS,BYYBOSMBODIOAH,BURSMJDVY,TKOGVMH,VTKN,BURBGIY,VYAJNIOA,TBUCOBT,NJYIOA,ZIUU,V,NBSNIOAH,V,DVURJOIOAH,V,PKXOBDIOA,BS,V,NKSMNSBUBKOAH,NBPVN,TKOGVMH,VTKN,OBT,BURBGIY,PJMNIOA,YBNXBC,BEKANBNJSM"
plaintext2 = decrypt(ciphertext2, a2, b2, M, alphabet)
print(f"Második szöveg dekódolva: {plaintext2}")