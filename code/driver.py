import sys
from time import sleep
from Connection import getIP
from socket import gethostbyname

args = sys.argv

args.remove('/code/driver.py')

IP = getIP()
print("My IP is ", IP)
serverIP = gethostbyname("socket-project_server_1")

if args[0] == 'manager':
    from ManagePeer2Peer import Manager
    server = Manager(IP)

    while True:
        print("Number of players: ", len(server.players), "\tNumber of Games: ", len(server.games))
        if len(server.games) > 0:
            output = ""
            for game in server.games:
                for player in game.players:
                    output += player.name + " "
            print(output)
        sleep(5)

elif args[0] == 'player':
    from managePlayer import Player
    myName = args[1]
    print("I am ", myName)
    sleep(5)
    player = Player(serverIP, myName)

    if len(args) > 2 and args[2] == 'start':
        #sleep(10)
        while True:
            if player.gameReady():
                player.startGame(args[3], args[4])
                break
                
    while True:
        if player.gameReady():
            player.queryGames()
        sleep(5)