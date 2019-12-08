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
unpad = lambda s : s[0:-ord(s[-1:])]


class ClientNS:
	def __init__(self, my_id, key_file):
		self.id = my_id
		self.trustmanager_key = None
		self.trustmanager_iv = None
		self.current_nonce = None
		self.key_file = key_file
		self.session_key = None
		self.session_iv = None
		self.server = None
		self.read_trustmanager_key()


	def read_trustmanager_key(self):
		try:
			with open('Keys/'+self.key_file) as fp:
				for line in fp:
					split = line.split('=')
					if split[0]=='key':
						self.trustmanager_key= split[1].rstrip("\n")
					elif split[0]=='iv ':
						self.trustmanager_iv= split[1].rstrip("\n")
		except Exception as err:
			print (">> !!USER DOESN'T HAS KEY!!\n")
			print(err)
			exit()
		finally:
			try:
				fp.close()

			except Exception as err:
				print (">> !!USER DOESN'T HAS KEY!!\n")
				print(err)
				exit()



	def round1_server(self):
		message = {"source":self.id}
		return message



	def round2_trustmanager(self,server_response):
		self.server = server_response['source']
		response = server_response['response']
		nonce = os.urandom(16)
		self.current_nonce = nonce
		message = {'source':self.id,'destination':self.server,'nonce':str(base64.b64encode(nonce),'utf-8'),'response':response}
		return message



	def round3_server(self,trustmanager_response):
		decryptor = AES.new(bytes(pad(self.trustmanager_key)[:32],'utf-8'), AES.MODE_CBC, bytes(pad(self.trustmanager_iv)[:16],'utf-8'))
		decrypted_response = json.loads(unpad(decryptor.decrypt(trustmanager_response)))
		nonce = base64.b64decode(decrypted_response['nonce'])
		if(nonce==self.current_nonce):
			self.session_key= base64.b64decode(decrypted_response['session_key'])
			self.session_iv=base64.b64decode(decrypted_response['session_iv'])
			final_response = decrypted_response['response']
			message = {'response':final_response}
			return message
		else:
			raise Exception("Nonce does not match")

	def round4_server(self,server_response):
		aes = AES.new(self.session_key[:32], AES.MODE_CBC, self.session_iv[:16])
		response = unpad(aes.decrypt(server_response))
		response = json.loads(response)
		nonce = base64.b64decode(response['nonce'])
		self.current_nonce = nonce
		calculated_nonce = int.from_bytes(nonce,byteorder='little')-1
		response = {'nonce':calculated_nonce}
		response = json.dumps(response)
		aes2 = AES.new(self.session_key[:32], AES.MODE_CBC, self.session_iv[:16])
		final_response = aes2.encrypt(bytes(pad(response),'utf-8'))
		return final_response

	def send_message(self,content):
		aes = AES.new(self.session_key[:32], AES.MODE_CBC, self.session_iv[:16])
		nonce = self.current_nonce
		message = {'nonce':str(base64.b64encode(nonce),'utf-8'),'content':content}
		message = json.dumps(message)
		encrypted_message = aes.encrypt(bytes(pad(message),'utf-8'))
		return encrypted_message

	def receive_message(self,message):
		decryptor = AES.new(self.session_key[:32], AES.MODE_CBC, self.session_iv[:16])
		message = decryptor.decrypt(message)
		message = unpad(message)
		print('received',message)
		decrypted_response = json.loads(message)
		nonce = base64.b64decode(decrypted_response['nonce'])
		self.current_nonce = nonce
		message = decrypted_response['content']
		return message
		
