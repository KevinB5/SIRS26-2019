import hashlib, sys, json
from Crypto.Cipher import AES
from base64 import b64decode, b64encode



BS = 16
pad = lambda s: s + (BS-len(s) % BS) *chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1:])]



def get_keys():

	with open("Keys/server.key", "r") as fp:
		for line in fp:
			split = line.split("=")
			
			if(split[0]=="key"):
				key = split[1].rstrip("\n")
				
			elif(split[0]=="iv "):
				iv = split[1].rstrip("\n")

	fp.close()
	return key, iv



#
#
#
def Server_NS_Encrypt_Points_File(key, iv):


	aes = AES.new(key[:32], AES.MODE_CBC, iv[:16])

	with open("vulns-points-2.txt", "rb") as file:
		message = file.read()
		
	file.close()
	

	with open("vulns-points-2.txt", "wb") as file:
		message = b64encode(message).decode()
		encrypted_message = aes.encrypt(pad(message))
		file.write(encrypted_message)

	file.close()


#
#
#
def Server_NS_Decrypt_Points_File(key, iv):
	
	aes = AES.new(key[:32], AES.MODE_CBC, iv[:16])
	
	with open("vulns-points-2.txt", "rb") as file:
		message = file.read()
		
	file.close()
		
		
	with open("vulns-points-2.txt", "wb") as file:
		encrypted_message = b64decode(unpad(aes.decrypt(message)))
		
		file.write(encrypted_message)

	file.close()



#
#
#
def read_file(str):

	with open("vulns-points-2.txt", "rb") as file:
		print("\n\n" + str, file.read(), "\n\n")
	
	file.close()




if __name__== "__main__":
	
	key, iv = get_keys()
	
	read_file("FIRST: ")
	Server_NS_Encrypt_Points_File(key, iv)

	read_file("SECOND: ")
	Server_NS_Decrypt_Points_File(key, iv)

	read_file("LAST: ")

















