import socket
import sys

total_players=2
questions=[]
answers=[]
options=[]
scoreboard[0]=0
scoreboard[1]=0
count =0
with open("questions.txt")  as q:
    questions[count]=q[count][0]
    options[questions[count]]=q[count][1]
    answers[questions[count]]=q[count][2]

sock=socket.socket(socket.AF_INET,socket.SOCK_SOCKDGRAM)
server_address=('localhost',10000)
sock.bind(server_address)
print("[*]Server Started at %s:%s"%server_address)
players=[]
countp=0
while(len(players)<total_players):
    data,address=sock.recvfrom(4096)
    if data=="connect" and address not in players :
        players[countp]=address

playerno=0
for question in questions:
    sock.sendto(question,players[playerno])
    data,address=sock.recvfrom()
    if address==players[playerno]:
        if data==answers[question]:
            scoreboard[playerno]+=1
            playerno+=1
        else:
            playerno+=1
    if playerno>1:
        playerno=0

if scoreboard[0]>scoreboard[1]:
    print("****Player 1 Wins****")

if scoreboard[0]<scoreboard[1]:
    print("****Player 2 Wins****")

else:
    print("****Tie Game****")
