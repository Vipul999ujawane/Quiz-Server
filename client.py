
import socket

client = socket.socket(socket.AF_INET,socket.SOCK_SOCKDGRAM)

server_address=('localhost',10000)
#client.connect(server_address)
print("[*]To Connect Press Y")
if input()=='Y':
    client.sendto("connect",server_address)
    #response = client.recv(4096)
    #print ("Server responded %s"%(response))
while True:
    data,address=client.recvfrom()
    if address==server_address:
        ans=input(data)
        client.sendto(ans,server_address)
