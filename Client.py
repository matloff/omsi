import sys
import thread

import ClientGlobals
import ClientRoutines
import NetworkMonitor



def main():
    # user inputs host, port number
    # socket and port hard-coded for now

    #lHost = raw_input("Please enter host name: ")
    #lPort = int(raw_input("Please enter port number: "))

    # prepare socket to connect to server
    #ClientRoutines.configureSocket()

    # connect to server


    # store exam questions file from server on local machine
    #lQuestionsFile = ClientRoutines.receiveExamQuestionsFile(ClientGlobals.gHost)



    # connect to server to download questions

    # begin monitoring processes
    # TODO: Need some method by which professor can specify duration of test, frequency of process sampling
    # allow professor to set how frequently process information will be recorded
    lSamplingFrequency = int(raw_input('Please enter time spacing in seconds: '))

    # professor specifies duration of exam
    lExamDuration = int(raw_input('Please enter test time in minutes: '))

    # create thread to monitor processes on student machine for duration of exam
    thread.start_new_thread(ClientRoutines.monitorProcesses, (lSamplingFrequency, lExamDuration))

    # begin monitoring network traffic

    # launch command line interface
    x = 10


if __name__ == '__main__':
    main()