import hashlib
import base64
import json
import os

# PBKDF2-HMAC-SHA3-256 hash készítése
def generate_hash(password, salt, iterations=1000):
    password_bytes = password.encode('utf-8')
    salt_bytes = base64.b64decode(salt)
    dk = hashlib.pbkdf2_hmac('sha3_256', password_bytes, salt_bytes, iterations)
    return base64.b64encode(dk).decode('utf-8')

# JSON fájl betöltése
json_file = 'Fajlok/PasswdSHA256Salt.json'
try:
    with open(json_file, 'r', encoding='utf-8') as f:
        json_data = json.load(f)
except FileNotFoundError:
    print(f"Hiba: A '{json_file}' fájl nem található a munkakönyvtárban ({os.getcwd()}).")
    exit()
except json.JSONDecodeError:
    print(f"Hiba: A '{json_file}' fájl nem érvényes JSON formátumú.")
    exit()

# Leggyakoribb jelszavak betöltése
common_passwords_file = 'Fajlok/10-million-password-list-top-10000.txt'
try:
    with open(common_passwords_file, 'r', encoding='utf-8', errors='ignore') as f:
        common_passwords = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print(f"Hiba: A '{common_passwords_file}' fájl nem található a munkakönyvtárban ({os.getcwd()}).")
    exit()

# Jelszavak keresése
found_passwords = {}

for user in json_data:
    name = user['name']
    target_hash = user['password']
    salt = user['salt']
    
    print(f"Checking passwords for {name}...")
    
    for password in common_passwords:
        current_hash = generate_hash(password, salt)
        
        if current_hash == target_hash:
            found_passwords[name] = password
            print(f"  Found password for {name}: {password}")
            break  # Ha megtaláltuk, tovább lépünk a következő felhasználóhoz

# Eredmények kiírása
print("\nFound passwords:")
for name, password in found_passwords.items():
    print(f"{name}: {password}")

if not found_passwords:
    print("No passwords were found from the common password list.")