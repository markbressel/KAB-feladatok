def caesar_visszafejt(sifrat, eltolás):
    # Az 54 szimbólum definiálása
    szimbólumok = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ? "
    
    visszafejtett = ""
    for karakter in sifrat:
        if karakter in szimbólumok:
            pozíció = szimbólumok.index(karakter)
            új_pozíció = (pozíció - eltolás) % 54
            visszafejtett += szimbólumok[új_pozíció]
        else:
            visszafejtett += karakter
    return visszafejtett

def ervenyes_szoveg_e(szoveg):
    # Ellenőrzi, hogy a szöveg csak a 54 szimbólumot tartalmazza
    szimbólumok = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ? ")
    if not all(karakter in szimbólumok for karakter in szoveg):
        return False
    # Ellenőrzi, hogy tartalmaz-e gyakori angol szavakat vagy elég szóközt
    szavak = szoveg.lower().split()
    gyakori_szavak = {"the", "is", "a", "and", "to", "of", "in", "that", "it", "for"}
    return sum(szo in gyakori_szavak for szo in szavak) >= 2 and szoveg.count(" ") >= 5

def megfejtes_brute_force(sifrat):
    # Az összes lehetséges kulcs kipróbálása (0-53)
    print(f"Titkosított szöveg (első 100 karakter): {sifrat[:100]}...")
    for eltolás in range(54):
        visszafejtett = caesar_visszafejt(sifrat, eltolás)
        print(f"Kulcs {eltolás}: {visszafejtett[:100]}...")
        if ervenyes_szoveg_e(visszafejtett):
            print(f"\n*** Megtalált kulcs: {eltolás} ***")
            print(f"Visszafejtett szöveg:\n{visszafejtett}")
            return eltolás, visszafejtett
    print("Nem található érvényes szöveg a lehetséges kulcsok között!")
    return None, None

# Fő program
def main():
    # Közvetlenül a megadott szöveg használata
    titkos_szoveg = """rEVwFPwzOVMQLDOxMEVwFKQBOBPQFKDvwaFOPQIVwzOVMQLDOxMEVwFPwxwzIxPPFzxIwPRyGBzQwTFQEwxwCxPzFKxQFKDwEFPQLOVw KzOVMQFLKwQBzEKFNRBPwExSBwyBBKwRPBAwPFKzBwxKzFBKQwQFJBPwyRQwQEBwMOLQBzQFLKwxDxFKPQwBUMLPROBwTxPwPLJBQFJBPwARyFLRPwxKAwJxKVwzFMEBOPwTBOBwyOLHBKwoEBwABPFDKwLCwKBTwzFMEBOPwxKAwQEBwzxMxyFIFQVwQLwxKxIVWBwxKAwyOBxHwQEBJwzLBSLISBAwLSBOwQFJBwnFKzBwQEBKwQEBwQBzEKFNRBPwExSBwyBBKwxAxMQBAwQLwMOLDOBPPwFKwzOVMQxKxIVPFPwxKAwQLwQEBwzLJMRQFKDwMLTBOwxSxFIxyIBwhLABOKwzOVMQLDOxMEVwDLBPwyBVLKAwzLKCFABKQFxIFQVwxIPLwxAAOBPPFKDwxPMBzQPwPRzEwxPwAxQxwFKQBDOFQVwxRQEBKQFzxQFLKwKLKOBMRAFxQFLKwxKAwLQEBOwPBzROFQVwLyGBzQFSBPwoEBwPRyGBzQwKLTwFKzIRABPwxIIwJxQEBJxQFzxIwQBzEKFNRBPwOBIxQFKDwQLwFKCLOJxQFLKwPBzROFQVwnBzLKAIVwzOVMQLDOxMEVwFPwzILPBIVwzLKKBzQBAwQLwPBSBOxIwCFBIAPwLCwJxQEBJxQFzPwxKAwzLJMRQBOwPzFBKzBwMOLSFAFKDwFKQBOBPQFKDwxMMIFzxQFLKPwCLOwJxKVwQEBLOBQFzxIwOBPRIQPwxKAwPQFJRIxQFKDwJxQEBJxQFzxIwOBPBxOzEwZOVMQLDOxMEVwTEFzEwTBwRPBwxPwxKwRJyOBIIxwQBOJwCLOwQEBwCFBIAwFKzIRAFKDwzOVMQxKxIVPFPwFPwIFKHBAwQLwxPMBzQPwLCwAFPzOBQBwJxQEBJxQFzPwKRJyBOwQEBLOVwxIDByOxwMOLyxyFIFQVwQEBLOVwPQxQFPQFzPwFKCLOJxQFLKwxKAwzLAFKDwQEBLOVwoEFOAIVwzOVMQLDOxMEVwExPwyBzLJBwxwHBVwQBzEKLILDVwQExQwFPwRPBAwRyFNRFQLRPIVwFKwzLJMRQBOwPVPQBJPwCOLJwPJxIIwABSFzBPwQLwIxODBwPBOSBOPwxKAwKBQTLOHPwoEBwJRIQFQRABwLCwPBzROFQVwQEOBxQPwFPwAOFSFKDwQEBwQOBKAwQLwMOLQBzQwAxQxwTEBKBSBOwMLPPFyIBwyBwFQwCLOwPQLOxDBwLOwAROFKDwQOxKPJFPPFLKwLSBOwKBQTLOHPwoEBwOBxABOwPELRIAwyBwTxOKBAwELTBSBOwQExQwOBxITLOIAwPBzROFQVwFPwxwzLJMIBUwMOLzBPPwFKwTEFzEwzOVMQLDOxMEVwzLKQOFyRQBPwLKIVwQEBwMOFJFQFSBPwxIDLOFQEJPwxKAwPzEBJBPwdKwMOxzQFzBwxQQxzHPwLCQBKwBUMILFQwMOLQLzLIwLOwFJMIBJBKQxQFLKwCIxTPwTBxHwMxPPTLOAPwLOwKBDIFDBKQwRPBOPwaROQEBOJLOBwQEBwPBzROFQVwDRxOxKQBBPwLCCBOBAwyVwzOVMQLDOxMEVwzxKKLQwyBwRKzLKAFQFLKxIwoEBwPBzROFQVwMOLSFABAwABMBKAPwLKwQEBwMLTBOwLCwxASBOPxOFBPwQEBFOwzLJMRQFKDwOBPLROzBPwxKAwQEBwQFJBwxSxFIxyIBwCLOwxKwxQQxzHwxPwTBIIwxPwLKwRKABOIVFKDwzLJMRQxQFLKxIwMOLyIBJPwTEFzEwxOBwyBIFBSBAwQLwyBwExOA"""
    
    kulcs, visszafejtett = megfejtes_brute_force(titkos_szoveg)
    if kulcs is not None:
        with open("visszafejtett.txt", "w", encoding="utf-8") as f:
            f.write(visszafejtett)
        print(f"Az eredeti szöveg mentve: visszafejtett.txt, kulcs: {kulcs}")
    else:
        print("További hibakeresés szükséges.")

if __name__ == "__main__":
    main()