from collections import defaultdict

def find_duplicate_passwords(file_path):
    # Hash-ekhez tartozó neveket tároló szótár
    hash_to_names = defaultdict(list)
    
    # Fájl beolvasása
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Sor értelmezése (JSON-szerű formátum)
                line = line.strip()
                if line:
                    # A sorból kivesszük a 'name' és 'password' értékeket
                    try:
                        # Egyszerűsített parsing: feltételezzük, hogy a formátum konzisztens
                        name_start = line.find("'name': '") + 9
                        name_end = line.find("'", name_start)
                        name = line[name_start:name_end]
                        
                        hash_start = line.find("'password': '") + 13
                        hash_end = line.find("'", hash_start)
                        hash_value = line[hash_start:hash_end]
                        
                        hash_to_names[hash_value].append(name)
                    except Exception as e:
                        print(f"Hibás sor: {line} - {e}")
    
        # Azonos hash-ekkel rendelkező személyek keresése
        duplicates = {hash_value: names for hash_value, names in hash_to_names.items() if len(names) > 1}
        
        # Eredmények kiírása
        if duplicates:
            print("Azonos jelszóval rendelkező személyek:")
            for hash_value, names in duplicates.items():
                print(f"Hash: {hash_value}")
                print(f"Személyek: {', '.join(names)}")
                print()
        else:
            print("Nincs azonos jelszóval rendelkező személy.")
    
    except FileNotFoundError:
        print(f"A fájl nem található: {file_path}")
    except Exception as e:
        print(f"Hiba történt: {e}")

# Fájl elérési útja
file_path = "Fajlok/PasswdSHA256.txt"

# Függvény meghívása
find_duplicate_passwords(file_path)