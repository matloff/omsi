__author__ = 'fdemoullin'

# Example class for how to use the Client interface
# All code on the Client-side should use this interface to communicate with the server
# This abstracts networking details like sockets, ports, and TCP byte separation

import Client


if Client.callFunctionOnServer("startUpRoutineStudent(fdemoullin@gmail.com)"):
    print "Question File was received"
if Client.sendFileToServer("ClientInputTest.txt"):
    print "As far as the client is concerned: File seems to have been sent."

