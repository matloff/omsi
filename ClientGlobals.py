import socket

gHost = socket.gethostbyname(socket.gethostname())
reversedDns = socket.gethostbyaddr(gHost)
gHost = reversedDns[0]
gPort = 5000

gStudentEmail = "fdemoullin@ucdavis.edu"
gStudentHomeDirectory = "StudentHomeDirectory"
