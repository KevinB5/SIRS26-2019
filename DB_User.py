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
		password = password
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