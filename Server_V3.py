import socket, ssl, MySQL, re


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)


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
	# Sanitize the Input
	#
	def sanitize_input(self, username):

		if( re.match("^[A-Za-z0-9_]*$", username) ):
			# username only uses letters, numbers and "_"
			return 1
		else:
			return 0

	
	#
	# Receive Message
	#
	def messageTransfer(self, command="default"):

		try:
			self.data = b""
			string_data=""
			while (self.data[-4:] != b"\n\r##"):
				self.data += self.connssl.recv(1024)

			self.data = self.data.replace(b"\n\r##", b"")
			decoded=self.data.decode("UTF-8")
			
			split_decoded=decoded.split("!-!")
			command=split_decoded[0]

			# deal with different possible received messages
			try:
				if(command=="login"):
					
					username = split_decoded[1]
					password = split_decoded[2]
					
					# sanitizing input ....
					sanitizeOutput = self.sanitize_input(username)
					
					self.userLogin(username,password, sanitizeOutput)
			
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
		if( goodInput ):
			
			if(MySQL.authenticate(user,pw)):
				print("USER AUTHENTICATED!!!\n")
				self.connssl.send(b"USER AUTHENTICATED!!!")
	
			else:
				print("USER NOT AUTHENTICATED!!!\n")
				self.connssl.send(b"USER NOT AUTHENTICATED!!!")
		else:
			print(">> USERNAME CAN ONLY CONTAIN NUMBERS, LETTERS AND _   \n")
			self.connssl.send(b"USERNAME CAN ONLY CONTAIN NUMBERS, LETTERS AND '_' !!!")



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


