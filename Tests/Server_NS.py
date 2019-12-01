import json 
import uuid
import os
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP

class ServerNS:
    def __init__(self, my_id):
        self.id = my_id
        self.my_key_pair = None
        self.shared_keys = {}
        self.session_key = None
        self.iv = None
        self.nonce = None

    def get_public_key(self,entity):
        if entity in self.shared_keys:
            return self.shared_keys[entity]
        return None

    def save_public_key(self,entity,public_key):
        self.shared_keys[entity] = public_key

    def generate_key_pair(self):
        self.my_key_pair = RSA.generate(1024, Random.new().read)

    def round1_client(self,client_message):
        if self.my_key_pair is None:
            self.generate_key_pair()
        my_public_key = self.my_key_pair.publickey

        print(self.my_key_pair)
        
        client = client_message['source']
        client_public_key = client_message['source_public_key']
        nonce = uuid.uuid4().hex

        if client_public_key != None and client_public_key != self.get_public_key(client):
            self.save_public_key(client,client_public_key)

        content = {'nonce':nonce,'destination':client}
        encryptor = PKCS1_OAEP.new(self.my_key_pair)

        content_bytes = json.dumps(content)
        print(content_bytes)
        encrypted_content = encryptor.encrypt(content_bytes)
        response = {'source':self.id,'source_public_key':my_public_key,'response':encrypted_content}

        return response

    def round3_client(self,client_message):
        message_decrypted = self.my_key_pair.decrypt(client_message, 32)
        message = JSON.parse(message_decrypted)
        
        self.nonce = message['nonce']
        self.session_key=message['session_key']
        self.iv=message['iv']
        nonce = uuid.uuid4().hex
        aes = AES.new(self.session_key, AES.MODE_CBC, self.iv)
        
        response = {'nonce':nonce}
        final_response = aes.encrypt(response)
        return final_response

    def round4_client(self,client_message):
        server_nonce = self.nonce- 1
        aes = AES.new(self.session_key, AES.MODE_CBC, self.iv)
        message = aes.decrypt(client_message)
        client_nonce = message['nonce']

        result=False
        if server_nonce == client_nonce:
            result=True
        

        response = {'result':result}
        return response
    