import random
import tkinter

keyLength = 1024
G_result = []


def fastExpMod(b, e, m):
    result = 1
    while e != 0:
        if (e % 2) == 1:
            result = (result * b) % m
        e //= 2
        b = (b * b) % m
    return result


def primeTest(n):
    q = n - 1
    k = 0
    while q % 2 == 0:
        k += 1;
        q /= 2
    a = random.randint(2, n - 2);
    if fastExpMod(a, q, n) == 1:
        return "inconclusive"
    for j in range(0, k):
        if fastExpMod(a, (2 ** j) * q, n) == n - 1:
            return "inconclusive"
    return "composite"


def findPrime(halfkeyLength):
    while True:
        n = random.randint(0, 2 * halfkeyLength)
        if n % 2 != 0:
            found = True
            for i in range(0, 10):
                if primeTest(n) == "composite":
                    found = False
                    break
            if found:
                return n


def extendedGCD(a, b):
    if b == 0:
        return (1, 0, a)
    x1 = 1
    y1 = 0
    x2 = 0
    y2 = 1
    while b != 0:
        q = a / b
        r = a % b
        a = b
        b = r
        x = x1 - q * x2
        x1 = x2
        x2 = x
        y = y1 - q * y2
        y1 = y2
        y2 = y
    return (x1, y1, a)


def selectE(fn, halfkeyLength):
    while True:
        e = random.randint(0, 2 * halfkeyLength)
        (x, y, r) = extendedGCD(e, fn)
        if r == 1:
            return e


def computeD(fn, e):
    (x, y, r) = extendedGCD(fn, e)
    if y < 0:
        return fn + y
    return y


def RandomKey():
    p = findPrime(keyLength / 2)
    q = findPrime(keyLength / 2)
    n = p * q
    fn = (p - 1) * (q - 1)
    e = selectE(fn, keyLength / 2)
    d = computeD(fn, e)
    # return (n, e, d)
    N.set(n)
    E.set(e)
    D.set(d)


def encrypt():
    global G_result
    result = []
    for char in plaintext.get():
        result.append(fastExpMod(ord(char), int(E.get()), int(N.get())))
    cyphertext.set(result)
    G_result = result


def decrypt():
    global G_result
    result = ''
    for c in G_result:
        result += (chr(fastExpMod(c, int(D.get()), int(N.get()))))
    decyphertext.set(result)


root = tkinter.Tk()
root.title("RSA")

tkinter.Label(root, text="RSA").pack()

fm1 = tkinter.Frame(root)
fm2 = tkinter.Frame(root)
fm3 = tkinter.Frame(root)
fm4 = tkinter.Frame(root)
fm5 = tkinter.Frame(root)
fm6 = tkinter.Frame(root)

tkinter.Label(fm1, text="n: ").pack(side=tkinter.LEFT)
N = tkinter.StringVar()
tkinter.Entry(fm1, textvariable=N, width=20).pack(side=tkinter.LEFT)
tkinter.Label(fm1, text="e: ").pack(side=tkinter.LEFT)
E = tkinter.StringVar()
tkinter.Entry(fm1, textvariable=E, width=20).pack(side=tkinter.LEFT)
tkinter.Label(fm1, text="d: ").pack(side=tkinter.LEFT)
D = tkinter.StringVar()
tkinter.Entry(fm1, textvariable=D, width=20).pack(side=tkinter.LEFT)

tkinter.Button(fm2, text="random key", fg="blue", bd=2, width=20, command=RandomKey).pack()

tkinter.Label(fm3, width=15, text="plaintext: ").pack(side=tkinter.LEFT)
plaintext = tkinter.StringVar()
tkinter.Entry(fm3, width=60, textvariable=plaintext).pack(side=tkinter.LEFT)

tkinter.Label(fm4, width=15, text="cyphertext: ").pack(side=tkinter.LEFT)
cyphertext = tkinter.StringVar()
tkinter.Entry(fm4, width=60, textvariable=cyphertext).pack(side=tkinter.LEFT)

tkinter.Label(fm5, width=15, text="decyphertext: ").pack(side=tkinter.LEFT)
decyphertext = tkinter.StringVar()
tkinter.Entry(fm5, width=60, textvariable=decyphertext).pack(side=tkinter.LEFT)

tkinter.Button(fm6, text="encrypt", fg="blue", bd=2, width=20, command=encrypt).pack(side=tkinter.LEFT)
tkinter.Button(fm6, text="decrypt", fg="blue", bd=2, width=20, command=decrypt).pack(side=tkinter.LEFT)

fm1.pack()
fm2.pack()
fm3.pack()
fm4.pack()
fm5.pack()
fm6.pack()

root.mainloop()
