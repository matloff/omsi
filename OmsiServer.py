import os
import select
import socket
import sys
import thread
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
        self.lock = thread.allocate_lock()
        self.totalClients = 0
        self.clientMap = {}  # who has connected, indexed by IP
        self.examDirectory = os.path.join('InstructorDirectory',examName)
        self.examQuestionsPath = \
           os.path.join('InstructorDirectory','Questions.txt')
        self.suppFilePath= \
           os.path.join('InstructorDirectory', 'SuppFile')

    def awaitConnections(self):
        # blocks and waits for connections
        print 'server awaiting connections\n'
        clientSocket, clientAddr = self.socket.accept()
        print 'connection from client at', clientAddr, '\n'
        clientIP = clientAddr[0]
        if not clientIP in self.clientMap:
            self.clientMap[clientIP] = []
            self.totalClients += 1
            print "new connection detected at {0}.\ntotal connections: {1}". \
               format(clientAddr, self.totalClients)

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

        except socket.error, (value, message):
            if lServerSocket:
                lServerSocket.close()
            raise RuntimeError("Could not open socket on Server: " + message)
            sys.exit(1)

    # handles client interaction: detects client connection delegates 
    # requests to the corresponding routines
    def requestHandler(self, pClientSocket, addr):
        while 1:
            data = pClientSocket.recv(1024)
            if len(data) == 0:
               print 'empty "data" received'
               break
            print 'client request:', data, '\n'

            lIsExecuted = ""

            if data[:8] == 'OMSI0001':  # client will send file to srvr
                print time.ctime()
                print 'request:', data
                fields = data.split('\0')
                print 'fields:',fields
                lFileName = fields[1]
                lStudentEmail = fields[2]
                print 'file to be sent is', lFileName
                print 'student ID:', lStudentEmail,
                print ', IP:', addr
                self.clientMap[addr[0]].append(lStudentEmail)
                print 'client list:'
                print self.clientMap
                tmp = self.clientMap.keys()[0] 
                tmp += ' ' + lStudentEmail
                tmp += ' ' + lFileName
                if len(fields) > 3:
                   tmp += ' ' + fields[3]
                   if len(fields) > 4:
                      tmp += ' ' + fields[4]
                # tmp += '\n'
                ### tmp = ' '.join(['{0} {1}'.format(k, v) for k,v in \
                ###    self.clientMap.iteritems()])
                self.examDirectoryLogFile.writelines(tmp)
                self.examDirectoryLogFile.flush()

                # try to receive the (entire) file; lIsExecuted is
                # success/failure code
                lIsExecuted = self.receiveFile(pClientSocket, 
                   lFileName, lStudentEmail)

                if lIsExecuted == "s":
                    # transmits TCP message: success
                    successmsg = lStudentEmail + ' successfully submitted ' 
                    print '************  client:'
                    print pClientSocket.getpeername()
                    successmsg = successmsg + lFileName 
                    print successmsg
                    pClientSocket.send(successmsg)

                else:
                   # transmits TCP message: fail
                   failmsg =  \
                      lStudentEmail + ' did not successfully submit ' + lFileName                       
                   print failmsg, '\n'
                   pClientSocket.send(failmsg)

            # client is requesting the questions file
            elif data == "ClientWantsQuestions":
                print 'sending questions to client'
                # this function handles error messages + edge cases
                qfl = self.sendQuestionsToClient(pClientSocket)
                print 'total of ',qfl, 'bytes read from questions file' 
            elif data == "ClientWantsSuppFile":
                if os.path.isfile(self.suppFilePath):
                    qfl = self.sendFileToClient(pClientSocket)
                    print 'total of ',qfl, 'bytes read from data file' 

            # client is executing a function
            # TODO: refactor this or just get rid of it!
            ### NM, 10/15/27: deleting for now
            ### else:
            ###     lIsExecuted = self.interpretClientString(data)
            else: 
               print 'illegal client request:', data, '\n'
               break
            print "Server waiting to recv data"
            data = pClientSocket.recv(1024)
            ## print "Server recvd data {0}".format(data)
            print 'server received',len(data), 'bytes\n'
            print 'first line:', data.split('\n')[0], '\n'

        # pClientSocket.shutdown(socket.SHUT_WR)

        # pClientSocket.close()   this was commented out in 2016!
        self.totalClients -= 1
        print "Closing socket at {0}".format(addr)
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
            print "File could not be created on the Server"
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

        print "Got file {0} from {1}".format(filename, email)
        if len(data) < 1024:
            pClientSocket.send("success")
            return

        while True:
            data = pClientSocket.recv(1024)
            newFile.write(data)
            if len(data) < 1024:
                pClientSocket.send("success")
                return



    # routine for receiving a file from a student
    def receiveFile(self, pClientSocket, pFileName, pStudentEmail):

        # open new file on the server
        lNewFile = self.openNewFileServerSide(pFileName, pStudentEmail)
        print 'new server file opened'

        # initialize success indicator to fail
        lSuccess = "f"
        # let the client know the server is ready
        pClientSocket.send("ReadyToAcceptClientFile")

        # receive the file
        while 1:
            # set a timeout for this
            ready = select.select([pClientSocket], [], [], 2)
            if ready[0]:
                lChunkOfFile = pClientSocket.recv(1024)
                print 'received:'
                print lChunkOfFile
                lNewFile.write(lChunkOfFile)
            else:
                break

        print("Finished accepting file")
        lSuccess = "s"

        if lSuccess == "f":
            # something went wrong
            print "File transfer was not successful"
        # close file, regardless of success
        lNewFile.close()

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
            print "Something wrong with reading the Questions file"
            lFileChunk = ""
            lExceptionOccurred = True

        # send the file
        while (lFileChunk):
            print 'sending file chunk\n'
            print 'first line:', lFileChunk.split('\n')[0], '\n'
            pClientSocket.send(lFileChunk)
            # print "Sending file chunk {0}".format(lFileChunk)
            lFileChunk = lOpenedQuestions.read(1024)
            qfilelen = qfilelen + len(lFileChunk)
        pClientSocket.send(chr(0))
        # print "Sending eof chunk {0}".format(lFileChunk)
        # pClientSocket.send(lFileChunk)

        # display success message for debugging purposes only
        # TODO: comment this out for prod. It clogs up the command prompt unnecessarily
        if lExceptionOccurred == False:
            print 'Successfully sent the questions file to a client'

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
                print "No such file"
                lFileChunk = ""
                lExceptionOccurred = True

            # send the file
            while (lFileChunk):
                print 'sending file chunk\n'
                print 'first line:', lFileChunk.split('\n')[0], '\n'
                pClientSocket.send(lFileChunk)
                # print "Sending file chunk {0}".format(lFileChunk)
                lFileChunk = lOpenedFile.read(1024)
                qfilelen = qfilelen + len(lFileChunk)
            pClientSocket.send(chr(0))
            # print "Sending eof chunk {0}".format(lFileChunk)
            # pClientSocket.send(lFileChunk)

            # display success message for debugging purposes only
            # TODO: comment this out for prod. It clogs up the command prompt unnecessarily
            if lExceptionOccurred == False:
                print 'Successfully sent file to a client'

            return qfilelen
        else:
            print 'No file to send'
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
            print 'Error: File does not exist or is not readable. Please check that the specified path is spelled ' \
                  'correctly and a file named \'Questions.txt\' is in the specified directory.'
            return False



# set up the connection, start listening, start the threads and 
# send feedback to client
def main():
    print "running"
    v = open('VERSION')
    version = v.readline()
    print 'Version', version
    # command line should be:  OmsiServer.py, port, exam name
    if len(sys.argv) <  3:
        print "Usage: OmsiServer.py port exam_name"
        sys.exit(1)
    hostname = socket.gethostname()
    omsiServer = OmsiServer(hostname,int(sys.argv[1]),sys.argv[2])
    os.mkdir(omsiServer.examDirectory)
    omsiServer.examDirectoryLogFile = \
       open(omsiServer.examDirectory + '/LOGFILE','w')
    omsiServer.version = version
    # connection information.
    print "Server for {0} is now running at {1}:{2}".format(sys.argv[2], \
       hostname, sys.argv[1])
    while True:
        omsiServer.awaitConnections()

if __name__ == '__main__':
    main()

