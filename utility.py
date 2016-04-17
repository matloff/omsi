#Utility tools for the application


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
				questions.append(question)
				question = ""
			elif 'QUESTION' in line:
				firstQuestion = True
				line = f.readline()
				while line and 'DESCRIPTION' not in line and 'QUESTION' not in line:
					question += line
					line = f.readline()
				questions.append(question)
				question = ""
			else:
				line = f.readline()
		return questions

