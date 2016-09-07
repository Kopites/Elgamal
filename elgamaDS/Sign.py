
import hashlib
import random
from elgamal import MakeElgamalKeysModule

FILE_NAME = "message.txt"

def getMD5(fileName):
    hash_md5 = hashlib.md5()
    return hash_md5.hexdigest()
def gcd(a, b):
    while b != 0:
        return gcd(b, a % b)
    return a

def naiveInverseMod(a, c):
    for b in range(0, c):
        temp = ((a % c) * (b % c)) % c
        if (temp == 1):
            return b
    return None


def signIn():
    p, alpha, Xa = 14384917, 705446, 7631169
    K = 0
    while True:
        K = random.randrange(0, p)
        if gcd(K, p - 1) == 1:
            break

    S1 = pow(alpha, K, p)
    temp = naiveInverseMod(K, p - 1)
    m = getMD5(FILE_NAME)
    M = int(m, 16)
    print("M1 = ", M)
    S2 = (temp * (M - Xa*S1) % (p - 1)) % (p - 1)
    print(S1, S2)
    return S1, S2


def main():
    FNAME1 = "message.txt"
    FNAME2 = "message1.txt"
    print(getMD5(FNAME1))
    print(getMD5(FNAME2))
    assert getMD5(FNAME1) == getMD5(FNAME2)
    #signIn()

if __name__ == '__main__':
    main()