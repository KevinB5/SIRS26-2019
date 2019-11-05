import random
import time
import hashlib


# Diffie-Hellman function
def Diffie_Hellman(p, g):

    # calculate "a", random number mod p
    # and the same for "b"
    a, b = random.randint(0,p), random.randint(0,p)

    #calculate "A", which is "g" raised to the "a" power mode p
    # and the same for "B"
    A, B = powerMod(g,a,p), powerMod(g,b,p)

    # generate a session key
    s1 = powerMod(B,a,p)
    s2 = powerMod(A,b,p)
    
    if( s1==s2 ):
        print("\nSession Key:", s1, "\n")

    # generate a key using SHA1 and s1
    print("Key", hashlib.sha1(hex(s1).encode()).digest(), "\n")



# Based on Applied Cryptography by Bruce Schneier
def powerMod(base, exponent, modulus):

    if(modulus == 1):
        return 0

    #Assert :: (modulus - 1) * (modulus - 1) does not overflow base

    result = 1
    base = base % modulus

    while(exponent > 0):

        if ( (exponent % 2) == 1):
            result = (result * base) % modulus

        exponent = exponent >> 1
        base = (base * base) % modulus


    return result


'''
p = int(b"ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff",16)

g = 2


Diffie_Hellman(p, g)
'''

