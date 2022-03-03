import socket
import threading
from time import sleep

DELIMITER = "\t"
ENCODING = 'utf-8'

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
            self.recv = False
            self.listenFlag = True
            self.start()

        def run(self):
            counter = 0
            while self.listenFlag:
                if len(self.sendBuffer) > 0:
                    print("Server sendBuffer:\t", self.sendBuffer)
                    self.sendMsg(self.sendBuffer)

                if self.recv: 
                    for msg in self.recvMsg(): self.recvBuffer.append(msg)
                counter += 1
                sleep(3)

        def sendMsg(self, msgs):
            output = b''
            sent = []
            nextSend = []

            for msg in msgs:

                if len(output + bytes(msg + DELIMITER, ENCODING)) <= 1024:
                    output += bytes(msg + DELIMITER, ENCODING)
                    
                else:
                    nextSend.append(msg)
                    
                sent.append(msg)

            #do this to not introduce skipping in above for loop- messages finally sent in order
            for msg in sent:
                self.sendBuffer.remove(msg)

            msgs = nextSend
            self.connection.sendall(output)
            
            self.recv = True

        def recvMsg(self):
            output = []
            data = self.connection.recv(1024)
            string = str(data, ENCODING)

            for s in string.split(DELIMITER):
                if s != '': output.append(s)

            return output


    def __init__(self, ipAddr, port):
        threading.Thread.__init__(self)

        self.arrClients = []

        self.address = (ipAddr, port)
        print("Server starting on ", self.address)
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
            for msg in msgs:
                output.append((client.address, msg))
                client.recvBuffer.remove(msg)
        return output

    def sendMsg(self, client, msg):
        client.sendBuffer.append(msg)

    def getClient(self, address):
        for client in self.arrClients:
            if client.address == address:
                return client

    def sendToAll(self, msg):
        print("hit here")
        for client in self.arrClients:
            client.sendBuffer.append(msg)

    def getNumClients(self):
        return len(self.arrClients)

##TCP Client
class Client(threading.Thread):

    def __init__(self, ipAddr, port):
        threading.Thread.__init__(self)

        self.sendBuffer = []
        self.recvBuffer = []
        
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = (ipAddr, port)
        self.keepAlive = True
        self.recv = True

        self.start()

    def run(self):
        self.sock.connect(self.address)

        while self.keepAlive:
            if len(self.sendBuffer) > 0:
                self.sendMsgs(self.sendBuffer)
            if self.recv: 
                for s in self.recvMsgs():
                    if s != '':
                        self.recvBuffer.append(s)

    def sendMsgs(self, msgs):
        output = b''
        nextSend = []

        for msg in msgs:
            if len(output + bytes(msg + DELIMITER, ENCODING)) <= 1024:
                output += bytes(msg + DELIMITER, ENCODING)
            else:
                nextSend.append(msg)
            self.sendBuffer.remove(msg)

        msgs = nextSend
        self.sock.sendall(output)
        self.recv = True


    def recvMsgs(self):
        data = self.sock.recv(1024)
        string = str(data, ENCODING)

        if data: self.recv = False

        return string.split(DELIMITER)

##UDP Peer
#class Peer(threading.Thread):

#    def __init__(self, ipAddr, port):
#        threading.Thread.__init__(self)
#
#        self.address = (ipAddr, port)
#        self.start()

#    def run(self):
        ##do stuff

