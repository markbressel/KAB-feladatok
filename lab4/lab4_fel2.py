def xor_files(file1, file2, output_file):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
        data1 = f1.read()
        data2 = f2.read()
        
        min_len = min(len(data1), len(data2))
        result = bytes(a ^ b for a, b in zip(data1[:min_len], data2[:min_len]))
        
        with open(output_file, 'wb') as out:
            out.write(result)

# Kulcs visszanyerése a képekből
xor_files('lab4\Fajlok\OTP_Massag.jpg', 'lab4\Fajlok\cryptOTP_Massag', 'recovered_key')

# A cryptHB visszafejtése a kulccsal
xor_files('lab4\Fajlok\cryptHB', 'recovered_key', 'decrypted_HB.docx')