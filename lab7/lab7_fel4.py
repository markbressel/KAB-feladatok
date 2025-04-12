import random
import time
from math import gcd

def miller_rabin(n, k=5):
    if n == 2 or n == 3:
        return True
    if n < 2 or n % 2 == 0:
        return False
    
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    
    for _ in range(k):
        a = random.randrange(2, n-1)
        x = pow(a, s, n)
        if x == 1 or x == n-1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n-1:
                break
        else:
            return False
    return True

def generate_prime(bits):
    while True:
        n = random.getrandbits(bits)
        n |= (1 << bits - 1) | 1  # Make sure it's odd and has the right bit length
        if miller_rabin(n):
            return n

def generate_keys(bits):
    p = generate_prime(bits)
    q = generate_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Public exponent
    e = 65537
    
    # Private exponent
    d = pow(e, -1, phi)
    
    return (e, n), (d, n, p, q)

def standard_decrypt(c, private_key):
    d, n, _, _ = private_key
    return pow(c, d, n)

def crt_decrypt(c, private_key):
    d, n, p, q = private_key
    
    # CRT components
    dp = d % (p - 1)
    dq = d % (q - 1)
    qinv = pow(q, -1, p)
    
    # Partial computations
    m1 = pow(c, dp, p)
    m2 = pow(c, dq, q)
    
    # Combine using CRT
    h = (qinv * (m1 - m2)) % p
    m = m2 + h * q
    
    return m

def compare_methods(message, key_size=1024):
    print(f"Comparing RSA decryption methods with {key_size}-bit key")
    
    # Generate keys
    public_key, private_key = generate_keys(key_size // 2)  # Each prime is half the key size
    e, n = public_key
    
    # Encrypt message
    c = pow(message, e, n)
    
    # Test standard decryption
    start_time = time.time()
    m1 = standard_decrypt(c, private_key)
    standard_time = time.time() - start_time
    
    # Test CRT decryption
    start_time = time.time()
    m2 = crt_decrypt(c, private_key)
    crt_time = time.time() - start_time
    
    print(f"\nResults:")
    print(f"Standard decryption time: {standard_time:.6f} seconds")
    print(f"CRT decryption time: {crt_time:.6f} seconds")
    print(f"Speedup factor: {standard_time/crt_time:.2f}x")
    print(f"Both methods give same result: {m1 == m2}")

if __name__ == "__main__":
    # Test with different message and key sizes
    message = random.getrandbits(64)
    compare_methods(message, key_size=1024)
    compare_methods(message, key_size=2048)