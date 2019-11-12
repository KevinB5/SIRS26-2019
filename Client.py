import socket, ssl

sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
ssl_sock = ssl.wrap_socket(sock, ca_certs="cert.pem", cert_reqs = ssl.CERT_REQUIRED)


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


try:
	ssl_sock.connect((HOST, PORT))
	print( ">> Conexão estabelecida!" )
except:
	print( ">> Conexão Perdida!" )


#f = open( "C:\\Users\\Documents\\Projecto\\demo.jpg", "rb" )

data = b"OLA"

#data = f.readlines()
#for line in data:
ssl_sock.send(data)

EOF = b"\n\r##"
ssl_sock.send(EOF)
#f.close()

ssl_sock.close()
print( ">> Envio terminado!" )
