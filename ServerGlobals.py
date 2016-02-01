import thread

import ExampleScriptServerSide

# dictionary to associate the function name with the function first class object
gFunctionDictionary = {
    'printA': ExampleScriptServerSide.printA,
    'printB': ExampleScriptServerSide.printB,
    'printMyOwnWords': ExampleScriptServerSide.printMyOwnWords,
    #'createStudentSubmissionDir': createStudentSubmissionDir,
}

# associate the socket with a port
# can leave this blank on the server side
gHost = ""
gPort = 20500

gServerExamDirectory = ""
gExamQuestionsFilePath = ""

# variable to track number of currently connected clients
gNumCurrentClients = 0

# lock to guard gNumCurrentClients
gNumCurrentClientsLock = thread.allocate_lock()

# variable to track number of total client connections
gNumTotalClients = 0

# lock to guard gNumTotalClients
gNumTotalClientsLock = thread.allocate_lock()