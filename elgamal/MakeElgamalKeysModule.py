import os, sys, random
from elgamal import RabinMillerModule

NAME = "Elgamal"
KEY_SIZE = 1024

class MakeElgamalKeys(object):

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
        #alpha = self.findPrimitiveRoot(p)
        alpha = random.randrange(1, p - 1)
        Xa = random.randrange(1, p)
        Ya = pow(alpha, Xa, p)

        publicKey = (p, alpha, Ya)
        privateKey = (p, alpha, Xa)

        print("Public key : ", publicKey)
        print("Private key: ", privateKey)
        return (publicKey, privateKey)

    def makeKeyFiles(self, name, keySize):

        if os.path.exists('%s_pubkey.txt' % (name)) or os.path.exists('%s_privkey.txt' % (name)):
            sys.exit(
                'WARNING: The file %s_pubkey.txt or %s_privkey.txt already exists! Use a different name or delete these files and re-run this program.' % (
                name, name))


        publicKey, privateKey = self.generateKeys(keySize)

        print('The public key is a %s and a %s digit number.' % (len(str(publicKey[0])), len(str(publicKey[1]))))
        print('Writing public key to file %s_pubkey.txt...' % (name))
        fo = open('%s_pubkey.txt' % (name), 'w')
        fo.write('%s,%s,%s,%s' % (keySize, publicKey[0], publicKey[1], publicKey[2]))
        fo.close()

        print()
        print('The private key is a %s and a %s digit number.' % (len(str(publicKey[0])), len(str(publicKey[1]))))
        print('Writing private key to file %s_privkey.txt...' % (name))
        fo = open('%s_privkey.txt' % (name), 'w')
        fo.write('%s,%s,%s,%s' % (keySize, privateKey[0], privateKey[1], privateKey[2]))
        fo.close()

def main():
    print("Make Elgamal keys  ...")
    objMakeKey = MakeElgamalKeys()
    objMakeKey.makeKeyFiles(NAME, KEY_SIZE)
    print("Key file made.")
if __name__ == '__main__':
    main()

