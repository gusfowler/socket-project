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

serverIP = ""
serverPort = 0

class Server:
    flag = True

    def __init__(self, ip, port, user):
        print("connecting to server ", ip, " on port ", port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverAddress = (ip, port)

        self.sock.connect(self.serverAddress)
        self.sock.sendall(user.encode())

        while self.flag:
            print(self.sock.recv(1024))

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

    def display_commands(self):
        print("Help Page goes here")

while True:
    command = input('enter command: ')
    cmd = command.split(" ")
    if cmd[0] == 'register':
        serverIP = cmd[2]
        serverPort = int(cmd[3])
        server = Server(serverIP, serverPort, cmd[1])