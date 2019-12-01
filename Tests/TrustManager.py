import json
import uuid
import os
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64decode,b64encode

class TrustManagerNS:
	def __init__(self):
		self.keys = None

	def get_public_key(self,entity):
		if self.keys.hasOwnProperty(entity):
			return self.keys[entity]
		else:
			return None

	def save_public_key(self,entity,public_key):
		self.keys[entity] = public_key

	# round1 is done on server side
	def round2_client(self,message):
		source = message['source']
		destination = message['destination']
		nonce = message['nonce']
		source_public_key = message['source_public_key']

		response = message['response']
		destination_public_key = message['destination_public_key']

		if source_public_key == None:
			source_public_key = self.get_public_key(source)
			if source_public_key == None:
				raise Exception('Source Public Key not known')

		if destination_public_key == None:
			destination_public_key = self.get_public_key(destination)
			if destination_public_key == None:
				raise Exception('Destination Public Key not known')

		print(type(destination_public_key))
		print(destination_public_key)
		destination_public_key = RSA.importKey(str(destination_public_key))
		decryptor = PKCS1_OAEP.new(destination_public_key)
		response_decrypted = json.loads(decryptor.decrypt(response))
		print(response_decrypted)

		nonce = uuid.uuid4().hex
		key = os.urandom(16)
		iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])
		session_key = AES.new(key, AES.MODE_CBC, iv)
		
		response_decrypted['session_key'] = session_key
		response_decrypted['iv'] = iv
		response_encrypted = destination_public_key.encrypt(response_decrypted)
		response_message = {'nonce':nonce,'destination':destination,'session_key':session_key,'iv':iv,'response':response_encrypted}
		final_response = source_public_key.encrypt(response_message, 32)

		self.save_public_key(source,source_public_key)
		self.save_public_key(destination,destination_public_key)
		return final_response
