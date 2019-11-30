import socket, ssl, DB_User, re, AuthManager


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
					
					username = split_decoded[1]
					password = split_decoded[2]
					
					# sanitizing input ....
					sanitizeOutput = self.sanitize_input_username(username)
					
					self.userLogin(username,password, sanitizeOutput)

				elif(command == "scoreboardMenu"):
					if(userAuthenticated==True):
						print("SENDING SCOREBOARDMENU TO USER\n")
						self.connssl.send(b"SCOREBOARDMENU")
					else:
						print("USER NOT AUTHENTICATED\n")
						self.connssl.send(b"NO AUTH")											


				elif(command == "submitMenu" and userAuthenticated==True ):
					if(userAuthenticated==True):
						print("SENDING SUBMIT MENU TO USER\n")
						self.connssl.send(b"SUBMITMENU")
					else:
						print("USER NOT AUTHENTICATED\n")
						self.connssl.send(b"NO AUTH")						


				elif(command == "checkScore" and userAuthenticated==True ):
					if(userAuthenticated==True):
						self.getAuthorization(1, username)
						if(userAuthorized==True):
							print("SENDING USER SCORE\n")
							self.connssl.send(b"CHECKSCORE")
						else:
							print("USER NOT AUTHORIZED\n")
							self.connssl.send(b"NO AUTHORIZATION")
					else:
						print("USER NOT AUTHENTICATED\n")
						self.connssl.send(b"NO AUTHENTICATION")

				elif(command == "checkTeamScore" and userAuthenticated==True ):
					if(userAuthenticated==True):
						self.getAuthorization(2, username)
						if(userAuthorized==True):
							print("SENDING TEAM SCORE\n")
							self.connssl.send(b"CHECKTEAMSCORE")
						else:
							print("USER NOT AUTHORIZED\n")
							self.connssl.send(b"NO AUTHORIZATION")
					else:
						print("USER NOT AUTHENTICATED\n")
						self.connssl.send(b"NO AUTHENTICATION")					


				elif(command == "checkVulnerability" and userAuthenticated==True ):
					if(userAuthenticated==True):
						self.getAuthorization(3, username)
						if(userAuthorized==True):
							print("SENDING TEAM VULNERABILITIES\n")
							self.connssl.send(b"CHECKVULNERABILITY")
						else:
							print("USER NOT AUTHORIZED\n")
							self.connssl.send(b"NO AUTHORIZATION")
						
					else:
						print("USER NOT AUTHENTICATED\n")
						self.connssl.send(b"NO AUTH")						

				elif(command == "checkFingerprint" and userAuthenticated==True ):
					if(userAuthenticated==True):
						self.getAuthorization(4, username)
						if(userAuthorized==True):
							print("SENDING TEAM FINGERPRINTS\n")
							self.connssl.send(b"CHECKFINGERPRINTS")
						else:
							print("USER NOT AUTHORIZED\n")
							self.connssl.send(b"NO AUTHORIZATION")
					else:
						print("USER NOT AUTHENTICATED\n")
						self.connssl.send(b"NO AUTH")

				elif(command == "submitVulnerability" and userAuthenticated==True ):
					if(userAuthenticated==True):
						self.getAuthorization(5, username)
						if(userAuthorized==True):
							print("ASKING USER FOR VULNERABILITY\n")
							self.connssl.send(b"SUBMITVULNERABILITY")
					else:
						print("USER NOT AUTHENTICATED\n")
						self.connssl.send(b"NO AUTH")		

				elif(command == "submitFingerprint" and userAuthenticated==True ):
					if(userAuthenticated==True):
						self.getAuthorization(6, username)
						if(userAuthorized==True):
							print("ASKING USER FOR FINGERPRINT\n")
							self.connssl.send(b"SUBMITFINGERPRINT")

					else:
						print("USER NOT AUTHENTICATED\n")
						self.connssl.send(b"NO AUTH")		

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
			
			if(MySQL.authenticate(user,pw)):
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


