
import sys
import random

DEFAULT_BLOCK_SIZE = 128 # 128 bytes
BYTE_SIZE = 256 # One byte has 256 different values.

class ElgamalCipher(object):
    def main(self):
        filename = 'encrypted_file.txt' # the file to write to/read from
        mode = 'decrypt'

        if mode == 'encrypt':
            fo = open("message.txt", "r")
            message = fo.read()
            fo.close()
            pubKeyFilename = 'Elgamal_pubkey.txt'
            print('Encrypting and writing to %s...' % (filename))
            encryptedText = self.encryptAndWriteToFile(filename, pubKeyFilename, message)

            print('Encrypted text:')
            print(encryptedText)

        elif mode == 'decrypt':
            privKeyFilename = 'Elgamal_privkey.txt'
            print('Reading from %s and decrypting...' % (filename))
            decryptedText = self.readFromFileAndDecrypt(filename, privKeyFilename)

            print('Decrypted text:')
            print(decryptedText)

    def getBlocksFromText(self, message, blockSize=DEFAULT_BLOCK_SIZE):
        # Converts a string message to a list of block integers. Each integer
        # represents 128 bytes

        messageBytes = message.encode('ascii') # convert the string to bytes
        blockInts = []
        for blockStart in range(0, len(messageBytes), blockSize):
            # Calculate the block integer for this block of text
            blockInt = 0
            for i in range(blockStart, min(blockStart + blockSize, len(messageBytes))):
                blockInt += messageBytes[i] * (BYTE_SIZE ** (i % blockSize))
            blockInts.append(blockInt)
        return blockInts

    def getTextFromBlocks(self, blockInts, messageLength, blockSize=DEFAULT_BLOCK_SIZE):

        message = []
        for blockInt in blockInts:
            blockMessage = []
            for i in range(blockSize - 1, -1, -1):
                if len(message) + i < messageLength:
                    asciiNumber = blockInt // (BYTE_SIZE ** i)
                    blockInt = blockInt % (BYTE_SIZE ** i)
                    blockMessage.insert(0, chr(asciiNumber))

            message.extend(blockMessage)
        return ''.join(message)

    def encryptMessage(self, message, publicKey, blockSize=DEFAULT_BLOCK_SIZE):

        encryptedBlocks = []
        p, alpha, Ya = publicKey

        for block in self.getBlocksFromText(message, blockSize):
            k = random.randrange(0, p)
            C1 = pow(alpha, k, p)
            C2 = (pow(Ya, k, p) * (block % p)) % p
            encryptedBlocks.append(C1)
            encryptedBlocks.append(C2)
        return encryptedBlocks

    def decryptMessage(self, encryptedBlocks, messageLength, privateKey, blockSize=DEFAULT_BLOCK_SIZE):

        decryptedBlocks = []
        p, alpha, Xa = privateKey
        for i in range(0, len(encryptedBlocks), 2):
            C1 = int(encryptedBlocks[i])
            C2 = int(encryptedBlocks[i + 1])
            R = pow(C1, p - 1 - Xa, p)
            M = ((R % p) * (C2 % p)) % p
            decryptedBlocks.append(M)

        return self.getTextFromBlocks(decryptedBlocks, messageLength, blockSize)

    def readKeyFile(self, keyFilename):
        # Given the filename of a file that contains a public or private key,
        # return the key as a (q, alpha, Xa) or (q, alpha, Ya) triple value.
        fo = open(keyFilename)
        content = fo.read()
        fo.close()
        keySize, q, alpha, XaorYa = content.split(',')
        return (int(keySize), int(q), int(alpha), int(XaorYa))


    def encryptAndWriteToFile(self, messageFilename, keyFilename, message, blockSize=DEFAULT_BLOCK_SIZE):

        keySize, q, alpha, Ya = self.readKeyFile(keyFilename)

        # Check that key size is greater than block size.
        if keySize < blockSize * 8: # * 8 to convert bytes to bits
            sys.exit('ERROR: Block size is %s bits and key size is %s bits. The Elgamal cipher requires the block size to be equal to or greater than the key size. Either decrease the block size or use different keys.' % (blockSize * 8, keySize))


        # Encrypt the message
        encryptedBlocks = self.encryptMessage(message, (q, alpha, Ya), blockSize)

        # Convert the large int values to one string value.
        for i in range(len(encryptedBlocks)):
            encryptedBlocks[i] = str(encryptedBlocks[i])
        encryptedContent = ','.join(encryptedBlocks)

        # Write out the encrypted string to the output file.
        encryptedContent = '%s_%s_%s' % (len(message), blockSize, encryptedContent)

        fo = open(messageFilename, 'w')
        fo.write(encryptedContent)
        fo.close()
        # Also return the encrypted string.
        return encryptedContent


    def readFromFileAndDecrypt(self, messageFilename, keyFilename):

        keySize, q, alpha, Xa = self.readKeyFile(keyFilename)

        # Read in the message length and the encrypted message from the file.
        fo = open(messageFilename)
        content = fo.read()
        messageLength, blockSize, encryptedMessage = content.split('_')
        messageLength = int(messageLength)
        blockSize = int(blockSize)

        # Check that key size is greater than block size.
        if keySize < blockSize * 8: # * 8 to convert bytes to bits
            sys.exit('ERROR: Block size is %s bits and key size is %s bits. The Elgamal cipher requires the block size to be equal to or greater than the key size. Did you specify the correct key file and encrypted file?' % (blockSize * 8, keySize))

        # Convert the encrypted message into large int values.
        encryptedBlocks = []
        for block in encryptedMessage.split(','):
            encryptedBlocks.append(int(block))

        # Decrypt the large int values.
        return self.decryptMessage(encryptedBlocks, messageLength, (q, alpha, Xa), blockSize)


def main():
    objElgamalCipher = ElgamalCipher()
    objElgamalCipher.main()
if __name__ == '__main__':
    main()