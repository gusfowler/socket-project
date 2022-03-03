import sys

import Connection
from time import sleep

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

count = 0
while True:
    num = server.getNumClients()
    while num > 0:
        count += 1
        server.sendToAll('hello world! ' + str(count))
        msgs = server.getMsgs()
        if len(msgs) > 0:
            print(msgs)
        sleep(Connection.SLEEP_TIME)    #SLEEP is essential - > if I try to flood something in the OS kills the thread