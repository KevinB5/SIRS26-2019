import json
import uuid
import os
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

from Crypto.Random import get_random_bytes

#from Crypto.Util.Padding import pad, unpad

from base64 import b64decode,b64encode
import random
import hashlib
import base64
from TrustManager_log import TrustManagerLog

BS = 16
pad = lambda s: s + (BS-len(s) % BS) *chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1:])]



class TrustManagerNS:
	
	def __init__(self):
		self.log = TrustManagerLog()



	def encrypt_shared_keys(self):

		key,iv = self.get_key("Keys/trustmanager.key")
		aes_key = AES.new(pad(key)[:16], AES.MODE_CBC, pad(iv)[:16])
		try:
			with open("Keys/shared_keys_temp","r") as fp:
				with open("Keys/shared_keys","a") as write_file:
					for line in fp:
						content = base64.b64encode(aes_key.encrypt(pad(line)))
						#print(content)
						#write_file.write(content)
						#write_file.flush()

		key,iv = self.get_key('Keys/trustmanager.key')
		aes_key = AES.new(bytes(pad(key)[:32],'utf-8'), AES.MODE_CBC, bytes(pad(iv)[:16],'utf-8'))
		try:
			with open('Keys/shared_keys_temp','r') as fp:
				with open('Keys/shared_keys','wb') as write_file:
					for line in fp:
						#content = base64.b64encode(aes_key.encrypt(bytes(pad(line),'utf-8')))
						content = aes_key.encrypt(bytes(pad(line),'utf-8'))
						print('written: ',content)
						write_file.write(content)
						write_file.write('\n'.encode('utf-8'))
						write_file.flush()

		finally:
			write_file.close()
			fp.close()



	def read_shared_key(self,entity):

		filename="Keys/"
		key,iv = self.get_key("Keys/trustmanager.key")
		aes_key = AES.new(pad(key)[:16], AES.MODE_CBC, pad(iv)[:16])

		filename='Keys/'
		key,iv = self.get_key('Keys/trustmanager.key')
		aes_key = AES.new(bytes(pad(key)[:32],'utf-8'), AES.MODE_CBC, bytes(pad(iv)[:16],'utf-8'))

		try:
			with open('Keys/shared_keys','rb') as fp:
				for line in fp:

					line = base64.b64decode(line)
					line = unpad(aes_key.decrypt(line))
					split = line.split(":")
					if split[0]==entity:
						filename += split[1].rstrip("\n")
						#print(filename)

					#print('line base64 ',line)
					#line = base64.b64decode(line)

					#print('decoded ',line)
					#line = str(line)[2:]
					#print('test ',line[:-1])
					
					line = aes_key.decrypt(line[:-1])
					#print('TEMP ',str(line))
					
					#TODO: TEMPORARY FIX
					#pad_index = line.index("key")
					#line = line[2:pad_index+3]
					
					line = (unpad(line))[:-1]
					#print('UNPAD ',line)
					split = str(line).split(':')
					#print('SPLIT ',str(split))
					#print('COMPARE ',str(split[0])[2:],' and ',entity)
					if str(split[0])[2:]==entity:
						#print('SPLIT ',split)
						filename += str(split[1])[:-1]
						print('SUCCESS ',filename)

						return self.get_key(filename)
		finally:
			fp.close()
		
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
		finally:
			f.close()
		#print(key,'and',iv)
		return key,iv



	# round1 is done on server side
	def round2_client(self,message):
		source = message['source']
		destination = message['destination']
		nonce = message['nonce']
		response = message['response']

		self.log.writeLog(source,destination,nonce,'Received connection request','ACCEPTED','info')
		
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
		print('encrypting: ',content_bytes)
		print('')
		print('ENCRYPTED: ',encrypted_response)
		response_message = {'nonce':nonce,'destination':destination,'session_key':str(base64.b64encode(key),'utf-8'),\
		'session_iv':str(base64.b64encode(iv),'utf-8'),'response': str(encrypted_response)}
		print('final ',response_message)

		client_key,client_iv = self.read_shared_key(source)
		client_encryptor = AES.new(bytes(pad(client_key)[:32],'utf-8'), AES.MODE_CBC, bytes(pad(client_iv)[:16],'utf-8'))
		
		response_message = json.dumps(response_message)
		#print(response_message)
		final_response = client_encryptor.encrypt(bytes(pad(response_message),'utf-8'))
		return final_response
