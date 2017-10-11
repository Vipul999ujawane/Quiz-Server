import socket
import json

questions=[]
answers={}
options={}
players=[]
score=[0,0]
count=0

def cplayerno (i):
    if i>1:
        return 0
    else:
        return i

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
server_address=('localhost',10000)
server.bind(server_address)

def challenge(add):
    print("Challenged")
    server.sendto("Do you want to challenge? (Y/N)",add)
    data,recvr=server.recvfrom(10)
    if(recvr==add):
        return data

print("[*]Server started at %s:%s"%(server_address))
print("[*]Rules of the Game\n[*]Reply with only the option letter\n[*]If you answer correctly, you area awarded 2 points.\n[*If you answer incorrectly, you get no points.\n[*]Correct challenged questions, are awarded one point, wrong are penalised with -2 points. [*]Withdrawal of Challenged is penalised with -1 point")
while len(players)<2:
    data,address=server.recvfrom(10)
    if(data=="connect" and address not in players):
        server.sendto("[*]Connection Completed Successfully",address)
        players.append(address)
        print("[*]Player "+str(len(players))+" joined from "+address[0]+":"+str(address[1]))
#print(players)
print("[*]The Quiz Begins")
playerno=0;
for question in questions:
    o=""
    for i in range(4):
        o+=options[question][i]+" "
    print(question+"\n"+o)
    print(players[cplayerno(playerno)])
    print(cplayerno(playerno))
    print(cplayerno(playerno+1))
    c=challenge(players[cplayerno(playerno+1)])
    server.sendto("[*] "+question+"\n"+o,players[cplayerno(playerno)])
    ans,playah=server.recvfrom(10)
    if(playah==players[cplayerno(playerno)]):
        if(ans==answers[question]):
            server.sendto("[*]Right answer. You are awared 2 points. Any key to continue",players[cplayerno(playerno)])
            score[cplayerno(playerno)]+=2
            rand=server.recv(10)
        else:
            server.sendto("[*]Wrong answer. Any key to continue ",players[cplayerno(playerno)])
            rand=server.recv(10)
            if(c=='Y'):
                server.sendto("[*](Challenge Question. Send 0 to opt out.) "+question+"\n"+o,players[cplayerno(playerno+1)])
                response,chall=server.recvfrom(10)
                if(chall==players[cplayerno(playerno+1)]):
                    if(response=='0'):
                        server.sendto("[*]Challenge bypassed. You lose one point. Any key to continue",players[cplayerno(playerno+1)])
                        score[cplayerno(playerno+1)]-=1
                        rand=server.recv(10)
                    if(response==answers[question]):
                        server.sendto("[*]Correct answer. You get one point. Any key to continue",players[cplayerno(playerno+1)])
                        score[cplayerno(playerno+1)]+=1
                        rand=server.recv(10)
                    else:
                        server.sendto("[*]Wrong answer. You lose two points. Any key to continue",players[cplayerno(playerno+1)])
                        score[cplayerno(playerno+1)]-=2
                        rand=server.recv(10)
        playerno+=1
        playerno=cplayerno(playerno)

print("Player 1")
print(score[0])
print("Player 2")
print(score[1])
server.sendto("End",players[0])
server.sendto("End",players[1])
