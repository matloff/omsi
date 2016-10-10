#Utility tools for the application
from OmsiQuestion import *
import pdb
import shlex

#Will return an array of OMSIQuestion objects
def ParseQuestions(filename):
	with open(filename,'r') as f:
		foundDescription = False
		firstQuestion = False

		question = ""
		questions = []
		line = f.readline()
		while line:
			if 'DESCRIPTION' in line:
				foundDescription = True
				line = f.readline()
				while line and 'DESCRIPTION' not in line and 'QUESTION' not in line:
					question += line
					line = f.readline()
				q = OmsiQuestion(question,0)
				questions.append(q)
				question = ""
			elif 'QUESTION' in line:
				firstQuestion = True
				
				filetype = '.txt'
				flags = ""
				words = shlex.split(line)
				compileProgram = "n" 
				compiler = ""
				runProgram = "n"
				runCmd = ""

				for i in range(len(words)):
					if words[i] == '-ext':
						if i+1 >= len(words):
							print("Error! Unexpected end of arguments...")
						else:
							print("Setting type to {0}".format(words[i+1]))
							filetype = words[i+1]
						i+= 1
					if words[i] == '-flags':
						if i+1 >= len(words):
							print("Error! Unexpected end of arguments...")
						else:
							fl = words[i+1]
							print("Setting flags to {0}".format(fl))
							flags = fl
					if words[i] == '-com':  #check if question can be compiled
						if i+1 >= len(words):
							print("Error! Unexpected end of arguments...")
						else:
							com = words[i+1]
							print("Setting compiler option to {0}".format(com))
							compileProgram = 'y'
							compiler = com
					if words[i] == '-run':  #check if question can be run
						if i+1 >= len(words):
							print("Error! Unexpected end of arguments...")
						else:
							runCmd = words[i+1]
							runProgram = 'y'
							print("Setting run-command option to {0}".format(runCmd))
							runCmd = runCmd



				line = f.readline()
				while line and 'DESCRIPTION' not in line and 'QUESTION' not in line:
					question += line
					line = f.readline()
				q = OmsiQuestion(question,len(questions),filetype,flags, compileProgram, compiler, runProgram, runCmd) 
				questions.append(q)
				question = ""
			else:
				line = f.readline()
		return questions

