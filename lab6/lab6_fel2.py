import json
import hashlib
from base64 import b64encode

def calculate_sha3_256_hash(password):
    """Számít egy SHA3-256 hash-t a megadott jelszóból, és Base64 kódolással adja vissza."""
    sha3_256 = hashlib.sha3_256()
    sha3_256.update(password.encode('utf-8'))
    return b64encode(sha3_256.digest()).decode('utf-8')

def find_common_passwords(json_file, common_passwords_file):
    # JSON fájl beolvasása
    with open(json_file, 'rt', encoding='utf-8') as f:
        persons = json.load(f)
    
    # Gyakori jelszavak beolvasása
    common_passwords = []
    with open(common_passwords_file, 'rt', encoding='utf-8') as f:
        common_passwords = [line.strip() for line in f if line.strip()]
    
    # Hash-ek kiszámítása a gyakori jelszavakhoz
    common_password_hashes = {pwd: calculate_sha3_256_hash(pwd) for pwd in common_passwords}
    
    # Egyezések keresése
    matches = []
    for person in persons:
        name = person['name']
        hash_value = person['password']
        # Ellenőrizzük, hogy a hash szerepel-e a gyakori jelszavak hash-ei között
        for pwd, pwd_hash in common_password_hashes.items():
            if hash_value == pwd_hash:
                matches.append((name, pwd))
                break
    
    # Eredmények kiírása
    if matches:
        print("Személyek, akiknek a jelszava a leggyakoribb jelszavak közül került ki:")
        for name, password in matches:
            print(f"Név: {name}, Jelszó: {password}")
    else:
        print("Nincs olyan személy, akinek a jelszava a gyakori jelszavak között lenne.")

# Fájlok elérési útja
json_file = "Fajlok/PasswdSHA256.json"
common_passwords_file = "Fajlok/10-million-password-list-top-10000.txt"

# Függvény meghívása
find_common_passwords(json_file, common_passwords_file)