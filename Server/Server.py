import socket, ssl, DB_User, DB_Scoreboard, re, AuthManager
import System_log


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
		
		System_log.writeSystemLog('Server','Server started','info')
		
		print (">> WAITING CONNECTION\n")
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((HOST, PORT))
		self.sock.listen(1)
	
		#
		# Receive Connection
		#
		try:
			System_log.writeSystemLog('Server','Connection attempt','info')
			
			self.newsocket, self.clientSocket = self.sock.accept()
			print (">> ATTEMPT OF CONNECTION")
				
			self.connssl = ssl.wrap_socket(self.newsocket, server_side=True, certfile = "cert.pem", keyfile = "certkey.pem", ssl_version=ssl.PROTOCOL_TLSv1)

		except Exception as err:
			System_log.writeSystemLog('Server','Connection attempt failed','error')

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
		System_log.writeSystemLog('Server','Server closed','info')
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
		global username
		
		System_log.writeUserLog('',username,'Scoreboard access','Scoreboard','Request','info')
		if(userAuthenticated==True):
			System_log.writeUserLog('',username,'Scoreboard access','Scoreboard','Accept','info')
			print("SENDING SCOREBOARDMENU TO USER\n")
			self.connssl.send(b"SCOREBOARDMENU")
		else:
			System_log.writeUserLog('',username,'Scoreboard access','Scoreboard','Rejected','warning')
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
			System_log.writeUserLog('',username,'User score access','Scoreboard','Request','info')
			if(self.getAuthorization(1, username)):
				print("SENDING USER SCORE\n")
				points = DB_Scoreboard.get_user_score(username)
				System_log.writeUserLog('',username,'User score access','Scoreboard','Accepted','info')
				self.connssl.send(bytes(str(points),"utf-8"))
			else:
				System_log.writeUserLog('',username,'User score access','Scoreboard','Rejected','warning')
				print("USER NOT AUTHORIZED\n")
				self.connssl.send(b"NO AUTHORIZATION")

		else:
			System_log.writeUserLog('',username,'User score access, user not authenticated','Scoreboard','Rejected','error')
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
		
				#TODO: Add filename on log
				System_log.writeUserLog('',username,'Submited vulnerability attempt','Vulnerability','Request','info')
				if( bool ):
					#TODO: Add filename on log
					System_log.writeUserLog('',username,'Submited vulnerability successfull','Vulnerability','Accepted','info')
					print("ADDED NEW VULNS")
		
				else:
					#TODO: Add filename on log
					System_log.writeUserLog('',username,'Submited vulnerability already exists','Vulnerability','Rejected','warning')
					print("ALREADY HAVE THIS VULNS")
					
					
			else:
				System_log.writeUserLog('',username,'Submited vulnerability attempt, user not authenticated','Vulnerability','Rejected','error')
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
				System_log.writeUserLog('Server','Failed in command reception','error')
				print(err)
			
		except Exception as err:
			print(">>!!FAILED THE TRANSFER!!!\n")
			System_log.writeUserLog('Server','Failed transfering message','error')
			print(err)
		
		
	#
	# Autenticar user
	#
	def userLogin(self, user, pw, goodInput):
		global userAuthenticated
		
		if( goodInput ):
			System_log.writeUserLog('',user,'Authentication','Users','Request','info')
			if(DB_User.authenticate(user,pw)):
				System_log.writeUserLog('',user,'Authentication','Users','Accepted','info')
				print("USER AUTHENTICATED!!!\n")
				self.connssl.send(b"USER AUTHENTICATED!!!")
				userAuthenticated=True
	
			else:
				System_log.writeUserLog('',user,'Authentication','Users','Rejected','info')
				print("USER NOT AUTHENTICATED!!!\n")
				self.connssl.send(b"USER NOT AUTHENTICATED!!!")
				userAuthenticated=False
		else:
			System_log.writeUserLog('',user,'Authentication, wrong input','Users','Rejected','error')
			print(">> USERNAME CAN ONLY CONTAIN NUMBERS, LETTERS AND _   \n")
			self.connssl.send(b"USERNAME CAN ONLY CONTAIN NUMBERS, LETTERS AND '_' !!!")



	def getAuthorization(self, operation, user):
		global userAuthorized
		
		if(AuthManager.getAuthorizationValues(operation, user)):
			userAuthorized=True
			System_log.writeUserLog('',user,'Authorization - operation:'+operation,'Users','Accepted','info')
			return userAuthorized
		else:
			System_log.writeUserLog('',user,'Authorization - operation:'+operation,'Users','False','info')
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


