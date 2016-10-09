
import select
import socket
import os
import pdb


# module that provides an interface for all client-requests to server
class OmsiClient:
    def __init__(self, gHost, gPort, gStudentEmail):
        # Store the original host name that was entered for UI purposes.
        self.origHost = gHost
        # Make sure the hostname is the actual address.
        self.gHost = socket.gethostbyname(gHost)
        self.gPort = gPort
        self.gStudentEmail = gStudentEmail
        self.omsiSocket = None

        try:
            self.assertSocketCanBeCreated()
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
    def createExamQuestionsFile(self):

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
    def openFileOnClient(self, pFileName):
        try:
          lFilePath = os.path.join('', pFileName)
          lOpenFile = open(lFilePath, "r")
          return lOpenFile
        except IOError:
            try:
                # file was not in the home directory, try to see id the file is in the code's directory
                lOpenFile = open(pFileName, "r")
                return lOpenFile
            except:
                # file was not to be found at all. The name is wrong or the file is somewhere unexpected
                print "Error: File %s could not be opened. Make sure you entered the correct filename and the file is in your home directory" % pFileName
                return False


    # download exam questions from professor's machine
    def getExamQuestionsFile(self, pClientSocket):

        # filename = self.createExamQuestionsFile()
        # create local file to write exam questions to
        lExamQuestionsFile = self.createExamQuestionsFile()

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
                # ready = select.select([pClientSocket], [], [], 2)
                print "Client Waiting to recv"
                lChunkOfFile = pClientSocket.recv(1024)
                print "Client recvd chunk {0}".format(lChunkOfFile)

                if lChunkOfFile != '':
                    lExamQuestionsFile.write(lChunkOfFile)
                if len(lChunkOfFile) < 1024:
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
            # close socket

            # return File
            return lSuccess, lExamQuestionsFile


    # sends a file from the client to the server
    def sendFileToServer(self, pFileName):

        # open the file -> this handles exceptions effectively
        print "Opening file " + pFileName
        lOpenFile = self.openFileOnClient(pFileName)

        try:
            ldebugging = lOpenFile.read(1024)
            lOpenFile.seek(0)
            lCanIReadFromFile = True
        except:
            lCanIReadFromFile = False

        # if file is ready to be sent, connect to the server
        if not lCanIReadFromFile:
            return "File could not be submitted to the server because it was unable to be opened for read! Please retry and make sure you are submitting a valid file."

        try:
            if not self.omsiSocket:
                self.omsiSocket = self.configureSocket()

            # tell the server that we are sending a file
            msg = "OMSI0001" + pFileName + "\0" + self.gStudentEmail + "\0"

            # # block this before sending the filename, otherwise both the command and the file name will be appended on the server
            # lDebugging = self.omsiSocket.recv(1024);
            # print lDebugging

            # # send the name of the file
            # self.omsiSocket.send(pFileName)

            # # block client until server is ready to accept the email of the student
            # lDebugging = self.omsiSocket.recv(1024)
            # print lDebugging

            # #send the student email
            # self.omsiSocket.send(self.gStudentEmail)

            # # all information has been sent, get the go sign from the server
            # lResponse = self.omsiSocket.recv(1024)

            # if something went wrong server side, abort
            # if lResponse != "ReadyToAcceptClientFile":
            #     print "The server aborted prior to transmission of file, check server logs for more details.\nResponse was {0}".format(lResponse)
            #     return

            # send the file
            lFileChunk = lOpenFile.read(1024 - len(msg))
            lFileChunk = msg + lFileChunk
            print "file chunk " + lFileChunk
            while (lFileChunk):
                print "Sending File %s" % pFileName
                self.omsiSocket.send(lFileChunk)
                lFileChunk = lOpenFile.read(1024)

            lOpenFile.close()

            lServerResponse = self.omsiSocket.recv(1024)

            print lServerResponse


            return lServerResponse
        except ValueError as e:
            raise ValueError("Error sending file to server!", pFileName, e)
        except socket.error as e:
            print "Got error {0} for {1}.\nSetting socket to none and retrying...".format(e, pFileName)
            self.omsiSocket = None
            self.sendFileToServer(pFileName)








