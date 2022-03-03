import sys
import socket
from time import sleep

import Connection

IP = Connection.getIP()
PORT = 5000

#if len(sys.argv > 0):
#    for arg in sys.argv:
#        if arg == '-a':
#            IP = sys.argv[sys.argv.where('-a') + 1]
#        elif arg == '-p':
#            PORT = sys.argv[sys.argv.where('-p') + 1]

sleep(3)
print("My IP is:\t", IP)
IP = socket.gethostbyname("socket-project_server_1")
#IP = '172.19.0.3'
print("Server IP is:\t", IP)
server = Connection.Client(IP, PORT)

count = 0 
while True:
    if len(server.recvBuffer) > 0: 
        current = []
        for msg in server.recvBuffer:
            current.append(msg)
        print("Driver:\t", server.recvBuffer)
        for msg in current:
            server.recvBuffer.remove(msg)
            count += 1
        server.sendBuffer.append("Recvieved! " + str(count))
    sleep(Connection.SLEEP_TIME)
