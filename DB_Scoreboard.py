import mysql.connector
import sys
import hashlib

def connect():
	db = mysql.connector.connect(
			host="localhost",
			user="SIRSGROUP26",
			passwd="group26",
			database="SIRS26SCOREBOARD"
		)
	return db

def get_group_scoreboard(group_id):
	try:
		db = connect()

		group_id = str(group_id)
		cursor = db.cursor(prepared=True)
		query = "SELECT username,points,num_vul FROM Scoreboard WHERE group_id=%s ORDER BY points DESC LIMIT 10"
		parameters = (group_id)
		cursor.execute(query,parameters)
		result = cursor.fetchall()

		print(result)
		return result;


	except Exception as e:
		# UNCOMENT FOR DATABASE LOGIN DEBUG
		# print("Error connecting to the server")
		print(e)

	finally:
		if db.is_connected():
			cursor.close()
			db.close()

def get_user_score(user_id):
	try:
		db = connect()

		user_id = str(user_id)
		cursor = db.cursor(prepared=True)
		query = "SELECT username,points,num_vul FROM Scoreboard WHERE user_id=%s LIMIT 1"
		parameters = (user_id)
		cursor.execute(query,parameters)
		result = cursor.fetchone()

		print(result)
		return result;


	except Exception as e:
		# UNCOMENT FOR DATABASE LOGIN DEBUG
		# print("Error connecting to the server")
		print(e)

	finally:
		if db.is_connected():
			cursor.close()
			db.close()

def add_score_vulnerability(user_id,points,name_vul):
	# When private key system is done, use:  user_id+private_key+name_vul
	content = str(user_id)+name_vul
	fingerprint = hashlib.sha256(content.encode()).hexdigest()

	if(vulnerability_exist(fingerprint)):
		return False

	else:
		try:
			db = connect()

			user_id = str(user_id)
			name_vul = str(name_vul)

			cursor = db.cursor(prepared=True)
			query = "SELECT points,num_vul FROM Scoreboard WHERE user_id=%s"
			parameters = (user_id)
			cursor.execute(query,parameters)
			result = cursor.fetchone()
			print(result)

			updated_points=result[0]+points
			updated_num_vul=result[1]+1
			print(user_id,' update ',updated_points,' ',updated_num_vul)
			
			cursor = db.cursor(prepared=True)
			query = "UPDATE Scoreboard SET points=%s,num_vul=%s WHERE user_id=%s"
			parameters = [updated_points,updated_num_vul,user_id]
			cursor.execute(query,parameters)
			db.commit()
			#print('updated')
			#print(cursor.rowcount,' records affected')
			
			cursor = db.cursor(prepared=True)
			query = "INSERT INTO Vulnerability (user_id,fingerprint,name_vul) VALUES (%s,%s,%s)"
			parameters = [user_id,fingerprint,name_vul]
			cursor.execute(query,parameters)
			db.commit()
			print('inserted')
			#print(cursor.rowcount,' records affected')
			
			return True

		except Exception as e:
			# UNCOMENT FOR DATABASE LOGIN DEBUG
			# print("Error connecting to the server")
			print(e)

		finally:
			if db.is_connected():
				cursor.close()
				db.close()

def vulnerability_exist(fingerprint):
	try:
		db = connect()

		fingerprint = str(fingerprint)

		print(fingerprint)
		cursor = db.cursor(prepared=True)
		query = "SELECT id_vul FROM Vulnerability WHERE fingerprint=%s"
		parameters = [fingerprint]
		cursor.execute(query,parameters)
		result = cursor.fetchone()

		print(result)
		return result;


	except Exception as e:
		# UNCOMENT FOR DATABASE LOGIN DEBUG
		# print("Error connecting to the server")
		print(e)

	finally:
		if db.is_connected():
			cursor.close()
			db.close()



