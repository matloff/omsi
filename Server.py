__author__ = 'fdemoullin'

# this is the main script on the professor's machine, this needs to run without interruption
# TODO: make this support ftp file transfers

import sys

try:
    import socket
except ImportError:
    print 'Cannot import socket. Exiting...'
    sys.exit()

try:
    import thread
except ImportError:
    print 'Cannot import thread. Exiting...'
    sys.exit()

# import modules that contain functions called by a client
import ExampleScriptServerSide

# function dictionary
# stores function names and corresponding functions that this server class uses
gFunctionDictionary = {
    # associate the function name with the function first class object
    # TODO: make this accept parameters
    'printA': ExampleScriptServerSide.printA,
    'printB': ExampleScriptServerSide.printB,
    'printMyOwnWords': ExampleScriptServerSide.printMyOwnWords
}

# associate the socket with a port
gHOST = "" # can leave this blank on the server side
gPORT = 20500 #int(sys.argv[1])

# keep track of how many clients are connected right now
lNumberOfClients = 0

# set up a lock to guard nclnt
lNumberOfClientsLock = thread.allocate_lock()

# set up the connection, start listening, start the threads and send feedback to client
def main():
    # keep track of total traffic
    lTotalNumberOfConnections = 0

    # create a socket
    try:
        # create Internet TCP socket (domain, type)
        lServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # bind address(gHost, gPort) to socket
        lServerSocket.bind((gHOST, gPORT))

        # accept "call" from client
        lServerSocket.listen(5) # maximum number of 5 queued connections, should be irrelevant as all connections fork into a new thread

    except socket.error, (value,message):
        if lServerSocket:
            lServerSocket.close()
        print "Could not open socket on Server: " + message
        sys.exit(1)

    # main loop
    while True:

        print "waiting for connection, so far: %s connections" %lTotalNumberOfConnections

        # block until connection arrives
        lClientsocket, lAddr = lServerSocket.accept()
        print 'connection detected at:', lAddr

        # starts new thread (function, args_tuple) for new client
        thread.start_new_thread(handler, (lClientsocket, lAddr))
        thread.start_new_thread(handler, (lClientsocket,lAddr))
        lTotalNumberOfConnections += 1


def handler(pClientsocket, addr):
    global lNumberOfClients, lNumberOfClientsLock

    # acquire a lock, blocking = True, timeout = -1
    lNumberOfClientsLock.acquire()
    lNumberOfClients += 1
    # unlock
    lNumberOfClientsLock.release()

    #print 'number of clinents currently connected: %s' %lTotalNumberOfConnections

    data = pClientsocket.recv(1024)

    lIsExecuted = interpreteClientString(data)

    if lIsExecuted == "s":
       print "Function was properly executed"

       # transmits TCP message: success
       pClientsocket.send("s")

    else:
        # transmits message: fail
       pClientsocket.send(lIsExecuted)

    pClientsocket.close()

    lNumberOfClientsLock.acquire()
    lNumberOfClients -= 1
    lNumberOfClientsLock.release()

    return

# transform input string into function object and make the call to the corresponding function in the back-end
def interpreteClientString(pClientString):

    lSplitUpFunction = pClientString.split("(")
    lFunctionName = lSplitUpFunction[0]

    if lSplitUpFunction[0] in gFunctionDictionary:
        # look up function in dictionary and make the call
        if len(lSplitUpFunction) == 1:
            gFunctionDictionary[lFunctionName]()
        else:
            lParameters = lSplitUpFunction[1].split(")")[0]
            if lParameters:
                gFunctionDictionary[lFunctionName](lParameters)
        return "s"
    else:
        lErrorMessage = "The function you are trying to call is not defined on the Server"
        raise RuntimeError(lErrorMessage)
        return lErrorMessage

# this scrip is the "Main" scrip on the back-end. It is supposed to be run by itself
if __name__ == '__main__':
    main()
