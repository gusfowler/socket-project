#!/usr/bin/env python3

'''
SAMPLE UDP CLIENT CODE FROM COMPUTER NETWORKING BOOK
from socket import *
serverName = 'hostname'
serverPort = 12000; # change to group number
clientSocket = socket(AF_INET, SOCK_ DGRAM)
message = raw_input('Input lowercase sentence: ')
clientSocket.sendto(message.encode(), (serverName, serverPort))
modifiedMessage, serverAddress = clientSocket. recvfrom(2048)
print(modifiedMessage.decode())
clientSocket.close()
'''

from atexit import register
import pickle
import socket
import sys
import threading
import time

serverIP = ""
serverPort = 0
currentServer = ''

def display_commands(self):
        print("Help Page goes here")

class Server (threading.Thread):
    flag = True
    ID = 0
    myUserName = ''

    def __init__(self, ip, port, user, threadID):
        threading.Thread.__init__(self)
        #TCP SOCKET CONNECT
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverAddress = (ip, port)
        self.ID = threadID
        self.myUserName = user
        print(self.myUserName, " connecting to server ", ip, " on port ", port, " and thread ", self.ID)

        self.sock.connect(self.serverAddress)
        self.sendMsg(user.encode())

        while self.flag:
            data = self.recvMsg()
            if len(data) > 0:
                if data == b'SUCCESS':
                    print("Successfully registered with ", serverIP, " on port ", serverPort)
                elif data == b'FAILURE':
                    print("Failed to register with server, probably because I am using the same name of someone already registered. New name?")
                else:
                    print("Unknown what was recieved")
            else:
                break

    def sendMsg(self, msg):
        self.sock.sendall(msg)

    def recvMsg(self):
        return self.sock.recv(1024)

class Player:
    flag = True

    def __init__(self, hostIP, hostPort):
        print("connecting to ", hostIP, " on port ", hostPort)
        self.sock = socket.socket(socket.AF_INET, socket. SOCK_DGRAM)
        self.serverAddress = (hostIP, hostPort)
    
    def listen(self, port):
        sock = socket.socket(socket.AF_INET, socket. SOCK_DGRAM)
        try:
            sock.bind((socket.gethostname(), port))
        except:
            s = socket.socket(socket.AF_INET, socket. SOCK_DGRAM)
            s.connect((self.hostIP, port))
            #sock.bind((s.getsockname() [8], port))
        while self.flag:
            raw_bytes, addr = sock.recvfrom(1024)
            data = pickle.loads(raw_bytes)

while True:
    command = input('enter command: ')
    cmd = command.split(" ")
    if cmd[0] == 'register':
        serverIP = cmd[2]
        serverPort = int(cmd[3])
        currentServer = Server(serverIP, serverPort, cmd[1], threading.activeCount() + 1)
    elif cmd[0] == 'help':
        display_commands()