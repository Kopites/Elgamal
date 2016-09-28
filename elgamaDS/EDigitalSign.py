import hashlib
import random
import time

from elgamaDS import ElgamalCipherModule
from elgamaDS import MakeElgamalKeysModule


class Sign(object):
    def gcd(self, a, b):
        while b != 0:
            a, b = b, a % b
        return a

    def egcd(self, a, b):
        if a == 0:
            return (b, 0, 1)
        else:
            g, y, x = self.egcd(b % a, a)
            return (g, x - (b // a) * y, y)

    def modinv(self, a, m):
        g, x, y = self.egcd(a, m)
        if g != 1:
            raise Exception('modular inverse does not exist')
        else:
            return x % m

    def getMD5file(self, fileName):
        hasher = hashlib.md5()
        with open(fileName, 'rb') as afile:
            buf = afile.read()
            hasher.update(buf)
        return int(hasher.hexdigest(), 16)

    def getinput(self):
        try:
            x = input()
        except NameError as e:
            for pname, pvalue in vars(e).iteritems():
                print((pname, ": ", pvalue))
            error_string = str(e)
            x = error_string[error_string.index('\'') + 1: error_string.rfind('\'')]
        return x

    def signIn(self, PRIV_KEY, FILE_NAME):
        S = []
        p, alpha, Xa = PRIV_KEY
        K = 0
        while True:
            K = random.randrange(0, p)
            if self.gcd(K, p - 1) == 1:
                break

        M = self.getMD5file(FILE_NAME)
        S1 = pow(alpha, K, p)
        S2 = (self.modinv(K, p - 1) * (M - Xa * S1) % (p - 1)) % (p - 1)
        S.append(S1)
        S.append(S2)
        return S

    def verify(self, PUB_KEY, S, FILE_NAME):
        S1, S2 = S
        p, alpha, Ya = PUB_KEY
        M = self.getMD5file(FILE_NAME)
        V1 = pow(alpha, M, p)
        V2 = (pow(Ya, S1, p) * pow(S1, S2, p)) % p
        return V1 == V2

    def genKeys(self, KEY_SIZE):
        # Sinh cap khoa cua A va B
        start_time = time.time()
        make_key = MakeElgamalKeysModule.MakeElgamalKeys()
        print("                     1. GENREATE KEYS")
        print("+ generating keys A ...........")
        keysA = make_key.main("KeysA", KEY_SIZE)
        print("+ generating keys B ...........")
        keysB = make_key.main("KeysB", KEY_SIZE)
        print("=================== Finished generate Keys in %.4s seconds! ======================" % (
        time.time() - start_time))
        print()
        return keysA, keysB


def run():
    print("=================== ELGAMAL_DIGITAL_SIGNATURE =====================")
    KEY_SIZE = 1024
    # Sinh 2 cap khoa A & B
    sign = Sign()
    keysA, keysB = sign.genKeys(KEY_SIZE)

    #############################################################################
    # Ky vao van ban file: message.txt
    # Sinh gia tri S va ghi vao File
    pubKeyA, priKeyA = keysA
    S = sign.signIn(priKeyA, FILE_NAME="message.txt")
    S_PLAIN_FILE_NAME = "S_plain.txt"
    fo = open(S_PLAIN_FILE_NAME, "w")
    fo.write(str(S))
    fo.close()
    # Ma hoa file message.txt -> message_encrypted.txt
    # @docs: main(self, mode, key_file, file_to_encrypt_decrypt, out_file)

    ENCRYPTED_FILE_NAME = "encrypted_message.txt"
    MESSAGE_FILE_NAME = "message.txt"
    DECRYPTED_FILE_NAME = "decrypted_message.txt"
    S_CIPHER_FILE_NAME = "S_cipher.txt"
    print()

    ##############################################################################
    print("                     2. ENCRYPT MESSAGE")
    print("+ Encrypting %s ...... " % MESSAGE_FILE_NAME)
    cipherUtils = ElgamalCipherModule.ElgamalCipher()
    # Ma hoa message & S bang khoa cong khai B
    cipherUtils.main("encrypt", "KeysB_pubkey.txt", MESSAGE_FILE_NAME, ENCRYPTED_FILE_NAME)
    cipherUtils.main("encrypt", "KeysB_pubkey.txt", S_PLAIN_FILE_NAME, S_CIPHER_FILE_NAME)
    print("+ Finished encrypt %s" % MESSAGE_FILE_NAME)
    print()

    ##############################################################################
    print("                     3. DECRYPT MESSAGE")
    print("+ Decrypting %s ...... " % DECRYPTED_FILE_NAME)
    # Kiem tra chu ky
    # Giai ma message & S bang khoa bi mat B
    cipherUtils.main("decrypt", "KeysB_privkey.txt", ENCRYPTED_FILE_NAME, DECRYPTED_FILE_NAME)
    cipherUtils.main("decrypt", "KeysB_privkey.txt", S_CIPHER_FILE_NAME, S_PLAIN_FILE_NAME)

    print("+ Finished decrypt %s" % DECRYPTED_FILE_NAME)
    print()
    ###############################################################################
    print("                     4. CHECK FILE")
    while True:
        try:
            print("+ Enter File name to Check(ex:message.txt): ")
            UNKNOWN_FILE_NAME = sign.getinput()
            print("Decrypt and write to file %s" % UNKNOWN_FILE_NAME)

            if sign.verify(pubKeyA, S, UNKNOWN_FILE_NAME) == True:
                print("===> YES_Your document is safe(CIA) :) <===")
            else:
                print("===> NO_Your document is not Integrity :( <===")
            print("+ Are you want to continue(y/n)?")
            c = sign.getinput()
            if c == 'n':
                break
        except (FileNotFoundError):
            print("File %s not found exception!" % UNKNOWN_FILE_NAME)
            pass
    print("======================== ALL DONE! ========================")
    print()
    ################################################################################


if __name__ == '__main__':
    run()
