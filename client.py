
import socket

client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

server_address=('127.0.0.1',10000)
#client.connect(server_address)
print("[*]To Connect Press Y")
ans=raw_input()
if ans=='Y':
    client.sendto("connect",server_address)
    data,address = client.recvfrom(4096)
    if address==server_address:
        print ("Server responded %s"%(data))
while True:
    data,address=client.recvfrom(4096)
    print(data)
    if address==server_address:
        a=raw_input()
        client.sendto(a,server_address)
