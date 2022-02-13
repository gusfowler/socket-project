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

from asyncio.windows_events import NULL
import pickle
import socket
import threading
import time

class Player (threading.Thread):

    playerName = ''
    playerIP = ''
    connection = NULL
    ID = 0

    def __init__(self, name, ip, conn, threadID):
        threading.Thread.__init__(self)
        self.playerName = name
        self.playerIP = ip
        self.connection = conn
        self.ID = threadID

        print("New Player ", name, " at ip ", ip, " on thread # ", self.ID)
        self.sendMsg(b'ACK')

    def sendMsg(self, data):
        self.connection.sendall(data)

    def recvMsg(self):
        return self.connection.recv(1024)

class Manager:
    flag = True

    arrPlayers = []
    activeGames = {}

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

            newPlayer = Player(str(repr(connection.recv(1024))), address, connection, threading.currentThread() + 1)
            self.listOfPlayers.append(newPlayer)
            

    ## MILESTONE REQUIREMENTS
    def register(self, address, port):
        if len(user) >= 16 or port > 23499:
            return 'FAILURE'
        elif name not in listOfUsers:
            self.listOfUsers[user] = user
            print(f'User Registered: {user}')
            return 'SUCCESS'

    #def query_players():

    #def query_games():

    #def de_register():


Manager(65432)