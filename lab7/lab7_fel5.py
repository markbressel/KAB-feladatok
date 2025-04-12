import os

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

# Read keys from files
def read_key_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        return tuple(map(int, lines))

# Read binary file as a single integer
def read_encrypted_file(filename):
    with open(filename, 'rb') as f:
        data = f.read()
    return int.from_bytes(data, byteorder='big')

# Main decryption function
def decrypt_double_rsa():
    # Read keys
    n, e = read_key_file('key_e.txt')
    n2, f = read_key_file('key_f.txt')
    assert n == n2, "Moduli must be equal"

    # Read encrypted files
    cnr1 = read_encrypted_file('RSAcr1')
    cnr2 = read_encrypted_file('RSAcr2')

    # Calculate x and y using extended Euclidean algorithm
    _, x, y = extended_gcd(e, f)

    # Calculate original message
    msg_int = pow(cnr1, x, n) * pow(cnr2, y, n) % n

    # Convert to bytes and decode
    msg_bytes = msg_int.to_bytes((msg_int.bit_length() + 7) // 8, byteorder='big')
    return msg_bytes.decode('utf-8')

if __name__ == '__main__':
    try:
        original_text = decrypt_double_rsa()
        print(f"Decrypted message: {original_text}")
    except Exception as e:
        print(f"Error occurred: {e}")