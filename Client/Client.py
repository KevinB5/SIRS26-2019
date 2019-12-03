import socket, ssl, getpass, os, re
import Client_NS

sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM)
ssl_sock = ssl.wrap_socket(sock, ca_certs="cert.pem", cert_reqs=ssl.CERT_REQUIRED)


HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)

# Global Variables
username =''

def mainMenu():
	global username
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
			secondMenu()
		
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




def secondMenu():
		
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
			scoreboardMenu()
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
			submitMenu()
		else:
			print("2-UNKNOWN SERVER RESPONSE, TRY AGAIN")
			secondMenu()

	elif (command=="0"):
		mainMenu()
		
	else:
		print("WRONG COMMAND\n")
		secondMenu()





def scoreboardMenu():
		
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
		scoreboardMenu()



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
		
		scoreboardMenu()


	elif (command=="3"):
		command_as_string = "checkScoreboard"+"!-!"
		ssl_sock.send(command_as_string.encode())
		username_as_string = username+"!-!"
		ssl_sock.send(username_as_string.encode())
		EOF = b"\n\r##"
		ssl_sock.send(EOF)
		# message received from server
		scoreboard = ssl_sock.recv(1024)
		
		#printing the scoreoboard
		print("-" * 300 + "SCOREBOARD" + "-"*270)
		print("\n\n" + " "*10 + "User  ;" + " "*35 + "Points  ;" + " "*10 + "Number of Vulnerabilites;" + " "*10 + "Last_update;" + " "*30 + "\n" )

		scoreboard = str(scoreboard, "utf-8")[1:-1]
		scoreboard = scoreboard.replace("'","")
		scoreboard = scoreboard.replace(" ","")
		scoreboard = re.findall("[^(),]+", scoreboard[1:-1])
		
		for i in range(0,len(scoreboard),10):
		
			print(" "*10 + scoreboard[i+0] + " " *(40-len(scoreboard[i+0])), end="")
			print(" "*2 + scoreboard[i+1] + " " *(10-len(scoreboard[i+1])), end="")
			print(" "*10 + scoreboard[i+2] + " " *(30-len(scoreboard[i+2])), end="")
			
			date = scoreboard[i+4] + "/" + scoreboard[i+5] + "/" + scoreboard[i+6]
			time = scoreboard[i+7] + ":" + scoreboard[i+8] + ":" + scoreboard[i+9]
			print(  date + " " + time, "\n")
		

		scoreboardMenu()

	elif (command=="4"):
		command_as_string = "checkTeamVulnsandFingerprints"+"!-!"
		ssl_sock.send(command_as_string.encode())
		username_as_string = username+"!-!"
		ssl_sock.send(username_as_string.encode())
		EOF = b"\n\r##"
		ssl_sock.send(EOF)
		
		# message received from server
		mess = ssl_sock.recv(1024)
		
		if(mess == b"NO AUTHORIZATION"):
			print("\n\n" + "-"*20 + "ONLY THE TEAM LEADER IS AUTHORIZED TO SEE THE EXPLOITS OF THE TEAM" + "-"*20 + "\n")
		
		else:
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
		
		
		
		scoreboardMenu()



	elif (command=="0"):
		secondMenu()

		
	else:
		print("WRONG COMMAND\n")
		scoreboardMenu()





def submitMenu():
		
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
			
			submitMenu()
		

		else:
			print("UNKNOWN SERVER RESPONSE, TRY AGAIN")
			submitMenu()


	elif (command=="0"):
		secondMenu()

	else:
		print("WRONG COMMAND\n")
		submitMenu()



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




""" start the client side """
try:
	ssl_sock.connect((HOST, PORT))
	print( "\n>> CONNECTION ESTABLISHED !" )

except:
	print( "\n>> CONNECTION LOST!" )


mainMenu()


'''
if __name__ == "__main__":

	start()
'''


# f = open( "C:\\Users\\Documents\\Projecto\\demo.jpg", "rb" )
#data = b"OLA"
# data = f.readlines()
# for line in data:


# f.close()

# ssl_sock.close()
# print( ">> Envio terminado!" )
