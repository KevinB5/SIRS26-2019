import socket, random, pickle, hashlib, hmac
from set5ch33 import powerMod
from math import pow


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

N = int(b"ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff",16)

g = 2
k = 3
I = b"foo@bar.com"
P = b"password"




# solution of challenge 36 of set 5 (Client)
def set5ch36_C():


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            
        s.connect((HOST, PORT))
        
        # calculate the value of A
        a = random.randint(0, N)
        A = powerMod(g,a,N)

        # send I, A = g**a % N (a la Diffie Hellman)
        s.sendall(pickle.dumps([I, A]) )

        # received values from S
        data = pickle.loads(s.recv(1024))

        salt, B = data[0], data[1]

        #calculate uH = SHA256(A|B), u = integer of uH
        uH = hashlib.sha256( (A+B).to_bytes(256, byteorder="big") ).hexdigest()
        u = int(uH, 16)

        print("VALUE OF u:", u, "\n\n")
           
        # Generate string xH = SHA256(salt|password)
        xH = hashlib.sha256( salt.to_bytes(4, byteorder="big") + P ).hexdigest()
        
        # Convert xH to integer x
        x = int(xH, 16)
        
        print("VALUE OF X:", x, "\n\n")
        
        # Generate S = (B - k * g**x)**(a + u * x) % N
        S = powerMod(B - (k * powerMod(g,x,N)), a + (u * x), N)

        print("VALUE OF S:", S, "\n\n")

        # Generate K = SHA256(S)
        K = hashlib.sha256( S.to_bytes(256, byteorder="big") ).digest()

        h = hmac.new( K, salt.to_bytes(4, byteorder="big"), hashlib.sha256)
        
        s.sendall( h.digest() )

        print("\nSide C -> Result:", s.recv(1024).decode(), "\n")

        s.close()



set5ch36_C()



