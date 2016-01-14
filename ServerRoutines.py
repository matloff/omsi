
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



# requests professor select which directory to store test questions, student submissions
# return path of file containing test questions
def startUpRoutineProfessor():

    lQuestionFilePath = 1

    while(lQuestionFilePath):
        print('Please enter a home directory for the application.')
        print("This will be the directory that all students' files will be stored in.")
        print("Before pressing enter, check that the exam questions are in the directory and named 'Questions.txt'.")

        # professor enters directory path
        Server.gServerHomeDirectory = raw_input()

        # attempt to open file containing test questions
        lQuestionFilePath = openFile(Server.gServerHomeDirectory)

    return lQuestionFilePath


# if file found, return file path
# if file not found, print error message and return
def openFile(pNewHomeDirectory):

    # test to make sure file can be read
    # if this fails, IOError will be thrown
    try:
      lFilePath = os.path.join(pNewHomeDirectory, 'Questions.txt')
      lOpenFile = open(lFilePath, 'r')
      lTest = lOpenFile.readline()
      lOpenFile.close()
      return lFilePath

    except IOError:
      print "Error: File does not appear to exist."
      print "Please check that the specified path is spelled correctly and a file named 'Questions.txt' " \
            "is in the specified directory."
      return 1



