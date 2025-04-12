import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
import binascii

def find_password():
    target_hash = "591a6e49ad819403426545301221da1764be6c58727b18831cc7d4bf8dbff4e9"
    passwords = ["myPassword000", "problem7_6", "password2025", "myPass2025", "password7_6"]
    
    for password in passwords:
        if hashlib.sha256(password.encode()).hexdigest() == target_hash:
            return password
    return None

def decrypt_aes_key(private_key_path, password, encrypted_key_path):
    # Read encrypted AES key
    with open(encrypted_key_path, 'r') as f:
        encrypted_key = binascii.unhexlify(f.read().strip())
    
    # Load and decrypt private key
    with open(private_key_path, 'rb') as f:
        private_key = RSA.import_key(f.read(), passphrase=password)
    
    # Create cipher and decrypt
    cipher = PKCS1_OAEP.new(private_key)
    aes_key = cipher.decrypt(encrypted_key)
    return aes_key

def decrypt_image(encrypted_file_path, aes_key, output_path):
    # Read encrypted file
    with open(encrypted_file_path, 'rb') as f:
        data = f.read()
    
    # Extract IV and ciphertext
    iv = data[:16]
    ciphertext = data[16:]
    
    # Create cipher and decrypt
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(ciphertext)
    
    # Write decrypted image
    with open(output_path, 'wb') as f:
        f.write(decrypted_data)

def main():
    # Find correct password
    password = find_password()
    if not password:
        print("Password not found!")
        return
    
    # Decrypt AES key
    aes_key = decrypt_aes_key(
        'RSA_privKey7_6.pem',
        password,
        'cryptedAESkey7_6.txt'
    )
    
    # Decrypt image
    decrypt_image(
        'crypted7_6.jpg',
        aes_key,
        'decrypted7_6.jpg'
    )
    print("Image decrypted successfully!")

if __name__ == "__main__":
    main()