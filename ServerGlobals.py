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
gHOST = ""
gPORT = 20500 #int(sys.argv[1])

gServerExamDirectory = ""
gExamQuestionsFilePath = ""

# variable to track number of currently connected clients
gNumCurrentClients = 0

# set up a lock to guard gNumCurrentClients
gNumCurrentClientsLock = thread.allocate_lock()