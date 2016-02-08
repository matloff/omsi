__author__ = 'fdemoullin'

# Example class for how to use the Client interface
# All code on the Client-side should use this interface to communicate with the server
# This abstracts networking details like sockets, ports, and TCP byte separation

import ClientRoutines
import ClientGlobals


ClientGlobals.gStudentEmail = raw_input("Enter email for this test suite: ")
ClientGlobals.gHost = raw_input("Enter Host name: ")
ClientGlobals.gPort = int(raw_input("Enter Port name: "))


print "File was downloaded"

i = 0
while (i < 100):

    lSocket = ClientRoutines.configureSocket()
    ClientRoutines.receiveExamQuestionsFile(lSocket)

    ClientRoutines.sendFileToServer("Question1.txt")

    ClientRoutines.sendFileToServer("Question2.txt")

    i = i + 1

