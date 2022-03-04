import Connection
import threading

NUM_CLIENTS = 0
PORTS_USED = []

class Manager(threading.Thread):
    class Peer:
        def __init__(self, sendPort, recvPort):
            self.sendPort = sendPort
            self.recvPort = recvPort
 
    def __init__(self, IP, PORT):
        if IP is None:
            IP = Connection.getIP()
        self.server = Connection.Server(IP, PORT)
        PORTS_USED.append(PORT)

        self.start()

    def run(self):
        while server:
            if server.getNumClients() > NUM_CLIENTS:
                NUM_CLIENTS = server.getNumClients()