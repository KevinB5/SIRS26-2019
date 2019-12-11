import mysql.connector, sys, hashlib, json
from datetime import datetime
import System_log

def connect():
	db = mysql.connector.connect(
			host="localhost",
			user="SIRSGROUP26",
			passwd="group26",
			database="SIRS26SCOREBOARD"
		)
	System_log.writeSystemLog("Database Scoreboard","Connection attempt","info")
	return db





def get_user_score(username):
	try:
		db = connect()

		# TODO check if username is present in Scoreboard
 
		# retrieve points of the username
		cursor = db.cursor(prepared=True)
		query = "SELECT points FROM Scoreboard WHERE username=%s"
		parameters = [username]
		cursor.execute(query,parameters)
		result = cursor.fetchone()

		System_log.writeSystemLog('Database Scoreboard','Connection successful','info')
		#print(result)
		return result[0];


	except Exception as e:
		# UNCOMENT FOR DATABASE LOGIN DEBUG
		# print("Error connecting to the server")
		System_log.writeSystemLog('Database Scoreboard','Connection failed','error')
		print(e)

	finally:
		if db.is_connected():
			cursor.close()
			db.close()
			System_log.writeSystemLog('Database Scoreboard','Connection closed','info')




def get_user_vulnsAndfingerprint(username):
	try:
		db = connect()
		cursor = db.cursor(prepared=True)
		query = "SELECT username, fingerprint, name_vul FROM Vulnerability WHERE username=%s;"
		parameters = [username]
		cursor.execute(query,parameters)
		result = cursor.fetchall()
		
		return result;
	
	
	except Exception as e:
		# UNCOMENT FOR DATABASE LOGIN DEBUG
		# print("Error connecting to the server")
		print(e)
	
	finally:
		if db.is_connected():
			cursor.close()
			db.close()
			System_log.writeSystemLog('Database Scoreboard','Connection successful','info')



def get_scoreboard(group_id):
	try:
		db = connect()
		cursor = db.cursor(prepared=True)
		query = "SELECT username, points, num_vul, last_update  FROM Scoreboard WHERE group_id=%s;"
		parameters = [group_id]
		cursor.execute(query,parameters)
		result = cursor.fetchall()

		print("RESULT SCOREBOARD:",result)

		return result
	
	
	except Exception as e:
		# UNCOMENT FOR DATABASE LOGIN DEBUG
		# print("Error connecting to the server")
		System_log.writeSystemLog('Database Scoreboard','Connection failed','error')
		print(e)
	
	finally:
		if db.is_connected():
			cursor.close()
			db.close()




def get_team_vulnsAndfingerprint(group_id):
	try:
		db = connect()
		cursor = db.cursor(prepared=True)
		query = "SELECT username, fingerprint, name_vul FROM Vulnerability WHERE group_id=%s;"
		parameters = [group_id]
		cursor.execute(query,parameters)
		result = cursor.fetchall()
		
		print("RESULT TEAM VULNS:",result)
		
		return result;
	
	
	except Exception as e:
		# UNCOMENT FOR DATABASE LOGIN DEBUG
		# print("Error connecting to the server")
		print(e)
	
	finally:
		if db.is_connected():
			cursor.close()
			db.close()
			System_log.writeSystemLog("Database Scoreboard","Connection closed","info")




def add_score_vulnerability(fingerprint, vulns, username, group_id,updated_points):
	

	result = vulnerability_exist(fingerprint, vulns, username)

	if(result == False):
		return False

	else:
		try:
			db = connect()
			
			# Updated Points and Number of Vulnerabilities
			
			#updated_points = len(result)*10
			updated_numVul = len(result)
			
			cursor = db.cursor(prepared=True)
			query = "UPDATE Scoreboard SET points=points+%s, num_vul=num_vul+%s WHERE username=%s"
			parameters = [updated_points,updated_numVul,username]
			cursor.execute(query,parameters)
			db.commit()
			
			# Insert the new vulnerabilities
			for nameVuln in result:
				cursor = db.cursor(prepared=True)
				query = "INSERT INTO Vulnerability (username,group_id,fingerprint,name_vul) VALUES (%s,%s,%s,%s)"
				parameters = [username,group_id,fingerprint,nameVuln]
				cursor.execute(query,parameters)
				db.commit()
			
			System_log.writeSystemLog('Database Scoreboard','Connection successful','info')
			return True

		except Exception as e:
			# UNCOMENT FOR DATABASE LOGIN DEBUG
			# print("Error connecting to the server")
			System_log.writeSystemLog('Database Scoreboard','Connection failed','error')
			print(e)

		finally:
			System_log.writeSystemLog('Database Scoreboard','Connection closed','info')
			if db.is_connected():
				cursor.close()
				db.close()



def vulnerability_exist(fingerprint, vulns, username):
	try:
		db = connect()
		
		# query the scoreboard to check if vuln was already submitted
		cursor = db.cursor(prepared=True)
		query = "SELECT name_vul FROM Vulnerability WHERE fingerprint=%s AND username=%s"
		parameters = [fingerprint, username]
		cursor.execute(query,parameters)
		result = cursor.fetchall()

		print('RESULT EXIST',result)
		if( result == [] ):
			return vulns


		notRepeated = []
		
		for vuln in vulns:
			repeated = False
			
			for storedVuln in result:
				if( storedVuln[0].decode() == vuln ):
					repeated = True
					break
	
			if( not repeated ):
				notRepeated.append(vuln)
	
	
		System_log.writeSystemLog('Database Scoreboard','Connection successful','info')
		# Return the vulns to be added to DB , else return False
		if( len(notRepeated) != 0 ):
			return notRepeated

		else:
			return False


	except Exception as e:
		# UNCOMENT FOR DATABASE LOGIN DEBUG
		# print("Error connecting to the server")
		System_log.writeSystemLog('Database Scoreboard','Connection failed','error')
		print(e)

	finally:
		if db.is_connected():
			cursor.close()
			db.close()
			System_log.writeSystemLog('Database Scoreboard','Connection closed','info')



