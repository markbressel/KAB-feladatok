def caesar_visszafejt_bajtok(sifrat, eltolás):
    # Függvény a bájtok visszafejtésére adott eltolással
    visszafejtett = bytearray()
    for bajt in sifrat:
        visszafejtett.append((bajt - eltolás) % 256)
    return bytes(visszafejtett)

def ervenyes_txt_e(bajtok):
    # Ellenőrzi, hogy a bájtok csak nyomtatható ASCII karaktereket (32-126), 
    # valamint 10 (\n) és 13 (\r) kódokat tartalmaznak-e
    for bajt in bajtok:
        if bajt != 10 and bajt != 13 and (bajt < 32 or bajt > 126):
            return False
    return True

def megfejtes_brute_force(bemeneti_fajl):
    # Az összes lehetséges kulcs kipróbálása (0-255)
    try:
        with open(bemeneti_fajl, 'rb') as f:
            titkosított_bajtok = f.read()
        
        for eltolás in range(256):
            visszafejtett_bajtok = caesar_visszafejt_bajtok(titkosított_bajtok, eltolás)
            if ervenyes_txt_e(visszafejtett_bajtok):
                # Ha a visszafejtett tartalom érvényes szöveg, kiírjuk és mentjük
                print(f"Megtalált kulcs: {eltolás}")
                print(f"Visszafejtett szöveg: {visszafejtett_bajtok.decode('ascii')[:100]}...")  # Első 100 karakter
                with open("visszafejtett.txt", "wb") as f:
                    f.write(visszafejtett_bajtok)
                print("Visszafejtett állomány mentve: visszafejtett.txt")
                return eltolás, visszafejtett_bajtok
        print("Nem található érvényes szöveg a lehetséges kulcsok között!")
        return None, None
    
    except FileNotFoundError:
        print("Hiba: A bemeneti fájl nem található!")
        return None, None
    except Exception as e:
        print(f"Hiba történt: {e}")
        return None, None

# Fő program
def main():
    bemeneti_fajl = input("Add meg a titkosított fajl utvonalat: ")
    kulcs, visszafejtett = megfejtes_brute_force(bemeneti_fajl)
    if kulcs is not None:
        print(f"Az eredeti állomány visszafejtve, kulcs: {kulcs}")

if __name__ == "__main__":
    main()