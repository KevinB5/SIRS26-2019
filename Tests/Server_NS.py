import os, pickle
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Util.Padding import pad, unpad
from base64 import b64decode,b64encode




BS = 16
pad = lambda s: s + (BS-len(s) % BS) *chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1:])]


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
                    split = line.split("=")
                    if split[0]=="key":
                        self.trustmanager_key= b64decode(split[1].rstrip("\n"))[:32]
                    elif split[0]=="iv ":
                        self.trustmanager_iv= b64decode(split[1].rstrip("\n"))[:16]
        finally:
            fp.close()



    def round1_client(self,client_message):        
        client = client_message["source"]
		
        nonce = os.urandom(16)
        content = {"nonce":b64encode(nonce), "destination":client}


        aes_key = self.trustmanager_key
        iv = self.trustmanager_iv

        trustmanager_session = AES.new(aes_key, AES.MODE_CBC, iv)
        content_bytes = pickle.dumps(content)
		
		
		
		
        encrypted_content = trustmanager_session.encrypt(pad(content_bytes, AES.blocksize))

        #content = {'nonce':base64.b64encode(nonce).rstrip('\n'),'destination':client}
        content = {'nonce':str(base64.b64encode(nonce),'utf-8'),'destination':client}
        aes_key = bytes(pad(self.trustmanager_key)[:32],'utf-8')
        iv = bytes(pad(self.trustmanager_iv)[:16],'utf-8')
        print('SERVER KEYS ',aes_key,' IV ',iv)
        #aes_key = os.urandom(16)
        #iv = os.urandom(16)
        trustmanager_session = AES.new(aes_key, AES.MODE_CBC, iv)

        content_bytes = json.dumps(content)
        #print(content_bytes)
        #print(pad(content_bytes))
        encrypted_content = trustmanager_session.encrypt(bytes(pad(content_bytes),'utf-8'))

        #print('ENCRYPTED: ',encrypted_content)
        response = {'source':self.id,'response':encrypted_content}
        return response



    def round3_client(self,client_message):
        aes_key = bytes(pad(self.trustmanager_key)[:32],'utf-8')
        iv = bytes(pad(self.trustmanager_iv)[:16],'utf-8')
        #print('USED KEY TRUST ',aes_key,' iv ',iv)
        decryptor = AES.new(aes_key, AES.MODE_CBC, iv)
        response = client_message['response']
        decrypted_response = decryptor.decrypt(bytes(response[2:-1],'utf-8').decode('unicode-escape').encode('ISO-8859-1'))
        decrypted_response = unpad(decrypted_response)
        decrypted_response = json.loads(str(decrypted_response,'utf-8'))

        self.session_key=base64.b64decode(decrypted_response['session_key'])
        self.session_iv=base64.b64decode(decrypted_response['session_iv'])
        #nonce = uuid.uuid4().hex
        nonce = os.urandom(16)
        self.nonce = nonce
        print('r3 nonce ',nonce)

        session = AES.new(self.session_key, AES.MODE_CBC, self.session_iv)
        
        print('SERVER NONCE ',str(base64.b64encode(nonce),'utf-8'))
        response = {'nonce': str(base64.b64encode(nonce),'utf-8')}
        response = json.dumps(response)
        final_response = session.encrypt(bytes(pad(response),'utf-8'))
        return final_response

    def round4_client(self,client_message):
        #server_nonce = nonce- 1
        server_nonce =  int.from_bytes(self.nonce,byteorder='little')-1
        aes = AES.new(self.session_key, AES.MODE_CBC, self.session_iv)
        message = unpad(aes.decrypt(client_message))
        message = json.loads(str(message,'utf-8'))

        #message = json.loads(message)
        client_nonce = message['nonce']

        print('SERVER NONCE: ',server_nonce)
        print('CLIENT NONCE: ',client_nonce)
        result=False
        if server_nonce == client_nonce:
            result=True
        
        #response = {'result':result}
        #response = json.dumps(response)
        #final_response = aes.encrypt(pad(response))
        return result
    
