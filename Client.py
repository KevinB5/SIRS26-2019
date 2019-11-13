import socket, ssl
import getpass

sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
ssl_sock = ssl.wrap_socket(sock, ca_certs="cert.pem", cert_reqs = ssl.CERT_REQUIRED)


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


try:
	ssl_sock.connect((HOST, PORT))
	print( ">> Conexão estabelecida!" )
except:
	print( ">> Conexão Perdida!" )


# f = open( "C:\\Users\\Documents\\Projecto\\demo.jpg", "rb" )

#data = b"OLA"
print("Please choose an option:")
print("1: Login")
print("0: Exit")
command=input()
# data = f.readlines()
while (command!="0"):
	if (command=="1"):
	# for line in data:
		username=input("Insert your username:")
		print("Insert your password:")
		password=getpass.getpass()
		command="login"+"!-!"
		command_as_bytes=command.encode()
		ssl_sock.send(command_as_bytes)
		username_string=username+"!-!"
		username_as_bytes=username_string.encode()
		ssl_sock.send(username_as_bytes)
		password_as_string=password+"!-!"
		password_as_bytes=password_as_string.encode()
		ssl_sock.send(password_as_bytes)
		EOF = b"\n\r##"
		ssl_sock.send(EOF)
		print( ">> Envio terminado!" )
	else:
		print("Wrong Command")
		print("Please choose an option:")
		print("1: Login")
		print("0: Exit")
		command=input()

if (command=="0"):
		data=b"exit"
		ssl_sock.send(data)
		EOF = b"\n\r##"
		ssl_sock.send(EOF)
		ssl_sock.close()
		print( ">> Ligação terminada!" )


# f.close()

# ssl_sock.close()
# print( ">> Envio terminado!" )
