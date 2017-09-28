import socket
import json

questions=[]
answers={}
options={}
players=[]
count=0

with open("quiz.json") as o:
    a=json.load(o)
    for i in a:
        questions.append(i['question'])
        answers[i['question']]=i['answer']
        options[i['question']]=i['options']
        #print (" [*] "+str(count)+"   "+str(i))
        count+=1

server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
server.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
server_address=address=('localhost',10000)
server.bind(server_address)

print("[*]Server started at %s:%s"%(server_address))
while len(players)<2:
    data,address=server.recvfrom(4096)
    if(data=="connect" and address not in players):
        server.sendto("[*]Connection Completed Successfully",address)
        players.append(address)
        print("[*]Player "+str(len(players))+" joined from "+address[0])
#print(players)
print("[*]The Quiz Begins")
playerno=0;
for question in questions:
    o=""
    for i in range(4):
        o+=options[question][i]+" "
    print(question+"\n"+o)
    print(players[playerno])
    server.sendto(question+"\n"+o,players[playerno])
    data,address=server.recvfrom(4096)
    if(address==players[playerno]):
        print(data)
    playerno+=1
    if playerno>1:
        playerno=0
