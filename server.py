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
server_address=address=('localhost',10000)
server.bind(server_address)

print("[*]Server started at %s:%s"%(server_address))
print("[*]Rules of the Game\n[*]Reply with only the option letter\n[*]If you answer correctly, you area awarded 2 points.\n[*If you answer incorrectly, you get no points.\n[*]Correct challenged questions, are awarded one point, wrong are penalised with -2 points. [*]Withdrawal of Challenged is penalised with -1 point")
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
    print(players[cplayerno(playerno)])
    server.sendto("[*]Do you want to challenge?(Y/N)",players[cplayerno(playerno+1)])
    resp,challenger=server.recvfrom(4096)
    if(challenger==players[cplayerno(playerno+1)]):
        if resp=='Y':
            server.sendto("[*] "+question+"\n"+o,players[cplayerno(playerno)])
            ans=""
            playah=()
            ans,playah==server.recvfrom(4096)
            print(ans)
            print(playah)
            if playah==players[cplayerno(playerno)]:
                if ans==answers[question]:
                    score[cplayerno(playerno)]+=2
                    server.sendto("[*]Correct Answer. You are awared 2 points.",players[cplayerno(playerno)])
                else:
                    server.send("{[*]Wrong Answer. You are awarded 0 points.",players[cplayerno(playerno)])
                    server.sendto("[*](Challenged Question. 0 to ignore Challenged Question) "+question+"\n"+o,players[cplayerno(playerno+1)])
                    challenge,chall==server.recvfrom(4096)
                    if chall==players[cplayerno(playerno+1)]:
                        if challenge=='0':
                            score[cplayerno(playerno+1)]-=1
                            server.send("{[*]Wrong Answer. You are awarded -1 points.",players[cplayerno(playerno)])
                        elif challenge==answers[question]:
                            score[cplayerno(playerno+1)]+=1
                            server.send("{[*]Wrong Answer. You are awarded 1 point.",players[cplayerno(playerno)])
                        else:
                            score[cplayerno(playerno+1)]-=2
                            server.send("{[*]Wrong Answer. You are awarded -2 points.",players[cplayerno(playerno)])
        else:
            server.sendto("[*] "+question+"\n"+o,players[cplayerno(playerno)])
            ans,playah==server.recvfrom(4096)
            if playah==players[cplayerno(playerno)]:
                if ans==answers[question]:
                    score[cplayerno(playerno)]+=2
                    server.sendto("[*]Correct Answer. You are awared 2 points.",players[cplayerno(playerno)])
                else:
                    server.send("{[*]Wrong Answer. You are awarded 0 points.",players[cplayerno(playerno)])
    data,address=server.recvfrom(4096)
    playerno+=1
print(score[0])
print(score[1])
