import sys
from collections import defaultdict

def get_letter_positions(text):
    """Betűk pozícióinak meghatározása egy szövegben."""
    positions = defaultdict(list)
    for i, char in enumerate(text):
        if char.isalpha():
            positions[char].append(i)
    return positions

def create_mapping(ciphertext, plaintext):
    """Helyettesítési térkép létrehozása titkosított és nyílt szöveg alapján."""
    if len(ciphertext) != len(plaintext):
        return None
    mapping = {}
    reverse_mapping = {}
    for c, p in zip(ciphertext, plaintext):
        if c.isalpha():
            if c in mapping and mapping[c] != p:
                return None  # Inkonzisztens térkép
            if p in reverse_mapping and reverse_mapping[p] != c:
                return None  # Nem egyértelmű
            mapping[c] = p
            reverse_mapping[p] = c
    return mapping

def decrypt(ciphertext, mapping):
    """Szöveg visszafejtése a térkép alapján."""
    return ''.join(mapping.get(c, c) for c in ciphertext)

def solve_case(lines):
    """Egy teszteset megoldása."""
    target = "the quick brown fox jumps over the lazy dog"
    target_positions = get_letter_positions(target)
    
    # Keressük a cél szöveg titkosított változatát
    for candidate in lines:
        if len(candidate) != len(target):
            continue
        candidate_positions = get_letter_positions(candidate)
        
        # Ellenőrizzük, hogy a betűismétlések megfelelnek-e
        valid = True
        for char, pos_list in target_positions.items():
            found = False
            for c in candidate_positions:
                if len(candidate_positions[c]) == len(pos_list):
                    found = True
                    break
            if not found:
                valid = False
                break
        
        if not valid:
            continue
        
        # Próbáljuk létrehozni a térképet
        mapping = create_mapping(candidate, target)
        if mapping is None:
            continue
        
        # Ellenőrizzük az összes sort a térképpel
        all_valid = True
        for line in lines:
            decrypted = decrypt(line, mapping)
            if not all(c.isalpha() or c == ' ' for c in decrypted):
                all_valid = False
                break
        
        if all_valid:
            return target
    
    return "No solution"

def main():
    # Bemenet olvasása
    lines = sys.stdin.read().splitlines()
    n = int(lines[0])  # Tesztesetek száma
    test_cases = []
    current_case = []
    
    # Tesztesetek szétválasztása
    for line in lines[2:]:  # 2-től kezdve, mert 0: n, 1: üres
        if line.strip() == "":
            if current_case:
                test_cases.append(current_case)
                current_case = []
        else:
            current_case.append(line.strip())
    if current_case:
        test_cases.append(current_case)
    
    # Tesztesetek megoldása
    results = []
    for case in test_cases:
        result = solve_case(case)
        results.append(result)
    
    # Kimenet
    print("\n".join(results))
    print()  # Extra üres sor a végén

if __name__ == "__main__":
    main()