import socket, ssl, DB_User, DB_Scoreboard, re, AuthManager


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

#Global Variables

userAuthenticated=False
userAuthorized=False
username=""



class ServerSocket:
	
	#
	# Connect
	#
	def socketConnect(self):
		
		print (">> WAITING CONNECTION\n")
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((HOST, PORT))
		self.sock.listen(1)
	
		#
		# Receive Connection
		#
		try:
			self.newsocket, self.clientSocket = self.sock.accept()
			print (">> ATTEMPT OF CONNECTION")
				
			self.connssl = ssl.wrap_socket(self.newsocket, server_side=True, certfile = "cert.pem", keyfile = "certkey.pem", ssl_version=ssl.PROTOCOL_TLSv1)

		except Exception as err:
			print (">> !!USER DOESNT HAS PERMISSIONS!!\n")
			print(err)
	
		print (">> RECEIVED CONNECTION\n")


	#
	# Close connection
	#
	def	socketClose(self):
	
		self.newsocket.close()
		self.sock.close()
		print (">>FINALIZED SOCKET")
		exit()

	#
	# Get User Credentials for Database Usage
	#
	def userCredentials(self, user, password):
		try:
			if(self.connssl.recv(1024))!="login":
				self.send("WRONG OPTION!!")
			else:
				username = user.connssl.recv(1024)
				password = pw.connssl.recv(1024)
	
		except Exception as err:
			print (">>!!WRONG CREDENTIALS!!\n")
			print(err)


	#
	# Sanitize the Input for username
	#
	def sanitize_input_username(self, username):

		if( re.match("^[A-Za-z0-9_]*$", username) ):
			# username only uses letters, numbers and "_"
			return 1
		else:
			return 0

	#
	# Sanitize the Input for commands
	#
	def sanitize_input_command(self, command):

		if( re.match("^[A-Za-z_]*$", command) ):
			# username only uses letters, numbers and "_"
			return 1
		else:
			return 0



	def login(self, split_decoded):
		global username
		
		username = split_decoded[1]
		password = split_decoded[2]
				
		# sanitizing input ....
		sanitizeOutput = self.sanitize_input_username(username)
					
		self.userLogin(username,password, sanitizeOutput)



	def scoreboardMenu(self):
		global userAuthenticated
		
		if(userAuthenticated==True):
			print("SENDING SCOREBOARDMENU TO USER\n")
			self.connssl.send(b"SCOREBOARDMENU")
		else:
			print("USER NOT AUTHENTICATED\n")
			self.connssl.send(b"NO AUTH")



	def submitMenu(self):
		global userAuthenticated
		
		if(userAuthenticated==True):
			print("SENDING SUBMITMENU TO USER\n")
			self.connssl.send(b"SUBMITMENU")
		else:
			print("USER NOT AUTHENTICATED\n")
			self.connssl.send(b"NO AUTH")



	def checkScore(self):
		global userAuthenticated
		global username
		
		if(userAuthenticated==True):
			
			if(self.getAuthorization(1, username)):
				print("SENDING USER SCORE\n")
				points = DB_Scoreboard.get_user_score(username)
				self.connssl.send(bytes(str(points),"utf-8"))
			else:
				print("USER NOT AUTHORIZED\n")
				self.connssl.send(b"NO AUTHORIZATION")

		else:
			print("USER NOT AUTHENTICATED\n")
			self.connssl.send(b"NO AUTHENTICATION")



	def checkVulnerabilityandFingerprint(self):
		global userAuthenticated
		global username
		
		if(userAuthenticated==True):
			
			if(self.getAuthorization(2, username)):
				print("SENDING USER VULNERABILITIES AND FINGERPRINTS\n")
				self.connssl.send(b"CHECKVULNERABILITY")
			else:
				print("USER NOT AUTHORIZED\n")
				self.connssl.send(b"NO AUTHORIZATION")
			
		else:
			print("USER NOT AUTHENTICATED\n")
			self.connssl.send(b"NO AUTH")



	def submitVulnerability(self):
		global userAuthenticated
		global username

		if(userAuthenticated==True):
			
			self.getAuthorization(3, username)
			if(userAuthorized==True):
			
				print("ASKING USER FOR VULNERABILITY\n")
				self.connssl.send(b"SUBMITVULNERABILITY")
					
				print (">>A Decorrer Transferencia")
						
				# receiving the binary file
				binFile = b""
				while (binFile[-4:] != b"\n\r##"):
					binFile += self.connssl.recv(1024)
			
				binFile = binFile.replace(b"\n\r##", b"")
					
				print (">>Transferencia Concluida \n\n>>A Decorrer Transferencia")
				
				# receiving the vulnerabilities file
				vulnFile = b""
				while (vulnFile[-4:] != b"\n\r##"):
					vulnFile += self.connssl.recv(1024)
			
				vulnFile = vulnFile.replace(b"\n\r##", b"")
				
				print (">>Transferencia Concluida")
				
				splitLines = vulnFile.split()
				vulns = []
				
				for i in range(len(splitLines)):
					if( splitLines[i] == b"Vulnerability:"):
						vulns.append(str(splitLines[i+1], "utf-8"))
				
				# Adding vulnerabilities to DB
				bool = DB_Scoreboard.add_score_vulnerability(binFile, vulns, username)
		
				if( bool ):
					print("ADDED NEW VULNS")
		
				else:
					print("ALREADY HAVE THIS VULNS")
					
					
			else:
				print("USER NOT AUTHENTICATED\n")
				self.connssl.send(b"NO AUTH")





	#
	# Receive Message
	#
	def messageTransfer(self, command="default"):
		global userAuthenticated
		global username
		global userAuthorized
		
		try:
			self.data = b""
			string_data=""
			while (self.data[-4:] != b"\n\r##"):
				self.data += self.connssl.recv(1024)

			self.data = self.data.replace(b"\n\r##", b"")
			decoded=self.data.decode("UTF-8")
			
			split_decoded=decoded.split("!-!")
			command=split_decoded[0]
			print(command)

			# deal with different possible received messages
			try:
				if(command=="login"):
					self.login(split_decoded)

				elif(command == "scoreboardMenu"):
					self.scoreboardMenu()

				elif(command == "submitMenu" and userAuthenticated==True ):
					self.submitMenu()

				elif(command == "checkScore" and userAuthenticated==True ):
					self.checkScore()

				elif(command == "checkVulnerability" and userAuthenticated==True ):
					self.checkVulnerabilityandFingerprint()

				elif(command == "submitVulnerability" and userAuthenticated==True ):
					self.submitVulnerability()

				elif(command == "exit"):
					self.socketClose()
				
				else:
					self.send(b"WRONG COMMAND")

			except Exception as err:
				print (">>!!FAILED IN COMMAND!!\n")
				print(err)
			
		except Exception as err:
			print(">>!!FAILED THE TRANSFER!!!\n")
			print(err)
		
		
	#
	# Autenticar user
	#
	def userLogin(self, user, pw, goodInput):
		global userAuthenticated
		
		if( goodInput ):
			
			if(DB_User.authenticate(user,pw)):
				print("USER AUTHENTICATED!!!\n")
				self.connssl.send(b"USER AUTHENTICATED!!!")
				userAuthenticated=True
	
			else:
				print("USER NOT AUTHENTICATED!!!\n")
				self.connssl.send(b"USER NOT AUTHENTICATED!!!")
				userAuthenticated=False
		else:
			print(">> USERNAME CAN ONLY CONTAIN NUMBERS, LETTERS AND _   \n")
			self.connssl.send(b"USERNAME CAN ONLY CONTAIN NUMBERS, LETTERS AND '_' !!!")



	def getAuthorization(self, operation, user):
		global userAuthorized
		
		if(AuthManager.getAuthorizationValues(operation, user)):
			userAuthorized=True
			return userAuthorized
		else:
			userAuthorized=False
			return userAuthorized



x = ServerSocket()
x.socketConnect()


while(1):
	x.messageTransfer()







#print ( ">>>IP Remoto: %s" % self.clientSocket[0] )
#print ( ">>>Porta Remota: %d" % self.clientSocket[1] )

#print (">>A Decorrer Transferencia")

#print (">>>Mensagem Recebida : %s" % self.data)

#print(decoded)

#print(split_decoded)

#self.imageOut = open( "C:\\Users\\Documents\\Projecto\\demo_out.jpg", "wb" )
#self.imageOut.write(self.data)
#self.imageOut.close()


