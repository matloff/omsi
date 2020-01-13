import os
import select
import socket
import sys
import _thread
import threading
import pdb
import time

# March 14, 2019:  SuppFile acquisition removed by NM.


class OmsiServer:

    def __init__(self, gHost, gPort, examName):
        self.gHost = gHost
        self.gPort = gPort
        self.examName = examName

        self.socket = self.createSocket()  # listening socket
        self.lock = _thread.allocate_lock()
        self.totalClients = 0
        self.clientMap = {}  # who has connected, indexed by IP
        self.examDirectory = os.path.join('InstructorDirectory',examName)
        self.examQuestionsPath = \
           os.path.join('InstructorDirectory','Questions.txt')
        self.suppFilePath= \
           os.path.join('InstructorDirectory', 'SuppFile')

    def awaitConnections(self):
        # blocks and waits for connections
        print('server awaiting connections\n')
        self.examDirectoryLogFile.write('serverawaiting connections\n')

        clientSocket, clientAddr = self.socket.accept()
        print('connection from client at', clientAddr, '\n')
        self.examDirectoryLogFile.write('connection from client at' + str(clientAddr) + '\n')

        clientIP = clientAddr[0]
        if not clientIP in self.clientMap:
            self.clientMap[clientIP] = []
            self.totalClients += 1
            print("New connection detected at {0}.\nTotal connections: {1}". \
               format(clientAddr, self.totalClients))
            
            self.examDirectoryLogFile.write("""
                 New connection detected at {0}.\nTotal connections: {1}\n"""\
                 .format(clientAddr, self.totalClients))

        threading.Thread(target=self.requestHandler, 
           args=(clientSocket, clientAddr,)).start()

    # sets up the socket that the students connect to
    def createSocket(self):
        try:
            # create Internet TCP socket (domain, type)
            lServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # bind address(gHost, gPort) to socket
            ### lServerSocket.bind((self.gHost, self.gPort))
            lServerSocket.bind(('', self.gPort))

            # accept "call" from client
            lServerSocket.listen(5) # maximum number of 5 queued connections, should be irrelevant as all connections fork into a new thread

            # TODO: might need to be placed after except block
            return lServerSocket

        except socket.error as sockerror:
            (value, message) = sockerror.args
            if lServerSocket:
                lServerSocket.close()
            raise RuntimeError("Could not open socket on Server: " + message)
            sys.exit(1)

    # handles client interaction: detects client connection delegates 
    # requests to the corresponding routines
    def requestHandler(self, pClientSocket, addr):
        while 1:
            data = pClientSocket.recv(1024).decode("utf-8")
            if len(data) == 0:
               print('Empty "data" received')
               self.examDirectoryLogFile.write('Empty "data" received\n')
               break
            print('client request:', data, '\n')
            self.examDirectoryLogFile.write('client request:' + str(data) + '\n')

            lIsExecuted = ""

            if data[:8] == 'OMSI0001':  # client will send file to server
                print(time.ctime())
                print('Request: ', data)
                
                self.examDirectoryLogFile.write(time.ctime() + '\n')
                self.examDirectoryLogFile.write('Request: ' + str(data) + '\n')

                fields = data.split('\0')
                print('Fields: ', fields)
                self.examDirectoryLogFile.write('Fields: ' + str(fields) + '\n')

                #Validate the file name sent by the client to protect
                #against directory traversal attacks.
                lFileName = fields[1]
                if "../" in lFileName:
                   break

                lStudentEmail = fields[2]
                print('File to be sent: ', lFileName)
                print('Student ID: ', lStudentEmail, end=' ')
                print('IP: ', addr)
 
                self.examDirectoryLogFile.write('File to be sent: ' + str(lFileName) + '\n')
                self.examDirectoryLogFile.write('Student ID: ' + str(lStudentEmail) + '\n')
                self.examDirectoryLogFile.write('IP: ' + str(addr) + '\n')

                self.clientMap[addr[0]].append(lStudentEmail)

                tmp = list(self.clientMap.keys())[0] 
                tmp += ' ' + lStudentEmail
                tmp += ' ' + lFileName
                if len(fields) > 3:
                   tmp += ' ' + fields[3]
                   if len(fields) > 4:
                      tmp += ' ' + fields[4]

                self.examDirectoryLogFile.writelines(str(tmp) + '\n')
                self.examDirectoryLogFile.flush()

                # try to receive the (entire) file; lIsExecuted is
                # success/failure code
                lIsExecuted = self.receiveFile(pClientSocket, 
                   lFileName, lStudentEmail)

                if lIsExecuted == "s":
                    # transmits TCP message: success
                    successmsg = lStudentEmail + ' successfully submitted ' 
                    print('************  client:')
                    print(pClientSocket.getpeername())
                
                    self.examDirectoryLogFile.write('************  client:\n')
                    self.examDirectoryLogFile.write(str(pClientSocket.getpeername()) + '\n')

                    successmsg = successmsg + lFileName 
                    print(successmsg)
                    self.examDirectoryLogFile.write(successmsg + '\n')

                    pClientSocket.send(str.encode(successmsg))

                else:
                   # transmits TCP message: fail
                   failmsg =  \
                      lStudentEmail + ' did not successfully submit ' + lFileName                       
                   print(failmsg, '\n')
                   self.examDirectoryLogFile.write(failmsg + '\n')
                   pClientSocket.send(str.encode(failmsg))

            # client is requesting the questions file
            elif data == "ClientWantsQuestions":
                print('Sending questions to client')
                self.examDirectoryLogFile.write('Sending questions to client\n')

                # this function handles error messages + edge cases
                qfl = self.sendQuestionsToClient(pClientSocket)
                print('Total of ',qfl, 'bytes read from questions file')
                self.examDirectoryLogFile.write('Total of ' + str(qfl) + ' bytes read from questions file\n')
            elif data == b"ClientWantsSuppFile":
                if os.path.isfile(self.suppFilePath):
                    qfl = self.sendFileToClient(pClientSocket)
                    print('Total of ',qfl, 'bytes read from data file') 
                    self.examDirectoryLogFile.write('Total of ' + str(qfl) + ' bytes read from data file\n')

            # client is executing a function
            # TODO: refactor this or just get rid of it!
            ### NM, 10/15/27: deleting for now
            ### else:
            ###     lIsExecuted = self.interpretClientString(data)
            else: 
               print('Illegal client request:', data, '\n')
               self.examDirectoryLogFile.write('Illegal client request: ' + str(data) + '\n')
               break
            print("Server waiting to recv data")
            self.examDirectoryLogFile.write("Server waiting to recv data\n")
            data = pClientSocket.recv(1024).decode("utf-8")

            print('Server received', len(data), 'bytes\n')
            print('First line:', data.split('\n')[0], '\n')
            self.examDirectoryLogFile.write('Server received ' + str(len(data)) + ' bytes\n')
            self.examDirectoryLogFile.write('First line: ' + str(data.split('\n')[0]) + '\n')

        # pClientSocket.shutdown(socket.SHUT_WR)

        # pClientSocket.close()   this was commented out in 2016!
        self.totalClients -= 1
        print("Closing socket at {0}".format(addr))
        self.examDirectoryLogFile.write("Closing socket at {0}\n".format(addr))
        return  # end while


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
    def interpretClientString(self, pClientString):

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
    def openNewFileServerSide(self, pNameOfNewFile, pStudentEmail):
         # create new or trunctate old file - hence the w flag
        try:
            # home directory has to exist, we just assert this
            assert os.path.exists(self.examDirectory)

            # append student email to Server home directory
            lDirectoryPath = os.path.join(self.examDirectory, pStudentEmail)

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
            print("File could not be created on the Server")
            self.examDirectoryLogFile.write("File could not be created on the Server\n")
            return False

    def parseSubmitFileRequest(self, pClientSocket, data):
        email = ''
        filename = ''
        # the filename starts at index 8 of the data message,
        # just past 'OMSI0001'
        i = 8
        j = 8
        length = len(data)

        # parse out filename
        while j < length:
            if data[j] == '\0':
                filename = data[i:j]
                break
            j += 1
        i = j + 1
        j = i

        # parse out email
        while j < length:
            if data[j] == '\0':
                email = data[i:j]
                break
            j += 1
        i = j + 1

        newFile = self.openNewFileServerSide(filename, email)

        newFile.write(data[i:])

        print("Got file {0} from {1}".format(filename, email))
        self.examDirectoryLogFile.write("Got file {0} from {1}\n".format(filename, email))
        if len(data) < 1024:
            pClientSocket.send(str.encode("success"))
            return

        while True:
            data = pClientSocket.recv(1024)
            newFile.write(data)
            if len(data) < 1024:
                pClientSocket.send(str.encode("success"))
                return



    # routine for receiving a file from a student
    def receiveFile(self, pClientSocket, pFileName, pStudentEmail):

        # open new file on the server
        # lNewFile = self.openNewFileServerSide(pFileName, pStudentEmail)
        # print 'new server file opened'

        # initialize success indicator to fail
        lSuccess = "f"
        # let the client know the server is ready
        pClientSocket.send(str.encode("ReadyToAcceptClientFile"))

        # receive the file
        tmpFile = ''
        while 1:
            # set a timeout for this
            ready = select.select([pClientSocket], [], [], 2)
            if ready[0]:
                lChunkOfFile = pClientSocket.recv(1024).decode("utf-8")
                tmpFile += lChunkOfFile
                print('Received from '+pStudentEmail+':')
                print(lChunkOfFile)
                self.examDirectoryLogFile.write('Received from ' + pStudentEmail + ':\n')
                self.examDirectoryLogFile.write(lChunkOfFile + '\n')
                ## lNewFile.write(lChunkOfFile)
            else:
                # avoid overwriting an existing file with an empty one
                if len(tmpFile) == 0: break
                print('creating/updating student answer file')
                self.examDirectoryLogFile.write('Creating/updating student answer file\n')
                lNewFile = self.openNewFileServerSide(pFileName, pStudentEmail)
                lNewFile.write(str.encode(tmpFile))
                lNewFile.close()
                print("Finished accepting file")
                self.examDirectoryLogFile.write("Finished accepting file\n")
                lSuccess = "s"
                break

        # print("Finished accepting file")
        # lSuccess = "s"

        if lSuccess == "f":
            # something went wrong
            print("File transfer was not successful")
            self.examDirectoryLogFile.write("File transfer was not successful\n")
        ### close file, regardless of success
        ##lNewFile.close()

        # return success information
        return lSuccess

    # routine for sending the questions file to a student
    def sendQuestionsToClient(self, pClientSocket):
        #send the Questions File to the client
        try:
            lOpenedQuestions = open(self.examQuestionsPath, 'r')
            lFileChunk = lOpenedQuestions.read(1024)
            qfilelen = len(lFileChunk)
            lExceptionOccurred = False
        except IOError:
            print("Something wrong with reading the Questions file")
            self.examDirectoryLogFile.write("Something wrong with reading the Questions file\n")
            lFileChunk = ""
            lExceptionOccurred = True

        # send the file
        while (lFileChunk):
            print('Sending file chunk\n')
            print('First line:', lFileChunk.split('\n')[0], '\n')
            self.examDirectoryLogFile.write("Sending file chunk\n")
            self.examDirectoryLogFile.write("First line: " + str(lFileChunk.split('\n')[0]) + '\n')

            pClientSocket.send(str.encode(lFileChunk))
            # print "Sending file chunk {0}".format(lFileChunk)
            lFileChunk = lOpenedQuestions.read(1024)
            qfilelen = qfilelen + len(lFileChunk)
        pClientSocket.send(str.encode(chr(0)))
        # print "Sending eof chunk {0}".format(lFileChunk)
        # pClientSocket.send(lFileChunk)

        # display success message for debugging purposes only
        # TODO: comment this out for prod. It clogs up the command prompt unnecessarily
        if lExceptionOccurred == False:
            print('Successfully sent the questions file to a client')
            self.examDirectoryLogFile.write("Successfully sent the questions file to a client\n")

        return qfilelen
 
    # routine for sending a file to a student
    def sendFileToClient(self, pClientSocket):
        fn = self.suppFilePath
        if os.path.isfile(fn):
            #send the data File to the client
            try:
                lOpenedFile = open(fn, 'r')
                lFileChunk = lOpenedFile.read(1024)
                qfilelen = len(lFileChunk)
                lExceptionOccurred = False
            except IOError:
                print("No such file")
                self.examDirectoryLogFile.write("No such file\n")
                lFileChunk = ""
                lExceptionOccurred = True

            # send the file
            while (lFileChunk):
                print('Sending file chunk\n')
                print('First line:', lFileChunk.split('\n')[0], '\n')
                self.examDirectoryLogFile.write("Sending file chunk\n")
                self.examDirectoryLogFile.write("First line: " + str(lFileChunk.split('\n')[0]) + '\n')

                pClientSocket.send(str.encode(lFileChunk))
                # print "Sending file chunk {0}".format(lFileChunk)
                lFileChunk = lOpenedFile.read(1024)
                qfilelen = qfilelen + len(lFileChunk)
            pClientSocket.send(chr(0))
            # print "Sending eof chunk {0}".format(lFileChunk)
            # pClientSocket.send(lFileChunk)

            # display success message for debugging purposes only
            # TODO: comment this out for prod. It clogs up the command prompt unnecessarily
            if lExceptionOccurred == False:
                print('Successfully sent file to a client')
                self.examDirectoryLogFile.write("Successfully sent file to a client\n")

            return qfilelen
        else:
            print('No file to send')
            self.examDirectoryLogFile.write("No file to send\n")
        return False

    # asks professor to specify directory to store exam questions and student submissions
    # confirms that the exam questions file is in the directory
    # stores directory path, file path as Server.gServerExamDirectory, Server.gExamQuestionsFilePath
    def startUpExamDirectory(self):

        lExamQuestionsFilePath = False

        while not lExamQuestionsFilePath:
            ### print """Please enter a home directory for the exam. This will be the directory that all students\' files will be stored in.\nBefore pressing enter, please check that the exam questions are in the directory and named \'Questions.txt\'."""

            # Hard coding for testing purposes.
            ### NM del  self.examDirectory = "InstructorDirectory"

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
            print('Error: File does not exist or is not readable. Please check that the specified path is spelled ' \
                  'correctly and a file named \'Questions.txt\' is in the specified directory.')
            self.examDirectoryLogFile.write('Error: File does not exist or is not readable. Please check that the specified path is spelled ' \
                  'correctly and a file named \'Questions.txt\' is in the specified directory.\n')
            return False



# set up the connection, start listening, start the threads and 
# send feedback to client
def main():
    print("Running")
    v = open('VERSION')
    version = v.readline()
    print('Version: ', version)
    # command line should be:  python3 OmsiServer.py <port> <exam name>
    if len(sys.argv) <  3:
        print("Usage: python3 OmsiServer.py <port> <exam name>")
        sys.exit(1)
    hostname = socket.gethostname()
    omsiServer = OmsiServer(hostname,int(sys.argv[1]),sys.argv[2])
    os.mkdir(omsiServer.examDirectory)
    omsiServer.examDirectoryLogFile = \
       open(omsiServer.examDirectory + '/LOGFILE','w')
    omsiServer.version = version
    # connection information.
    print("Server for {0} is now running at {1}:{2}".format(sys.argv[2], \
       hostname, sys.argv[1]))
    omsiServer.examDirectoryLogFile.write("Server for {0} is now running at {1}:{2}\n"\
          .format(sys.argv[2], hostname, sys.argv[1]))
    while True:
        omsiServer.awaitConnections()

if __name__ == '__main__':
    main()

