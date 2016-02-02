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
        lServerSocket.bind((ServerGlobals.gHost, ServerGlobals.gPort))

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

    # increment number of current clients
    ServerGlobals.gNumCurrentClientsLock.acquire()
    ServerGlobals.gNumCurrentClients += 1
    ServerGlobals.gNumCurrentClientsLock.release()

    # accept initial request
    data = pClientSocket.recv(1024)

    #
    lIsExecuted = ""

    # client is sending a file
    if data == "ClientIsSendingAFile":

        # tell the client that we are ready to accept the file name
        pClientSocket.send("WhatIsTheFileName?")
        # now actually read the file name
        lFileName = pClientSocket.recv(1024)

        # tell the client that we are ready to accept the student email
        pClientSocket.send("WhatIsTheStudentName?")
        lStudentEmail = pClientSocket.recv(2048)

        lIsExecuted = receiveFile(pClientSocket, lFileName, lStudentEmail)

    # client is requesting the questions file
    elif data == "ClientWantsQuestions":
        #send the Questions File to the client
        #pClientSocket.send("file")
        try:
            lOpenedQuestions = open(ServerGlobals.gExamQuestionsFilePath, 'r')
            lFileChunk = lOpenedQuestions.read(1024)
        except IOError:
            print "Something went wrong while reading the Questions file"

        # send the file
        while (lFileChunk):
            pClientSocket.send(lFileChunk)
            lFileChunk = lOpenedQuestions.read(1024)
        print 'Finished sending the questions file to a client'

    # client is executing a function
    else:
        lIsExecuted = interpretClientString(data)

    if lIsExecuted == "s":
       print "Action was properly executed"

       # transmits TCP message: success
       pClientSocket.send("s")


    else:
       # transmits TCP message: fail
       pClientSocket.send("f")

    pClientSocket.close()


    # decrease number of current connections
    ServerGlobals.gNumCurrentClientsLock.acquire()
    ServerGlobals.gNumCurrentClients -= 1
    ServerGlobals.gNumCurrentClientsLock.release()

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
def interpretClientString(pClientString):

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
            createStudentSubmissionDir(lParameters)
            return "file"
        else:
            lErrorMessage = "The function you are trying to call is not defined on the Server"
            raise RuntimeError(lErrorMessage)
            return lErrorMessage


def openNewFileServerSide(pNameOfNewFile, pStudentEmail):

    # TODO: incorportate pStudentEmail into file path
    # TODO: check if student has a directory already, if not create it, else write file into it

     # create new or trunctate old file - hence the w flag
    try:
        # home directory has to exist, we just assert this
        assert os.path.exists(ServerGlobals.gServerExamDirectory)

        # append student email to Server home directory
        lDirectoryPath = os.path.join(ServerGlobals.gServerExamDirectory, pStudentEmail)

        # check if directory exists, if not we create it
        if os.path.exists(lDirectoryPath) == False:
            os.mkdir(lDirectoryPath)

        lDebugging = 'debuggingFile.txt'

        # append fileName to ServerDirectory + Email subdirectory
        # create / override file
        # TODO: keep track of all versions of a submission file
        lFilePath = os.path.join(lDirectoryPath, lDebugging)
        lNewFile = open(lFilePath, 'wb')

        return lNewFile
    except IOError:
        print "File could not be created on the Server"
        return False


def receiveFile(pClientSocket, pFileName, pStudentEmail):

    # open new file on the server
    lNewFile = openNewFileServerSide(pFileName, pStudentEmail)

    # initialize success indicator to false
    lSuccess = "f"
    try:
        # let the client know the server is ready
        pClientSocket.send("ReadyToAcceptClientFile")

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
        ServerGlobals.gServerExamDirectory = "ProfessorHomeDirectory"

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