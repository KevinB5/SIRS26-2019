from Crypto.Util.number import long_to_bytes
from Crypto.PublicKey import RSA
import os, pickle


def exmp():
	
	aux = pickle.dumps([1,2])
	#auxEnc = aux**2) % 5
	
	auxInt = int.from_bytes(aux, "big")
	print(auxInt)
	
	bits = 1024
	rsa = RSA.generate(bits, os.urandom)
	
	N = rsa.n
	e = rsa.e
	d = rsa.d
	
	encr = pow(auxInt,e,N)
	decr = pow(encr,d,N)
	
	byt = long_to_bytes(decr)
	auxR = pickle.loads(byt)
	
	print(auxR )
	print(auxR[1] )



exmp()

