def create_keyword_alphabet(keyword):
    # Kulcsszó alapján egyedi ábécé létrehozása
    keyword = "".join(sorted(set(keyword.upper()), key=lambda x: keyword.upper().index(x)))  # Egyedi betűk, eredeti sorrendben
    standard_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    keyword_alphabet = keyword + "".join(c for c in standard_alphabet if c not in keyword)
    return keyword_alphabet

def caesar_titkosit(szoveg, keyword, eltolás):
    # Keyword Caesar titkosítás
    keyword_alphabet = create_keyword_alphabet(keyword)
    standard_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    titkosított = ""
    
    for karakter in szoveg:
        if karakter in standard_alphabet:
            # A standard ábécében lévő pozíció eltolása
            pozíció = standard_alphabet.index(karakter)
            új_pozíció = (pozíció + eltolás) % 26
            titkosított += keyword_alphabet[új_pozíció]
        else:
            titkosított += karakter  # Nem betű karakterek változatlanok
    return titkosított

def caesar_visszafejt(sifrat, keyword, eltolás):
    # Keyword Caesar visszafejtés
    keyword_alphabet = create_keyword_alphabet(keyword)
    standard_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    visszafejtett = ""
    
    for karakter in sifrat:
        if karakter in keyword_alphabet:
            # A kulcsszó ábécéjében lévő pozíció visszafejtése
            pozíció = keyword_alphabet.index(karakter)
            új_pozíció = (pozíció - eltolás) % 26
            visszafejtett += standard_alphabet[új_pozíció]
        else:
            visszafejtett += karakter
    return visszafejtett

def fajl_feldolgozas(bemeneti_fajl, kimeneti_titkositott, kimeneti_visszafejtett, keyword, eltolás):
    # Fájl beolvasása és feldolgozása
    try:
        # Beolvasás és nagybetűssé alakítás
        with open(bemeneti_fajl, 'r', encoding='utf-8') as f:
            eredeti_szoveg = f.read().upper()
        
        print(f"Eredeti szoveg nagybetusen:\n{eredeti_szoveg[:100]}...\n")
        
        # Titkosítás
        titkosított_szoveg = caesar_titkosit(eredeti_szoveg, keyword, eltolás)
        print(f"Titkosított szoveg:\n{titkosított_szoveg[:100]}...\n")
        
        # Visszafejtés
        visszafejtett_szoveg = caesar_visszafejt(titkosított_szoveg, keyword, eltolás)
        print(f"Visszafejtett szoveg:\n{visszafejtett_szoveg[:100]}...\n")
        
        # Titkosított szöveg mentése
        with open(kimeneti_titkositott, 'w', encoding='utf-8') as f:
            f.write(titkosított_szoveg)
        print(f"Titkosított szoveg mentve: {kimeneti_titkositott}")
        
        # Visszafejtett szöveg mentése
        with open(kimeneti_visszafejtett, 'w', encoding='utf-8') as f:
            f.write(visszafejtett_szoveg)
        print(f"Visszafejtett szoveg mentve: {kimeneti_visszafejtett}")
        
    except FileNotFoundError:
        print("Hiba: A bemeneti fajl nem talalhato! Ellenorizd az eleresi utat!")
    except Exception as e:
        print(f"Hiba tortent: {e}")

# Fő program
def main():
    # Fájlnevek, kulcsszó és eltolás bekérése
    bemeneti_fajl = input("Add meg a bemeneti fajl teljes eleresi utjat: ")
    kimeneti_titkositott = input("Add meg a titkosított fajl nevet/utvonalat: ") or "titkosított.txt"
    kimeneti_visszafejtett = input("Add meg a visszafejtett fajl nevet/utvonalat: ") or "visszafejtett.txt"
    keyword = input("Add meg a kulcsszot: ").strip()
    
    while True:
        try:
            eltolás = int(input("Add meg az eltolás merteket (0-25): "))
            if 0 <= eltolás <= 25:
                break
            print("Kerlek 0 es 25 kozotti szamot adj meg!")
        except ValueError:
            print("Kerlek ervenyes szamot adj meg!")
    
    # Fájl feldolgozása
    fajl_feldolgozas(bemeneti_fajl, kimeneti_titkositott, kimeneti_visszafejtett, keyword, eltolás)

# Program futtatása
if __name__ == "__main__":
    main()