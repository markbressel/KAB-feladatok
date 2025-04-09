import numpy as np

# Karakterek konvertálása számokká és vissza (a=0, b=1, ..., z=25, szóköz=26)
def char_to_num(c):
    if c == ' ': return 26
    return ord(c) - ord('a')

def num_to_char(n):
    if n == 26: return ' '
    return chr(n + ord('a'))

# Modulo 27 inverz kiszámítása (bővített Euklideszi algoritmus)
def mod_inverse(a, m):
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        gcd, x1, y1 = extended_gcd(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y
    
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Nincs inverz, mert a szám nem relatív prím 27-tel")
    return (x % m + m) % m

# Kulcsmátrix meghatározása a megadott párokból
# "pu" -> "oa" és "or" -> "we"
P = np.array([[char_to_num('p'), char_to_num('o')],  # p=15, o=14
              [char_to_num('u'), char_to_num('r')]]) # u=20, r=17
C = np.array([[char_to_num('o'), char_to_num('w')],  # o=14, w=22
              [char_to_num('a'), char_to_num('e')]]) # a=0, e=4

# P mátrix inverzének kiszámítása modulo 27
det_P = (P[0,0] * P[1,1] - P[0,1] * P[1,0]) % 27
det_P_inv = mod_inverse(det_P, 27)
P_inv = np.array([[P[1,1], -P[0,1]], [-P[1,0], P[0,0]]]) * det_P_inv
P_inv = P_inv % 27

# Kulcsmátrix: K = C * P_inv
K = (C @ P_inv) % 27

# Dekódoló mátrix: K inverze modulo 27
det_K = (K[0,0] * K[1,1] - K[0,1] * K[1,0]) % 27
det_K_inv = mod_inverse(det_K, 27)
K_inv = np.array([[K[1,1], -K[0,1]], [-K[1,0], K[0,0]]]) * det_K_inv
K_inv = K_inv % 27

# Fájl beolvasása és dekódolás
def decrypt_text(ciphertext, K_inv):
    plaintext = ""
    for i in range(0, len(ciphertext), 2):
        block = np.array([char_to_num(ciphertext[i]), char_to_num(ciphertext[i+1])])
        decrypted_block = (K_inv @ block) % 27
        plaintext += num_to_char(decrypted_block[0]) + num_to_char(decrypted_block[1])
    return plaintext

# outHill.txt beolvasása
try:
    with open('outHill.txt', 'r') as file:
        ciphertext = file.read().strip()
except FileNotFoundError:
    print("Az 'outHill.txt' fájl nem található!")
    exit()

# Dekódolás és eredmény kiírása
plaintext = decrypt_text(ciphertext, K_inv)
print("Az eredeti szöveg:", plaintext)