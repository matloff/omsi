__author__ = 'fdemoullin'

import sys
import os
import Server

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
    lQuestionFile = openFile(lNewHomeDirectory)

    return lQuestionFile

# creates a folder for each student that connects to the server
# there is an issue still when a student connects twice, 2 different folders are created right now
# We need student ID or somthing like that
def startUpRoutineStudent(pQuestionFile, pFirstName, pLastName):
    #create name for folder which is composed of sys.path (gloable in Server), last name and then first name
    lIdealPathName = Server.gServerHomeDirectory + pLastName + pFirstName
    # create new folder
    if not os.path.exists():
        os.makedirs(lIdealPathName)
    else:
        # TODO: find a solution for this issue
        # either 2 students have the same name (fist and last name), or the students connected twice (because they want to get the questions again or for whatever reason)
        print 'Error: the file path already exists on the server'
        startUpRoutineStudent(pQuestionFile, pFirstName, pLastName, 0) # this is a terrible solution
    sendQuestionsToStudent()

# overloading the startUpRoutingStudent
# this function is only ever called from within this module
# this function should resolve the issue when two students have the same name by adding a different folder and appending a suffix
# TODO: find a better solution to this problem
def startUpRoutineStudent(pQuestionFile, pFirstName, pLastName, pSuffix):
    #create name for folder which is composed of sys.path, last name and then first name
    lIdealPathName = sys.path + pLastName + pFirstName + pSuffix
    # create new folder
    if not os.path.exists():
        os.makedirs(lIdealPathName)
    else:
        # either 2 students have the same name (fist and last name), or the students connected twice (because they want to get the questions again or for whatever reason)
        print 'Error: the file path already exists on the server'
        startUpRoutineStudent(pQuestionFile, pFirstName, pLastName, pSuffix + 1)
    return sendQuestionsToStudent()

def sendQuestionsToStudent():
    #launch the transfer of the questions file from the server to the client
    return "file"

# tries to open the question file
# returns the question file if it is found
# re-runs startUpRoutineProfessor if it fails
def openFile(pNewHomeDirectory):
    try:
      lOpenFile = os.path.join(pNewHomeDirectory, 'Questions.txt')
      return lOpenFile
    except IOError:
      print "Error: File does not appear to exist, create a file called 'Questions.txt' and make sure you store it in the specified directory."
      # try again
      startUpRoutineProfessor()



