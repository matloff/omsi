__author__ = 'fdemoullin'

# server script
# should be run without interruption on professor's machine

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

    # print information about ip and port
    print "Host address: %s" % ServerGlobals.gHost
    print "Port number: %s" % ServerGlobals.gPort


    while True:
        # server is now ready to accept connections
        print "Number of Total Connections: %s" % ServerGlobals.gNumTotalClients

        # block until connection arrives
        lClientsocket, lAddr = lServerSocket.accept()
        print "Connection detected at:", lAddr

        # increase number of total connections
        ServerGlobals.gNumTotalClientsLock.acquire()
        ServerGlobals.gNumTotalClients += 1
        ServerGlobals.gNumTotalClientsLock.release()

        # start new thread (function, args_tuple) for each new connection
        # lAddr is not used right now. However python syntax requires a tuple as input parameters to a new thread
        thread.start_new_thread(ServerRoutines.clientHandler, (lClientsocket, lAddr))

# this script is the "Main" script on the back-end. It is supposed to be run by itself
if __name__ == '__main__':
    main()
