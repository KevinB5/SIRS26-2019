import os, pickle, socket, random, hashlib, hmac
from set5ch33 import powerMod
from math import pow


HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432        # The port used by the server

N = int(b"ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff",16)

g = 2
k = 3
I = b"foo@bar.com"
P = b"password"



# solution of challenge 36 of set 5 (Server)
def set5ch36_S():

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        
        with conn:
                
            data = pickle.loads(conn.recv(1024))
            if not data:
                return 0

            # Generate salt as random integer
            salt = random.randint(0, 1000)
        
            # Generate string xH = SHA256(salt|password)
            xH = hashlib.sha256( salt.to_bytes(4, byteorder="big") + P ).hexdigest()
            
            # Convert xH to integer x
            x = int(xH, 16)
            
            print("VALUE OF X:", x, "\n\n")
            
            # Generate v = g**x % N
            v = powerMod(g,x,N)
           
            print("VALUE OF V:", v, "\n\n")
           
            # received values of I and A
            I, A = data[0], data[1]
        
            # calculate the value of B
            b = random.randint(0, N)
            B = k*v + powerMod(g,b,N)

            conn.sendall( pickle.dumps([salt, B]) )

            #calculate uH = SHA256(A|B), u = integer of uH
            uH = hashlib.sha256( (A+B).to_bytes(256, byteorder="big") ).hexdigest()
            u = int(uH, 16)

            # Generate S = (A * v**u) ** b % N
            S = powerMod(A * powerMod(v,u,N), b, N)

            print("VALUE OF S:", S, "\n\n")

            # Generate K = SHA256(S)
            K = hashlib.sha256( S.to_bytes(256, byteorder="big") ).digest()

            # received HMAC
            HMAC_rec = conn.recv(1024)

            # HMAC calculated by S
            h = (hmac.new( K, salt.to_bytes(4, byteorder="big"), hashlib.sha256)).digest()

            if(h == HMAC_rec):
                conn.sendall(b"OK")
                print("\nSide S -> Result: OK \n")
            else:
                conn.sendall(b"NOT EQUAL")
                print("\nSide S -> Result: KO \n")


        conn.close()

    s.close()





set5ch36_S()

