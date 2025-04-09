def gcd(a, b):
    """Legnagyobb közös osztó kiszámítása."""
    while b:
        a, b = b, a % b
    return a

def brute_force_inverse(a, b):
    """Multiplikatív inverz keresése az összes érték kipróbálásával."""
    if gcd(a, b) != 1:
        return None  # Nincs inverz, ha nem relatív prímek
    for x in range(b):
        if (a * x) % b == 1:
            return x
    return None

def extended_gcd(a, b):
    """Kiterjesztett Eukleidészi algoritmus: ax + by = gcd(a, b)."""
    if a == 0:
        return b, 0, 1
    gcd_val, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd_val, x, y

def extended_euclidean_inverse(a, b):
    """Multiplikatív inverz a kiterjesztett Eukleidészi algoritmussal."""
    g, x, _ = extended_gcd(a, b)
    if g != 1:
        return None  # Nincs inverz, ha nem relatív prímek
    return x % b  # Biztosítjuk, hogy pozitív és b-nél kisebb legyen

def is_prime(n):
    """Ellenőrzi, hogy egy szám prímszám-e."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def euler_phi(n):
    """Euler-függvény kiszámítása: relatív prímek száma n-ig."""
    result = n
    i = 2
    while i * i <= n:
        if n % i == 0:
            while n % i == 0:
                n //= i
            result = result * (i - 1) // i
        i += 1
    if n > 1:
        result = result * (n - 1) // n
    return result

def mod_pow(base, exp, mod):
    """Hatékony hatványozás modulo mod."""
    result = 1
    base %= mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result

def fermat_euler_inverse(a, b):
    """Multiplikatív inverz a kis Fermat-tétel vagy Euler-tétel alapján."""
    if gcd(a, b) != 1:
        return None  # Nincs inverz, ha nem relatív prímek
    if is_prime(b):
        # Kis Fermat-tétel: a^(b-2) mod b
        return mod_pow(a, b - 2, b)
    else:
        # Euler-tétel: a^(phi(b)-1) mod b
        phi_b = euler_phi(b)
        return mod_pow(a, phi_b - 1, b)

def main():
    # Tesztelés
    test_cases = [(5, 18), (3, 7), (10, 13), (7, 15)]
    
    for a, b in test_cases:
        print(f"\nMultiplikatív inverz keresése: a={a}, b={b}")
        
        # 1. módszer: Brute force
        result1 = brute_force_inverse(a, b)
        print(f"1. Brute force: {result1}")
        
        # 2. módszer: Kiterjesztett Eukleidészi
        result2 = extended_euclidean_inverse(a, b)
        print(f"2. Kiterjesztett Eukleidészi: {result2}")
        
        # 3. módszer: Fermat/Euler
        result3 = fermat_euler_inverse(a, b)
        print(f"3. Fermat/Euler: {result3}")
        
        # Ellenőrzés
        if result1 is not None:
            assert (a * result1) % b == 1, "Hiba a brute force-ban!"
        if result2 is not None:
            assert (a * result2) % b == 1, "Hiba az Eukleidésziben!"
        if result3 is not None:
            assert (a * result3) % b == 1, "Hiba a Fermat/Euler-ben!"

if __name__ == "__main__":
    main()