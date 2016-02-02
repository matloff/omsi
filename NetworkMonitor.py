import datetime
import socket

# TODO: do we need to parse packets? what info should we save?

def collectPackets(pEndTime):

    # open file to store network traffic information
    lOutputFile = open('traffic-' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '.txt', 'w')

    #create an INET, raw socket
    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

    # collect network traffic from student's machine
    while datetime.datetime.now() < pEndTime:
        print s.recvfrom(65565)

    lOutputFile.close()

    return lOutputFile
