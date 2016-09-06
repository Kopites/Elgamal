# This is my tries

from elgamal import Temp


def main():
    # sinh khoa voi do dai = key size
    keysize = 1024
    cryptoUtils = Temp.CryptoUltis()
    keys = cryptoUtils.generateKeys(keysize)
    priv = keys["privateKey"]
    publ = keys["publicKey"]

    message = 1234567899876543212322222222222222222221231
    # Thuc hien ma hoa

    cipherTextTemp = cryptoUtils.encrypt(publ, message)
    cipherText = cipherTextTemp["cipherText"]
    print("encrypted text = ", cipherText.C1, " --",  cipherText.C2)

    # Thuc hien giai ma
    plainText = cryptoUtils.decrypt(priv, cipherText)
    print("decrypted text = ", plainText)

    assert (message == plainText)
    return 0

if __name__ == '__main__':
    main()