import string

def caesar_cipher(text, shift):
    result = []
    for char in text:
        if char.isalpha():
            shifted = chr((ord(char.upper()) - 65 + shift) % 26 + 65)
            result.append(shifted.lower() if char.islower() else shifted)
        else:
            result.append(char)
    return ''.join(result)

def score_text(text):
    common_words = ['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'i', 'it']
    score = 0
    words = text.lower().split()
    for word in words:
        if word in common_words:
            score += 1
    return score

def decrypt_text(cipher_text, keyword_list):
    best_score = -float('inf')
    best_decrypted = ''
    best_keyword = ''
    best_shift = 0

    for keyword in keyword_list:
        for shift in range(1, 26):  # Caesar cipher shift
            decrypted = caesar_cipher(cipher_text, shift)
            score = score_text(decrypted)
            if score > best_score:
                best_score = score
                best_decrypted = decrypted
                best_keyword = keyword
                best_shift = shift
    
    return best_decrypted, best_score, best_keyword, best_shift

def main():
    cipher_text = "TJC VRCCFS NO TJC KIASSBKAI CRA LAEC SCZCRAI MNTADICKNMTRBDXTBNMS TN SKBCMKC AME JCIPCE IAG TJC ONXMEATBNMS NO SCZCRAI UCSTCRM SKBCMTBOBK TRAEBTBNMS, IBFC PJBINSNPJG, JBSTNRBNVRAPJG AME LATJCLATBKS"
    keyword_list = ["SECRET", "CIPHER", "KEY", "CODE", "CRYPTO", "DECODE", "ENCRYPT"]  # Additional keywords

    decrypted_text, score, keyword, shift = decrypt_text(cipher_text, keyword_list)

    print(f"Legjobb kulcsszó: {keyword}, Eltolás: {shift}, Pontszám: {score}")
    print(f"Dekódolt szöveg (első 200 karakter): {decrypted_text[:200]}")

if __name__ == "__main__":
    main()
