import decimal
import math
from functools import reduce

def read_key_file(filename):
    try:
        with open(filename, 'r') as f:
            n = int(f.readline().strip())
            return n, 3  # For this attack, we know e=3
    except FileNotFoundError:
        print(f"Error: Could not find file {filename}")
        raise
    except ValueError as ve:
        print(f"Error parsing number from {filename}: {ve}")
        raise

def read_crypt_file(filename):
    try:
        with open(filename, 'rb') as f:
            content = f.read()
            # Convert bytes to integer
            return int.from_bytes(content, byteorder='big')
    except FileNotFoundError:
        print(f"Error: Could not find file {filename}")
        raise
    except ValueError as ve:
        print(f"Error parsing number from {filename}: {ve}")
        raise

def chinese_remainder_theorem(moduli, remainders):
    total = 0
    product = reduce(lambda x, y: x * y, moduli)
    
    for modulus_i, remainder_i in zip(moduli, remainders):
        p = product // modulus_i
        total += remainder_i * p * pow(p, -1, modulus_i)
    
    return total % product

def main():
    # Read public keys and ciphertexts
    n1, e1 = read_key_file('key200_1.txt')
    n2, e2 = read_key_file('key200_2.txt')
    n3, e3 = read_key_file('key200_3.txt')
    
    c1 = read_crypt_file('cryptE3_1')
    c2 = read_crypt_file('cryptE3_2')
    c3 = read_crypt_file('cryptE3_3')
    
    # Apply Chinese Remainder Theorem
    moduli = [n1, n2, n3]
    remainders = [c1, c2, c3]
    x = chinese_remainder_theorem(moduli, remainders)
    
    # Calculate cube root
    decimal.getcontext().prec = 100
    nr = math.ceil(pow(x, 1/decimal.Decimal(3)))
    
    # Convert to bytes and decode
    try:
        message = nr.to_bytes((nr.bit_length() + 7) // 8, 'big').decode('utf-8')
        print(f"Recovered message: {message}")
    except:
        print(f"Raw number: {nr}")

if __name__ == "__main__":
    main()