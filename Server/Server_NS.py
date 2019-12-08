import os, pickle, json
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
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
            with open('Keys/'+self.key_file) as fp:
                for line in fp:
                    split = line.split("=")
                    if split[0]=="key":
                        self.trustmanager_key= split[1].rstrip("\n")
                    elif split[0]=="iv ":
                        self.trustmanager_iv= split[1].rstrip("\n")
        finally:
            try:
                fp.close()
            except Exception as err:
                print (">> !!SERVER DOESN'T HAS KEY!!\n")
                print(err)
                exit()



    def round1_client(self,client_message):        
        client = client_message["source"]
        nonce = os.urandom(16)
        self.nonce = nonce
        content = {'nonce':str(b64encode(nonce),'utf-8'),'destination':client}
        aes_key = bytes(pad(self.trustmanager_key)[:32],'utf-8')
        iv = bytes(pad(self.trustmanager_iv)[:16],'utf-8')
        trustmanager_session = AES.new(aes_key, AES.MODE_CBC, iv)

        content_bytes = json.dumps(content)
        encrypted_content = trustmanager_session.encrypt(bytes(pad(content_bytes),'utf-8'))
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

        nonce_check = b64decode(decrypted_response['nonce'])
        if(nonce_check==self.nonce):
            self.session_key=b64decode(decrypted_response['session_key'])
            self.session_iv=b64decode(decrypted_response['session_iv'])
            nonce = os.urandom(16)
            self.nonce = nonce

            session = AES.new(self.session_key, AES.MODE_CBC, self.session_iv)
            response = {'nonce': str(b64encode(nonce),'utf-8')}
            response = json.dumps(response)
            final_response = session.encrypt(bytes(pad(response),'utf-8'))
            return final_response
        else:
            raise Exception("Nonce does not match")

    def round4_client(self,client_message):
        server_nonce =  int.from_bytes(self.nonce,byteorder='little')-1
        aes = AES.new(self.session_key, AES.MODE_CBC, self.session_iv)
        message = unpad(aes.decrypt(client_message))
        message = json.loads(str(message,'utf-8'))
        client_nonce = message['nonce']

        #print('SERVER NONCE: ',server_nonce)
        #print('CLIENT NONCE: ',client_nonce)
        result=False
        if server_nonce == client_nonce:
            result=True
        return result
    
    def send_message(self,content):
        aes = AES.new(self.session_key[:32], AES.MODE_CBC, self.session_iv[:16])
        nonce = os.urandom(16)
        self.nonce = nonce
        message = {'nonce':str(b64encode(nonce),'utf-8'),'content':content}
        message = json.dumps(message)
        encrypted_message = aes.encrypt(bytes(pad(message),'utf-8'))
        return encrypted_message

    def receive_message(self,message):
        decryptor = AES.new(self.session_key[:32], AES.MODE_CBC, self.session_iv[:16])
        decrypted_response = json.loads(unpad(decryptor.decrypt(message)))

        #print('DECRYPTED ',decrypted_response)
        nonce = b64decode(decrypted_response['nonce'])
        if(nonce==self.nonce):
            message = decrypted_response['content']
            return message
        else:
            raise Exception("Nonce does not match")