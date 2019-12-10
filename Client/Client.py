import socket, ssl, getpass, os, re, pickle, signal, sys
from Crypto.Util.number import long_to_bytes
from Crypto.PublicKey import RSA
from Client_NS import ClientNS

#sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
#ssl_sock = ssl.wrap_socket(sock, ca_certs="cert.pem", cert_reqs=ssl.CERT_REQUIRED)



HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
PORT2 = 65440




def signal_handler(signal, frame):
	print('\n>>PROGRAM TERMINATED\n')
	sys.exit(0)
	
	signal.signal(signal.SIGINT, signal_handler)





class Client_Socket:


	def __init__(self, ssl_sock, username, client_ns):
		self.ssl_sock = ssl_sock
		self.client_ns = client_ns
		self.username = username
	


	def sendFile(self,file):
	
		print (">>Transfering file")
		
		# sending the vulns file
		f = open( file, "rb" )
		data = ""
		data = f.read()
		
		print("FILE IS: ",data)
		
		self.send_encrypted(str(data))
		f.close()
		
		EOF = b"\n\r##"
		self.ssl_sock.send(EOF)
		
		print (">>Transfer concluded")
	
	
	#
	#
	#
	def send_encrypted(self, message):
		message = self.client_ns.send_message(message)
		self.ssl_sock.send(message)


	#
	#
	#
	def menus(self):
		
		next = self.mainMenu()
		
		while(1):
			if( next == "MAIN_MENU"):
				next = self.mainMenu()
			
			elif( next == "SECOND_MENU"):
				next = self.secondMenu()
			
			elif( next == "SCOREBOARD_MENU"):
				next = self.scoreboardMenu()
			
			elif( next == "SUBMIT_MENU"):
				next = self.submitMenu()
			
			elif( next == "COMPUTE_FINGERPRINT"):
				next = self.computeFingerprint()




	def mainMenu(self):
		print("\nPLEASE CHOOSE AN OPTION:")
		print("1: LOGIN")
		print("0: EXIT")
		# ask user for input

		command=input()
		if (command=="1"):
		
			password=getpass.getpass()

			command_as_string = "login"+"!-!"+username+"!-!"+password+"!-!"
			self.send_encrypted(command_as_string)
			
			EOF = b"\n\r##"
			self.ssl_sock.send(EOF)
			
			# message that says if username and password are correct
			mess = self.client_ns.receive_message(self.ssl_sock.recv(1024))
			print( "\n>>", mess )
			
			if(mess=="USER AUTHENTICATED!!!"):
				return "SECOND_MENU"
		
			elif(mess =="USER NOT AUTHENTICATED!!!"):
				return "MAIN_MENU"
			
			else:
				print("SOMETHING WENT WRONG\n")


		elif (command=="0"):
			data="exit"
			self.send_encrypted(data)
			EOF = b"\n\r##"
			self.ssl_sock.send(EOF)
			self.ssl_sock.close()
			print( "\n>> CONNECTION TERMINATED" )
			exit()
			
		else:
			print("WRONG COMMAND\n")
			return "MAIN_MENU"




	def secondMenu(self):
			
		print("\nPLEASE CHOOSE AN OPTION:")
		print("1: SCOREBOARD")
		print("2: SUBMIT")
		print("3: COMPUTE FINGERPRINT")
		print("0: LAST MENU")
		# ask user for input
		command=input()
		
		if (command=="1"):
			command_as_string = "scoreboardMenu"+"!-!"+username+"!-!"
			self.send_encrypted(command_as_string)
			
			EOF = b"\n\r##"
			self.ssl_sock.send(EOF)

			# message received from server
			mess = self.client_ns.receive_message(self.ssl_sock.recv(1024))
			print( "\n>>", mess )
			
			if(mess=="SCOREBOARDMENU"):
				return "SCOREBOARD_MENU"
			else:
				print("UNKNOWN SERVER RESPONSE, TRY AGAIN")
				return "SECOND_MENU"


		elif (command=="2"):
			command_as_string = "submitMenu"+"!-!"+username+"!-!"
			self.send_encrypted(command_as_string)
			
			EOF = b"\n\r##"
			self.ssl_sock.send(EOF)

			# message received from server
			mess = self.client_ns.receive_message(self.ssl_sock.recv(1024))
			print( "\n>>", mess)
			
			if(mess=="SUBMITMENU"):
				return "SUBMIT_MENU"
			else:
				print("2-UNKNOWN SERVER RESPONSE, TRY AGAIN")
				return "SECOND_MENU"


		elif(command=="3"):
				send = ""
				
				command_as_string = "computeFingerprint"+"!-!"
				send += command_as_string
				
				username_as_string = username+"!-!"
				send += username_as_string
				
				self.send_encrypted(send)
				
				EOF = b"\n\r##"
				self.ssl_sock.send(EOF)
				
				# message received from server
				mess = self.client_ns.receive_message(self.ssl_sock.recv(1024))
				print( "\n>>", mess )
				
				if(mess == "COMPUTEFINGERPRINT"):
					return "COMPUTE_FINGERPRINT"
				
				else:
					print("3-UNKNOWN SERVER RESPONSE, TRY AGAIN")
					return "SECOND_MENU"


		elif (command=="0"):
			return "MAIN_MENU"

		else:
			print("WRONG COMMAND\n")
			return "SECOND_MENU"




	def computeFingerprint(self):
		
			file = input("\n\nBINARY FILE:")
			
			# if it does not find file ...
			while (not os.path.isfile(file)) or (not os.path.exists(file)):
				file = input("\nNO SUCH FILE !!! TRY AGAIN \n\nBINARY FILE:")
			
			# sending the binary file
			self.sendFile(file)
			
			# receive the fingerprint
			data, fingerprint = b"", b""
			while (data[-4:] != b"\n\r##"):
				data += self.ssl_sock.recv(1024)
		
			fingerprint = data.replace(b"\n\r##", b"")
			fingerprint = self.client_ns.receive_message(fingerprint)
		
			print("\n\n FINGERPRINT:" , fingerprint, "\n\n")

			return "SUBMIT_MENU"



	def scoreboardMenu(self):
		print("\nPLEASE CHOOSE AN OPTION:")
		print("1: CHECK SCORE")
		print("2: CHECK VULNERABILITIES AND FINGERPRINTS")
		print("3: CHECK TEAM SCOREBOARD ( ONLY ALLOWED FOR TEAM LEADERS ) ")
		print("4: CHECK TEAM VULNERABILITIES AND FINGERPRINTS ( ONLY ALLOWED FOR TEAM LEADERS ) ")
		print("0: LAST MENU")
		# ask user for input
		command=input()
		
		if (command=="1"):
			command_as_string = "checkScore"+"!-!"+username+"!-!"
			self.send_encrypted(command_as_string)
			
			EOF = b"\n\r##"
			self.ssl_sock.send(EOF)
			
			# message received from server
			mess = client_ns.receive_message(self.ssl_sock.recv(1024))

			print("\n\nUSER SCORE IS", mess,"\n" )
			return "SCOREBOARD_MENU"


		elif (command=="2"):
			command_as_string = "checkVulnsandFingerprints"+"!-!"+username+"!-!"
			self.send_encrypted(command_as_string)
			
			EOF = b"\n\r##"
			self.ssl_sock.send(EOF)

			# message received from server
			mess = client_ns.receive_message(self.ssl_sock.recv(1024))
			
			# print in terminal : User ; Fingerprint ; Name_Vuln ;
			newAux = re.findall("[^(),]+", mess[1:-1])
			print("\n\nUser  ;" + " "*60 + "Fingerprint  ;" + " "*70 + "Name_Vuln  ;\n" )

			k = 0
			for name in newAux:
				strAux = name[1:-1]
				strAux = strAux.replace("'","")
			
				k = k + 1
				sep = "    ;    "
				
				if( k % 4 == 0):
					print("\n")
					sep = ""
			
				print(strAux + sep, end="")
			print("\n\n")
			
			return "SCOREBOARD_MENU"


		elif (command=="3"):
			command_as_string = "checkScoreboard"+"!-!"+username+"!-!"
			self.send_encrypted(command_as_string)
			
			EOF = b"\n\r##"
			self.ssl_sock.send(EOF)
			
			# message received from server
			scoreboard = b""
			while True:
				packet = self.ssl_sock.recv(1024)
				if b"\n\r##" in packet:
					break
				scoreboard += packet

			scoreboard = self.client_ns.receive_message(scoreboard)


			if( scoreboard == "NO AUTHORIZATION"):
				print("\n\n" + "-"*20 + "ONLY THE TEAM LEADER IS AUTHORIZED TO SEE THE SCOREBOARD OF THE TEAM" + "-"*20 + "\n")

			else:
				#printing the scoreoboard
				print("-" * 300 + "SCOREBOARD" + "-"*270)
				print("\n\n" + " "*10 + "User  ;" + " "*35 + "Points  ;" + " "*10 + "Number of Vulnerabilites;" + " "*10 + "Last_update;" + " "*30 + "\n" )
				print(scoreboard)


			return "SCOREBOARD_MENU"



		elif (command=="4"):
			command_as_string = "checkTeamVulnsandFingerprints"+"!-!"+username+"!-!"
			self.send_encrypted(command_as_string)
			
			EOF = b"\n\r##"
			self.ssl_sock.send(EOF)
			
			# message received from server
			mess = b""
			while True:
				packet = self.ssl_sock.recv(1024)
				if(b"\n\r##" in packet):
					break
				mess += packet
			
			mess = self.client_ns.receive_message(mess)


			if(mess == "NO AUTHORIZATION"):
				print("\n\n" + "-"*20 + "ONLY THE TEAM LEADER IS AUTHORIZED TO SEE THE EXPLOITS OF THE TEAM" + "-"*20 + "\n")

			else:
				mess = pickle.loads(mess)
				# print in terminal : User ; Fingerprint ; Name_Vuln ;
				print("\n\nUser  ;" + " "*60 + "Fingerprint  ;" + " "*95 + "Name_Vuln  ;\n" )
				
				for i in range(0, len(mess)):
					user, fing, vuln = mess[i][0], mess[i][1], mess[i][2]
					print(user + " "*(20) + fing + " "*(20) + vuln)
			

			return "SCOREBOARD_MENU"


		elif (command=="0"):
			return "SECOND_MENU"
			
		else:
			print("WRONG COMMAND\n")
			return "SCOREBOARD_MENU"




	def submitMenu(self):
		print("\nPLEASE CHOOSE AN OPTION:")
		print("1: BINARY AND VULNERABILITIES")
		print("0: LAST MENU")
		
		# ask user for input
		command=input()
		
		if (command=="1"):
			command_as_string = "submitVulnerability"+"!-!"+username+"!-!"
			self.send_encrypted(command_as_string)
		
			EOF = b"\n\r##"
			self.ssl_sock.send(EOF)

			# message received from server
			mess = self.client_ns.receive_message(self.ssl_sock.recv(1024))
			print( "\n>>", mess)

			if(mess=="SUBMITVULNERABILITY"):
				
				print("BINARY:", end="")
				file = input()
				
				# if it does not find file ...
				while (not os.path.isfile(file)) or (not os.path.exists(file)):
					print("NO SUCH FILE !!! TRY AGAIN \n\nBINARY:", end="")
					file = input()
				
				# sending the binary file
				self.sendFile(file)
				
				#EOF = b"\n\r##"
				#ssl_sock.send(EOF)
				
				print("VULNERABILITIES:", end="")
				file2 = input()
				
				# if it does not find file ...
				while (not os.path.isfile(file2)) or (not os.path.exists(file2)):
					print("NO SUCH FILE !!! TRY AGAIN \n\nVULNERABILITIES:", end="")
					file2 = input()
				
				# sending the vulns file
				self.sendFile(file2)

				#EOF = b"\n\r##"
				#ssl_sock.send(EOF)
				
				return "SUBMIT_MENU"
			

			else:
				print("UNKNOWN SERVER RESPONSE, TRY AGAIN")
				return "SUBMIT_MENU"


		elif (command=="0"):
			return "SECOND_MENU"
			
		else:
			print("WRONG COMMAND\n")
			return "SUBMIT_MENU"



def NS_Protocol_Client():

	try:
		sockServer = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
		sockTrustManager = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
		
		username=input("USERNAME: ")
		client_ns = ClientNS(username,username.lower()+".key")
		
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
		
		'''
		try:
			ssl_sock = ssl.wrap_socket(sockServer, ca_certs="cert.pem", cert_reqs=ssl.CERT_REQUIRED)
		except Exception as err:
				print (">> !!INVALID CERTIFICATE!!\n")
				print(err)
		'''
		
		return sockServer, username, client_ns
	
		#System_log.writeSystemLog('Server','Server closed','info')
		#exit()
		
	except Exception as err:
				print (">> !!CLIENT COULD NOT CONNECT!!\n")
				#print(err)
				#exit()




""" start the client side """
if __name__ == "__main__":
	
	ssl_sock,username,client_ns = NS_Protocol_Client()
	client = Client_Socket(ssl_sock, username, client_ns)
	client.menus()


