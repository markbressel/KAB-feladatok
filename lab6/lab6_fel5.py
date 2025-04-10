import hashlib
import base64
import json
import os
import time
import bcrypt
from pylibscrypt import scrypt

# Eredeti hash generálás (PBKDF2-HMAC-SHA256, nem SHA3-256, mert az nem támogatott natívan)
def generate_hash(password, salt, iterations=1000, hash_algorithm='sha256'):
    password_bytes = password.encode('utf-8')
    salt_bytes = base64.b64decode(salt)
    dk = hashlib.pbkdf2_hmac(hash_algorithm, password_bytes, salt_bytes, iterations)
    return base64.b64encode(dk).decode('utf-8')

# Scrypt hash generálás
def generate_scrypt_hash(password, salt):
    salt_bytes = base64.b64decode(salt)
    # Paraméterek: N=2^14, r=8, p=1 (ajánlott alapértékek)
    hash_bytes = scrypt(password.encode('utf-8'), salt_bytes, N=16384, r=8, p=1)
    return base64.b64encode(hash_bytes).decode('utf-8')

# Bcrypt hash generálás
def generate_bcrypt_hash(password, salt):
    # Bcrypt saját salt-ot generál, de mi használjuk a megadottat is
    salt_bytes = base64.b64decode(salt)
    # A bcrypt csak az első 72 byte-ot használja a jelszóból, és a salt-nak 16 bájtnak kell lennie
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt_bytes[:16])  # Salt rövidítése, ha szükséges
    return hashed.decode('utf-8')

# Fájlok betöltése
def load_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            if filename.endswith('.json'):
                return json.load(f)
            else:
                return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"Hiba: '{filename}' fájl nem található a munkakönyvtárban ({os.getcwd()}).")
        exit()
    except json.JSONDecodeError:
        print(f"Hiba: '{filename}' fájl nem érvényes JSON formátumú.")
        exit()

# Mentés különböző hash algoritmusokkal
def save_hashed_passwords(users, algorithm='scrypt'):
    output_file = f'Passwd{algorithm.capitalize()}.json'
    hashed_users = []
    
    for user in users:
        password = user['password']  # Itt már a nyers jelszó van tárolva
        salt = user['salt']
        
        if algorithm == 'scrypt':
            hashed_password = generate_scrypt_hash(password, salt)
        elif algorithm == 'bcrypt':
            hashed_password = generate_bcrypt_hash(password, salt)
        else:
            hashed_password = generate_hash(password, salt, 1000000)
        
        hashed_users.append({
            "name": user["name"],
            "password": hashed_password,
            "salt": salt,
            "algorithm": algorithm
        })
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(hashed_users, f, indent=4)
    print(f"\n{algorithm} hashelt jelszavak elmentve: {output_file}")
    return output_file

# Jelszó feltörés próbálkozás
def try_crack_passwords(hashed_file, common_passwords):
    print(f"\nMegpróbáljuk feltörni a {hashed_file} jelszavakat...")
    hashed_data = load_file(hashed_file)
    
    for user in hashed_data:
        name = user['name']
        target_hash = user['password']
        salt = user['salt']
        algorithm = user.get('algorithm', 'pbkdf2')
        
        print(f"\nPróbáljuk feltörni {name} jelszavát ({algorithm})...")
        
        start_time = time.time()
        cracked = False
        
        for password in common_passwords:
            try:
                if algorithm == 'scrypt':
                    current_hash = generate_scrypt_hash(password, salt)
                elif algorithm == 'bcrypt':
                    # Bcrypt-hez külön kezelés, mert a salt benne van a hash-ben
                    current_hash = bcrypt.hashpw(password.encode('utf-8'), target_hash.encode('utf-8')).decode('utf-8')
                else:
                    current_hash = generate_hash(password, salt, 1000000)
                
                if current_hash == target_hash:
                    print(f"  FELTÖRVE: {password} ({(time.time()-start_time):.2f} másodperc alatt)")
                    cracked = True
                    break
                    
            except Exception as e:
                print(f"  Hiba: {str(e)}")
                continue
                
        if not cracked:
            print(f"  Nem sikerült feltörni ({(time.time()-start_time):.2f} másodperc alatt)")

# Fő program
def main():
    # Adatok betöltése
    json_data = load_file('Fajlok/PasswdSHA256Salt.json')
    common_passwords = load_file('Fajlok/10-million-password-list-top-10000.txt')
    
    # 1. Feltörjük az eredeti jelszavakat (1000 iteráció)
    found_passwords = {}
    cracked_users = []
    
    for user in json_data:
        name = user['name']
        target_hash = user['password']
        salt = user['salt']
        
        for password in common_passwords:
            current_hash = generate_hash(password, salt, 1000)
            if current_hash == target_hash:
                found_passwords[name] = password
                # Elmentjük a felhasználót a nyers jelszóval a következő lépéshez
                cracked_users.append({
                    "name": name,
                    "password": password,  # Nyers jelszó
                    "salt": salt
                })
                break
    
    # 2. Készítünk erősített verziókat
    scrypt_file = save_hashed_passwords(cracked_users, 'scrypt')
    bcrypt_file = save_hashed_passwords(cracked_users, 'bcrypt')
    
    # 3. Megpróbáljuk feltörni az új jelszavakat
    try_crack_passwords(scrypt_file, common_passwords)
    try_crack_passwords(bcrypt_file, common_passwords)

if __name__ == "__main__":
    main()