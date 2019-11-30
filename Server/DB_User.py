import mysql.connector
import sys

def connect():
	db = mysql.connector.connect(
			host="localhost",
			user="SIRSGROUP26",
			passwd="group26",
			database="SIRS26USERS"
		)
	return db



def authenticate(user, password):
	try:
		db = connect()

		# UNCOMENT FOR USER & PASS CONSOLE INPUT
		# username = raw_input("Insert your username:")
		# password = raw_input("Insert your password:")

		# Username and Password coming from Server.py
		username = user
		password = hashlib.sha256(password.encode()).hexdigest()
		cursor = db.cursor(prepared=True)
		query = "SELECT username FROM Users WHERE username=%s AND password=%s;"
		parameters = (username,password)
		cursor.execute(query,parameters)
		result = cursor.fetchone()

		if result != None:
			# UNCOMENT FOR DATABASE LOGIN DEBUG
			# print('Login Successful')
			return True;
		else:
			return False;
			# sys.exit()


	except Exception as e:
		# UNCOMENT FOR DATABASE LOGIN DEBUG
		# print("Error connecting to the server")
		print(e)

	finally:
		if db.is_connected():
			cursor.close()
			db.close()

def authorization(username, auth_type):
	try:
		db = connect()

		# UNCOMENT FOR USER & PASS CONSOLE INPUT
		# username = raw_input("Insert your username:")
		# password = raw_input("Insert your password:")

		# Username and Password coming from Server.py
		username = str(username)
		auth_type = str(auth_type)
		cursor = db.cursor(prepared=True)
		query = "SELECT username FROM Users WHERE username=%s AND auth_type=%s;"
		parameters = (username,auth_type)
		cursor.execute(query,parameters)
		result = cursor.fetchone()

		if result != None:
			# UNCOMENT FOR DATABASE LOGIN DEBUG
			# print('Login Successful')
			return True;
		else:
			return False;
			# sys.exit()


	except Exception as e:
		# UNCOMENT FOR DATABASE LOGIN DEBUG
		# print("Error connecting to the server")
		print(e)

	finally:
		if db.is_connected():
			cursor.close()
			db.close()



def getUsersList():
	try:
		db = connect()
		cursor = db.cursor(prepared=True)
		query = "SELECT username FROM Users ;"
		cursor.execute(query)
		result = cursor.fetchall()
		decodedresult=[]
		for row in result:
			decodedresult.append(row[0].decode('utf-8'))

		return decodedresult;

	except Exception as e:
		print(e)

	finally:
		if db.is_connected():
			cursor.close()
			db.close()



def getGroupIDList():
	try:
		db = connect()
		cursor = db.cursor(prepared=True)
		query = "SELECT group_id FROM Users ;"
		cursor.execute(query)
		result = cursor.fetchall()
		return result


	except Exception as e:
		print(e)

	finally:
		if db.is_connected():
			cursor.close()
			db.close()



def getUserGroupID(username):
	try:
		db = connect()

		# UNCOMENT FOR USER & PASS CONSOLE INPUT
		# username = raw_input("Insert your username:")
		# password = raw_input("Insert your password:")

		# Username and Password coming from Server.py
		username = str(username)
		group_id ='group_id'
		cursor = db.cursor()
		query = "SELECT group_id FROM Users WHERE" + username + ";"
		cursor.execute(query)
		result = cursor.fetchone()

		if result != None:
			# UNCOMENT FOR DATABASE LOGIN DEBUG
			# print('Login Successful')
			return result;
		else:
			return False;
			# sys.exit()


	except Exception as e:
		# UNCOMENT FOR DATABASE LOGIN DEBUG
		# print("Error connecting to the server")
		print(e)

	finally:
		if db.is_connected():
			cursor.close()
			db.close()



def getUserAuthType(username):
	try:
		db = connect()

		# UNCOMENT FOR USER & PASS CONSOLE INPUT
		# username = raw_input("Insert your username:")
		# password = raw_input("Insert your password:")

		# Username and Password coming from Server.py
		username = str(username)
		cursor = db.cursor()
		query = "SELECT auth_type FROM Users WHERE" + username + ";"
		cursor.execute(query)
		result = cursor.fetchone()

		if result != None:
			# UNCOMENT FOR DATABASE LOGIN DEBUG
			# print('Login Successful')
			return result;
		else:
			return False;
			# sys.exit()


	except Exception as e:
		# UNCOMENT FOR DATABASE LOGIN DEBUG
		# print("Error connecting to the server")
		print(e)

	finally:
		if db.is_connected():
			cursor.close()
			db.close()




