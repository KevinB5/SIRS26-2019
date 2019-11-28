import json
import uuid
import os
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random

class Server_NS:
	def __init__(self, my_id):
		self.id = my_id
		self.my_key_pair = None
		self.shared_keys = None
		self.session_key = None
		self.iv = None
        self.nonce

    def get_public_key(entity):
    	if self.shared_keys.hasOwnProperty(entity):
    		return self.shared_keys[entity]
    	else:
    		return None

    def save_public_key(entity,public_key):
    	self.shared_keys[entity] = public_key

    	def generate_key_pair():
		self.my_key_pair = RSA.generate(1024, Random.new().read)

    def round1_client(client_message):
    	if self.my_key_pair == None:
    		my_public_key = None
    	else
    		my_public_key = self.my_key_pair.publickey

        message = JSON.parse(client_message)
        client = message['source']
        client_public_key = message['source_public_key']
        nonce = uuid.uuid4().hex

        if client_public_key != None and client_public_key != get_public_key(client):
            save_public_key(client,client_public_key)

    	content = {'nonce':nonce,'destination':client}
        encrypted_content = self.my_key_pair.privatekey.encrypt(content, 32)
    	response = {'source':self.id,'source_public_key':my_public_key,'response':encrypted_content}

        return encrypted_response

    def round3_client(client_message):
    	message_decrypted = self.my_key_pair.privatekey.decrypt(client_message, 32)
    	message = JSON.parse(message_decrypted)
    	
        self.nonce = message['nonce']
        self.session_key=message['session_key']
        self.iv=message['iv']
        nonce = uuid.uuid4().hex
        aes = AES.new(self.session_key, AES.MODE_CBC, self.iv)
        
    	response = {'nonce':nonce}
        final_response = aes.encrypt(response)
    	return final_response

    def round4_client(client_message):
        server_nonce = self.nonce- 1
        aes = AES.new(self.session_key, AES.MODE_CBC, self.iv)
        message = aes.decrypt(client_message)
        client_nonce = message['nonce']

        result=False
        if server_nonce == client_nonce:
            result=True
        

        response = {'result':result}
        return response
    