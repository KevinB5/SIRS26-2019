import socket, ssl, getpass, os, re, pickle
from Crypto.Util.number import long_to_bytes
from Crypto.PublicKey import RSA
from Client_NS import ClientNS

#sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
#ssl_sock = ssl.wrap_socket(sock, ca_certs="cert.pem", cert_reqs=ssl.CERT_REQUIRED)


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
PORT2 = 65440

def send_encrypted(ssl_sock,client_ns,message):
		message = client_ns.send_message(message)
		ssl_sock.send(message)

def mainMenu(ssl_sock,username,client_ns):
	print("\nPLEASE CHOOSE AN OPTION:")
	print("1: LOGIN")
	print("0: EXIT")
	# ask user for input

	command=input()
	if (command=="1"):
	
		print('Insert your password:')
		password=getpass.getpass()

		command_as_string = "login"+"!-!"+username+"!-!"+password+"!-!"
		#send_encrypted(ssl_sock,client_ns,command_as_string)
		
		#username_as_string = username+"!-!"
		#send_encrypted(ssl_sock,client_ns,username_as_string)
		
		#password_as_string = password+"!-!"
		#send_encrypted(ssl_sock,client_ns,password_as_string)
		
		EOF = b"\n\r##"
		ssl_sock.send(EOF)
		
		# message that says if username and password are correct
		mess = ssl_sock.recv(1024)
		mess = client_ns.receive_message(mess)
		print( "\n>>", str(mess, "utf-8") )
		if(str(mess, "utf-8")=="USER AUTHENTICATED!!!"):
			secondMenu(ssl_sock,username,client_ns)
		
		elif((str(mess, "utf-8")=="USER NOT AUTHENTICATED!!!")):
			mainMenu(ssl_sock,username,client_ns)
		
		else:
			print("SOMETHING WENT WRONG\n")


	elif (command=="0"):
		data="exit"
		send_encrypted(ssl_sock,client_ns,data)
		EOF = b"\n\r##"
		ssl_sock.send(EOF)
		ssl_sock.close()
		print( "\n>> CONNECTION TERMINATED" )
		
	else:
		print("WRONG COMMAND\n")
		mainMenu(ssl_sock,username,client_ns)




def secondMenu(ssl_sock,username,client_ns):
		
	print("\nPLEASE CHOOSE AN OPTION:")
	print("1: SCOREBOARD")
	print("2: SUBMIT")
	print("0: LAST MENU")
	# ask user for input
	command=input()
	
	if (command=="1"):
		command_as_string = "scoreboardMenu"+"!-!"
		send_encrypted(ssl_sock,client_ns,command_as_string.encode())
		username_as_string = username+"!-!"
		send_encrypted(ssl_sock,client_ns,username_as_string.encode())
		EOF = b"\n\r##"
		ssl_sock.send(EOF)

		# message received from server
		mess = ssl_sock.recv(1024)
		mess = client_ns.receive_message(mess)
		print( "\n>>", str(mess, "utf-8") )
		if(str(mess, "utf-8")=="SCOREBOARDMENU"):
			scoreboardMenu(ssl_sock,username,client_ns)
		else:
			print("UNKNOWN SERVER RESPONSE, TRY AGAIN")
			secondMenu(ssl_sock,username,client_ns)

	elif (command=="2"):
		command_as_string = "submitMenu"+"!-!"
		send_encrypted(ssl_sock,client_ns,command_as_string.encode())
		username_as_string = username+"!-!"
		send_encrypted(ssl_sock,client_ns,username_as_string.encode())
		EOF = b"\n\r##"
		ssl_sock.send(EOF)

		# message received from server
		mess = ssl_sock.recv(1024)
		mess = client_ns.receive_message(mess)
		print( "\n>>", str(mess, "utf-8") )
		
		if(str(mess, "utf-8")=="SUBMITMENU"):
			submitMenu(ssl_sock,username,client_ns)
		else:
			print("2-UNKNOWN SERVER RESPONSE, TRY AGAIN")
			secondMenu(ssl_sock,username,client_ns)

	elif (command=="0"):
		mainMenu(ssl_sock,username,client_ns)
		
	else:
		print("WRONG COMMAND\n")
		secondMenu(ssl_sock,username,client_ns)





def scoreboardMenu(ssl_sock,username,client_ns):
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
		send_encrypted(ssl_sock,client_ns,command_as_string.encode())
		username_as_string = username+"!-!"
		send_encrypted(ssl_sock,client_ns,username_as_string.encode())
		EOF = b"\n\r##"
		ssl_sock.send(EOF)
		
		# message received from server
		mess = ssl_sock.recv(1024)
		mess = client_ns.receive_message(mess)

		print("\n\nUSER SCORE IS", str(mess, "utf-8"),"\n" )
		scoreboardMenu(ssl_sock,username,client_ns)



	elif (command=="2"):
		command_as_string = "checkVulnsandFingerprints"+"!-!"
		send_encrypted(ssl_sock,client_ns,command_as_string.encode())
		username_as_string = username+"!-!"
		send_encrypted(ssl_sock,client_ns,username_as_string.encode())
		EOF = b"\n\r##"
		ssl_sock.send(EOF)

		# message received from server
		mess = ssl_sock.recv(1024)
		mess = client_ns.receive_message(mess)
		
		# print in terminal : User ; Fingerprint ; Name_Vuln ;
		newAux = re.findall("[^(),]+", mess[1:-1])
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
		
		scoreboardMenu(ssl_sock,username,client_ns)



	elif (command=="3"):
		command_as_string = "checkScoreboard"+"!-!"
		send_encrypted(ssl_sock,client_ns,command_as_string.encode())
		username_as_string = username+"!-!"
		send_encrypted(ssl_sock,client_ns,username_as_string.encode())
		EOF = b"\n\r##"
		ssl_sock.send(EOF)
		
		# message received from server
		scoreboard = ""
		while True:
			mess = ssl_sock.recv(1024)
			packet = client_ns.receive_message(mess)
			if "\n\r##" in packet:
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

		scoreboardMenu(ssl_sock,username,client_ns)



	elif (command=="4"):
		command_as_string = "checkTeamVulnsandFingerprints"+"!-!"
		send_encrypted(ssl_sock,client_ns,command_as_string.encode())
		username_as_string = username+"!-!"
		send_encrypted(ssl_sock,client_ns,username_as_string.encode())
		EOF = b"\n\r##"
		ssl_sock.send(EOF)
		
		# message received from server
		mess = ""
		while True:
			mess = ssl_sock.recv(1024)
			packet = client_ns.receive_message(mess)
			if "\n\r##" in packet:
				break
			mess += packet
	

		if(mess == "NO AUTHORIZATION"):
			print("\n\n" + "-"*20 + "ONLY THE TEAM LEADER IS AUTHORIZED TO SEE THE EXPLOITS OF THE TEAM" + "-"*20 + "\n")

		else:
			mess = pickle.loads(mess)
			# print in terminal : User ; Fingerprint ; Name_Vuln ;
			print("\n\nUser  ;" + " "*60 + "Fingerprint  ;" + " "*95 + "Name_Vuln  ;\n" )
			
			for i in range(0, len(mess)):
				user, fing, vuln = mess[i][0], mess[i][1], mess[i][2]
				print(user + " "*(20) + fing + " "*(20) + vuln)
		

		scoreboardMenu(ssl_sock,username,client_ns)


	elif (command=="0"):
		secondMenu(ssl_sock,username,client_ns)

		
	else:
		print("WRONG COMMAND\n")
		scoreboardMenu(ssl_sock,username,client_ns)





def submitMenu(ssl_sock,username,client_ns):
	print("\nPLEASE CHOOSE AN OPTION:")
	print("1: BINARY AND VULNERABILITIES")
	print("0: LAST MENU")
	
	# ask user for input
	command=input()
	
	if (command=="1"):
		command_as_string = "submitVulnerability"+"!-!"
		send_encrypted(ssl_sock,client_ns,command_as_string.encode())
		username_as_string = username+"!-!"
		send_encrypted(ssl_sock,client_ns,username_as_string.encode())
		EOF = b"\n\r##"
		ssl_sock.send(EOF)

		# message received from server
		mess = ssl_sock.recv(1024)
		mess = client_ns.receive_message(mess)
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
			sendFile(ssl_sock,file,client_ns)
			
			submitMenu(ssl_sock,username,client_ns)
		

		else:
			print("UNKNOWN SERVER RESPONSE, TRY AGAIN")
			submitMenu(ssl_sock,username,client_ns)


	elif (command=="0"):
		secondMenu(ssl_sock,username,client_ns)

	else:
		print("WRONG COMMAND\n")
		submitMenu(ssl_sock,username,client_ns)



def sendFile(ssl_sock,file,client_ns):

	print (">>Transfering file")
	
	# sending the vulns file
	f = open( file, "r" )
	data = ""
	data = f.read()
	send_encrypted(ssl_sock,client_ns,data)
			
	EOF = b"\n\r##"
	ssl_sock.send(EOF)
	f.close()
			
	print (">>Transfer concluded")



def NS_Protocol_Client():

	sockServer = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
	sockTrustManager = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
	
	print("\nPLEASE INSERT YOUR USERNAME:")
	username=input("Username: ")
	client_ns = ClientNS(username,username.lower()+'.key')
	# Alice sends her name "Alice" to server
	print("\n\nSENDING STEP 1")
	sockServer.connect((HOST, PORT))
	mess = client_ns.round1_server()
	sockServer.send( pickle.dumps(mess) )
	print( "\n" )

	print("RECEIVING STEP 2")
	mess = pickle.loads(sockServer.recv(1024))
	print( mess, "\n" )
	result = client_ns.round2_trustmanager(mess)
	print('result: ',result)

	print("SENDING STEP 3")
	sockTrustManager.connect((HOST, PORT2))
	sockTrustManager.send( pickle.dumps(result) )
	print( "\n" )

	print("RECEIVING STEP 4")
	mess = pickle.loads(sockTrustManager.recv(1024))
	print( mess, "\n" )
	result = client_ns.round3_server(mess)
	print('result: ',result)

	print("SENDING STEP 5")
	sockServer.send( pickle.dumps(result) )
	print( "\n" )

	print("\nRECEIVING STEP 6")
	mess = pickle.loads(sockServer.recv(1024))
	print( mess, "\n" )
	result = client_ns.round4_server(mess)
	print('result: ',result)

	print("SENDING STEP 7")
	sockServer.send( pickle.dumps(result) )
	print( "\n" )
	

	#sockServer.close()
	sockTrustManager.close()
	print ("\n>>FINALIZED SOCKET\n\n")
	try:
		ssl_sock = ssl.wrap_socket(sockServer, ca_certs="cert.pem", cert_reqs=ssl.CERT_REQUIRED)
	except Exception as err:
			print (">> !!INVALID CERTIFICATE!!\n")
			print(err)
	return ssl_sock,username,client_ns
	#System_log.writeSystemLog('Server','Server closed','info')
	#exit()




""" start the client side """
#try:

ssl_sock,username,client_ns = NS_Protocol_Client()
mainMenu(ssl_sock,username,client_ns)
	#ssl_sock.connect((HOST, PORT))
#print( "\n>> CONNECTION ESTABLISHED !" )

#except:
#	print( "\n>> CONNECTION LOST!" )






'''
if __name__ == "__main__":

	start()
'''
