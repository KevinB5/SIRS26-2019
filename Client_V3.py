import socket, ssl
import getpass

sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
ssl_sock = ssl.wrap_socket(sock, ca_certs="cert.pem", cert_reqs = ssl.CERT_REQUIRED)


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


try:
	ssl_sock.connect((HOST, PORT))
	print( "\n>> CONNECTION ESTABLISHED !" )
except:
	print( "\n>> CONNECTION LOST!" )


command="2"


while (command!="0"):
	
	print("\nPLEASE CHOOSE AN OPTION:")
	print("1: LOGIN")
	print("0: EXIT")

	# ask user for input
	command=input()
	
	if (command=="1"):
	
		username=input("Insert your username:")
		print("Insert your password:")
		password=getpass.getpass()

		command_as_string = "login"+"!-!"
		ssl_sock.send(command_as_string.encode())
		
		username_as_string = username+"!-!"
		ssl_sock.send(username_as_string.encode())
		
		password_as_string = password+"!-!"
		ssl_sock.send(password_as_string.encode())
		
		EOF = b"\n\r##"
		ssl_sock.send(EOF)
		
		# message that says if username and password are correct
		mess = ssl_sock.recv(1024)
		print( "\n>>", str(mess, "utf-8") )

	else:
		print("WRONG COMMAND")
		print("PLEASE CHOOSE AN OPTION:")
		print("1: LOGIN")
		print("0: EXIT")



if (command=="0"):
		data=b"exit"
		ssl_sock.send(data)
		EOF = b"\n\r##"
		ssl_sock.send(EOF)
		ssl_sock.close()
		print( "\n>> CONNECTION TERMINATED" )








# f = open( "C:\\Users\\Documents\\Projecto\\demo.jpg", "rb" )
#data = b"OLA"
# data = f.readlines()
# for line in data:


# f.close()

# ssl_sock.close()
# print( ">> Envio terminado!" )
