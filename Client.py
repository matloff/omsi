__author__ = 'fdemoullin'

import socket
import sys
import ProcessMonitor
import NetworkMonitor
import ClientRoutines


def main():
    # user inputs host, port number
    # socket and port hard-coded for now
    lPort = 20500
    lPort = socket.gethostname()
    #lHost = raw_input("Please enter host name: ")
    #lPort = int(raw_input("Please enter port number: "))

    # create file to store test questions
    lQuestionsFile = ClientRoutines.receiveExamQuestionsFile()



    # connect to server to download questions

    # begin monitoring processes

    # begin monitoring network traffic

    # launch command line interface


if __name__ == '__main__':
    main()