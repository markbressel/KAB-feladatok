import numpy as np
from pathlib import Path

def hill_decrypt_block(cipher_block, inv_key_matrix):
    """Decrypt a single block using Hill cipher"""
    cipher_vec = np.array([byte for byte in cipher_block])
    plain_vec = np.dot(inv_key_matrix, cipher_vec) % 256
    return bytes([int(x) for x in plain_vec])

def cbc_hill_decrypt(input_file, output_file, key_matrix, iv):
    """Main decryption function for CBC mode with Hill cipher"""
    try:
        # Convert key to numpy array and get block size
        key_matrix = np.array(key_matrix).reshape(2, 2)
        block_size = 2  # Since we're using 2x2 matrix
        
        # Calculate inverse matrix mod 256
        det = int(round(np.linalg.det(key_matrix)))
        det_inv = pow(det, -1, 256)
        inv_key_matrix = (det_inv * np.round(det * np.linalg.inv(key_matrix))).astype(int) % 256
        
        # Read encrypted file
        with open(input_file, 'rb') as f:
            cipher_data = f.read()
        
        # Split into blocks
        blocks = [cipher_data[i:i+block_size] for i in range(0, len(cipher_data), block_size)]
        
        # CBC decryption
        decrypted_data = bytearray()
        prev_block = bytes(iv)
        
        for block in blocks:
            if len(block) < block_size:
                block = block.ljust(block_size, b'\x00')
            
            decrypted_block = hill_decrypt_block(block, inv_key_matrix)
            plain_block = bytes([d ^ p for d, p in zip(decrypted_block, prev_block)])
            decrypted_data.extend(plain_block)
            prev_block = block
        
        # Write decrypted data
        with open(output_file, 'wb') as f:
            f.write(decrypted_data)
        
        # Verify GIF signature
        with open(output_file, 'rb') as f:
            magic = f.read(6)
            if magic[:3] == b'GIF' and magic[3:6] in [b'87a', b'89a']:
                print(f"Success! Decrypted GIF saved to {output_file}")
            else:
                print("Warning: Output doesn't appear to be a valid GIF file")
                
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Given parameters
    key_matrix = [27, 131, 22, 101]  # 2x2 matrix flattened
    iv = [129, 131]  # Initialization vector
    
    # File paths
    input_file = 'lab5\Fajlok\cryptHillCBC_TheCircleIsComplete'
    output_file = 'lab5\Fajlok\decrypted.gif'
    
    # Perform decryption
    cbc_hill_decrypt(input_file, output_file, key_matrix, iv)