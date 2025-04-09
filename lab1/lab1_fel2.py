def caesar_visszafejt(sifrat, eltolás):
    # Függvény a szöveg visszafejtésére adott eltolással
    visszafejtett = ""
    for karakter in sifrat:
        if karakter.isalpha():  # Csak betűkre alkalmazzuk a visszafejtést
            szam = (ord(karakter) - ord('A') - eltolás) % 26
            visszafejtett += chr(szam + ord('A'))
        else:
            visszafejtett += karakter
    return visszafejtett

def megfejtes_brute_force(sifrat):
    # Az összes lehetséges kulcs kipróbálása (0-25)
    for eltolás in range(26):
        visszafejtett = caesar_visszafejt(sifrat, eltolás)
        print(f"Kulcs {eltolás}: {visszafejtett[:50]}...")  # Első 50 karakter kiírása
        # Ellenőrizzük, hogy értelmes-e (manuálisan kell megvizsgálni)
    return None  # A kulcsot manuálisan kell kiválasztani az értelmes szöveg alapján

# A titkosított szöveg
titkos_szoveg = """GUR TERRXF BS GUR PYNFFVPNY REN ZNQR FRIRENY ABGNOYR PBAGEVOHGVBAF GB FPVRAPR NAQ URYCRQ YNL GUR SBHAQNGVBAF BS FRIRENY JRFGREA FPVRAGVSVP GENQVGVBAF, YVXR CUVYBFBCUL, UVFGBEVBTENCUL NAQ ZNGURZNGVPF. GUR FPUBYNEYL GENQVGVBA BS GUR TERRX NPNQRZVRF JNF ZNVAGNVARQ QHEVAT EBZNA GVZRF JVGU FRIRENY NPNQRZVP VAFGVGHGVBAF VA PBAFGNAGVABCYR, NAGVBPU, NYRKNAQEVN NAQ BGURE PRAGERF BS TERRX YRNEAVAT JUVYR RNFGREA EBZNA FPVRAPR JNF RFFRAGVNYYL N PBAGVAHNGVBA BS PYNFFVPNY FPVRAPR. TERRXF UNIR N YBAT GENQVGVBA BS INYHVAT NAQ VAIRFGVAT VA CNVQRVN (RQHPNGVBA). CNVQRVN JNF BAR BS GUR UVTURFG FBPVRGNY INYHRF VA GUR TERRX NAQ URYYRAVFGVP JBEYQ JUVYR GUR SVEFG RHEBCRNA VAFGVGHGVBA QRFPEVORQ NF N HAVIREFVGL JNF SBHAQRQ VA PBAFGNAGVABCYR NAQ BCRENGRQ VA INEVBHF VAPNEANGVBAF."""

# Tesztelés
print("Az összes lehetséges visszafejtés kipróbálása:")
megfejtes_brute_force(titkos_szoveg)