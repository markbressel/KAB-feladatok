import hashlib
import base64
import json
import os

# Hash generálás függvény
def generate_hash(password, salt, iterations=1000, hash_algorithm='sha3_256'):
    password_bytes = password.encode('utf-8')
    salt_bytes = base64.b64decode(salt)
    dk = hashlib.pbkdf2_hmac(hash_algorithm, password_bytes, salt_bytes, iterations)
    return base64.b64encode(dk).decode('utf-8')

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

# Feltört jelszavak mentése erősített verzióban
def save_strong_passwords(users, output_file='Fajlok/StrongPasswdSHA256Salt.json'):
    strong_users = []
    for user in users:
        strong_user = {
            "name": user["name"],
            "password": generate_hash(user["password"], user["salt"], 1000000),
            "salt": user["salt"]
        }
        strong_users.append(strong_user)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(strong_users, f, indent=4)
    print(f"\nErősített jelszavak elmentve: {output_file}")

# Fő program
def main():
    # Adatok betöltése
    json_data = load_file('Fajlok/PasswdSHA256Salt.json')
    common_passwords = load_file('Fajlok/10-million-password-list-top-10000.txt')
    
    # 1. Feltörjük az eredeti jelszavakat (1000 iteráció)
    found_passwords = {}
    for user in json_data:
        name = user['name']
        target_hash = user['password']
        salt = user['salt']
        
        for password in common_passwords:
            current_hash = generate_hash(password, salt, 1000)
            if current_hash == target_hash:
                found_passwords[name] = password
                break
    
    # Eredmények kiírása
    print("Eredeti jelszavak feltörése (1000 iteráció):")
    for name, password in found_passwords.items():
        print(f"{name}: {password}")
    
    if not found_passwords:
        print("Nem található feltörhető jelszó.")
        return
    
    # 2. Készítünk egy listát a feltört felhasználókról
    cracked_users = [user for user in json_data if user['name'] in found_passwords]
    
    # 3. Elmentjük az erősített jelszavakat
    save_strong_passwords(cracked_users)
    
    # 4. Megpróbáljuk feltörni az erősített jelszavakat
    print("\nMegpróbáljuk feltörni az erősített jelszavakat (1,000,000 iteráció)...")
    strong_data = load_file('Fajlok/StrongPasswdSHA256Salt.json')
    
    strong_cracked = False
    for user in strong_data:
        name = user['name']
        target_hash = user['password']
        salt = user['salt']
        original_password = found_passwords[name]
        
        print(f"\nPróbáljuk feltörni {name} jelszavát...")
        print(f"Eredeti jelszó: {original_password}")
        
        # Próbáljuk meg az eredeti jelszót (nagy iterációval)
        start_time = time.time()
        current_hash = generate_hash(original_password, salt, 1000000)
        elapsed_time = time.time() - start_time
        
        print(f"1 hash kiszámítása 1,000,000 iterációval: {elapsed_time:.2f} másodperc")
        
        if current_hash == target_hash:
            print("SIKERES feltörés! (azonos jelszó, csak több iterációval)")
            strong_cracked = True
        else:
            print("Nem sikerült feltörni (túl sok idő lenne a brute-force)")
    
    if not strong_cracked:
        print("\nÖsszefoglalás: Az 1,000,000 iterációval készített jelszavakat")
        print("nem sikerült feltörni a leggyakoribb jelszavak listájával.")
        print("Az iterációszám növelése jelentősen megnöveli a jelszavak biztonságát.")

if __name__ == "__main__":
    import time  # Az időméréshez
    main()