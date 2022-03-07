from ManagePeer2Peer import playerConnection
from time import sleep
import random

SUITS = ['Diamonds', 'Clubs', 'Hearts', 'Spades']
RANKS = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

DECK = []
for suit in SUITS:
    for rank in RANKS:
        DECK.append((suit, rank))

class Player:
    class Game:
        def __init__(self):
            self.dealerName = ""
            self.players = []
            print("New Game!")

    class Dealer:
        def __init__(self):
            self.deck = DECK
            random.shuffle(self.deck)
            print(self.deck)
            self.playersDelt = []

        def getHand(self, player):
            hand = []
            for x in range(0, 6):
                hand.append(self.deck.pop(0))
            self.playersDelt.append(player)

    def __init__(self, serverIP, myName):
        self.connection = playerConnection(serverIP, myName)
        self.name = myName
        self.game = None
        self.cards = []
        self.dealer = None

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

    def sendMsg(self, msg, player):
        fellowPlayer = self.connection.getFellowPlayer(player)
        if fellowPlayer != -1:
            address = fellowPlayer.address
            self.connection.UDPSocket.putMsg("GAME " + msg, address)
        else:
            print("Failed to send to ", player)
            return -1
    
    def getMsgs(self):
        output = self.connection.getGameMsgs()
        newOut = []
        for msg in output:
            split = msg[0].split(' ')
            split.remove('GAME')
            text = ""
            for part in split:
                text += part + " "
            text = text.strip()
            newOut.append((text, msg[1]))
        return newOut

    def hand(self):
        if not self.game is None:
            if self.name == self.game.dealerName:
                print("I am the Dealer!")
                self.dealer = self.Dealer()
                while True:
                    incoming = self.getMsgs()
                    for msg in incoming:
                        player = self.connection.getFellowPlayerByAddress(msg[1])
                        if msg[0] == 'HAND':
                            hand = self.dealer.getHand(player.NAME)
                            for card in hand:
                                self.sendMsg("CARD " + card[0] + " " + card[1], player.name)

            else:
                self.sendMsg('HAND', self.game.dealerName)
                sleep(1) 
                print(self.getMsgs())

    def queryGames(self):
        self.connection.server.sendMsg('QUERY GAME')
        gameMsgs = self.getMsgs()
        for gameMsg in gameMsgs:
            if gameMsg[1] == 'server' and self.name in gameMsg[0]:
                game = self.Game()
                msg = gameMsg[0]
                msg = msg.split(" ")
                if msg[0] == 'DEALER':
                    msg.remove('DEALER')
                    game.dealerName = msg[0]
                    msg.remove(game.dealerName)
                if msg[0] == 'PEER':
                    msg.remove('PEER')
                    while len(msg) > 0:
                        game.players.append(msg.pop(0))
                self.game = game

                    
