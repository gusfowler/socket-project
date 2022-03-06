#from ManagePeer2Peer import Player as playerConnection

class manageGame:
    def __init__(self, dealer, numAddtlPlayers, server):
        self.players = []
        self.dealer = dealer
        self.players.append(self.dealer)
        self.numPlayers = numAddtlPlayers + 1
        self.server = server

    def addPlayers(self, arrPlayers):
        for player in arrPlayers:
            if len(self.players) < self.numPlayers:
                if not player in self.players and player.inGame == False:
                    self.players.append(player)
                    player.inGame = True
            else:
                break
        if len(self.players) == self.numPlayers:
            return 0
        else:
            return -1

    def notify(self):
        for player in self.players:
            players_string = ""
            for fellowPlayer in self.players:
                if not player is fellowPlayer:
                    players_string += player.name + " "
            players_string = players_string.strip()
            self.server.sendMsg(player.address, "GAME " + players_string)
            if player is self.dealer:
                self.server.sendMsg(player.address, "DEALER")
            
