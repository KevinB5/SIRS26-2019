import json
import uuid
import os
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

from Crypto.Random import get_random_bytes

#from Crypto.Util.Padding import pad, unpad
import socket, ssl
from base64 import b64decode,b64encode
import random
import hashlib
import base64
from TrustManager_log import TrustManagerLog

import signal
import sys

from threading import Thread

def signal_handler(signal, frame):
	print('\n>>PROGRAM TERMINATED\n')
	sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

BS = 16
pad = lambda s: s + (BS-len(s) % BS) *chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1:])]

#HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
#PORT = 65433       # Port to listen on (non-privileged ports are > 1023)
#PORT2 = 65440
HOST = "192.168.1.100"
PORT = 65432

class TrustManagerNS:
	
	def __init__(self):
		self.log = TrustManagerLog()



	def encrypt_shared_keys(self):


		key,iv = self.get_key('Keys/trustmanager.key')
		aes_key = AES.new(bytes(pad(key)[:32],'utf-8'), AES.MODE_CBC, bytes(pad(iv)[:16],'utf-8'))
		try:
			with open('Keys/shared_keys_temp','r') as fp:
				with open('Keys/shared_keys','wb') as write_file:
					for line in fp:
						#content = base64.b64encode(aes_key.encrypt(bytes(pad(line),'utf-8')))
						content = aes_key.encrypt(bytes(pad(line),'utf-8'))
						#print('written: ',content)
						write_file.write(content)
						write_file.write('\n'.encode('utf-8'))
						write_file.flush()

		finally:
			try:
				write_file.close()
				fp.close()
			except Exception as err:
				print (">> !!TRUST MANAGER DOESN'T HAS KEY!!\n")
				print(err)
				exit()



	def read_shared_key(self,entity):

		filename='Keys/'
		key,iv = self.get_key('Keys/trustmanager.key')
		aes_key = AES.new(bytes(pad(key)[:32],'utf-8'), AES.MODE_CBC, bytes(pad(iv)[:16],'utf-8'))

		try:
			with open('Keys/shared_keys','rb') as fp:
				for line in fp:
					line = aes_key.decrypt(line[:-1])
					line = (unpad(line))[:-1]
					split = str(line).split(':')
					if str(split[0])[2:]==entity:
						filename += str(split[1])[:-1]
						#print('SUCCESS ',filename)

						return self.get_key(filename)
		finally:
			try:
				fp.close()
			except Exception as err:
				print (">> !!USER DOESN'T HAS KEY!!\n")
				print(err)
				exit()
		
		return None

		

	def get_key(self,filename):
		key = None
		iv = None
		try:
			with open(filename) as f:
				for line in f:
					split = line.split('=')
					if split[0]=='key':
						key= split[1].rstrip("\n")
					elif split[0]=='iv ':
						iv= split[1].rstrip("\n")
					elif split[0]=='validation'
						validation= split[1].rstrip("\n")
		finally:	
			try:
				f.close()
			except Exception as err:
				print (">> !!USER DOESN'T HAS KEY!!\n")
				print(err)
				exit()
		#print(key,'and',iv)
		return key,iv



	# round1 is done on server side
	def round2_client(self,message):
		try:
			source = message['source']
			destination = message['destination']
			nonce = message['nonce']
			response = message['response']
			response = base64.b64decode(response)

			self.log.writeLog(source,destination,nonce,'Received connection request','REQUEST','info')
			
			#print('RESULT ',self.read_shared_key(destination))
			server_key,server_iv = self.read_shared_key(destination)
			server_encryptor = AES.new(bytes(pad(server_key)[:32],'utf-8'), AES.MODE_CBC, bytes(pad(server_iv)[:16],'utf-8'))
			decrypted_response = json.loads(unpad(server_encryptor.decrypt(response)))
			for key,value in decrypted_response.items():
				decrypted_response.pop(key)
				decrypted_response[str(key)] = str(value)
			#print(decrypted_response)

			key = os.urandom(32)
			iv = os.urandom(16)
			#iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])

			#session_key = AES.new(key, AES.MODE_CBC, iv)
			#print('nonce ',decrypted_response['nonce'])

			#new_reponse = {'nonce1':decrypted_response['nonce'],
			new_response = {'source':source,'session_key':str(base64.b64encode(key),'utf-8'),\
			'session_iv':str(base64.b64encode(iv),'utf-8'),'nonce':decrypted_response['nonce']}

			content_bytes = json.dumps(new_response)
			#print('TEST ',content_bytes)
			server_encryptor2 = AES.new(bytes(pad(server_key)[:32],'utf-8'), AES.MODE_CBC, bytes(pad(server_iv)[:16],'utf-8'))
			#print('SERVER KEY ',bytes(pad(server_key)[:32],'utf-8'),' iv ',bytes(pad(server_iv)[:16],'utf-8'))

			encrypted_response = server_encryptor2.encrypt(bytes(pad(content_bytes),'utf-8'))
			#print('ENCRYPTED: ',encrypted_response)
			response_message = {'nonce':nonce,'destination':destination,'session_key':str(base64.b64encode(key),'utf-8'),\
			'session_iv':str(base64.b64encode(iv),'utf-8'),'response': str(encrypted_response)}
			#print('final ',response_message)

			client_key,client_iv = self.read_shared_key(source)
			client_encryptor = AES.new(bytes(pad(client_key)[:32],'utf-8'), AES.MODE_CBC, bytes(pad(client_iv)[:16],'utf-8'))
			
			response_message = json.dumps(response_message)
			#print(response_message)
			final_response = client_encryptor.encrypt(bytes(pad(response_message),'utf-8'))

			self.log.writeLog(source,destination,nonce,'Authentication granted','ACCEPTED','info')
			return final_response
		except Exception as err:
				print (">> !!AUTHENTICATION INTERRUPTED!!\n")
				self.log.writeLog(source,destination,nonce,'Authentication rejected','REJECTED','error')
				#print(err)
				#exit()
				

def NS_Protocol_TrustManager(sock):

	try:
		print ("\n\n>> WAITING CONNECTION\n")
		
		socketClient, clientSocket = sock.accept()
		trust = TrustManagerNS()

		print("RECEIVED STEP 3")
		mess = json.loads(socketClient.recv(1024).decode())
		#print( mess, "\n" )
		result = trust.round2_client(mess)
		#print('result: ',result)

		print("SENDING STEP 4")
		socketClient.send( result )

		print (">>FINALIZED CONNECTION\n\n")
		
		trust.log.writeLog("","","",'Connection closed','REJECTED','warning')

	except Exception as err:
				print (">> !!CONNECTION INTERRUPTED!!\n")
				trust.log.writeLog("","","",'Connection terminated','REJECTED','error')
	#			print(err)
				#NS_Protocol_TrustManager(sock)
				#exit()

	#exit()
def main():
	#incrementPort=0
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.bind((HOST, PORT2))
		sock.listen(5)
		while(1):
			#Thread(target=NS_Protocol_TrustManager, args=(PORT2+incrementPort)).start()
			NS_Protocol_TrustManager(sock)
			#incrementPort+=1
		socketClient.close()
		sock.close()
		print (">>FINALIZED SOCKET\n\n")
	except Exception as err:
				print (">> !!TRUST MANAGER COULD NOT START!!\n")
				#print(err)
				#exit()

if __name__== "__main__":
	main()
