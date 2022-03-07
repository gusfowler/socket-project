from time import sleep

SLEEP_TIME = 3

class manageGame:
    def __init__(self, dealer, numAddtlPlayers, server):
        self.players = []
        self.dealer = dealer
        self.players.append(self.dealer)
        self.numPlayers = numAddtlPlayers + 1
        self.server = server
        self.sentTo = 0

    def addPlayers(self, arrPlayers):
        for player in arrPlayers:
            if len(self.players) < self.numPlayers:
                if (not (player in self.players)) and player.inGame == False:
                    self.players.append(player)
                    player.inGame = True
            else:
                break
        if len(self.players) == self.numPlayers:
            return 0
        else:
            return -1

    def gameMsg(self):
        output = ""
        output += "DEALER " + self.dealer.name + " PEERS "
        for player in self.players:
            if player != self.dealer:
                output += player.name + " "
        output = output.strip()
        return output
                        
            