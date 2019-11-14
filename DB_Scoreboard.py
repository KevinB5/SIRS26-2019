import mysql.connector
import sys

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

def vulnerability_exist(fingerprint):
	try:
		db = connect()

		fingerprint = str(fingerprint)
		cursor = db.cursor(prepared=True)
		query = "SELECT fingerprint FROM Vulnerability WHERE fingerprint=%s LIMIT 1"
		parameters = (fingerprint)
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