import socket
import sys

# module that provides an interface for all server related requests
# sets up connection with the running server on localhost and port 12345
# all methods are static and should be called statically

# global variable to keep track of the socket
gPORT = 20500 # hardcoding the port number TODO: make based on user input
gHOST = socket.gethostname()

# setter
# pHost = IP address provided by prof
# pPort = Port provided by prof
def setUpServer(pHost, pPort):
    global gPORT, gHOST

    # deactivated during testing phase! The connection is set up on localhost

    # gPORT = pPort
    # gHOST = pHost

# executes a function on the server
# input function name to be executed
# return value True or False depending on success on server
def callFunctionOnServer(functionName):
    # connection on localhost for now
    global gPORT, gHOST
    try:
        # create local Internet TCP socket (domain, type)
        lSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # initiate server connection to global
        lSocket.connect( (gHOST, gPORT) )
        lSocket.send(functionName)
    
    #connection problem
    except socket.error, (value,message):
        if lSocket:
            # close socket
            lSocket.close()
        raise RuntimeError("Could not open socket on Client: " + message)
        return False

    return getResponseFromServer(lSocket)

# close the connection
def getResponseFromServer(pSocket):
    # this will block the client until response was received
    lServerResponse = pSocket.recv(sys.getsizeof("f"))
    pSocket.close()
    if lServerResponse == "s":
        return True
    else:
        return False

