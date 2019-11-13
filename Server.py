import socket, ssl
import MySQL


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)





class ServerSocket:
	
	def socketConnect(self):
		
		print (">>Socket Criado a Aguardar Conexao")
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.bind((HOST, PORT))
		self.sock.listen(1)
	
		# Receber Conexao
		try:
			self.newsocket, self.clientSocket = self.sock.accept()
			print (">>Existe uma tentatica de Conexao")
				
			self.connssl = ssl.wrap_socket(self.newsocket, server_side=True, certfile = "cert.pem", keyfile = "certkey.pem", ssl_version=ssl.PROTOCOL_TLSv1)

		except Exception as err:
			print (">>!!Este Utilizador nao tem permissao!!\n")
			print(err)
	
	
		print (">>Conexao Recebida")
		print ( ">>>IP Remoto: %s" % self.clientSocket[0] )
		print ( ">>>Porta Remota: %d" % self.clientSocket[1] )


	# Get User Credentials for Database Usage
	def userCredentials(self, user, password):
		try:
			if(self.connssl.recv(1024))!='login':
				self.send("Wrong Option!")
			else:
				username=user.connssl.recv(1024)
				password=pw.connssl.recv(1024)
		except Exception as err:
			print (">>!!Falhou a apurar as credenciais!!\n")
			print(err)

	# Receber mensagem
	def messageTransfer(self,command="default"):
		try:

			print (">>A Decorrer Transferencia")
			self.data = b""
			string_data=""
			while (self.data[-4:] != b"\n\r##"):
				self.data += self.connssl.recv(1024)

		
			self.data = self.data.replace(b"\n\r##", b"")
			print (">>>Mensagem Recebida : %s" % self.data)
			decoded=self.data.decode('UTF-8')
			print(decoded)
			split_decoded=decoded.split('!-!')
			print(split_decoded)
			command=split_decoded[0]

			try:
				if command=='login':
					username=split_decoded[1]
					password=split_decoded[2]
					userLogin(username,password)
					x.messageTransfer()
				elif command == 'exit':
					x.socketClose()
				else:
					x.send(b"Wrong Command")
					x.messageTransfer()

			except Exception as err:
				print (">>!!Falhou no command!!\n")
				print(err)

			#self.imageOut = open( "C:\\Users\\Documents\\Projecto\\demo_out.jpg", "wb" )
			#self.imageOut.write(self.data)
			#self.imageOut.close()
			
		except Exception as err:
			print (">>!!Falhou a Transferencia!!\n")
			print(err)
		
	def socketClose(self):

		self.newsocket.close()
		self.sock.close()
		print (">>Socket finalizado")

# Autenticar user	
def userLogin(user,pw):

	if(MySQL.authenticate(user,pw)):
		print("USER AUTHENTICATED")
	else:
		print("USER NOT AUTHENTICATED")


x = ServerSocket()
x.socketConnect()
x.messageTransfer()