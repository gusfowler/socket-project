import sys

import Connection
from ManagePeer2Peer import Manager
from time import sleep

IP = Connection.getIP()
#PORT = 5000

#if len(sys.argv > 0):
#    for arg in sys.argv:
#        if arg == '-a':
#            IP = sys.argv[sys.argv.where('-a') + 1]
#        elif arg == '-p':
#            PORT = sys.argv[sys.argv.where('-p') + 1]

print("My IP is:\t", IP)
server = Manager(IP)

count = 0
while True:
    print("Number of players:\t", len(server.players))
    sleep(5)