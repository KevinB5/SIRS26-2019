import json
import uuid
import os
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random
from base64 import b64decode,b64encode
import base64

BS = 16
pad = lambda s: s + (BS-len(s) % BS) *chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]

class ClientNS:
	def __init__(self, my_id,key_file):
		self.id = my_id
		self.trustmanager_key = None
		self.trustmanager_iv = None
		self.key_file = key_file
		self.session_key = None
		self.session_iv = None
		self.server = None
		self.read_trustmanager_key()


	def read_trustmanager_key(self):
		try:
			with open(self.key_file) as fp:
				for line in fp:
					split = line.split('=')
					if split[0]=='key':
						self.trustmanager_key= split[1].rstrip("\n")
					elif split[0]=='iv ':
						self.trustmanager_iv= split[1].rstrip("\n")
		finally:
			fp.close()

	def round1_server(self):
		message = {'source':self.id}
		return message

	def round2_trustmanager(self,server_response):
		self.server = server_response['source']
		response = server_response['response']
		#nonce = uuid.uuid4().hex
		nonce = os.urandom(16)

		message = {'source':self.id,'destination':self.server,'nonce':base64.encodestring(nonce).rstrip('\n'),'response':response}
		return message

	def round3_server(self,trustmanager_response):
		decryptor = AES.new(pad(self.trustmanager_key)[:16], AES.MODE_CBC, pad(self.trustmanager_iv)[:16])
		decrypted_response = json.loads(unpad(decryptor.decrypt(trustmanager_response)))
		#print(decrypted_response)

		for key,value in decrypted_response.iteritems():
			decrypted_response.pop(key)
			decrypted_response[str(key)] = str(value)
		#print(decrypted_response)

		self.session_key= base64.decodestring(decrypted_response['session_key'])
		self.session_iv=base64.decodestring(decrypted_response['iv'])
		final_response = base64.decodestring(decrypted_response['response'])

		#print('final ',base64.decodestring(final_response))
		message = {'response':final_response}
		return message

	def round4_server(self,server_response):
		aes = AES.new(self.session_key, AES.MODE_CBC, self.session_iv)
		response = unpad(aes.decrypt(server_response))
		#print('ROUND 4 SERVER ',response)
		response = json.loads(response)
		nonce = base64.decodestring(response['nonce'])
		nonce = ''.join(str(ord(c)) for c in nonce)
		calculated_nonce = int(nonce) - 1
		#print('estimated nonce ',calculated_nonce)
		response = {'nonce1':calculated_nonce,'nonce':calculated_nonce}
		response = json.dumps(response)
		#print(response)
		final_response = aes.encrypt(pad(response))
		return final_response
