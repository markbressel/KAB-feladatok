def caesar_titkosit_bajtok(bajtok, eltolás):
    # Függvény a bájtok titkosítására
    titkosított = bytearray()
    for bajt in bajtok:
        # Minden bájtot eltolunk, modulo 256-tal maradunk a bájt tartományban (0-255)
        titkosított.append((bajt + eltolás) % 256)
    return bytes(titkosított)

def caesar_visszafejt_bajtok(sifrat, eltolás):
    # Függvény a bájtok visszafejtésére (ellentétes eltolás)
    return caesar_titkosit_bajtok(sifrat, -eltolás)

def fajl_feldolgozas(bemeneti_fajl, kimeneti_titkositott, kimeneti_visszafejtett, eltolás):
    # Bináris fájl beolvasása és feldolgozása
    try:
        # Bináris módú beolvasás
        with open(bemeneti_fajl, 'rb') as f:
            eredeti_bajtok = f.read()
        
        # Titkosítás
        titkosított_bajtok = caesar_titkosit_bajtok(eredeti_bajtok, eltolás)
        
        # Visszafejtés
        visszafejtett_bajtok = caesar_visszafejt_bajtok(titkosított_bajtok, eltolás)
        
        # Titkosított fájl mentése
        with open(kimeneti_titkositott, 'wb') as f:
            f.write(titkosított_bajtok)
        print(f"Titkosított fájl mentve: {kimeneti_titkositott}")
        
        # Visszafejtett fájl mentése
        with open(kimeneti_visszafejtett, 'wb') as f:
            f.write(visszafejtett_bajtok)
        print(f"Visszafejtett fájl mentve: {kimeneti_visszafejtett}")
        
        # Ellenőrzés: az eredeti és visszafejtett megegyezik-e
        if eredeti_bajtok == visszafejtett_bajtok:
            print("A visszafejtés sikeres, az eredeti és visszafejtett fájl megegyezik!")
        else:
            print("Hiba: A visszafejtett fájl nem egyezik az eredetivel!")
            
    except FileNotFoundError:
        print("Hiba: A bemeneti fájl nem található!")
    except Exception as e:
        print(f"Hiba történt: {e}")

# Fő program
def main():
    # Fájlnevek és eltolás bekérése
    bemeneti_fajl = input("Add meg a bemeneti fajl utvonalat: ")
    kimeneti_titkositott = input("Add meg a titkosított fajl nevet/utvonalat: ") or "titkosított.bin"
    kimeneti_visszafejtett = input("Add meg a visszafejtett fajl nevet/utvonalat: ") or "visszafejtett.bin"
    
    while True:
        try:
            eltolás = int(input("Add meg az eltolás merteket (0-255): "))
            if 0 <= eltolás <= 255:
                break
            print("Kerlek 0 es 255 kozotti szamot adj meg!")
        except ValueError:
            print("Kerlek ervenyes szamot adj meg!")
    
    # Fájl feldolgozása
    fajl_feldolgozas(bemeneti_fajl, kimeneti_titkositott, kimeneti_visszafejtett, eltolás)

# Program futtatása
if __name__ == "__main__":
    main()