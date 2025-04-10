# A crypted8_2.jpg AES-CTR módszerrel volt rejtjelezve, ahol az alkalmazott nonce 
# a titkosított file első 8 bájtja és a counter értéke 1-től indul. 
# Határozzuk meg az eredeti jpg filet, ha az AES 32 bájtos kulcs titkosított értékét 
# a Diffie-Hellman kulcserét alkalmazva lehet meghatározni a következőképpen:

# olvassuk ki a publikus paramétereket a DHKey8_2.txt állományból, azaz rendre a p, q, r egész számok hexa értékét,

# olvassuk ki a privát kulcs hexa értékét az APrivFile.txt állományból,

# olvassuk ki a publikus kulcs hexa értékét az BPubFile.txt állományból,

# a közös K kulcsból hozzuk létre a 32 bájtos AES kulcsot, alkalmazva az scrypt kulcs deriváló függvényt, 
# ahol a salt hexa értéke: 438bcc1fd2bb1363e90fb6ff4756bc58, a CPU/Memory költség értéke: 2 ** 10, 
# a blokk méret: 8, a párhuzamossági paraméter: 1.

import hashlib
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Util import Counter
from Crypto.PublicKey import DSA
from Crypto.Random import get_random_bytes
import binascii

# Olvassa be a DH kulcsokat a fájlokból
def read_dh_parameters():
    with open("DHKey8_2.txt", "r") as f:
        p = int(f.readline(), 16)
        q = int(f.readline(), 16)
        r = int(f.readline(), 16)
    return p, q, r

def read_private_key():
    with open("APrivFile.txt", "r") as f:
        private_key_hex = f.read().strip()
    return int(private_key_hex, 16)

def read_public_key():
    with open("BPubFile.txt", "r") as f:
        public_key_hex = f.read().strip()
    return int(public_key_hex, 16)

# Diffie-Hellman kulcscsere
def diffie_hellman_shared_key(private_key, public_key, p):
    # Közös kulcs kiszámítása a Diffie-Hellman kulcscsere alapján
    shared_key = pow(public_key, private_key, p)
    return shared_key

# Scrypt kulcs deriválása
def derive_aes_key(shared_key):
    salt = binascii.unhexlify("438bcc1fd2bb1363e90fb6ff4756bc58")
    aes_key = scrypt(shared_key.to_bytes((shared_key.bit_length() + 7) // 8, 'big'), salt, 32, N=2**10, r=8, p=1)
    return aes_key

# Visszafejtés AES-CTR módban
def decrypt_aes_ctr(input_file, output_file, aes_key):
    # Olvassuk be a titkosított fájlt
    with open(input_file, "rb") as f:
        ciphertext = f.read()
    
    # Az első 8 bájt a nonce
    nonce = ciphertext[:8]
    cipher = AES.new(aes_key, AES.MODE_CTR, counter=Counter.new(128, nonce=nonce))
    
    # A titkosított adat visszafejtése
    decrypted_data = cipher.decrypt(ciphertext[8:])
    
    # Írjuk ki az eredeti fájlt
    with open(output_file, "wb") as f:
        f.write(decrypted_data)

if __name__ == "__main__":
    # Olvassuk be a paramétereket
    p, q, r = read_dh_parameters()
    private_key = read_private_key()
    public_key = read_public_key()
    
    # Számítsuk ki a közös kulcsot a Diffie-Hellman kulcscserével
    shared_key = diffie_hellman_shared_key(private_key, public_key, p)
    print(f"Shared key (hex): {hex(shared_key)}")
    
    # Deriváljunk AES kulcsot a közös kulcsból scrypt segítségével
    aes_key = derive_aes_key(shared_key)
    print(f"AES Key (hex): {binascii.hexlify(aes_key)}")
    
    # Visszafejtés AES-CTR módban
    decrypt_aes_ctr("crypted8_2.jpg", "decrypted_image.jpg", aes_key)
    print("Visszafejtés kész, az eredeti kép a 'decrypted_image.jpg' fájlban található.")
