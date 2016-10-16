class OmsiQuestion:
    def __init__(self,question,number,filetype='.txt',flags="", compileProgram = "", compiler = "", runProgram = "", runCmd = ""):
        self.number = number
        self.filetype = filetype
        self.answer = "Write your answer here..."
        self.question = question
        self.flags = flags
        self.compileProgram = compileProgram
        self.runProgram = runProgram
        self.runCmd = runCmd
    
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
    
    def getCompileProgram(self):
        return self.compileProgram
    
    def getCompiler(self):
        return self.compiler
    
    def getRunProgram(self):
        return self.runProgram
    
    def getRunCmd(self):
        return self.runCmd.split(" ")#added split