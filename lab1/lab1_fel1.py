# Caesar-titkosító program szövegállományhoz, különböző mappák kezelésére

def caesar_titkosit(szoveg, eltolás):
    # Függvény a szöveg titkosítására
    titkosított = ""
    for karakter in szoveg:
        if karakter.isalpha():  # Csak betűkre alkalmazzuk a titkosítást
            szam = (ord(karakter) - ord('A') + eltolás) % 26
            titkosított += chr(szam + ord('A'))
        else:
            titkosított += karakter
    return titkosított

def caesar_visszafejt(sifrat, eltolás):
    # Függvény a szöveg visszafejtésére
    return caesar_titkosit(sifrat, -eltolás)

def fajl_feldolgozas(bemeneti_fajl, kimeneti_titkositott, kimeneti_visszafejtett, eltolás):
    # Fájl beolvasása és feldolgozása
    try:
        # Beolvasás és nagybetűssé alakítás
        with open(bemeneti_fajl, 'r', encoding='utf-8') as f:
            eredeti_szoveg = f.read().upper()
        
        print(f"Eredeti szöveg nagybetűsen:\n{eredeti_szoveg}\n")
        
        # Titkosítás
        titkosított_szoveg = caesar_titkosit(eredeti_szoveg, eltolás)
        print(f"Titkosított szöveg:\n{titkosított_szoveg}\n")
        
        # Visszafejtés
        visszafejtett_szoveg = caesar_visszafejt(titkosított_szoveg, eltolás)
        print(f"Visszafejtett szöveg:\n{visszafejtett_szoveg}\n")
        
        # Titkosított szöveg mentése fájlba
        with open(kimeneti_titkositott, 'w', encoding='utf-8') as f:
            f.write(titkosított_szoveg)
        print(f"Titkosított szöveg mentve: {kimeneti_titkositott}")
        
        # Visszafejtett szöveg mentése fájlba
        with open(kimeneti_visszafejtett, 'w', encoding='utf-8') as f:
            f.write(visszafejtett_szoveg)
        print(f"Visszafejtett szöveg mentve: {kimeneti_visszafejtett}")
        
    except FileNotFoundError:
        print("Hiba: A bemeneti fájl nem található! Ellenőrizd az elérési utat!")
    except Exception as e:
        print(f"Hiba történt: {e}")

# Fő program
def main():
    # Fájlnevek és eltolás bekérése
    print("Add meg a bemeneti fájl teljes elérési útját (pl. C:/Mappám/input.txt vagy ../input.txt)")
    bemeneti_fajl = input("Bemeneti fájl: ")
    kimeneti_titkositott = input("Add meg a titkosított fájl nevét/útvonalát (pl. titkosított.txt): ") or "titkosított.txt"
    kimeneti_visszafejtett = input("Add meg a visszafejtett fájl nevét/útvonalát (pl. visszafejtett.txt): ") or "visszafejtett.txt"
    
    while True:
        try:
            eltolás = int(input("Add meg az eltolás mértékét (1-25): "))
            if 1 <= eltolás <= 25:
                break
            print("Kérlek 1 és 25 közötti számot adj meg!")
        except ValueError:
            print("Kérlek érvényes számot adj meg!")
    
    # Fájl feldolgozása
    fajl_feldolgozas(bemeneti_fajl, kimeneti_titkositott, kimeneti_visszafejtett, eltolás)

# Program futtatása
if __name__ == "__main__":
    main()

# Magyarázat:
# 1. A bemeneti fájlhoz teljes elérési utat kérünk (pl. C:/Mappám/input.txt vagy relatív: ../input.txt)
# 2. A kimeneti fájlokhoz is megadható teljes útvonal, különben a Python fájl mappájába mentődnek
# 3. Windows esetén használj \\ vagy / elválasztót, Linux/Mac esetén / elválasztót
# 4. A hibakezelés jelzi, ha rossz az elérési út