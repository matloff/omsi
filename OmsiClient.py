
import select
import socket
import os

# module that provides an interface for all client-requests to server
def __init__(self, gHost, gPort, gStudentEmail):
    # Store the original host name that was entered for UI purposes.
    self.origHost = gHost
    # Make sure the hostname is the actual address.
    self.gHost = socket.gethostbyname(gHost)
    self.gPort = gPort
    self.gStudentEmail = gStudentEmail

    try:
        self.assertSocketCanBeCreated():
    except ValueError as e:
        raise ValueError('Unable to create socket! Check Parameters', self.origHost, self.gPort, e)

def assertSocketCanBeCreated(self):
    response = self.configureSocket()
    if response:
        response.close()
        return True
    return False

# initialization of socket, no connection is established yet
def configureSocket(self):
    try:
        # create TCP socket (domain, type)
        pSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # initiate server connection to global
        pSocket.connect((self.gHost, self.gPort))

        return pSocket

    # connection problem
    except socket.error, (value, message):
        # if socket was created, close socket
        if pSocket:
            pSocket.close()
        raise ValueError("Error configuring socket! " + message)
        return None


# creates file with the questions on the client's machine
def createExamQuestionsFile():

    try:

        lFilePath = 'ExamQuestions.txt'
        lNewFile = open(lFilePath, 'w')
        return lNewFile

    # something went wrong
    except IOError:
        return False


# close the connection
# returning success/failure message or initiating a file transfer from server to student
def getResponseFromServer(pSocket):
    # block until server response received
    lServerResponse = pSocket.recv(1024)
    print "Server Response: " + lServerResponse
    if lServerResponse != "file":
        pSocket.close()
        if lServerResponse == "s":
            return True
        else:
            print lServerResponse
            return False
    else:
        return 'file'


# TODO: Update this routine
# this opens a file with read permissions on the file
# ATTENTION: an open file is returned! Call file.close() on the returned object
def openFileOnClient(pFileName):
    try:
      lFilePath = os.path.join(ClientGlobals.gStudentHomeDirectory, pFileName)
      lOpenFile = open(lFilePath, "r")
      return lOpenFile
    except IOError:
        try:
            # file was not in the home directory, try to see id the file is in the code's directory
            lOpenFile = o
            pen(pFileName, "r")
            return lOpenFile
        except:
            # file was not to be found at all. The name is wrong or the file is somewhere unexpected
            print "Error: File %s could not be opened. Make sure you entered the correct filename and the file is in your home directory" % pFileName
            return False


# download exam questions from professor's machine
def getExamQuestionsFile(pClientSocket):

    
    # create local file to write exam questions to
    lExamQuestionsFile = createExamQuestionsFile(filename)

    # if file was not created, notify the user
    if not lExamQuestionsFile:
        print 'Error: Exam questions file could not be created on client\'s machine.'
        return

    # create boolean to track success
    lSuccess = False

    # if file was successfully created, notify server to begin sending exam questions
    try:
        print "Reading exam questions from server."

        pClientSocket.send("ClientWantsQuestions")

        # write data from server to file
        while True:
            ready = select.select([pClientSocket], [], [], 2)
            lChunkOfFile = pClientSocket.recv(1024)
            if ready[0] and lChunkOfFile != '':
                lExamQuestionsFile.write(lChunkOfFile)
            else:
                lSuccess = True
                break

    finally:
        # if exam questions were not successfully downloaded, print error
        if lSuccess:
            print "Exam questions successfully read from server."
        else:
            print "Error: Exam questions were not successfully read from server."

        # close file, regardless of success
        lExamQuestionsFile.close()

        # return File
        return lSuccess, lExamQuestionsFile


# sends a file from the client to the server
def sendFileToServer(pFileName):

    # open the file -> this handles exceptions effectively
    lOpenFile = openFileOnClient(pFileName)

    try:
        ldebugging = lOpenFile.read(1024)
        lOpenFile.close()
        lCanIReadFromFile = True
    except:
        lCanIReadFromFile = False

    # if file is ready to be sent, connect to the server
    if lCanIReadFromFile:

        if not configureSocket()[0]:
            print configureSocket()[1]
            return configureSocket()[1]

        # create and configure the socket
        lSocket = configureSocket()[1]

        # tell the server that we are sending a file
        lSocket.send("ClientIsSendingAFile")

        # block this before sending the filename, otherwise both the command and the file name will be appended on the server
        lDebugging = lSocket.recv(1024);

        # send the name of the file
        lSocket.send(pFileName)

        # block client until server is ready to accept the email of the student
        lDebugging = lSocket.recv(1024)

        #send the student email
        lSocket.send(ClientGlobals.gStudentEmail)

        # all information has been sent, get the go sign from the server
        lResponse = lSocket.recv(1024)

        # if something went wrong server side, abort
        if lResponse != "ReadyToAcceptClientFile":
            print "The server aborted prior to transmission of file, check server logs for more details"
            return

        # send the file
        lOpenFile = openFileOnClient(pFileName)
        lFileChunk = lOpenFile.read(1024)
        while (lFileChunk):
            print "Sending File %s" % pFileName
            lSocket.send(lFileChunk)
            lFileChunk = lOpenFile.read(1024)

        lOpenFile.close()

        lServerResponse = lSocket.recv(1024)

        print lServerResponse

        lSocket.close()

        return lServerResponse

    # print msg if file cannot be opened
    else:
        # Error message for a bad student submission file
        return "File could not be submitted to the server! Please retry and make sure you are submitting a valid file."

# simple setter
# pHost = IP address provided by prof
# pPort = Port provided by prof
def setUpServer(pHost, pPort):
    global gPORT, gHOST
    # deactivated during testing phase! The connection is set up on localhost
    # gPORT = pPort
    # gHOST = pHost