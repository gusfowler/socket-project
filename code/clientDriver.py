import sys
import socket
from time import sleep

import Connection

from ManagePeer2Peer import Player

IP = Connection.getIP()
print (sys.argv)
CLIENT_NAME = str(sys.argv[1])

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
player = Player(IP, CLIENT_NAME)


# while True:
#     if len(server.recvBuffer) > 0: 
#         print("Driver:\t", server.getMsgs())
#         server.sendMsg("REGISTER " + CLIENT_NAME)
#     sleep(Connection.SLEEP_TIME)
