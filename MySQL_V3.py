import mysql.connector, sys, hashlib


def authenticate(user, password):
	try:
		db = mysql.connector.connect(
			host="localhost",
			user="SIRSGROUP26",
			passwd="group26",
			database="SIRS26USERS"
		)
		
		# UNCOMENT FOR USER & PASS CONSOLE INPUT
		# username = raw_input("Insert your username:")
		# password = raw_input("Insert your password:")
	
		# Username and Password coming from Server.py
		username = user
		
		# hash of password given
		password = hashlib.sha256(password.encode()).hexdigest()
		
		# prepared sql statement
		cursor = db.cursor(prepared=True)
		query = "SELECT username FROM Users WHERE username=%s AND password=%s;"
		parameters = (username,password)
		cursor.execute(query,parameters)
		result = cursor.fetchone()
		
		if(result != None):
			# UNCOMENT FOR DATABASE LOGIN DEBUG
			print("\n>> LOGIN SUCCESSFUL")
			return True;
		else:
			print("\n>> USER DOESNT EXIST")
			return False;

	except Exception as e:
		# UNCOMENT FOR DATABASE LOGIN DEBUG
		print("ERROR CONNECTING TO THE SERVER")
		print(e)

	finally:
		if db.is_connected():
			cursor.close()
			db.close()


