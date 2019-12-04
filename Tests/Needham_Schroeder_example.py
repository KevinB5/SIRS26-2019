from Client_NS import ClientNS
from Server_NS import ServerNS
from TrustManager import TrustManagerNS


client = ClientNS("Admin","Keys/admin.key")
server = ServerNS("Server","Keys/server.key")
trustmanager = TrustManagerNS()


#trustmanager.encrypt_shared_keys()


print("1 client -> server")


print('1 client -> server')

result = client.round1_server()
print(result)
print("\n")
print("1 server -> client")
result = server.round1_client(result)
print(result)
print("")
'''
print("2 client -> trustmanager")
result = client.round2_trustmanager(result)
print(result)
print("")
print("2 trustmanager -> client")
result = trustmanager.round2_client(result)
print(result)
print("")
print("3 client -> server")
result = client.round3_server(result)
print(result)
print("")
print("3 server -> client")
result = server.round3_client(result)
print(result)
print("")
print("4 client -> server")
result = client.round4_server(result)
print(result)
print("")
print("4 server -> client")
result = server.round4_client(result)
print(result)

'''





