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
        #nonce = uuid.uuid4().hex
        nonce = os.urandom(16)

        content = {'nonce':base64.encodestring(nonce).rstrip('\n'),'destination':client}
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
        #TODO:
        #print('DECRYPTED R3: ',decrypted_response)

        first_coma = decrypted_response.index("source")
        #print('PLEASE ',decrypted_response[first_coma:])
        temporary_fix = '{'+decrypted_response[first_coma-1:]
        #print('TEMPORARY ',temporary_fix)
        temporary_fix = json.loads(temporary_fix)
        
        #self.nonce = temporary_fix['nonce']
        self.session_key=base64.decodestring(temporary_fix['session_key'])
        self.session_iv=base64.decodestring(temporary_fix['session_iv'])
        #nonce = uuid.uuid4().hex
        nonce = os.urandom(16)
        self.nonce = nonce

        session = AES.new(self.session_key, AES.MODE_CBC, self.session_iv)
        
        response = {'nonce': base64.encodestring(nonce).rstrip('\n')}
        response = json.dumps(response)
        final_response = session.encrypt(pad(response))
        return final_response

    def round4_client(self,client_message):
        #print('server nonce ',self.nonce)
        nonce = ''.join(str(ord(c)) for c in self.nonce)
        #print('server estimated nonce ',nonce)
        server_nonce = int(nonce)- 1
        aes = AES.new(self.session_key, AES.MODE_CBC, self.session_iv)
        message = unpad(aes.decrypt(client_message))
        #print('Round 4 message: ',message)

        first_coma = message.index("nonce")
        #print('PLEASE ',message[first_coma:])
        temporary_fix = '{'+message[first_coma-1:]
        #print('TEMPORARY ',temporary_fix)
        temporary_fix = json.loads(temporary_fix)

        #message = json.loads(message)
        client_nonce = temporary_fix['nonce']

        result=False
        if server_nonce == client_nonce:
            result=True
        
        #response = {'result':result}
        #response = json.dumps(response)
        #final_response = aes.encrypt(pad(response))
        return result
    