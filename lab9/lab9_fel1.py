#9. labor: Elliptikus görbe kriptográfia

# A signatures9_1.json állományban személyek nevei és a publikus kulcsaik 
# digitális aláírása található hexa formában. A digitális aláírások

#az Edwards-curve Digital Signature Algorithm (EdDSA) rfc8032 szabvány alapján kerültek meghatározásra,
#egy központi hatóság privát kulcsát alkalmazva lettek létre hozva, 
# amelynek publikus kulcsa az publicKeyECC_CA_9_1.pem állományban található,
#nem közvetlenül a tartalomra, hanem a hash értekre voltak kiszámolva, 
# ahol az alkalmazott hash az SHA512 volt és csak a nyers (raw) tartalom került aláírásra.
#Írjunk egy programot, amely elsőlépésben hitelesíti a publicKeyECC_B_9_1.pem állományban található publikus kulcsot, 
# azaz ellenőrzi, hogy szerepel-e a digitális aláírása a signatures9_1.json állományban, és meghatározza, hogy kié. 
# Második lépésben pedig alkalmazva a privateKeyECC_A_9_1.pem állományban levő privát kulcsot 
# egy DH-ECC kulcs megosztási eljárást alkalmazva létrehoz egy 32 bájtos titkos 
# kulcsként alkalmazható bájtszekvenciát. A jelszó: pasword_A_9_1

import json
from Crypto import Random
from Crypto.Signature import eddsa
from Crypto.Hash import SHA512
from Crypto.PublicKey import ECC
from Crypto.Protocol.DH import key_agreement
from Crypto.Hash import SHAKE128

def sign_verify(message, public_key, signature):
    verifier = eddsa.new(public_key, 'rfc8032')
    h = SHA512.new(message)
    return verifier.verify(h, signature)

def check():
    with open("publicKeyECC_B_9_1.pem", "r") as f:
        temp = f.read()

    pub_key_a = ECC.import_key(temp).export_key(format='raw')
    

    with open("publicKeyECC_CA_9_1.pem", "r") as f:
        temp = f.read()

    pub_key_ca = ECC.import_key(temp)

    with open("signatures9_1.json", "r") as f:
        temp = json.load(f)

    for json_elem in temp:
        name = json_elem['name']
        signautre = json_elem['signature']
        signature = bytes.fromhex(signautre)
        try:
            sign_verify(pub_key_a, pub_key_ca, signature)
            print(name, pub_key_a.hex(), signature.hex())
        except:
            continue

def mykdf(x):
    return SHAKE128.new(x).read(32)

def key_exchange():
    with open("privateKeyECC_A_9_1.pem", "r") as f:
        temp = f.read()
    
    password = "pasword_A_9_1"
    priv_key_a = ECC.import_key(temp, passphrase=password)

    with open("publicKeyECC_B_9_1.pem", "r") as f:
        temp = f.read()
    
    pub_key_b = ECC.import_key(temp)

    shared_key = key_agreement(static_priv=priv_key_a, static_pub=pub_key_b, kdf=mykdf)

    return shared_key
    


if __name__ == "__main__":
    # try:
    check()
    key = key_exchange()
    print("key: ", key.hex())
    # except:
        # print("error")