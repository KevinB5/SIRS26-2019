import logging
from imp import reload
import hashlib



def configUserLog(logging_level):
	reload(logging)
	logging.basicConfig(filename="./log/user.log"
		, level= logging_level\
	#	,filemode='w' \
		,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' \
		,datefmt='%m/%d/%Y %I:%M:%S %p')
# filemode='w' causes to overwrite the log file, use it for tests or to clean the log

def writeUserLog(user_id,username,action, sql_table, acceptance,type_of_message):
	try:
		# SQL table should be hashed 
		sql_table = password = hashlib.sha256(sql_table.encode()).hexdigest()
		message = """USER_ID:{user_id}; USERNAME:{username}; ACTION:{action}; \
SQL_TABLE:{sql_table}; ACCEPTANCE:{acceptance};""".format(user_id=user_id,username=username, \
	action=action,sql_table=sql_table,acceptance=acceptance)

		if(type_of_message.lower() == "info" ):
			configUserLog(logging.INFO)
			logging.info(message)
		elif(type_of_message.lower() == "warning" ):
			configUserLog(logging.WARNING)
			logging.warning(message)
		elif(type_of_message.lower() == "error" ):
			configUserLog(logging.ERROR)
			logging.error(message)
		elif(type_of_message.lower() == "critical" ):
			configUserLog(logging.CRITICAL)
			logging.critical(message)
		
	except Exception as e:
		print(e)

						
#
#
#
def configSystemLog(logging_level):
	reload(logging)
	logging.basicConfig(filename='./log/system.log'
		, level= logging_level\
	#	,filemode='w' \
		,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' \
		,datefmt='%m/%d/%Y %I:%M:%S %p')
# filemode='w' causes to overwrite the log file, use it for tests or to clean the log

def writeSystemLog(topic, event,type_of_message):
	try:
		# SQL table should be hashed 
		message = """TOPIC:{topic}; EVENT:{event};""".\
		format(topic=topic,event=event)

		if(type_of_message.lower() == "info" ):
			configSystemLog(logging.INFO)
			logging.info(message)
		elif(type_of_message.lower() == "warning" ):
			configSystemLog(logging.WARNING)
			logging.warning(message)
		elif(type_of_message.lower() == "error" ):
			configSystemLog(logging.ERROR)
			logging.error(message)
		elif(type_of_message.lower() == "critical" ):
			configSystemLog(logging.CRITICAL)
			logging.critical(message)
		
	except Exception as e:
		print(e)

						
'''
# To test the log
writeUserLog('2','Kevin','Login','Users','Accept','info')
writeUserLog('','Unknow','Login','Users','Reject','warning')
writeSystemLog('Database','Connection to database failed','error')
writeSystemLog('Server','Server crashed','criTical')
'''

