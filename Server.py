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
		
		
		# Receber mensagem
		try:
			print (">>A Decorrer Transferencia")
			self.data = b""
			while (self.data[-4:] != b"\n\r##"):
				self.data += self.connssl.recv(1024)
			
		
			self.data = self.data.replace(b"\n\r##", b"")
			print (">>>Mensagem Recebida : %s" % self.data)
			
			#autenticar
			MySQL.authenticate(self.data)
			#self.imageOut = open( "C:\\Users\\Documents\\Projecto\\demo_out.jpg", "wb" )
			#self.imageOut.write(self.data)
			#self.imageOut.close()
			print (">>Transferencia Concluida")
			
		except Exception as err:
			print (">>!!Falhou a Transferencia!!\n")
			print(err)
		
		
		self.newsocket.close()
		self.sock.close()
		print (">>Socket finalizado")



x = ServerSocket()
x.socketConnect()


