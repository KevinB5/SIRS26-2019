import logging
from imp import reload
import hashlib


class TrustManagerLog:
	def __init__(self):
		self.filename= "./log/trustmanager.log"

	def configTrustManagerLog(self,logging_level):
		reload(logging)
		logging.basicConfig(filename=self.filename
			, level= logging_level\
		#	,filemode='w' \
			,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s' \
			,datefmt='%m/%d/%Y %I:%M:%S %p')
	# filemode='w' causes to overwrite the log file, use it for tests or to clean the log

	def writeLog(self,source,destination,nonce,action, acceptance,type_of_message):
		try:
			message = """SOURCE:{source}; DESTINATION:{destination}; NONCE:{nonce}; \
	ACTION:{action};ACCEPTANCE:{acceptance};""".format(source=source,destination=destination, \
		nonce=nonce,action=action,acceptance=acceptance)

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
						


