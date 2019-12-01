from Client_NS import ClientNS
from Server_NS import ServerNS
from TrustManager import TrustManagerNS

client = ClientNS('client1')
server = ServerNS('server')
trustmanager = TrustManagerNS()

print('client -> server')
result = client.round1_server()
print(result)
print('')
print('server -> client')
result = server.round1_client(result)
print(result)
print('')
print('client -> trustmanager')
result = client.round2_trustmanager(result)
print(result)
print('')
print('trustmanager -> client')
result = trustmanager.round2_client(result)
print(result)
