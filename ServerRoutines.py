import os
import select
import socket
import sys

import ServerGlobals


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


# for each student that connects to the server, create a folder
# send file containing test questions to the student
def createStudentSubmissionDir(pStudentEmail):

    # create folder name as sys.path (global in Server) + email
    lIdealPathName = ServerGlobals.gServerHomeDirectory + pStudentEmail

    # create folder
    if not os.path.exists(lIdealPathName):
        os.makedirs(lIdealPathName)

    # initiate the questions to be sent to the student. Done in Server.py, based on socket
    return "file"


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


def openNewFileServerSide(pNameOfNewFile):
     # create new or trunctate old file - hence the w flag
    try:
        lNewFile = open(pNameOfNewFile, 'w')
        return lNewFile
    except IOError:
        print "File could not be created on the Server"
        return False


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


# asks professor to specify directory to store exam questions and student submissions
# confirms that the exam questions file is in the directory
# stores directory path, file path as Server.gServerExamDirectory, Server.gExamQuestionsFilePath
def startUpExamDirectory():

    lExamQuestionsFilePath = False

    while not lExamQuestionsFilePath:
        print 'Please enter a home directory for the exam. This will be the directory that all students\' files will ' \
              'be stored in.\nBefore pressing enter, please check that the exam questions are in the directory and ' \
              'named \'Questions.txt\'.'

        # professor enters directory path
        # hard coded for testing on Rylan's machine
        #Server.gServerHomeDirectory = raw_input()
        ServerGlobals.gServerExamDirectory = "/home/rylan/Documents/omsi/professorFileDirectory/"

        # confirm that exam questions file containing test questions
        lExamQuestionsFilePath = verifyExamQuestionsFile(ServerGlobals.gServerExamDirectory)

    ServerGlobals.gExamQuestionsFilePath = lExamQuestionsFilePath


# verify that specified directory contains exam questions file, returns file path
# if file not found or not readable, print error message and return false
def verifyExamQuestionsFile(pExamDirectory):

    # return path of exam questions file
    try:
        lExamQuestionsFilePath = os.path.join(pExamDirectory, 'Questions.txt')
        lOpenFile = open(lExamQuestionsFilePath, 'r')
        lOpenFile.close()
        return lExamQuestionsFilePath

    # if attempt to open file fails, print error and return false
    except IOError:
        print 'Error: File does not exist or is not readable. Please check that the specified path is spelled ' \
              'correctly and a file named \'Questions.txt\' is in the specified directory.'
        return False