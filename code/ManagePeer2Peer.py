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
    class Player:
        def __init__(self, address, name):
            self.address = address
            self.name = name
            self.Peers = []

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
                for peer in self.players:
                    if player.name != peer.name and (player, peer) not in self.pairs_evaled and (peer, player) not in self.pairs_evaled:
                        port = generatePort()
                        
                        PORTS_USED.append(port)
                        player.Peers.append((peer.address[0], port))
                        peer.Peers.append((player.address[0], port))
                        self.pairs_evaled.append((player, peer))

    def __init__(self, IP):
        threading.Thread.__init__(self)
        if IP is None:
            IP = Connection.getIP()
        self.server = Connection.Server(IP, PORT_LOWER_BOUND)
        self.pairs_evaled = []
        self.players = []
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
                    player = self.findPlayerByAddress(msg[0])
                    if player != -1: 
                        for peer in player.Peers:
                            self.server.sendMsg(msg[0], "PLAYER " + str(self.findPlayerByIP(peer[0]).name) + " " \
                            + peer[0] + " " + str(peer[1]))
                    else:
                        self.server.sendMsg(msg[0], 'FAILURE')

            sleep(Connection.SLEEP_TIME)

class Player(threading.Thread):
    def __init__(self, IP, NAME):
        threading.Thread.__init__(self)
        self.server = Connection.Client(IP, int(PORT_LOWER_BOUND))
        self.NAME = NAME
        self.Peers = []
        self.runFlag = True
        self.registered = False
        self.localSleepTime = 2

        self.start()

    def __del__(self):
        self.runFlag = False
        threading.Thread.__del__(self)

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
                    print(msg)

            if self.registered:
                self.server.sendMsg("QUERY PLAYERS")
                self.registered = False

        print(self.name, "\tdied")




                    
