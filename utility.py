#Utility tools for the application
from OMSIQuestion import *
import pdb

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
				words = line.split()

				for i in range(len(words)):
					if words[i] == '-ext':
						if i+1 >= len(words):
							print("Error! Unexpected end of arguments...")
						else:
							print("Setting type to {0}".format(words[i+1]))
							filetype = words[i+1]
						i+= 1

				line = f.readline()
				while line and 'DESCRIPTION' not in line and 'QUESTION' not in line:
					question += line
					line = f.readline()
				q = OMSIQuestion(question,len(questions),filetype) 
				questions.append(q)
				question = ""
			else:
				line = f.readline()
		return questions

