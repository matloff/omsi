__author__ = 'fdemoullin'

# server script
# should be run without interruption on professor's machine

import sys
import select
import socket
import thread

# import modules that contain functions called by a client
import ServerGlobals
import ServerRoutines

# set up the connection, start listening, start the threads and send feedback to client
def main():

    # run startup routine for the professor
    #    professor specifies the directory that will store student submissions
    #    program confirms that the directory contains the exam questions file
    ServerRoutines.startUpExamDirectory()

    # create socket
    lServerSocket = ServerRoutines.createSocket()

    while True:
        # server is now ready to accept connections
        print "Number of Current Connections: %s" %ServerGlobals.gNumCurrentClients
        print "Number of Total Connections: %s" %ServerGlobals.gNumTotalClients

        # block until connection arrives
        lClientsocket, lAddr = lServerSocket.accept()
        print "Connection detected at:", lAddr

        # increase total number of connections
        ServerGlobals.gNumTotalClientsLock.acquire()
        ServerGlobals.gNumCurrentClients += 1
        ServerGlobals.gNumTotalClientsLock.release()

        # start new thread (function, args_tuple) for each new connection
        # lAddr is not used right now. However python syntax requires a tuple as input parameters to a new thread
        thread.start_new_thread(ServerRoutines.clientHandler, (lClientsocket, lAddr))

# this scrip is the "Main" scrip on the back-end. It is supposed to be run by itself
if __name__ == '__main__':
    main()
