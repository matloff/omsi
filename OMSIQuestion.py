class OMSIQuestion:
	def __init__(self,question,number,filetype='.txt',flags=""):
		self.number = number
		self.filetype = filetype
		self.answer = "Write your answer here..."
		self.question = question
		self.flags = flags

	def getQuestion(self):
		return self.question

	def getAnswer(self):
		return self.answer

	def getFiletype(self):
		return self.filetype

	def getQuestionNumber(self):
		return self.number

	def setAnswer(self,ans):
		self.answer = ans

	def getFlags(self):
		return self.flags.split(" ")

