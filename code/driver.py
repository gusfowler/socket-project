import sys
from time import sleep
from Connection import getIP()
from socket import gethostbyname()

args = sys.argfv

args.remove('/code/driver.py')

IP = getIP()
print("My IP is ", IP)
serverIP = gethostbyname("socket-project_server_1")

if args[0] == 'manager':
    from ManagePeer2Peer import Manager
    server = Manager(IP)

    while True:
        print("Number of players: ", len(server.players), "\tNumber of Games: ", len(server.games))
        sleep(5)

elif args[0] == 'player':
    from ManagePeer2Peer import Player
    myName = args[1]
    player = Player(IP, myName)
