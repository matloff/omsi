__author__ = 'fdemoullin'

import sys

import ClientGlobals
import ClientRoutines
import ProcessMonitor
import NetworkMonitor



def main():
    # user inputs host, port number
    # socket and port hard-coded for now

    #lHost = raw_input("Please enter host name: ")
    #lPort = int(raw_input("Please enter port number: "))

    # prepare socket to connect to server
    ClientRoutines.configureSocket()

    # connect to server


    # create file to store test questions
    lQuestionsFile = ClientRoutines.receiveExamQuestionsFile(ClientGlobals.gHost)



    # connect to server to download questions

    # begin monitoring processes

    # begin monitoring network traffic

    # launch command line interface


if __name__ == '__main__':
    main()