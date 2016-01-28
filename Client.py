import sys
from threading import Thread

import ClientGlobals
import ClientRoutines

def main():
    # user inputs host, port number
    # socket and port hard-coded for now

    #lHost = raw_input("Please enter host name: ")
    #lPort = int(raw_input("Please enter port number: "))

    # prepare socket to connect to server
    lSocket = ClientRoutines.configureSocket()

    # connect to server to download questions


    # store exam questions file from server on local machine
    lQuestionsFile = ClientRoutines.receiveExamQuestionsFile(lSocket)


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


if __name__ == '__main__':
    main()