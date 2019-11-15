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

print('admin:',hashlib.sha256('admin'.encode()).hexdigest())
print('kevin:',hashlib.sha256('kevin'.encode()).hexdigest())
print('tiagom:',hashlib.sha256('tiagom'.encode()).hexdigest())
print('tiagos:',hashlib.sha256('tiagos'.encode()).hexdigest())
print('admin2:',hashlib.sha256('admin2'.encode()).hexdigest())
print('kevin2:',hashlib.sha256('kevin2'.encode()).hexdigest())
print('tiagom2:',hashlib.sha256('tiagom2'.encode()).hexdigest())
print('tiagos2:',hashlib.sha256('tiagos2'.encode()).hexdigest())
