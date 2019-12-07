import mysql.connector, sys, HashPwd, System_log

def connect():
	db = mysql.connector.connect(
			host="localhost",
			user="SIRSGROUP26",
			passwd="group26",
			database="SIRS26USERS"
		)
	System_log.writeSystemLog('Database Users','Connection attemp','info')
	return db



def authenticate(user, password):
	try:
		db = connect()

		# UNCOMENT FOR USER & PASS CONSOLE INPUT
		# username = raw_input("Insert your username:")
		# password = raw_input("Insert your password:")

		# Username and Password coming from Server.py
		username = user
		
		cursor = db.cursor(prepared=True)
		query = "SELECT username, password FROM Users WHERE username=%s;"
		parameters = [(username)]
		cursor.execute(query,parameters)
		result = cursor.fetchone()

		# to check if the hash matches the password
		hash = HashPwd.Hash(bytes(password, "utf-8"), user)
		#hash = HashPwd.Hash(bytes(password), user)

		System_log.writeSystemLog('Database Users','Connection successful','info')
		
		
		#print(result)
		#print( hash.get_hashed_password() )
		
		
		#if( hash.check_password(bytes(result[1], "utf-8")) == True ):
		if( hash.check_password(bytes(result[1])) == True ):
			# UNCOMENT FOR DATABASE LOGIN DEBUG
			# print('Login Successful')
			return True;
		else:
			return False;
			# sys.exit()


	except Exception as e:
		# UNCOMENT FOR DATABASE LOGIN DEBUG
		# print("Error connecting to the server")
		System_log.writeSystemLog('Database Users','Connection failed','error')
		print(e)

	finally:
		if db.is_connected():
			cursor.close()
			db.close()
			System_log.writeSystemLog('Database Users','Connection closed','info')



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

		System_log.writeSystemLog('Database Users','Connection successful','info')
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
		System_log.writeSystemLog('Database Users','Connection failed','error')
		print(e)

	finally:
		if db.is_connected():
			cursor.close()
			db.close()
			System_log.writeSystemLog('Database Users','Connection closed','info')



def getUsersList():
	try:
		db = connect()
		cursor = db.cursor(prepared=True)
		query = "SELECT username FROM Users;"
		cursor.execute(query)
		result = cursor.fetchall()
		decodedresult=[]
		System_log.writeSystemLog('Database Users','Connection successful','info')
		for row in result:
			decodedresult.append(row[0].decode('utf-8'))

		return decodedresult;

	except Exception as e:
		System_log.writeSystemLog('Database Users','Connection failed','error')
		print(e)

	finally:
		if db.is_connected():
			cursor.close()
			db.close()
			System_log.writeSystemLog('Database Users','Connection closed','info')



def getGroupIDList():
	try:
		db = connect()
		cursor = db.cursor(prepared=True)
		query = "SELECT group_id FROM Users;"
		cursor.execute(query)
		result = cursor.fetchall()

		System_log.writeSystemLog('Database Users','Connection successful','info')
		return result


	except Exception as e:
		System_log.writeSystemLog('Database Users','Connection failed','error')
		print(e)

	finally:
		if db.is_connected():
			cursor.close()
			db.close()
			System_log.writeSystemLog('Database Users','Connection closed','info')



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
		query = "SELECT group_id FROM Users WHERE username=%s;"
		parameters = [username]
		cursor.execute(query, parameters)
		result = cursor.fetchone()

		System_log.writeSystemLog('Database Users','Connection successful','info')
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
		System_log.writeSystemLog('Database Users','Connection failed','error')
		print(e)

	finally:
		if db.is_connected():
			cursor.close()
			db.close()
			System_log.writeSystemLog('Database Users','Connection closed','info')


def getUserAuthType(username):
	try:
		db = connect()

		# UNCOMENT FOR USER & PASS CONSOLE INPUT
		# username = raw_input("Insert your username:")
		# password = raw_input("Insert your password:")

		# Username and Password coming from Server.py
		username = str(username)
		cursor = db.cursor()
		query = "SELECT auth_type FROM Users WHERE username=%s;"
		parameters = [username]
		cursor.execute(query, parameters)
		result = cursor.fetchone()

		System_log.writeSystemLog('Database Users','Connection successful','info')
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
		System_log.writeSystemLog('Database Users','Connection failed','error')
		print(e)

	finally:
		if db.is_connected():
			cursor.close()
			db.close()
			System_log.writeSystemLog('Database Users','Connection closed','info')




