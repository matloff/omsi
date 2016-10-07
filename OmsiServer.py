import os
import select
import socket
import sys
import thread

import ServerGlobals

class OmsiServer:
    def __init__(self, gHost, gPort, examName):
        self.gHost = gHost
        self.gPort = gPort
        self.examName = examName

        self.socket = self.createSocket()
        self.lock = thread.allocate_lock()
        self.totalClients = 0
        self.clientMap = {}
        self.examDirectory = None
        self.examQuestionsPath = None

    def awaitConnections(self):
        #blocks and waits for connections
        clientSocket, clientAddr = self.socket.accept()
        if clientAddr in self.clientMap:
            self.clientMap[clientAddr] += 1
        else:
            self.clientMap[clientAddr] = 1
            self.totalClients += 1
            print "New Connection Detected at {0}.\nTotal Connections: {1}".format(clientAddr, self.totalClients)

        threading.Thread(target=self.requestHandler, args=(clientSocket, clientAddr,)).start()
    # sets up the socket that the students connect to
    def createSocket(self):
        try:
            # create Internet TCP socket (domain, type)
            lServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # bind address(gHost, gPort) to socket
            lServerSocket.bind((self.gHost, self.gPort))

            # accept "call" from client
            lServerSocket.listen(5) # maximum number of 5 queued connections, should be irrelevant as all connections fork into a new thread

            # TODO: might need to be placed after except block
            return lServerSocket

        except socket.error, (value, message):
            if lServerSocket:
                lServerSocket.close()
            raise RuntimeError("Could not open socket on Server: " + message)
            sys.exit(1)

    # handles client interaction: detects client connection delegates requests to the corresponding routines
    def requestHandler(self, pClientSocket, addr):

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

            if lIsExecuted == "s":
                # transmits TCP message: success

                print lStudentEmail + ' successfully submitted ' + lFileName + ' correctly.'
                pClientSocket.send(lStudentEmail + ' successfully submitted ' + lFileName)

            else:
               # transmits TCP message: fail
               print lStudentEmail + ' did not successfully submit ' + lFileName
               pClientSocket.send(lStudentEmail + ' did not successfully submit ' + lFileName)

        # client is requesting the questions file
        elif data == "ClientWantsQuestions":
            # this function handles error messages + edge cases
            sendQuestionsToClient(pClientSocket)

        # client is executing a function
        # TODO: refactor this or just get rid of it!
        else:
            lIsExecuted = interpretClientString(data)

        pClientSocket.close()

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

    # opens new file in a directory on the server
    def openNewFileServerSide(pNameOfNewFile, pStudentEmail):
         # create new or trunctate old file - hence the w flag
        try:
            # home directory has to exist, we just assert this
            assert os.path.exists(ServerGlobals.gServerExamDirectory)

            # append student email to Server home directory
            lDirectoryPath = os.path.join(ServerGlobals.gServerExamDirectory, pStudentEmail)

            # check if directory exists, if not we create it
            if os.path.exists(lDirectoryPath) == False:
                os.mkdir(lDirectoryPath)

            # append fileName to ServerDirectory + Email subdirectory
            # create / override file
            # TODO: keep track of all versions of a submission file
            lFilePath = os.path.join(lDirectoryPath, pNameOfNewFile)
            lNewFile = open(lFilePath, 'wb')

            return lNewFile
        except IOError:
            print "File could not be created on the Server"
            return False

    # routine for receiving a file from a student
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

    # routine for sending the questions file to a student
    def sendQuestionsToClient(pClientSocket):

        #send the Questions File to the client
        try:
            lOpenedQuestions = open(ServerGlobals.gExamQuestionsFilePath, 'r')
            lFileChunk = lOpenedQuestions.read(1024)
            lExceptionOccurred = False
        except IOError:
            print "Something went wrong while reading the Questions file"
            lFileChunk = ""
            lExceptionOccurred = True

        # send the file
        while (lFileChunk):
            pClientSocket.send(lFileChunk)
            lFileChunk = lOpenedQuestions.read(1024)

        # display success message for debugging purposes only
        # TODO: comment this out for prod. It clogs up the command prompt unnecessarily
        if lExceptionOccurred == False:
            print 'Successfully sent the questions file to a client'

        return

    # asks professor to specify directory to store exam questions and student submissions
    # confirms that the exam questions file is in the directory
    # stores directory path, file path as Server.gServerExamDirectory, Server.gExamQuestionsFilePath
    def startUpExamDirectory(self):

        lExamQuestionsFilePath = False

        while not lExamQuestionsFilePath:
            print """Please enter a home directory for the exam. This will be the directory that all students\' files will be stored in.\nBefore pressing enter, please check that the exam questions are in the directory and named \'Questions.txt\'."""

            # Hard coding for testing purposes.
            self.examDirectory = "ProfessorHomeDirectory"

            # confirm that exam questions file containing test questions
            lExamQuestionsFilePath = self.verifyExamQuestionsFile(self.examDirectory)

        self.examQuestionsPath = lExamQuestionsFilePath


    # verify that specified directory contains exam questions file, returns file path
    # if file not found or not readable, print error message and return false
    def verifyExamQuestionsFile(self, pExamDirectory):

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



# set up the connection, start listening, start the threads and send feedback to client
def main():
    print "running"

    if len(sys.argv) <  3:
        print "Usage: OmsiServer.py port ExamName"
        sys.exit(1)

    hostname = socket.gethostname()

    omsiServer = OmsiServer(hostname, int(sys.argv[1]), sys.argv[2])

    omsiServer.startUpExamDirectory()
  
    # print connection information.
    print "Server for {0} is now running at {1}:{2}".format(sys.argv[2], hostname, sys.argv[1])


    while True:
        omsiServer.awaitConnections()

# this script is the "Main" script on the back-end. It is supposed to be run by itself
if __name__ == '__main__':
    main()