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

    print "Exam Directory 2: " + ServerGlobals.gServerExamDirectory

    print "Test:" + ServerGlobals.gExamQuestionsFilePath

    # keep track of total number of connections
    lTotalNumberOfConnections = 0

    # create socket
    lServerSocket = createSocket()

    while True:
        # server is now ready to accept connections
        print "Total Number of Connections, thus far: %s" %lTotalNumberOfConnections

        # block until connection arrives
        lClientsocket, lAddr = lServerSocket.accept()
        print "Connection detected at:", lAddr

        # start new thread (function, args_tuple) for new client
        # lAddr is not used right now. However python syntax requires a tuple as input parameters to a new thread
        thread.start_new_thread(clientHandler, (lClientsocket, lAddr))

        # increase total number of connections
        lTotalNumberOfConnections += 1

def createSocket():
    try:
        # create Internet TCP socket (domain, type)
        lServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # bind address(gHost, gPort) to socket
        lServerSocket.bind((ServerGlobals.gHOST, ServerGlobals.gPORT))

        # accept "call" from client
        lServerSocket.listen(5) # maximum number of 5 queued connections, should be irrelevant as all connections fork into a new thread

        # TODO: might need to be placed after except block
        return lServerSocket

    except socket.error, (value,message):
        if lServerSocket:
            lServerSocket.close()
        print "Could not open socket on Server: " + message
        sys.exit(1)

def clientHandler(pClientSocket, addr):
    global gNumCurrentClients, gNumCurrentClientsLock, gExamQuestionsFilePath

    # acquire a lock, blocking = True, timeout = -1
    gNumCurrentClientsLock.acquire()
    gNumCurrentClients += 1
    # unlock
    gNumCurrentClientsLock.release()

    # accept initial request
    data = pClientSocket.recv(1024)

    # client is sending a file
    if data == "File":
        lIsExecuted = receiveFile(pClientSocket)

    # client is executing a function
    else:
        lIsExecuted = interpreteClientString(data)

    if lIsExecuted == "s":
       print "Action was properly executed"

       # transmits TCP message: success
       pClientSocket.send("s")

    elif lIsExecuted == "file":
        #send the Questions File to the client
        pClientSocket.send("file")
        try:
            lOpenedQuestions = open(gExamQuestionsFilePath, 'r')
            lFileChunk = lOpenedQuestions.read(1024)
        except IOError:
            print "Something went wrong while reading the Questions file"
            return
         # block this thread until client is ready to accept the file
        lResponse = pClientSocket.recv(1024) # client will send "ready" or "abort"
        # make sure the client respoinse was positive
        if lResponse != "ready":
            print "The server aborted prior to transmission of file, check server logs for more details"
            return
        while (lFileChunk):
            pClientSocket.send(lFileChunk)
            lFileChunk = lOpenedQuestions.read(1024)
        print 'Finished sending the file'
    else:
       # transmits TCP message: fail
       pClientSocket.send("f")

    pClientSocket.close()

    gNumCurrentClientsLock.acquire()
    gNumCurrentClients -= 1
    gNumCurrentClientsLock.release()

    return

# transform input string into function object and make the call to the corresponding function in the back-end
def interpreteClientString(pClientString):

    lSplitUpFunction = pClientString.split("(")
    lFunctionName = lSplitUpFunction[0]

    if lSplitUpFunction[0] in ServerGlobals.gFunctionDictionary:
        # look up function in dictionary and make the call
        if len(lSplitUpFunction) == 1:
            ServerGlobals.gFunctionDictionary[lFunctionName]()
        else:
            lParameters = lSplitUpFunction[1].split(")")[0]
            if lParameters:
                ServerGlobals.gFunctionDictionary[lFunctionName](lParameters)
        return "s"
    else:
        # special case for start up routines
        if lSplitUpFunction[0] == "createStudentSubmissionDir":
            lParameters = lSplitUpFunction[1].split(")")[0]
            ServerRoutines.createStudentSubmissionDir(lParameters)
            return "file"
        else:
            lErrorMessage = "The function you are trying to call is not defined on the Server"
            raise RuntimeError(lErrorMessage)
            return lErrorMessage

def receiveFile(pClientSocket):

    lNewFile = openNewFileServerSide("ServerOutput.txt")

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
