import json
import uuid
import os
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64decode,b64encode
import random
import hashlib
import base64
from TrustManager_log import TrustManagerLog

BS = 16
pad = lambda s: s + (BS-len(s) % BS) *chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]

class TrustManagerNS:
	def __init__(self):
		self.keys = None
		self.log = TrustManagerLog()

	def read_shared_key(self,entity):
		filename='Keys/'
		try:
			with open('Keys/shared_keys') as fp:
				for line in fp:
					split = line.split(':')
					if split[0]==entity:
						filename += split[1].rstrip("\n")
		finally:
			fp.close()
		key = None
		iv = None
		try:
			with open(filename) as fp:
				for line in fp:
					split = line.split('=')
					if split[0]=='key':
						key= split[1].rstrip("\n")
					elif split[0]=='iv ':
						iv= split[1].rstrip("\n")
		finally:
			fp.close()
		return key,iv

	# round1 is done on server side
	def round2_client(self,message):
		source = message['source']
		destination = message['destination']
		nonce = message['nonce']
		response = message['response']

		self.log.writeLog(source,destination,nonce,'Received connection request','ACCEPTED','info')
		
		server_key,server_iv = self.read_shared_key(destination)
		server_encryptor = AES.new(pad(server_key)[:16], AES.MODE_CBC, pad(server_iv)[:16])
		decrypted_response = json.loads(unpad(server_encryptor.decrypt(response)))
		for key,value in decrypted_response.iteritems():
			decrypted_response.pop(key)
			decrypted_response[str(key)] = str(value)
		#print(decrypted_response)

		key = os.urandom(16)
		iv = os.urandom(16)
		#iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])

		#session_key = AES.new(key, AES.MODE_CBC, iv)
		print('nonce ',decrypted_response['nonce'])

		new_reponse = {'nonce1':decrypted_response['nonce'],'source':source\
        ,'session_key':base64.encodestring(key).rstrip("\n"),'session_iv':base64.encodestring(iv).rstrip("\n"),'nonce':decrypted_response['nonce']}
        
		print(new_reponse)
		content_bytes = json.dumps(new_reponse)
		print('TEST ',content_bytes)
		encrypted_response = server_encryptor.encrypt(pad(content_bytes))

		#print(encrypted_response)
		response_message = {'nonce':nonce,'destination':destination,'session_key':base64.encodestring(key).rstrip("\n"),'iv':base64.encodestring(iv).rstrip("\n"),'response': base64.encodestring(encrypted_response).rstrip("\n")}
		#print('final',response)

		client_key,client_iv = self.read_shared_key(source)
		client_encryptor = AES.new(pad(client_key)[:16], AES.MODE_CBC, pad(client_iv)[:16])
		
		response_message = json.dumps(response_message)
		#print(response_message)
		final_response = client_encryptor.encrypt(pad(response_message))
		return final_response
