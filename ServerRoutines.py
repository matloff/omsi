
import Server
import os

# creates a folder for each student that connects to the server
# sends the questions file to the student
def startUpRoutineStudent(pStudentEmail):
    #create name for folder which is composed of sys.path (gloable in Server), last name and then first name
    lIdealPathName = Server.gServerHomeDirectory + pStudentEmail
    # create new folder
    if not os.path.exists(lIdealPathName):
        os.makedirs(lIdealPathName)
    # initiate the questions to be sent to the student. Done in Server.py, based on socket
    return "file"

# Lets professor specify a home directory for the entire application
# returns the question file for the exam
def startUpRoutineProfessor():
    print('Please enter a home directory for the application.')
    print("This will be the directory that all students' files will be stored in")
    print("Please store the exam questions in the directory and name that file 'Questions.txt'")

    #get the new path, we assume the prof is capable of getting it right
    lNewHomeDirectory = raw_input()
    #change system path was not generally supported on Slack, this is a workaround
    Server.gServerHomeDirectory = lNewHomeDirectory

    # open the QuestionFile
    lQuestionFilePath = openFile(lNewHomeDirectory)

    return lQuestionFilePath

# tries to open the question file
# returns the question file if it is found
# re-runs startUpRoutineProfessor if it fails
def openFile(pNewHomeDirectory):
    try:
      lFilePath = os.path.join(pNewHomeDirectory, 'Questions.txt')
      lOpenFile = open(lFilePath, 'r')

      # test to make sure we can open the file, if this failes, an IOException will be thrown
      lTest = lOpenFile.readline()
      lOpenFile.close()
      return lFilePath

    except IOError:
      print "Error: File does not appear to exist, create a file called 'Questions.txt' and make sure you store it in the specified directory."
      # try again
      startUpRoutineProfessor()



