import socket
import threading
from time import sleep

DELIMITER = "\t"
ENCODING = 'utf-8'
SLEEP_TIME = 1

def getIP():
    return socket.gethostbyname(socket.gethostname())

'''
    These are universal send and recvieve functions that should work for both TCP and UDP sockets.
    Now we just need to handle the creation of the UDP socket and the multithreading for that class.
    Within the Peer class, the socket variable needs to be named connection, and the send buffer sendBuffer,
    and the recieve buffer needs to be named recvBuffer.
'''
def sendMsg(msgs, selfSock):
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
        selfSock.sendBuffer.remove(msg)

    msgs = nextSend
    selfSock.connection.sendall(output)
            
    selfSock.recv = True

def recvMsg(selfSock):
    output = []
    data = selfSock.connection.recv(1024)
    string = str(data, ENCODING)

    for s in string.split(DELIMITER):
        if s != '': output.append(s)

    if data: selfSock.recv = False

    return output


##TCP Server
class Server(threading.Thread):
    class Client(threading.Thread):
        def __init__(self, connection, address):
            threading.Thread.__init__(self)
            self.connection = connection
            self.address = address
            print("New Client:\t", address)

            self.recvBuffer = []
            self.sendBuffer = [ "hello!"]
            self.recv = False
            self.listenFlag = True
            self.start()

        def __del__(self):
            self.listenFlag = False
            self.connection.close()

        def run(self):
            counter = 0
            while self.listenFlag:
                if len(self.sendBuffer) > 0:
                    print("Server sendBuffer:\t", self.sendBuffer)
                    sendMsg(self.sendBuffer, self)

                if self.recv: 
                    for msg in recvMsg(self): self.recvBuffer.append(msg)
                counter += 1
                sleep(SLEEP_TIME)

        def getAddress(self):
            return self.address


    def __init__(self, ipAddr, port):
        threading.Thread.__init__(self)

        self.arrClients = []

        self.address = (ipAddr, int(port))
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

    def sendMsg(self, address, msg):
        self.getClient(address).sendBuffer.append(msg)

    def sendMsg(self, client, msg):
        client.sendBuffer.append(msg)

    def getClient(self, address):
        for client in self.arrClients:
            if client.address == address:
                return client

    def sendToAll(self, msg):
        for client in self.arrClients:
            client.sendBuffer.append(msg)

    def getNumClients(self):
        return len(self.arrClients)

    def drop(self, address):
        self.arrClients.remove(self.getClient(address))


##TCP Client
class Client(threading.Thread):

    def __init__(self, ipAddr, port):
        threading.Thread.__init__(self)

        self.sendBuffer = []
        self.recvBuffer = []
        
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.address = (ipAddr, port)
        self.keepAlive = True
        self.recv = True

        self.start()

    def run(self):
        self.connection.connect(self.address)

        while self.keepAlive:
            if len(self.sendBuffer) > 0:
                sendMsg(self.sendBuffer, self)
            if self.recv: 
                for s in recvMsg(self):
                    if s != '':
                        self.recvBuffer.append(s)

    def getMsgs(self):
        output = []
        msgs = self.recvBuffer
        for msg in msgs:
            output.append(msg)
            self.recvBuffer.remove(msg)
        return output

    def sendMsg(self, msg):
        self.sendBuffer.append(msg)


# #UDP Peer
# class Peer(threading.Thread):

#    def __init__(self, ipAddr, port):
#        threading.Thread.__init__(self)

#        self.address = (ipAddr, port)
#        self.start()

#    def run(self):
#         #do stuff

