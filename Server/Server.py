import socket, ssl, DB_User, DB_Scoreboard, re, AuthManager
import System_log, Server_NS, hashlib, sys, json
from base64 import b64decode,b64encode
from Server_NS import ServerNS
from threading import Thread
from datetime import datetime

import signal
import sys

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

#Global Variables

class ServerSocket:
	
	def __init__(self, newsocket,server_ns):
		self.connssl = newsocket
		self.server_ns = server_ns
		self.username = None
		self.userAuthorized, self.userAuthenticated = False, False
		self.socketConnect()


	def send_encrypted(self,message):
		message = self.server_ns.send_message(message)
		self.connssl.send(message)

	#
	# Connect
	#
	def socketConnect(self):
		
		System_log.writeSystemLog('Server','Server started','info')
		
	
		#
		# Receive Connection
		#
		try:
			System_log.writeSystemLog("Server","Connection attempt","info")
			
			#self.connssl = self.newsocket

			while(1):
				self.messageTransfer()
	
		except Exception as err:
			System_log.writeSystemLog('Server','Connection attempt failed','error')

			print (">> !!USER DOESNT HAS PERMISSIONS!!\n")
			print(err)
	
		print (">> RECEIVED CONNECTION\n")



	#
	# Close connection
	#
	def	socketClose(self):
		
		self.connssl.close()
		#self.sock.close()
		print (">>FINALIZED SOCKET")
		System_log.writeSystemLog('Server','Server closed','info')
		signal_handler("I","I")



	#
	# Get User Credentials for Database Usage
	#
	def userCredentials(self, user, password):
		try:
			if(self.server_ns.receive_message(self.connssl.recv(1024)))!="login":
				mess = self.server_ns.send_message("WRONG OPTION!!")
				self.send(mess)
			else:
				self.username = self.server_ns.receive_message(user.connssl.recv(1024))
				password = self.server_ns.receive_message(pw.connssl.recv(1024))
	
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
	#
	#
	def toList(self, tuples):
	
		lista = []
		for tup in tuples:
			aux = []
			for i in range(0, len(tup)):				
				if( isinstance(tup[i], datetime)):
					aux.append(tup[i].strftime("%d/%m/%Y %H:%M:%S"))
				elif (isinstance(tup[i], bytes) or isinstance(tup[i], bytearray)):
					aux.append(tup[i].decode())		
				else:
					aux.append(tup[i])
					
			
			lista.append(aux)

		return lista






	def login(self, split_decoded):
		
		username = split_decoded[1]
		password = split_decoded[2]
				
		# sanitizing input ....
		sanitizeOutput = self.sanitize_input_username(username)
	
		self.userLogin(username,password, sanitizeOutput)



	def scoreboardMenu(self):
		
		System_log.writeUserLog('',self.username,'Scoreboard access','Scoreboard','Request','info')
		
		if(self.userAuthenticated==True):
			System_log.writeUserLog('',self.username,'Scoreboard access','Scoreboard','Accept','info')
			print("SENDING SCOREBOARDMENU TO USER\n")
			self.send_encrypted("SCOREBOARDMENU")
		
		else:
			System_log.writeUserLog('',self.username,'Scoreboard access','Scoreboard','Rejected','warning')
			print("USER NOT AUTHENTICATED\n")
			self.send_encrypted("NO AUTH")



	def submitMenu(self):
		
		if(self.userAuthenticated==True):
			print("SENDING SUBMITMENU TO USER\n")
			self.send_encrypted("SUBMITMENU")
		else:
			print("USER NOT AUTHENTICATED\n")
			self.send_encrypted("NO AUTH")


	#
	#
	#
	def checkScore(self):
		
		if(self.userAuthenticated == True):
			
			System_log.writeUserLog('',self.username,'User score access','Scoreboard','Request','info')
			self.getAuthorization(1, self.username)
			
			if(self.userAuthorized == True):
				print("SENDING USER SCORE\n")
				points = DB_Scoreboard.get_user_score(self.username)
				System_log.writeUserLog('',self.username,'User score access','Scoreboard','Accepted','info')
				self.send_encrypted(str(points))
			
			else:
				System_log.writeUserLog('',self.username,'User score access','Scoreboard','Rejected','warning')
				print("USER NOT AUTHORIZED\n")
				self.send_encrypted("NO AUTHORIZATION")

		else:
			System_log.writeUserLog('',self.username,'User score access, user not authenticated','Scoreboard','Rejected','error')
			print("USER NOT AUTHENTICATED\n")
			self.send_encrypted("NO AUTHENTICATION")


	#
	#
	#
	def checkVulnerabilityandFingerprint(self):
		
		if(self.userAuthenticated == True):
			
			self.getAuthorization(2, self.username)
			
			if(self.userAuthorized == True):
				result = DB_Scoreboard.get_user_vulnsAndfingerprint(self.username)
				complete_list = []
				#print('OLD RESULT',result)
				for i in range(len(result)):
					complete_list.append([result[i][0].decode(),result[i][1].decode()])

				#print('RESULT ',complete_list)
				result = json.dumps(complete_list)
				
				print("SENDING USER VULNS AND FINGERPRINTS \n")
				
				self.send_encrypted(result)
				self.connssl.send(b"\n\r##")
			else:
				print("USER NOT AUTHORIZED\n")
				
				self.send_encrypted("NO AUTHORIZATION")
				self.connssl.send(b"\n\r##")
		else:
			print("USER NOT AUTHENTICATED\n")
			
			self.send_encrypted("NO AUTH")
			self.connssl.send(b"\n\r##")


	#
	#
	#
	def checkScoreboard(self):
		
		if(self.userAuthenticated==True):
			
			self.getAuthorization(3, self.username)
			
			if(self.userAuthorized == True):
				group_id = DB_User.getUserGroupID(self.username)
				scoreboard = DB_Scoreboard.get_scoreboard(group_id[0])
				scoreboard = json.dumps(self.toList(scoreboard))
				
				print("SENDING SCOREBOARD \n")
				
				self.send_encrypted(scoreboard)
				self.connssl.send(b"\n\r##")
			
			else:
				print("USER NOT AUTHORIZED\n")
				self.send_encrypted("NO AUTHORIZATION")
				self.connssl.send(b"\n\r##")
	
		else:
			print("USER NOT AUTHENTICATED\n")
			self.send_encrypted("NO AUTHENTICATION")
			self.connssl.send(b"\n\r##")



	#
	#
	#
	def checkTeamVulnsandFingerprints(self):
		
		if(self.userAuthenticated == True):
			
			self.getAuthorization(5, self.username)
			
			if(self.userAuthorized == True):
				group_id = DB_User.getUserGroupID(self.username)
				teamVulnsandFing = DB_Scoreboard.get_team_vulnsAndfingerprint(group_id[0])
				teamVulnsandFing = json.dumps(self.toList(teamVulnsandFing))
				
				print("\n\nTEAM:", teamVulnsandFing, "\n\n")
				
				print("SENDING TEAM VULNS AND FINGERPRINTS \n")
				
				self.send_encrypted(teamVulnsandFing)
				self.connssl.send(b"\n\r##")
			
			else:
				print("USER NOT AUTHORIZED\n")
				self.send_encrypted("NO AUTHORIZATION")
				self.connssl.send(b"\n\r##")
		else:
			print("USER NOT AUTHENTICATED\n")
			self.send_encrypted("NO AUTHENTICATION")
			self.connssl.send(b"\n\r##")


	def checkVulnerabilityPoints(self,fingerprint,vulns):
		points=0
		try:
			with open('vulns-points','r') as fp:
				for line in fp:
					linesplit = line.split(';')
					if(linesplit[0]==fingerprint and linesplit[1] in vulns):
						points=points+int(linesplit[2])
			return points
		finally:
			try:
				fp.close()
			except Exception as err:
				print (">> !!VULNERABILITY FINGERPRINTS FILE DOES NOT EXIST!!\n")
				#print(err)
				exit()


	def submitVulnerability(self):

		if(self.userAuthenticated == True):
			
			self.getAuthorization(2, self.username)

			if(self.userAuthorized == True):
				print("ASKING USER FOR VULNERABILITY\n")
				self.send_encrypted("SUBMITVULNERABILITY")
				
				
				print (">>Transfering file")
						
				# receiving the fingerprint
				fingerprint = b""
				while (fingerprint[-4:] != b"\n\r##"):
					fingerprint += self.connssl.recv(1024)
			

				fingerprint = fingerprint.replace(b"\n\r##", b"")
				fingerprint = self.server_ns.receive_message(fingerprint)
				
				print("\nFINGERPRINT:",fingerprint, "\n\n")
					
				print (">>Transfer concluded \n\n>>Transfering file")


				

					# receiving the vulnerabilities file
				vulnFile = b""
				while (vulnFile[-4:] != b"\n\r##"):
					vulnFile += self.connssl.recv(1024)
				if (vulnFile != b"\n\r##"):

				
					vulnFile = vulnFile.replace(b"\n\r##", b"")
					vulnFile = self.server_ns.receive_message(vulnFile)
					vulnFile = b64decode(vulnFile.encode())

					print (">>Transfer concluded")
					
					
					splitLines, vulns = vulnFile.split(), []

					for i in range(len(splitLines)):
						if( splitLines[i] == b"Vulnerability:"):
							vulns.append(str(splitLines[i+1], "utf-8"))


					vulnerabilityPoints = self.checkVulnerabilityPoints(fingerprint,vulns)
						# Adding vulnerabilities to DB
					if(vulnerabilityPoints>0):
						group_id = DB_User.getUserGroupID(self.username)
						bool = DB_Scoreboard.add_score_vulnerability(fingerprint, vulns, self.username, group_id[0],vulnerabilityPoints)
				
						#TODO: Add filename on log
						System_log.writeUserLog('',self.username,'Submited vulnerabilities attempt','Vulnerability','Request','info')
						if( bool ):
							#TODO: Add filename on log
							System_log.writeUserLog('',self.username,'Submited vulnerabilities successfull','Vulnerability','Accepted','info')
							print("ADDED NEW VULNERABILITIES")
							self.send_encrypted("ADDED NEW VULNERABILITIES")
				
						else:
							#TODO: Add filename on log
							System_log.writeUserLog('',self.username,'Submited vulnerabilities already exists','Vulnerability','Rejected','warning')
							print("THIS VULNERABILITIES HAS ALREADY BEEN SUBMITED")
							self.send_encrypted("THIS VULNERABILITIES HAS ALREADY BEEN SUBMITED")
					else:
						System_log.writeUserLog('',self.username,'Submited vulnerability does not exists','Vulnerability','Rejected','warning')
						print("THIS FINGERPRINT OR VULNERABILITIES DOES NOT EXIST")
						self.send_encrypted("THIS FINGERPRINT OR VULNERABILITIES DOES NOT EXIST")
					
			else:
				System_log.writeUserLog('',self.username,'Submited vulnerability attempt, user not authenticated','Vulnerability','Rejected','error')
				print("USER NOT AUTHENTICATED\n")
				self.send_encrypted("NO AUTH")





	#
	# Receive Message
	#
	def messageTransfer(self, command="default"):
		
		try:
		#if(True):
			self.data, string_data, final_data = b"", "", ""
			while (self.data[-4:] != b"\n\r##"):
				self.data += self.connssl.recv(1024)
				#print('self.data ',self.data)

			final_data = self.data[:-4]

			#print('FINAL DATA',final_data)
			decoded = self.server_ns.receive_message(final_data)
			
			#decoded=self.data.decode("UTF-8")
			split_decoded=decoded.split("!-!")
			command=split_decoded[0]
			print('COMMAND: ',command)

			# deal with different possible received messages
			try:
				if(command=="login"):
					self.login(split_decoded)

				elif(command == "scoreboardMenu"):
					self.scoreboardMenu()

				elif(command == "submitMenu" and self.userAuthenticated == True ):
					self.submitMenu()

				elif(command == "checkScore" and self.userAuthenticated == True ):
					self.checkScore()

				elif(command == "checkVulnsandFingerprints" and self.userAuthenticated==True ):
					self.checkVulnerabilityandFingerprint()
				
				elif(command == "checkScoreboard" and self.userAuthenticated==True ):
					self.checkScoreboard()

				elif(command == "checkTeamVulnsandFingerprints" and self.userAuthenticated==True ):
					self.checkTeamVulnsandFingerprints()

				elif(command == "submitVulnerability" and self.userAuthenticated==True ):
					self.submitVulnerability()

				elif(command== "computeFingerprint" and self.userAuthenticated==True):
					self.computeFingerprint()

				elif(command == "exit"):
					self.socketClose()
				
				else:
					self.send("WRONG COMMAND")

			except Exception as err:
				print (">>!!FAILED IN COMMAND!!\n")
				System_log.writeSystemLog('Server','Failed in command reception','error')
				print(err)
			
		except Exception as err:
			print(">>!!FAILED THE TRANSFER!!!\n")
			System_log.writeSystemLog('Server','Failed transfering message','error')
			print(err)



	def computeFingerprint(self):
	
		if(self.userAuthenticated==True):
			
			self.getAuthorization(4, self.username)
			
			if(self.userAuthorized == True):
			
				self.send_encrypted("COMPUTEFINGERPRINT")
			
				print("\n\nASKING USER FOR BINARY FILE\n\n")
				
				data, final_data = b"", ""
				while (data[-4:] != b"\n\r##"):
					data += self.connssl.recv(1024)
				
				#
				if ( data != b"\n\r##"):
				#

					final_data = data.replace(b"\n\r##", b"")
					data = self.server_ns.receive_message(final_data)
					data = b64decode(data.encode())

					# calculate the fingerprint of the file
					hash_object = hashlib.sha512(data)
					fingerprint = hash_object.hexdigest()
		
					print("\n\nFINGERPRINT:", fingerprint, "\n\n")
		
					self.send_encrypted(str(fingerprint))
					self.connssl.send(b"\n\r##")


			else:
				System_log.writeUserLog("", self.username, "Compute fingerprint attempt, user not authorized", "Compute Fingerprint", "Rejected", "error")
				print("USER NOT AUTHORIZED\n")
				self.send_encrypted("NO AUTHORIZATION")
				self.connssl.send(b"\n\r##")
	
		else:
			System_log.writeUserLog("", self.username, "Compute fingerprint attempt, user not authenticated", "Compute Fingerprint", "Rejected", "error")
			print("USER NOT AUTHENTICATED\n")
			self.send_encrypted("NO AUTH")
			self.connssl.send(b"\n\r##")
		
	#
	# Autenticar user
	#
	def userLogin(self, user, pw, goodInput):
		
		if( goodInput ):
			
			System_log.writeUserLog('',user,'Authentication','Users','Request','info')
			
			if(DB_User.authenticate(user,pw)):
				System_log.writeUserLog('',user,'Authentication','Users','Accepted','info')
				print("USER AUTHENTICATED!!!\n")
				self.send_encrypted("USER AUTHENTICATED!!!")
				self.userAuthenticated = True
				self.username = user
	
			else:
				System_log.writeUserLog('',user,'Authentication','Users','Rejected','info')
				print("USER NOT AUTHENTICATED!!!\n")
				self.send_encrypted("USER NOT AUTHENTICATED!!!")
				self.userAuthenticated = False
		else:
			System_log.writeUserLog('',user,'Authentication, wrong input','Users','Rejected','error')
			print(">> USERNAME CAN ONLY CONTAIN NUMBERS, LETTERS AND _   \n")
			self.send_encrypted("USERNAME CAN ONLY CONTAIN NUMBERS, LETTERS AND '_' !!!")



	def getAuthorization(self, operation, user):
		
		if(AuthManager.getAuthorizationValues(operation, user)):
			
			self.userAuthorized = True
			System_log.writeUserLog("",user,"Authorization - operation:" + str(operation),"Users","Accepted","info")
	
		else:
			System_log.writeUserLog("",user,"Authorization - operation:"+ str(operation),"Users","False","info")
			self.userAuthorized=False




def NS_Protocol_Server(sock):

	try:
		
		print ("\n\n>> WAITING CONNECTION\n")
		
		socketClient, newSocket = sock.accept()

		server_ns = ServerNS("Server","server.key")

		print('\n>>STARTED TRUST MANAGER AUTHENTICATION\n\n')
		
		print("RECEIVED STEP 1")
		mess=socketClient.recv(1024)
		mess = json.loads(mess.decode())
		print( mess, "\n" )
		result = server_ns.round1_client(mess)
		print('result: ',result)

		print("SENDING STEP 3")
		socketClient.send( json.dumps(result).encode() )
		print( "\n" )


		print("RECEIVED STEP 5")
		mess = json.loads(socketClient.recv(1024).decode())
		print( mess, "\n" )
		result = server_ns.round3_client(mess)
		print('result: ',result)

		print("SENDING STEP 6")
		socketClient.send( result )
		print( "\n" )

		print("RECEIVED STEP 7")
		mess = socketClient.recv(1024)
		print( mess, "\n" )
		result = server_ns.round4_client(mess)
		print('result: ',result)

		print("VERIFY STEP 8")
		print( "\n" )
		
		if(result ==False):
			raise Exception('Trust Manager Authentication failed')


	except Exception as err:
				print (">> !!CONNECTION INTERRUPTED!!\n")
				print(err)
				exit()

	
	print ("\n>>FINALIZED TRUST MANAGER AUTHENTICATION\n\n")

	return socketClient,server_ns
	#System_log.writeSystemLog('Server','Server closed','info')
	#exit()






def main():
	#incrementPort = 0
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind((HOST, PORT))
		sock.listen(5)
		
		while True:
			newSocket,server_ns = NS_Protocol_Server(sock)
			Thread(target=ServerSocket, args=(newSocket, server_ns),daemon=True).start()

	except Exception as err:
				print (">> !!SERVER COULD NOT START!!\n")
				#print(err)
				#exit()



def signal_handler(signal, frame):
	print('\n>>CONNECTION CLOSED\n')
	sys.exit(0)


#NS_Protocol_Server()
if __name__== "__main__":
	signal.signal(signal.SIGINT, signal_handler)
	signal.signal(signal.SIGTERM, signal_handler)
	main()




