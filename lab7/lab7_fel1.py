import random
import string
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.number import getPrime, bytes_to_long, long_to_bytes

def generate_random_text(max_length):
    length = random.randint(max_length // 2, max_length)
    return ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length))

def basic_rsa_encrypt(message, e, n):
    m = bytes_to_long(message.encode())
    return pow(m, e, n)

def basic_rsa_decrypt(ciphertext, d, n):
    m = pow(ciphertext, d, n)
    return long_to_bytes(m).decode()

# Generate RSA key pair
key = RSA.generate(2048)
n = key.n
e = key.e
d = key.d

# Generate random text that fits within RSA modulus
max_text_length = (key.size_in_bits() // 8) - 11  # Leaving space for OAEP padding
plaintext = generate_random_text(max_text_length)
print(f"Original text: {plaintext}")

# Basic RSA encryption (multiple times)
print("\nBasic RSA encryption (multiple attempts):")
for i in range(3):
    encrypted = basic_rsa_encrypt(plaintext, e, n)
    print(f"Attempt {i+1}: {hex(encrypted)}")
    decrypted = basic_rsa_decrypt(encrypted, d, n)
    assert decrypted == plaintext

# RSA-OAEP encryption (multiple times)
print("\nRSA-OAEP encryption (multiple attempts):")
cipher = PKCS1_OAEP.new(key)
for i in range(3):
    encrypted = cipher.encrypt(plaintext.encode())
    print(f"Attempt {i+1}: {encrypted.hex()}")
    decrypted = PKCS1_OAEP.new(key).decrypt(encrypted).decode()
    assert decrypted == plaintext

print("\nObservation:")
print("Basic RSA encryption produces the same ciphertext every time (deterministic)")
print("RSA-OAEP produces different ciphertexts due to random padding (non-deterministic)")