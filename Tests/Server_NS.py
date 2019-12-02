import json 
import uuid
import os
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from base64 import b64decode,b64encode
import base64

BS = 16
pad = lambda s: s + (BS-len(s) % BS) *chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]

class ServerNS:
    def __init__(self, my_id,key_file):
        self.id = my_id
        self.trustmanager_key = None
        self.trustmanager_iv = None
        self.key_file = key_file
        self.session_key = None
        self.session_iv = None
        self.server = None
        self.read_trustmanager_key()
        self.nonce = None

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

    def round1_client(self,client_message):        
        client = client_message['source']
        nonce = uuid.uuid4().hex

        content = {'nonce':nonce,'destination':client}
        aes_key = pad(self.trustmanager_key)[:16]
        iv = pad(self.trustmanager_iv)[:16]
        #print('SERVER KEYS ',aes_key,' IV ',iv)
        #aes_key = os.urandom(16)
        #iv = os.urandom(16)
        trustmanager_session = AES.new(aes_key, AES.MODE_CBC, iv)

        content_bytes = json.dumps(content)
        #print(content_bytes)
        #print(pad(content_bytes))
        encrypted_content = trustmanager_session.encrypt(pad(content_bytes))
        #print('ENCRYPTED: ',encrypted_content)
        response = {'source':self.id,'response':encrypted_content}
        return response

    def round3_client(self,client_message):
        aes_key = pad(self.trustmanager_key)[:16]
        iv = pad(self.trustmanager_iv)[:16]
        decryptor = AES.new(aes_key, AES.MODE_CBC, iv)
        response = client_message['response']
        #decoded_response = base64.decodestring(response)
        #print(decoded_response)
        decrypted_response = unpad(decryptor.decrypt(response))
        #json.loads(unpad(
        first_coma = decrypted_response.index("s")
        print('PLEASE ',decrypted_response[first_coma-1:])
        print('DECRYPTED R3: ',decrypted_response)
        
        self.nonce = decrypted_response['nonce']
        self.session_key=decrypted_response['session_key']
        self.session_iv=decrypted_response['iv']
        nonce = uuid.uuid4().hex

        session = AES.new(self.session_key, AES.MODE_CBC, self.session_iv)
        
        response = {'nonce':nonce}
        response = json.dumps(response)
        final_response = session.encrypt(pad(response))
        return final_response

    def round4_client(self,client_message):
        server_nonce = self.nonce- 1
        aes = AES.new(self.session_key, AES.MODE_CBC, self.session_iv)
        message = unpad(aes.decrypt(client_message))
        message = json.loads(message)
        client_nonce = message['nonce']

        result=False
        if server_nonce == client_nonce:
            result=True
        
        response = {'result':result}
        response = json.dumps(response)
        final_response = aes.encrypt(pad(response))
        return response
    