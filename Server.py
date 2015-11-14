__author__ = 'fdemoullin'

# this is the main script on the professor's machine, this needs to run without interruption

import sys
import select

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
    'printA': ExampleScriptServerSide.printA,
    'printB': ExampleScriptServerSide.printB,
    'printMyOwnWords': ExampleScriptServerSide.printMyOwnWords
}

# associate the socket with a port
gHOST = "" # can leave this blank on the server side
gPORT = 20500 #int(sys.argv[1])

# keep track of how many clients are connected right now
# this needs to be an atomic variable
lNumberOfClients = 0
# set up a lock to guard lNumberOfClients
lNumberOfClientsLock = thread.allocate_lock()

# set up the connection, start listening, start the threads and send feedback to client
def main():
    # keep track of total traffic
    lTotalNumberOfConnections = 0

    # create a socket
    lServerSocket = createSocket()

    # main loop
    while True:
        # server is now ready to accept connections
        print "waiting for connection, so far: %s connections" %lTotalNumberOfConnections

        # block until connection arrives
        lClientsocket, lAddr = lServerSocket.accept()
        print 'connection detected at:', lAddr

        # starts new thread (function, args_tuple) for new client
        thread.start_new_thread(handler, (lClientsocket, lAddr)) # lAddr is not used right now. However python syntax requires a tuple as input parameters to a new thread

        # increase total number of connections
        lTotalNumberOfConnections += 1

def createSocket():
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

    return lServerSocket

def handler(pClientSocket, addr):
    global lNumberOfClients, lNumberOfClientsLock

    # acquire a lock, blocking = True, timeout = -1
    lNumberOfClientsLock.acquire()
    lNumberOfClients += 1
    # unlock
    lNumberOfClientsLock.release()

    #print 'number of clinents currently connected: %s' %lTotalNumberOfConnections

    # accept initial request
    data = pClientSocket.recv(1024)

    if data == "File":
        # client is sending a file
        lIsExecuted = receiveFile(pClientSocket)
    else:
        # client is executing a function
        lIsExecuted = interpreteClientString(data)

    if lIsExecuted == "s":
       print "Action was properly executed"

       # transmits TCP message: success
       pClientSocket.send("s")

    else:
       # transmits TCP message: fail
       pClientSocket.send("f")

    pClientSocket.close()

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

def receiveFile(pClientSocket):

    lNewFile = openNewFileServerSide()

    # something went wrong when creating the file, let the client know
    if (lNewFile == False):
        pClientSocket.send("abort")

    lSuccess = "f"
    try:
        # let the client know the server is ready
        pClientSocket.send("ready")

        # receive the file
        while 1:
            # set a timeout for this
            ready = select.select([pClientSocket], [], [], 2)
            if ready[0]:
                lChunkOfFile = pClientSocket.recv(1024)
                lNewFile.write(lChunkOfFile)
            else:
                break

        print("Finished accepting file")
        lSuccess = "s"
    finally:
        if lSuccess == "f":
            # something went wrong
            print "File transfer was not successful"
        # close file, regardless of success
        lNewFile.close()

        # return success information
        return lSuccess

def openNewFileServerSide(pNameOfNewFile):
     # create new or trunctate old file - hence the w flag
    try:
        lNewFile = open(pNameOfNewFile, 'w')
        return lNewFile
    except IOError:
        print "File could not be created on the Server"
        return False

# this scrip is the "Main" scrip on the back-end. It is supposed to be run by itself
if __name__ == '__main__':
    main()
