import json
import uuid
import os
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random

class Client_NS:
	def __init__(self, my_id):
		self.id = my_id
		self.my_key_pair = None
		self.shared_keys = None
		self.session_key = None
        self.iv = None
		self.server = None

    def get_public_key(entity):
    	if self.shared_keys.hasOwnProperty(entity):
    		return self.shared_keys[entity]
    	else:
    		return None

    def save_public_key(entity,public_key):
    	self.shared_keys[entity] = public_key

    	def generate_key_pair():
		self.my_key_pair = RSA.generate(1024, Random.new().read)

    def round1_server():
    	if self.my_key_pair == None:
    		my_public_key = None
    	else
    		my_public_key = self.my_key_pair.publickey

    	message = {'source_public_key':my_public_key,'source':self.id}
    	return message

    def round2_trustmanager(server_response):
    	if self.my_key_pair == None:
    		my_public_key = None
    	else
    		my_public_key = self.my_key_pair.publickey

    	server_response = JSON.parse(server_response)
    	self.server = server_response['source']
    	response = server_response['response']
        server_public_key = server_response['source_public_key']
        
        if server_public_key != None and server_public_key != get_public_key(self.server):
            save_public_key(self.server,server_public_key)

    	nonce = uuid.uuid4().hex

    	message = {'source_public_key':my_public_key,'source':self.id,'destination':self.server,'response':response}
    	return message

    def round3_server(trustmanager_response):
    	response_decrypted = self.my_key_pair.privatekey.decrypt(trustmanager_response, 32)
    	response = JSON.parse(response_decrypted)
    	self.session_key=response['session_key']
        self.iv=response['iv']
    	final_response = response['response']
    	message = {'response':final_response}
    	return message

    def round4_server(server_response):
        aes = AES.new(self.session_key, AES.MODE_CBC, self.iv)
        response = aes.decrypt(server_response)
        nonce = response['nonce'] - 1
    	response = {'nonce':nonce}
        final_response = aes.encrypt(response)

    	message = {'response':final_response}
    	return message

