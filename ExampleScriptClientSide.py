__author__ = 'fdemoullin'

# Example class for how to use the ServerInteracter interface
# All code on the Client-Side should use this interface to communicate with the server
# This abstracts networking details like sockets, ports, and TCP byte separation

import ServerInteracter

if ServerInteracter.callFunctionOnServer("printA"):
    print "Hurray, I executed printA() on the server"
if ServerInteracter.callFunctionOnServer("printB"):
    print "Hurray, I executed printB() on the server"