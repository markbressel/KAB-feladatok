#8. labor: a Diffie-Hellman kulcscsere, digitális aláírások

#Ha tudjuk, hogy a Diffie-Hellman kulcscseréhez szükséges prímszám a generatorsDH.txt állomány első értéke 
# és ha a generátor elem a további értékek közül valamelyik, szimuláljuk a Diffie-Hellman kulcscsét, 
# majd a meghatározott értéket az AES titkosító kulcsaként alkalmazva, 
# titkosítsunk és fejtsünk vissza egy nagyobb méretű állományt.

def read_file():
    with open("generatorsDH.txt", "r") as f:
        temp = f.read()
    
    lines = temp.split("\n")
    p = int(lines[0])
    q = (p-1)//2

    for line in lines[2:]:
        g = int(line)
        if pow(g, q, p) == 1:
            return g

if __name__ == "__main__":
    g = read_file()
    print(g)