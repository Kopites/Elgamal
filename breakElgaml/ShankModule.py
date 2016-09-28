
# break the Elgamal using Shank algorithm

import math

from elgamal import  ElgamalCipherModule
from elgamal import MakeElgamalKeysModule


class Shank(object):
    def __init__(self, keysize=0):
        self.keysize = keysize

    def genKeys(self):
        objMakeKeys = MakeElgamalKeysModule.MakeElgamalKeys()
        print("p, alpha, beta")
        objMakeKeys.generateKeys(self.keysize)

    def crack(self, p, alpha, beta):

        m = int(math.sqrt(p - 1))
        l1 = []
        for j in range(0, m):
            val = pow(alpha, m * j, p)
            l1.append(val)

        l2 = []
        for i in range(0, m):
            val = (beta * pow(alpha, i)) % p
            l2.append(val)
        res = []

        tmpx = 0
        for i in range(0, m):
            for j in range(0, m):
                if l1[i] == l2[j]:
                    x = (m * i - j) % (p - 1)
                    tmpx = x
                    res.append(x)

        if len(res) == 0:
            print("not found!")
        else:
            print(len(res))
            for x in res:
                print(x, end=" ")

        return tmpx

    def main(self):
        p, alpha, beta = 19237254,24678877,2950937
        self.crack(p, alpha, beta)
        return None

    def check(self, beta, alpha, x, p):
        assert beta == pow(alpha, x, p)
        print("passed!")

    def main(self):
        p, alpha, beta = 954829, 758750, 655544
        block_size = 128
        pubkey = (p, alpha, beta)

        message = "this is secrect message!"
        objEl = ElgamalCipherModule.ElgamalCipher()
        encryptedBlocks = objEl.encryptMessage(message, pubkey, block_size)
        print(encryptedBlocks)
        print("private key: ")
        x = self.crack(p, alpha, beta)
        privateKey = (p, alpha, x)
        decryptedText = objEl.decryptMessage(encryptedBlocks, len(message), privateKey, block_size)
        print(len(decryptedText))

        return None


if __name__ == '__main__':
    keysize = 1024
    obj = Shank(keysize)
    obj.genKeys()
    #obj.main()
    #obj.check()
