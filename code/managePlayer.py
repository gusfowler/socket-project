from ManagePeer2Peer import playerConnection
from time import sleep

class Player:
    def __init__(self, serverIP, myName):
        self.connection = playerConnection(serverIP, myName)
        self.name = myName

    def gameReady(self):
        return self.connection.helloFromAll

    def startGame(self, dealerName, numAddtlPlayers):
        self.connection.server.sendMsg('START GAME ' + dealerName + ' ' + str(numAddtlPlayers))
        while True:
            response = self.connection.server.getMsgs()
            if len(response) > 0 and response[0] == 'SUCCESS':
                print("Game Started")
                break
            elif len(response) > 0 and response[0] == 'FAILURE':
                print("Failed to start game")
                break
            else:
                sleep(1)
                continue

    def queryGames(self):
        self.connection.server.sendMsg('QUERY GAME')
        print(self.connection.getGameMsgs())