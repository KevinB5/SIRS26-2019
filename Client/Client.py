import socket, ssl, getpass, os


sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
ssl_sock = ssl.wrap_socket(sock, ca_certs="cert.pem", cert_reqs=ssl.CERT_REQUIRED)


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

# Global Variables
username =''

def mainMenu():
	global username
	print("\nPLEASE CHOOSE AN OPTION:")
	print("1: LOGIN")
	print("0: EXIT")
	# ask user for input
	command=input()
	if (command=="1"):
	
		username=input("Username:")
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
		if(str(mess, "utf-8")=="USER AUTHENTICATED!!!"):
			secondMenu()
		
		elif((str(mess, "utf-8")=="USER NOT AUTHENTICATED!!!")):
			mainMenu()
		
		else:
			print("SOMETHING WENT WRONG\n")


	elif (command=="0"):
		data=b"exit"
		ssl_sock.send(data)
		EOF = b"\n\r##"
		ssl_sock.send(EOF)
		ssl_sock.close()
		print( "\n>> CONNECTION TERMINATED" )
		
	else:
		print("WRONG COMMAND\n")
		mainMenu()




def secondMenu():
		
	print("\nPLEASE CHOOSE AN OPTION:")
	print("1: SCOREBOARD")
	print("2: SUBMIT")
	print("0: LAST MENU")
	# ask user for input
	command=input()
	
	if (command=="1"):
		command_as_string = "scoreboardMenu"+"!-!"
		ssl_sock.send(command_as_string.encode())
		username_as_string = username+"!-!"
		ssl_sock.send(username_as_string.encode())
		EOF = b"\n\r##"
		ssl_sock.send(EOF)

		# message received from server
		mess = ssl_sock.recv(1024)
		print( "\n>>", str(mess, "utf-8") )
		if(str(mess, "utf-8")=="SCOREBOARDMENU"):
			scoreboardMenu()
		else:
			print("UNKNOWN SERVER RESPONSE, TRY AGAIN")
			secondMenu()

	elif (command=="2"):
		command_as_string = "submitMenu"+"!-!"
		ssl_sock.send(command_as_string.encode())
		username_as_string = username+"!-!"
		ssl_sock.send(username_as_string.encode())
		EOF = b"\n\r##"
		ssl_sock.send(EOF)

		# message received from server
		mess = ssl_sock.recv(1024)
		print( "\n>>", str(mess, "utf-8") )
		
		if(str(mess, "utf-8")=="SUBMITMENU"):
			submitMenu()
		else:
			print("2-UNKNOWN SERVER RESPONSE, TRY AGAIN")
			secondMenu()

	elif (command=="0"):
		mainMenu()
		
	else:
		print("WRONG COMMAND\n")
		secondMenu()





def scoreboardMenu():
		
	print("\nPLEASE CHOOSE AN OPTION:")
	print("1: CHECK SCORE")
	print("2: CHECK VULNERABILITIES AND FINGERPRINTS")
	print("4: CHECK TEAM SCORE")
	print("0: LAST MENU")
	# ask user for input
	command=input()
	
	if (command=="1"):
		command_as_string = "checkScore"+"!-!"
		ssl_sock.send(command_as_string.encode())
		username_as_string = username+"!-!"
		ssl_sock.send(username_as_string.encode())
		EOF = b"\n\r##"
		ssl_sock.send(EOF)
		# message received from server
		mess = ssl_sock.recv(1024)

		print("\n\nUSER SCORE IS", str(mess, "utf-8"),"\n" )
		scoreboardMenu()


	elif (command=="2"):
		command_as_string = "checkVulnerability"+"!-!"
		ssl_sock.send(command_as_string.encode())
		username_as_string = username+"!-!"
		ssl_sock.send(username_as_string.encode())
		EOF = b"\n\r##"
		ssl_sock.send(EOF)

		# message received from server
		mess = ssl_sock.recv(1024)
		print( "\n>>", str(mess, "utf-8") )

		if(str(mess, "utf-8")=="CHECKVULNERABILITY"):
			print("THERE IS NO VULNERABILITIES")
			scoreboardMenu()

		else:
			print("UNKNOWN SERVER RESPONSE, TRY AGAIN")
			scoreboardMenu()


	elif (command=="3"):
		command_as_string = "checkTeamScore"+"!-!"
		ssl_sock.send(command_as_string.encode())
		username_as_string = username+"!-!"
		ssl_sock.send(username_as_string.encode())
		EOF = b"\n\r##"
		ssl_sock.send(EOF)
		# message received from server
		mess = ssl_sock.recv(1024)
		print( "\n>>", str(mess, "utf-8") )

		if(str(mess, "utf-8")=="CHECKTEAMSCORE"):
			print("USER 1 SCORE IS 20")
			print("USER 2 SCORE IS 200")
			print("USER 3 SCORE IS 500")
			scoreboardMenu()

		else:
			print("UNKNOWN SERVER RESPONSE, TRY AGAIN")
			scoreboardMenu()


	elif (command=="0"):
		secondMenu()

		
	else:
		print("WRONG COMMAND\n")
		scoreboardMenu()





def submitMenu():
		
	print("\nPLEASE CHOOSE AN OPTION:")
	print("1: BINARY AND VULNERABILITIES")
	print("0: LAST MENU")
	
	# ask user for input
	command=input()
	
	if (command=="1"):
		command_as_string = "submitVulnerability"+"!-!"
		ssl_sock.send(command_as_string.encode())
		username_as_string = username+"!-!"
		ssl_sock.send(username_as_string.encode())
		EOF = b"\n\r##"
		ssl_sock.send(EOF)

		# message received from server
		mess = ssl_sock.recv(1024)
		print( "\n>>", str(mess, "utf-8") )

		if(str(mess, "utf-8")=="SUBMITVULNERABILITY"):
			
			print("BINARY:", end="")
			file = input()
			
			# if it does not find file ...
			while (not os.path.isfile(file)) or (not os.path.exists(file)):
				print("NO SUCH FILE !!! TRY AGAIN \n\nBINARY:", end="")
				file = input()
			
			# sending the binary file
			sendFile(file,ssl_sock)
			
			
			print("VULNERABILITIES:", end="")
			file = input()
			
			# if it does not find file ...
			while (not os.path.isfile(file)) or (not os.path.exists(file)):
				print("NO SUCH FILE !!! TRY AGAIN \n\nVULNERABILITIES:", end="")
				file = input()
			
			# sending the vulns file
			sendFile(file, ssl_sock)
			
			submitMenu()
		

		else:
			print("UNKNOWN SERVER RESPONSE, TRY AGAIN")
			submitMenu()


	elif (command=="0"):
		secondMenu()

	else:
		print("WRONG COMMAND\n")
		submitMenu()



def sendFile(file, ssl_sock):

	print (">>A Decorrer Transferencia")
	
	# sending the vulns file
	f = open( file, "rb" )
	data = ""
	data = f.read()
	ssl_sock.send(data)
			
	EOF = b"\n\r##"
	ssl_sock.send(EOF)
	f.close()
			
	print (">>Transferencia Concluida")




""" start the client side """
try:
	ssl_sock.connect((HOST, PORT))
	print( "\n>> CONNECTION ESTABLISHED !" )

except:
	print( "\n>> CONNECTION LOST!" )


mainMenu()


'''
if __name__ == "__main__":

	start()
'''


# f = open( "C:\\Users\\Documents\\Projecto\\demo.jpg", "rb" )
#data = b"OLA"
# data = f.readlines()
# for line in data:


# f.close()

# ssl_sock.close()
# print( ">> Envio terminado!" )
