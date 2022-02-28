from curses.ascii import DEL
import socket
import sys
import threading
import time

DELIMITER = "\t"

def getIP():
    return socket.gethostbyname(socket.gethostname())

##TCP Server
class Server(threading.Thread):
    class Client(threading.Thread):
        def __init__(self, connection, address):
            threading.Thread.__init__(self)
            self.connection = connection
            self.address = address
            print("New Client:\t", address)

            self.recvBuffer = []
            self.sendBuffer = []

            self.listenFlag = True
            self.start()

        def run(self):
            while self.listenFlag:
                print(None)
                if len(self.sendBuffer) > 0:
                    self.sendMsg(self.sendBuffer)

                self.recvBuffer.append(str for msg in self.recvMsg())

        def sendMsg(self, msgs):
            for msg in msgs:
                self.connection.sendall(msg + DELIMITER)

        def recvMsg(self):
            data = self.connection.recv(1024)
            string = repr(data)

            return [str for s in string.split(DELIMITER)]


    def __init__(self, ipAddr, port):
        threading.Thread.__init__(self)

        self.arrClients = []

        self.address = (ipAddr, port)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listenFlag = True
        self.start()

    def run(self):
        try:
            self.server.bind(self.address)
        except Exception:
            print("Server:\t", Exception)
        
        while self.listenFlag:
            self.server.listen()
            connection, address = self.server.accept()

            self.arrClients.append(self.Client(connection, address))

    def getMsgs(self):
        output = []
        for client in self.arrClients:
            msgs = client.recvBuffer

            output.append(client.address + ": " + str for s in msgs)
        return output

    def sendMsg(self, client, msg):
        client.sendBuffer.append(msg)

    def getClient(self, address):
        for client in self.arrClients:
            if client.address == address:
                return client

    def sendToAll(self, msg):
        for client in self.arrClients:
            client.sendBuffer.append(msg)

##TCP Client
class Client(threading.Thread):

    def __init__(self, ipAddr, port):
        threading.Thread.__init__(self)

        self.sendBuffer = []
        self.recvBuffer = []
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = (ipAddr, port)
        self.keepAlive = True

        self.start()

    def run(self):
        self.sock.connect(self.address)

        while self.keepAlive:
            if len(self.sendBuffer) > 0:
                self.sendMsgs()
            self.recvBuffer.append(str for s in self.recvMsgs())

    def sendMsgs(self):
        for msg in self.sendBuffer:
            self.sock.sendall(msg + DELIMITER)

    def recvMsgs(self):
        data = self.sock.recv(1024)
        string = repr(data)

        return [str for s in string.split(DELIMITER)]

##UDP Peer
#class Peer(threading.Thread):

#    def __init__(self, ipAddr, port):
#        threading.Thread.__init__(self)
#
#        self.address = (ipAddr, port)
#        self.start()

#    def run(self):
        ##do stuff

