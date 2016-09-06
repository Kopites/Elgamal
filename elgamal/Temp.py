
import random
from elgamal import RabinMillerModule


class CryptoUltis(object):

    class PublicKey(object):
        def __init__(self, p=None, alpha=None, Ya=None):
            self.p = p
            self.alpha = alpha
            self.Ya = Ya

    class PrivateKey(object):
        def __init__(self, p=None, alpha=None, Xa=None):
            self.p = p
            self.alpha = alpha
            self.Xa = Xa

    class CipherText(object):
        def __init__(self, C1=None, C2=None):
            self.C1 = C1
            self.C2 = C2

    def findPrimitiveRoot(self, p):
        if p == 2:
            return 1
        p1 = 2
        p2 = (p - 1) // p1

        while True:
            g = random.randrange(2, p - 1)
            if not (pow(g, (p - 1) // p1, p) == 1):
                if not (pow(g, (p - 1) // p2, p) == 1):
                    return g

    def generateKeys(self, keysize):
        rabinOjb = RabinMillerModule.RabinMiller()
        p = rabinOjb.generateLargePrime(keysize)
        alpha = self.findPrimitiveRoot(p)
        Xa = random.randrange(1, p)
        Ya = pow(alpha, Xa, p)

        publicKey = self.PublicKey(p, alpha, Ya)
        privateKey = self.PrivateKey(p, alpha, Xa)

        return {'privateKey': privateKey, 'publicKey': publicKey}

    def encrypt(self, publicKey, plainText):
        p, alpha, Ya = publicKey.p, publicKey.alpha, publicKey.Ya
        k = random.randrange(0, p)
        C1 = pow(alpha, k, p)
        C2 = (pow(Ya, k, p) * (plainText % p)) % p
        cipherText = self.CipherText(C1, C2)

        return {'cipherText': cipherText}

    def decrypt(self, privateKey, cipherText):
        p, alpha, Xa = privateKey.p, privateKey.alpha, privateKey.Xa
        C1, C2 = cipherText.C1, cipherText.C2
        R = pow(C1, p - 1- Xa, p)
        message = ((R % p) * (C2 % p)) % p

        return message


def main():

    keysize = 1024
    obj = CryptoUltis()
    keys = obj.generateKeys(keysize)
    priv = keys["privateKey"]
    publ = keys["publicKey"]

    text = 2306199411051995
    print("original Plain Text: ", text)
    # Encryption

    cipherText = obj.encrypt(publ, text)
    cipher = cipherText["cipherText"]
    print("encrypted Text: ", cipher.C1, cipher.C2)

    # Decryption
    mess = obj.decrypt(priv, cipher)
    print("sau khi giai ma: ", mess)
    return 0




str = "qu"
ans = 0
BYTE_SIZE = 256
BLOCK_SIZE = 3
id = 0
for i in str:
    ans += ord(i) * pow(BYTE_SIZE, id)
    id += 1
print(ans)


for i in range(BLOCK_SIZE - 1, -1, -1):
    asciiNumber = ans // (BYTE_SIZE ** i)
    ans = ans % (BYTE_SIZE ** i)
    print(asciiNumber)