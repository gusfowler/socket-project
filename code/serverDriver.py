import sys

import Connection

IP = Connection.getIP()
PORT = 5000

#if len(sys.argv > 0):
#    for arg in sys.argv:
#        if arg == '-a':
#            IP = sys.argv[sys.argv.where('-a') + 1]
#        elif arg == '-p':
#            PORT = sys.argv[sys.argv.where('-p') + 1]

print("My IP is:\t", IP)
server = Connection.Server(IP, PORT)

while True:
    server.sendToAll('hello world!')