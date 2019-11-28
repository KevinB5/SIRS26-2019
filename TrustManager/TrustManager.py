import json
import uuid
import os
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

class TrustManager:
	def __init__(self, keys):
    	self.keys = keys

    def get_public_key(entity):
    	if self.keys.hasOwnProperty(entity):
    		return self.keys[entity]
    	else:
    		return None

    def save_public_key(entity,public_key):
    	self.keys[entity] = public_key

	def receive_and_respond(message):
		message = JSON.parse(message)
		source = message['source']
		destination = message['destination']
		nonce = message['nonce']
		source_public_key = message['source_public_key']

		server_response = message['response']
		destination_public_key = server_response['destination_public_key']

		if source_public_key == None:
			source_public_key = self.get_public_key(source)
				if source_public_key == None:
					raise Exception('Source Public Key not known')

		if destination_public_key == None:
			destination_public_key = self.get_public_key(destination)
				if destination_public_key == None:
					raise Exception('Destination Public Key not known')

		server_response_decrypted = JSON.parse(destination_public_key.decrypt(server_response))

		nonce = uuid.uuid4().hex
		key = os.urandom(16)
		iv = ''.join([chr(random.randint(0, 0xFF)) for i in range(16)])
		session_key = AES.new(key, AES.MODE_CBC, iv)
		
		server_response_decrypted['session_key'] = session_key
		server_response_encrypted = destination_public_key.encrypt(server_response_decrypted)
		response_message = {'nonce':nonce,'destination':destination,'session_key':session_key,'server_response':server_response_encrypted}
		final_response = source_public_key.encrypt(response_message, 32)

		self.save_public_key(source,source_public_key)
		self.save_public_key(destination,destination_public_key)
		return final_response
