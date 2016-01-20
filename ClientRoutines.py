import select
import socket

import Checksum
import ClientGlobals


# module that provides an interface for all server related requests
# sets up connection with the running server on localhost and port 20500
# all methods are static and should be called statically


# executes a function on the server
# input function name to be executed
# return value True or False depending on success on server
def callFunctionOnServer(functionName):

    #create and configure the socket
    lSocket = configureSocket()

    # execute the function
    lSocket.send(functionName)

    # see what the server has to say and return it
    lServerResponse = getResponseFromServer(lSocket)

    if lServerResponse == "s" or lServerResponse == "f":
        return lServerResponse
    else:
        # the server is trying to send a file
        if lServerResponse == "file":
            receiveExamQuestionsFile(lSocket)
        else:
            return "f"


def computeChecksum(filename):

    # values students need to copy down for reference
    h = Checksum.checksum(filename)

    print 'Please hand copy the following value and turn it into the professor: ' + h


# initialization of socket, no connection is established yet
def configureSocket():
    # connection on localhost for now

    try:
        # create local Internet TCP socket (domain, type)
        pSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # initiate server connection to global
        pSocket.connect( (ClientGlobals.gHost, ClientGlobals.gPort) )
        return pSocket

    #connection problem
    except socket.error, (value,message):
        if pSocket:
            # close socket
            pSocket.close()
        raise RuntimeError("Could not open socket on Client: " + message)
        return False


def createExamQuestionsFile():
    # create new or trunctate old file - hence the w flag
    try:
        lNewFile = open("ExamQuestions.txt", 'w')
        return lNewFile
    except IOError:
        print "Error: Exam questions file could not be created on Client's machine\n"
        return False


# close the connection
# returning success/failure message or initiating a file transfer from server to student
def getResponseFromServer(pSocket):
    # block until server response received
    lServerResponse = pSocket.recv(1024)
    if lServerResponse != "file":
        pSocket.close()
        if lServerResponse == "s":
            return True
        else:
            print lServerResponse
            return False
    else:
        return "file"

# this opens a file with read permissions on the file
# ATTENTION: an open file is returned! Call file.close() on the returned object
def openFile(pFileName):
    try:
      lOpenFile = open(pFileName, "r")
      return lOpenFile
    except IOError:
      print "Error: File does not appear to exist."
      return 0


# download exam questions from professor's machine
def receiveExamQuestionsFile(pClientSocket):

    # create local file to write exam questions to
    lExamQuestionsFile = createExamQuestionsFile()

    # if file was not created, notify the server
    if not lExamQuestionsFile:
        pClientSocket.send("abort")

    # create boolean to track
    lSuccess = False
    try:
        # if file was successfully created, notify server to begin sending exam questions
        pClientSocket.send("ready")

        print "Reading file from server\n"

        # write data from server to file
        while True:
            ready = select.select([pClientSocket], [], [], 2)
            lChunkOfFile = pClientSocket.recv(1024)
            if ready[0] and lChunkOfFile != '':
                lExamQuestionsFile.write(lChunkOfFile)
            else:
                print "Finished accepting file"
                lSuccess = True
                break

    finally:
        # if exam questions were not successfully downloaded, print error
        if not lSuccess:
            print "Error: File transfer was not successful"

        # close file, regardless of success
        lExamQuestionsFile.close()

        # return success information
        return lSuccess


# sends a file from the student to the professor
# submission of file
def sendFileToServer(pFileName):

    # create and configure the socket
    lSocket = configureSocket()

    # open the file
    lOpenFile = openFile(pFileName)

    if (lOpenFile):

        # first tell the server that we are sending a file
        lSocket.send("File")

        # block client until server is ready to accept the file
        lResponse = lSocket.recv(1024) # server will send "ready" or "abort"

        # check if something went wrong server side
        if lResponse != "ready":
            print "The server aborted prior to transmission of file, check server logs for more details"
            return

        # codes for abort?

        # send the file
        lFileChunk = lOpenFile.read()
        while (lFileChunk):
            print 'Sending File'
            lSocket.send(lFileChunk)
            lFileChunk = lOpenFile.read(1024)

        # any chance that the file cant be sent?

    # print msg if file cannot be opened
    else:
        # Error message for a bad student submission file
        print "Unable to read file: " + pFileName + "." \
                                                    "Make sure your submission file is in the " \
                                                    "right directory and is of type .txt."
    # closing the file
    lOpenFile.close()
    return getResponseFromServer(lSocket)

# simple setter
# pHost = IP address provided by prof
# pPort = Port provided by prof
def setUpServer(pHost, pPort):
    global gPORT, gHOST
    # deactivated during testing phase! The connection is set up on localhost
    # gPORT = pPort
    # gHOST = pHost