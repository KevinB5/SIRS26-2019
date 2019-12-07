import socket, ssl, getpass, os, re, Client_NS, pickle
from Crypto.Util.number import long_to_bytes
from Crypto.PublicKey import RSA

sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
ssl_sock = ssl.wrap_socket(sock, ca_certs="cert.pem", cert_reqs=ssl.CERT_REQUIRED)


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
PORT2 = 65440



def mainMenu():
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
			secondMenu(username)
		
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




def secondMenu(username):
		
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
			scoreboardMenu(username)
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
			submitMenu(username)
		else:
			print("2-UNKNOWN SERVER RESPONSE, TRY AGAIN")
			secondMenu(username)

	elif (command=="0"):
		mainMenu()
		
	else:
		print("WRONG COMMAND\n")
		secondMenu(username)





def scoreboardMenu(username):
		
	print("\nPLEASE CHOOSE AN OPTION:")
	print("1: CHECK SCORE")
	print("2: CHECK VULNERABILITIES AND FINGERPRINTS")
	print("3: CHECK SCOREBOARD")
	print("4: CHECK TEAM VULNERABILITIES AND FINGERPRINTS")
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
		scoreboardMenu(username)



	elif (command=="2"):
		command_as_string = "checkVulnsandFingerprints"+"!-!"
		ssl_sock.send(command_as_string.encode())
		username_as_string = username+"!-!"
		ssl_sock.send(username_as_string.encode())
		EOF = b"\n\r##"
		ssl_sock.send(EOF)

		# message received from server
		mess = ssl_sock.recv(1024)
		
		# print in terminal : User ; Fingerprint ; Name_Vuln ;
		newAux = re.findall(b"[^(),]+", mess[1:-1])
		print("\n\nUser  ;" + " "*60 + "Fingerprint  ;" + " "*70 + "Name_Vuln  ;\n" )

		k = 0
		for name in newAux:
			strAux = str(name, "utf-8")[1:-1]
			strAux = strAux.replace("'","")
		
			k = k + 1
			sep = "    ;    "
			
			if( k % 4 == 0):
				print("\n")
				sep = ""
		
			print(strAux + sep, end="")
		print("\n\n")
		
		scoreboardMenu(username)



	elif (command=="3"):
		command_as_string = "checkScoreboard"+"!-!"
		ssl_sock.send(command_as_string.encode())
		username_as_string = username+"!-!"
		ssl_sock.send(username_as_string.encode())
		EOF = b"\n\r##"
		ssl_sock.send(EOF)
		
		# message received from server
		scoreboard = b""
		while True:
			packet = ssl_sock.recv(1024)
			if b"\n\r##" in packet:
				break
			scoreboard += packet
		
		scoreboard = pickle.loads(scoreboard)
		
		
		#printing the scoreoboard
		print("-" * 300 + "SCOREBOARD" + "-"*270)
		print("\n\n" + " "*10 + "User  ;" + " "*35 + "Points  ;" + " "*10 + "Number of Vulnerabilites;" + " "*10 + "Last_update;" + " "*30 + "\n" )

		for i in range(0,len(scoreboard)):
			username, points =  str(scoreboard[i][0],'utf-8'), str(scoreboard[i][1])
			numberOfVulns, date = str(scoreboard[i][2]), str(scoreboard[i][3])
		
			print(" "*10 + username + " " *(40-len(username)), end="")
			print(" "*2 + points + " " *(10-len(points)), end="")
			print(" "*10 + numberOfVulns + " " *(30-len(numberOfVulns)), end="")
			print(  date, "  \n")

		scoreboardMenu(username)



	elif (command=="4"):
		command_as_string = "checkTeamVulnsandFingerprints"+"!-!"
		ssl_sock.send(command_as_string.encode())
		username_as_string = username+"!-!"
		ssl_sock.send(username_as_string.encode())
		EOF = b"\n\r##"
		ssl_sock.send(EOF)
		
		# message received from server
		mess = b""
		while True:
			packet = ssl_sock.recv(1024)
			if b"\n\r##" in packet:
				break
			mess += packet
	

		if(mess == b"NO AUTHORIZATION"):
			print("\n\n" + "-"*20 + "ONLY THE TEAM LEADER IS AUTHORIZED TO SEE THE EXPLOITS OF THE TEAM" + "-"*20 + "\n")

		else:
			mess = pickle.loads(mess)
			# print in terminal : User ; Fingerprint ; Name_Vuln ;
			print("\n\nUser  ;" + " "*60 + "Fingerprint  ;" + " "*95 + "Name_Vuln  ;\n" )
			
			for i in range(0, len(mess)):
				user, fing, vuln = mess[i][0], mess[i][1], mess[i][2]
				print(user + " "*(20) + fing + " "*(20) + vuln)
		

		scoreboardMenu(username)


	elif (command=="0"):
		secondMenu(username)

		
	else:
		print("WRONG COMMAND\n")
		scoreboardMenu(username)





def submitMenu(username):
		
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
			
			submitMenu(username)
		

		else:
			print("UNKNOWN SERVER RESPONSE, TRY AGAIN")
			submitMenu(username)


	elif (command=="0"):
		secondMenu(username)

	else:
		print("WRONG COMMAND\n")
		submitMenu(username)



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



def NS_Protocol_Client():

	sockServer = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
	sockTrustManager = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
	
	# Alice sends her name "Alice" to server
	print("\n\nSENDING STEP 1")
	sockServer.connect((HOST, PORT))
	sockServer.send( pickle.dumps("Alice") )
	print( "\n" )

	print("RECEIVING STEP 2")
	mess = pickle.loads(sockServer.recv(1024))
	print( mess, "\n" )

	print("SENDING STEP 3")
	sockTrustManager.connect((HOST, PORT2))
	sockTrustManager.send( pickle.dumps("Encrypted Message -- From Client") )
	print( "\n" )

	print("RECEIVING STEP 4")
	mess = pickle.loads(sockTrustManager.recv(1024))
	print( mess, "\n" )

	print("SENDING STEP 5")
	sockServer.send( pickle.dumps("Encrypted Message -- From Client") )
	print( "\n" )

	print("\nRECEIVING STEP 6")
	mess = pickle.loads(sockServer.recv(1024))
	print( mess, "\n" )

	print("SENDING STEP 7")
	sockServer.send( pickle.dumps("Encrypted Message -- From Client") )
	print( "\n" )
	

	sockServer.close()
	sockTrustManager.close()
	print ("\n>>FINALIZED SOCKET\n\n")
	#System_log.writeSystemLog('Server','Server closed','info')
	exit()




""" start the client side """
try:
	#NS_Protocol_Client()
	ssl_sock.connect((HOST, PORT))
	print( "\n>> CONNECTION ESTABLISHED !" )

except:
	print( "\n>> CONNECTION LOST!" )


mainMenu()



'''
if __name__ == "__main__":

	start()
'''
