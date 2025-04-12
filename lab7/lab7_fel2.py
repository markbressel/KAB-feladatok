from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
import math

def fermat_factorization(n):
    a = math.isqrt(n) + 1
    b2 = a*a - n
    while not math.isqrt(b2) ** 2 == b2:
        a += 1
        b2 = a*a - n
    b = math.isqrt(b2)
    return a + b, a - b

# Read the RSA public key
with open('RSA_pubKey7_2.pem', 'rb') as f:
    pub_key = RSA.import_key(f.read())

# Factorize n to get p and q
p, q = fermat_factorization(pub_key.n)

# Create private key components
n = pub_key.n
e = pub_key.e
d = pow(e, -1, (p-1)*(q-1))

# Create private key
priv_key = RSA.construct((n, e, d))
cipher_rsa = PKCS1_OAEP.new(priv_key)

# Read and decrypt the AES key
with open('cryptedAESkey7_2.txt', 'r') as f:
    encrypted_aes_key = bytes.fromhex(f.read().strip())
aes_key = cipher_rsa.decrypt(encrypted_aes_key)

# Read the encrypted file
with open('crypted7_2.png', 'rb') as f:
    data = f.read()

# Extract components
nonce = data[:12]
ciphertext = data[12:-16]
tag = data[-16:]

# Create cipher and decrypt
cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
cipher.update(b'AES_GCMEncryption 2025.04.01')
plaintext = cipher.decrypt_and_verify(ciphertext, tag)

# Save the decrypted file
with open('decrypted7_2.png', 'wb') as f:
    f.write(plaintext)

print("Decryption completed. File saved as 'decrypted7_2.png'")