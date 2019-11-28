import json

def receive(message, public_key):
	source = message['source']
	destination = message['destination']
	nonce = message['nonce']
	server_response = message['response']

	if public_key == None:
		#verificar public keys
		pass
