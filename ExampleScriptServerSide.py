__author__ = 'fdemoullin'

#import ServerRoutines

# Example of a script that runs on the server (like grading scrip for example)
# Define a bunch of functions here that are supposed to be initiated from a client, as well as helper functions that are not direcly called from client
# Put the functions that need to be called directly from client into the functionDictionary in the ServerOld.py file
# When the client requests a function to be executed, the request will pass through ServerInteracter, then through Server, then end up her

# example of a function, this function will be called directly from the client
def printA():
    print "A"
    return

def printB():
    print "B"
    return

def printMyOwnWords(pToBePrinted):
    print pToBePrinted
    return