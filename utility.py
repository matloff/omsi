#Utility tools for the application
from OMSIQuestion import *
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
				q = OMSIQuestion(question,0)
				questions.append(q)
				question = ""
			elif 'QUESTION' in line:
				firstQuestion = True
				
				filetype = '.txt'
				flags = ""
				words = shlex.split(line)

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


				line = f.readline()
				while line and 'DESCRIPTION' not in line and 'QUESTION' not in line:
					question += line
					line = f.readline()
				q = OMSIQuestion(question,len(questions),filetype,flags) 
				questions.append(q)
				question = ""
			else:
				line = f.readline()
		return questions

