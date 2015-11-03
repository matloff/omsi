__author__ = 'fdemoullin'

# this is the main script on the professor's machine, this needs to run without interruption
# TODO: make this support ftp file transfers

import socket
import thread
import sys

# import any modules that contain functions called directly from the clients
import ExampleScriptServerSide

# function dictionary, stores all the functions that this server class uses
gFunctionDictionary = {
    # associate the function name with the function first class object
    # TODO: make this accept parameters
    'printA': ExampleScriptServerSide.printA,
    'printB': ExampleScriptServerSide.printB
}

# associate the socket with a port
gHOST = "" # can leave this blank on the server side
gPORT = 20500 #int(sys.argv[1])

# keep track of how many clients there are
lNumberOfClients = 0
# set up a lock to guard nclnt
lNumberOfClientsLock = thread.allocate_lock()

# set up the connection, start listening, start the threads and send feedback to client
def main():
    # keep track of total traffic
    lTotalNumberOfConnections = 0

    # create a socket
    try:
        lServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        lServerSocket.bind((gHOST, gPORT))

        # accept "call" from client
        lServerSocket.listen(5) # maximum number of 5 queued connections, should be irrelevant as all connections fork into a new thread

    except socket.error, (value,message):
        if lServerSocket:
            lServerSocket.close()
        print "Could not open socket on Server: " + message
        sys.exit(1)

    # main loop
    while 1:
        print "waiting for connection, so far: %s connections" %lTotalNumberOfConnections
        lClientsocket, lAddr = lServerSocket.accept()
        print 'connection detected at:', lAddr
        thread.start_new_thread(handler, (lClientsocket, lAddr))
        lTotalNumberOfConnections += 1


def handler(pClientsocket, addr):
    global lNumberOfClients, lNumberOfClientsLock

    lNumberOfClientsLock.acquire()
    lNumberOfClients += 1
    lNumberOfClientsLock.release()

    while 1:
        data = pClientsocket.recv(1024)
        break
    lIsExecuted = interpreteClientString(data)

    if lIsExecuted:
       print "Function was properly executed"
       pClientsocket.send("s")
    else:
       pClientsocket.send("f")

    pClientsocket.close()

    lNumberOfClientsLock.acquire()
    lNumberOfClients -= 1
    lNumberOfClientsLock.release()

    return



# transform input string into function object and make the call to the corresponding function in the back-end
def interpreteClientString(pClientString):

    if pClientString in gFunctionDictionary:
        # look up function in dictionary and make the call
        gFunctionDictionary[pClientString]()
        return True
    else:
        raise RuntimeError("The function you are trying to call is not defined on the Server")
        return False

# this scrip is the "Main" scrip on the back-end. It is supposed to be run by itself
if __name__ == '__main__':
    main()
