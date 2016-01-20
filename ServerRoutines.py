
import Server
import os

# for each student that connects to the server, create a folder
# send file containing test questions to the student
def startUpRoutineStudent(pStudentEmail):

    # create folder name as sys.path (global in Server) + email
    lIdealPathName = Server.gServerHomeDirectory + pStudentEmail

    # create folder
    if not os.path.exists(lIdealPathName):
        os.makedirs(lIdealPathName)

    # initiate the questions to be sent to the student. Done in Server.py, based on socket
    return "file"



# asks professor to specify directory to store exam questions and student submissions
# confirms that the exam questions file is in the directory, returns path of file
def startUpExamDirectory():

    lExamQuestionsFilePath = False

    while not lExamQuestionsFilePath:
        print 'Please enter a home directory for the exam. This will be the directory that all students\' files will ' \
              'be stored in.\nBefore pressing enter, please check that the exam questions are in the directory and ' \
              'named \'Questions.txt\'.'

        # professor enters directory path
        # hard coded for testing on Rylan's machine
        #Server.gServerHomeDirectory = raw_input()
        Server.gServerExamDirectory = "/home/rylan/Documents/omsi/professorFileDirectory/"

        # confirm that exam questions file containing test questions
        lExamQuestionsFilePath = verifyExamQuestionsFile(Server.gServerExamDirectory)

        print lExamQuestionsFilePath

    return lExamQuestionsFilePath


# verify that specified directory contains exam questions file, returns file path
# if file not found or not readable, print error message and return false
def verifyExamQuestionsFile(pExamDirectory):

    # return path of exam questions file
    try:
        lExamQuestionsFilePath = os.path.join(pExamDirectory, 'Questions.txt')
        lOpenFile = open(lExamQuestionsFilePath, 'r')
        lOpenFile.close()
        return lExamQuestionsFilePath

    # if attempt to open file fails, print error and return false
    except IOError:
        print 'Error: File does not exist or is not readable. Please check that the specified path is spelled ' \
              'correctly and a file named \'Questions.txt\' is in the specified directory.'
        return False



