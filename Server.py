#!/usr/bin/env python3

'''
SAMPLE UP SERVER CODE FROM COMPUTER NETWORKING BOOK
from socket import *
serverPort = 12000 #change to group number
serverSocket = socket(AF_NET, SOCK_DGRAM)
serverSocket. bind(("', serverPort))
print ("The server is ready to receive")
flag = true
while flag:
    message, clientAddress = serverSocket. recvfrom(2048)
    modifiedMessage = message. decode().upper()
    serverSocket,sendto(modifiedMessage,encode(),clientAddress)
'''

import pickle
import socket
import threading
import time

class Player (threading.Thread):
    flag = True
    recieveFlag = False

    playerName = ''
    playerIP = ''
    connection = 0
    myManager = ''
    ID = 0

    def __init__(self, manager, name, ip, conn, threadID):
        threading.Thread.__init__(self)
        self.myManager = manager
        self.playerName = name
        self.playerIP = ip
        self.connection = conn
        self.ID = threadID
        self.start()

    def run(self):
        print("New Player ", self.playerName, " at ip ", self.playerIP, " on thread # ", self.ID)
        self.sendMsg(b'SUCCESS')

        while self.flag:
            data = b''
            if self.recieveFlag:
                data = self.recvMsg()
                if len(data) > 0:
                    if data == b'QUERY PLAYERS':
                        self.sendPlayers()
                else:
                    print("no data")
                    break
    
    def sendPlayers(self):
        ###
        numPlayers = self.myManager.getNumPlayers()
        print(str(numPlayers).encode('utf-8'), numPlayers)
        self.sendMsg(str(numPlayers).encode('utf-8'))
        if not (self.recvMsg() == b'ACK'):
            print("did not acknowledge number of players for client loop")
        else:
            for x in range(0, numPlayers):
                player = self.myManager.getPlayerAt(x)
                if player != -1:
                    while True:
                        self.sendMsg(player.playerName.encode('utf-8'))
                        if not b'ACK' == self.recvMsg(): continue
                        else: break
                    while True:
                        self.sendMsg(player.playerIP[0].encode('utf-8'))
                        if not b'ACK' == self.recvMsg(): continue
                        else: break
                    while True:
                        self.sendMsg(str(player.playerIP[1]).encode('utf-8'))
                        if not b'ACK' == self.recvMsg(): continue
                        else: break
                print("waiting on ack")
                if self.recvMsg() == b'ACK': continue
                else:
                    print("did not acknowledge reciept of player")
                    break


    def sendMsg(self, data):
        self.connection.sendall(data)
        self.recieveFlag = True

    def recvMsg(self):
        return self.connection.recv(1024)

    def getName(self):
        return self.playerName

class Manager:
    flag = True

    arrPlayers = []
    activeGames = []

    serverHost = '10.0.0.170'
    serverPort = 0

    def __init__(self, port):
        self.serverPort = port
        print("Starting server on", self.serverHost, "port", self.serverPort)
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.server.bind((self.serverHost, self.serverPort))
        except:
            print(self.server.getsockname()[0])
            self.server.bind((self.server.getsockname()[0], self.serverPort))
        while self.flag:
            self.server.listen()
            connection, address = self.server.accept()

            #attempt to register all connections
            self.register(address, connection)

    ## MILESTONE REQUIREMENTS
    def register(self, address, connection):
        #check if user with same name exists
        nameExists = False
        name = str(repr(connection.recv(1024)))
        for player in self.arrPlayers:
            if name == player.getName():
                nameExists = True

        #create and register new player if name is not present
        if not nameExists: 
            newPlayer = Player(self, name, address, connection, threading.activeCount() + 1)
            self.arrPlayers.append(newPlayer)
        #if it does already exist drop with failure code
        else:
            connection.sendall(b'FAILURE')
            connection.close()

    def getNumPlayers(self):
        return len(self.arrPlayers)

    def getPlayerAt(self, num):
        return self.arrPlayers[num]

    def getPlayerByName(self, name):
        found = False
        for player in self.arrPlayers:
            if player.playerName == name:
                found = True
                return player
        if not found:
            print("Searched arrPlayers for nonexisitant player")
            return -1
    #def query_players():

    #def query_games():

    #def de_register():


Manager(65432)