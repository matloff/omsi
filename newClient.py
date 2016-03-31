import sys
import os
import time
import re
from threading import Thread

import ClientGlobals
import ClientRoutines

def main():
    # user inputs host, port number
    # socket and port hard-coded for now

    #ClientGlobals.gHost = '168.150.21.93' #raw_input("Please enter host address: ")
    #ClientGlobals.gPort = int(raw_input("Please enter port number: "))

    # prepare socket to connect to server
    # lSocket = ClientRoutines.configureSocket()

    # store exam questions file from server on local machine
    # TODO: figure out why this appends an f at the very end of the questions file on the Client side
    # lQuestionsFile = ClientRoutines.receiveExamQuestionsFile(lSocket)


    # begin monitoring processes
    # TODO: Need some method by which professor can specify duration of test, frequency of process sampling
    # allow professor to set how frequently process information will be recorded
    lSamplingFrequency = 10#int(raw_input('Please enter time spacing in seconds: '))

    # professor specifies duration of exam
    lExamDuration = 1#int(raw_input('Please enter test time in minutes: '))

    # TODO: determine whether we want one submission, or multiple submissions
    # create thread to monitor processes on student machine for duration of exam
    # Thread(target=ClientRoutines.monitorProcesses, args=(lSamplingFrequency, lExamDuration)).start()

    # begin monitoring network traffic
    # Thread(target=ClientRoutines.monitorNetworkTraffic, args=(lExamDuration)).start()

    # launch command line interface
    x = 10


    fName = os.path.expanduser("~/.vimrc")
    path = os.getcwd() + "/vimtest.vim"


    f = open(fName,'r+')

    command = "nmap ;loadomsi :source " + path + "<CR>"

    lineFound = False
    
    for line in f:
        if re.match(command, line):
            lineFound = True
            break

    if not lineFound:
        command = "nmap ;loadomsi :source " + path + "<CR>\n"
        f.write(command)
        f.flush()
        f.close

    raw_input("\n\nGetting ready to launch vim. Once vim is launched type the command ';loadomsi' to begin. Press enter to continue...\n")

    os.system("vim")


if __name__ == '__main__':
    main()

