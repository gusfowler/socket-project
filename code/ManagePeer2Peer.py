import Connection
import threading
from time import sleep

## CHECKING TO SEE IF SUBLIME TEXT WORKS
PORTS_USED = []
GROUP_NUMBER = 44
PORT_LOWER_BOUND = (((GROUP_NUMBER / 2) * 1000) + 1000)
PORT_UPPER_BOUND = (((GROUP_NUMBER / 2) * 1000) + 1499)

def generatePort():
    for port in range(int(PORT_LOWER_BOUND), int(PORT_UPPER_BOUND) + 1):
        if port not in PORTS_USED:
            return port
    print("ERROR:\tALL PORTS USED")
    return -1

class Manager(threading.Thread):
    from Game import manageGame
    class Player:
        def __init__(self, address, name):
            self.address = address
            self.name = name
            self.UDPPort = 0
            self.inGame = False

    def findPlayer(self, name):
        for player in self.players:
            if player.name == name:
                return player
        return -1

    def findPlayerByAddress(self, address):
        for player in self.players:
            if address == player.address:
                return player
        return -1

    def findPlayerByIP(self, IP):
        for player in self.players:
            if IP == player.address[0]:
                return player
        return -1

    def registerPlayer(self, address, name):
        player = self.Player(address, name)
        self.players.append(player)

        if len(self.players) > 1:
            for player in self.players:
                if player.UDPPort == 0:
                    port = generatePort()
                    player.UDPPort = port
                    PORTS_USED.append(port)

    def __init__(self, IP):
        threading.Thread.__init__(self)
        if IP is None:
            IP = Connection.getIP()
        self.server = Connection.Server(IP, PORT_LOWER_BOUND)
        self.pairs_evaled = []
        self.players = []
        self.games = []
        PORTS_USED.append(PORT_LOWER_BOUND)

        self.start()

    def run(self):
        while self.server:
            incomingMessages = self.server.getMsgs()

            for msg in incomingMessages:
                if msg[0][1] not in PORTS_USED: PORTS_USED.append(msg[0][1])

                if 'REGISTER' in msg[1]:
                    register = msg[1].split(' ')
                    if self.findPlayer(register[1]) == -1:
                        self.registerPlayer(msg[0], register[1])
                        self.server.sendMsg(msg[0], "SUCCESS")
                    else:
                        self.server.sendMsg(msg[0], "FAILURE")
                        self.server.drop(msg[0])
                
                if 'QUERY PLAYERS' == msg[1]:
                    for player in self.players:
                        self.server.sendMsg(msg[0], "PLAYER " + player.name + " " + player.address[0] + " " + str(player.UDPPort))

                if 'START GAME' in msg[1]:
                    startMsg = msg[1].split(' ')
                    dealerName = startMsg[2]
                    numberAddtlPlayers = int(startMsg[3])

                    if self.findPlayer(dealerName) != -1 and numberAddtlPlayers <= 3 and numberAddtlPlayers >= 1:
                        newGame = manageGame(self.findPlayer(dealerName), numAddtlPlayers, self.server)
                        if newGame.addPlayers(self.players) == -1:
                            self.server.sendMsg(msg[0], 'FAILURE')
                        else:
                            newGame.notify()
                            self.games.append(newGame)
                    else:
                        self.server.sendMsg(msg[0], 'FAILURE')


            sleep(Connection.SLEEP_TIME)

class Player(threading.Thread):
    class fellowPlayer:
        def __init__(self, name, ip, port):
            self.NAME = name
            self.address = (ip, port)
            print("New Fellow Player:\t", self.NAME, " ", self.address[0], " ", self.address[1])
            self.saidHello = False

    def __init__(self, IP, NAME):
        threading.Thread.__init__(self)
        self.server = Connection.Client(IP, int(PORT_LOWER_BOUND))
        self.UDPSocket = None
        self.NAME = NAME
        self.myIP = ''
        self.myPort = 0
        self.fellowPlayers = []
        self.runFlag = True
        self.registered = False
        self.localSleepTime = 2
        self.helloFromAll = True
        self.start()

    def __del__(self):
        self.runFlag = False
        threading.Thread.__del__(self)

    def initUDP(self):
        self.UDPSocket = Connection.Peer(self.myIP, self.myPort)

    def parsePlayer(self, msg):
        input = msg.split(" ")
        name = ''
        ip = ''
        port = 0

        count = 0
        for part in input:
            if part == 'PLAYER':
                count += 1
                continue
            if count == 1:
                count += 1
                name = part
                continue
            if count == 2:
                ip = part
                count += 1
                continue
            if count == 3:
                port = int(part)
                continue

        if name == self.NAME:
            self.myIP = ip
            self.myPort = port
            print("My UDP Port is ", self.myPort)
            self.initUDP()
        else:
            player = self.fellowPlayer(name, ip, port)
            self.fellowPlayers.append(player)
        
    def run(self):
        while self.runFlag:
            msgs = self.server.getMsgs()

            for msg in msgs:
                if msg == 'hello!':
                    self.server.sendMsg("REGISTER " + self.NAME)
                    sleep(self.localSleepTime)
                    newMsgs = self.server.getMsgs()
                    if len(newMsgs) > 0 and newMsgs[0] == 'SUCCESS':
                        self.registered = True
                    else:
                        print("Register Error")
                        self.runFlag = False

                if 'PLAYER' in msg:
                    self.parsePlayer(msg)

            if self.registered:
                self.server.sendMsg("QUERY PLAYERS")
                self.registered = False

            if not self.UDPSocket is None:
                for player in self.fellowPlayers:
                    if player.saidHello == False: 
                        self.helloFromAll = False

                if not self.helloFromAll:
                    for player in self.fellowPlayers:
                        if not player.saidHello:
                            self.UDPSocket.putMsg("Hello from " + self.NAME, player.address)
                    recvMsgs = self.UDPSocket.getMsgs()
                    if len(recvMsgs) > 0:
                        for msg in recvMsgs:
                            name = ""
                            for player in self.fellowPlayers:
                                if msg[1] == player.address:
                                    name = player.NAME
                                    player.saidHello = True
                            print(msg[0], "\t", name)
                    self.helloFromAll = True
                    

            sleep(Connection.SLEEP_TIME)

        print(self.name, "\tdied")




                    
