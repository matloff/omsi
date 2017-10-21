
from Tkinter import *
from threading import Timer
import tkMessageBox
import tkFileDialog
import tkSimpleDialog
import os
import stat
import OmsiQuestion
import sys, subprocess
import filecmp
import time
import OmsiClient 

import pdb

# This is the GUI portion of the OMSI application.
class OmsiGui(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.parent = master
        self.QuestionsArr = []
        self.curqNum = -1
        self.widgets()
        self.host = None
        self.port = None
        self.email = None
        self.OmsiClient = None

    def donothing(self):
        filewin = Toplevel(self.parent)
        button = Button(filewin, text="Do nothing button")
        button.pack()

    # The action for when the open button is clicked in the file
    # menu. Not currently used. Probably should delete.
    def onOpen(self):
        ftypes = [('Python files', '*.py'), ('All files', '*')]
        dlg = tkFileDialog.Open(self, filetypes=ftypes)
        fl = dlg.show()
        if fl != '':
            f = open(fl, "r")
            text = f.read()
            self.txt.insert(END, text)

    def helloCallback(self):
        s = "This size is {0}".format(self.parent.winfo_height())
        tkMessageBox.showinfo("Hello Python", s)

    # Updates the question box with the question when a question
    # is clicked in the listbox
    def updateQuestionBox(self, qNum=None):
        if not self.QuestionsArr:
            return

        if self.curqNum == qNum:
            return
        self.question.config(state=NORMAL)

        self.question.delete("1.0", END)
        self.question.insert(END, self.QuestionsArr[qNum].getQuestion())
        self.question.config(state=DISABLED)


    # Updates the answer box when the question is clicked
    # in the listbox
    def updateAnswerBox(self, qNum=None):
        # qNum 0 refers to the description
        if not self.QuestionsArr:
            return

        if qNum == self.curqNum:
            return

        if self.curqNum > 0 and not qNum == 'cpyqtoa':
            self.QuestionsArr[self.curqNum]. \
               setAnswer(self.txt.get("1.0", END).encode('utf-8'))

        self.txt.delete("1.0", END)
        if qNum ==  'cpyqtoa': qNum = self.curqNum
        if not qNum == None and qNum > 0:
            self.txt.insert(END, self.QuestionsArr[qNum].getAnswer())
        self.curqNum = qNum

    # One of the items in the question list was clicked
    def listboxSelected(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        self.updateQuestionBox(index)
        self.updateAnswerBox(index)

    # The disconnect button was clicked.
    def disconnectFromServer(self):
        self.host = None
        self.port = None
        self.email = None
        self.cancel()

    # The user entered the server info and clicked connect.
    def enteredServerInfo(self):
        # Make sure all the info is valid.
        if not self.validate():
            self.hostEntry.focus_set()
            return

        # Create a connection and close the connection info box if 
        # successful.
        try:
            self.OmsiClient = \
               OmsiClient.OmsiClient(self.host, self.port, self.email)
            self.dBox.withdraw()
            self.dBox.update_idletasks()
            self.cancel()
        except ValueError as e:
            tkMessageBox.showwarning("Error", e)

    # The user canceled the connect to server box.
    def cancel(self, event=None):
        self.parent.focus_set()
        self.dBox.destroy()

    # This is run to auto save the current answer.
    def autoSave(self):
        t = Timer(120, self.autoSave)
        # Guy on stack overflow said this helps with
        # being able to end the main thread without complications
        t.daemon = True
        t.start()
        if self.curqNum > 0:
            self.saveAnswer(self.curqNum)

    def saveAllAnswers(self):
        for i in range(1, len(self.QuestionsArr)):
            self.saveAnswer(i)

    def saveAnswer(self, qNum=None):
        if not qNum:
            qNum = self.curqNum

        if qNum == 0:
            return

        # make sure what is in the array is the most up to date
        if qNum == self.curqNum:
            self.QuestionsArr[qNum].setAnswer(self.txt.get("1.0", END).
               encode('utf-8'))

        filename = "omsi_answer{0}{1}". \
           format(qNum, self.QuestionsArr[qNum].getFiletype())
        with open(filename, 'w') as f:
            st = os.stat(filename)
            os.chmod(filename, \
               st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            f.write(self.QuestionsArr[qNum].getAnswer())

    # function compile Program
    # compiles the program file with given flags
    # Shows result as a pop-up box
    def compileProgram(self, qNum = None):
        compiler = ""
        msg = ""  #records messeges
        
        if not qNum:
            qNum = self.curqNum

        fType = self.QuestionsArr[qNum].getFiletype()  # file type
        # name of the file to be compiled
        fName = "omsi_answer{0}{1}". \
           format(qNum, self.QuestionsArr[qNum].getFiletype()) 
        flags = self.QuestionsArr[qNum].getFlags() # get flags
        # flags = ["-"+x for x in flags] #adding "-" before flags

        compileProg = self.QuestionsArr[qNum].getCompileProgram()

        if compileProg == 'y':
        # selecting compiler
            '''if fType == ".c": # Removing hard coded compiler for C/C++
                compiler = "gcc"
            elif fType == ".cpp":
                compiler = "g++"
            else:'''
            compiler = self.QuestionsArr[qNum].getCompiler()

            execName = "omsi_answer{0}".format(qNum) # name of the executable

            if not os.path.isfile(fName):   #check if file exists
                msg = "File not found. Please make sure you have saved the file."
                tkMessageBox.showinfo("Error", msg)
                return False 
            infile = None  #for proc
            outfile = open("com_" + str(qNum), 'w') #for proc
            errfile = open("errfile", 'w')  #for proc

            # generating executable...
            startTime = time.time()  #start time
            print "Compiling with {0} {1} -o {2} {3}".format(compiler, ' '.join(flags), execName,fName)

            proc = subprocess.Popen([compiler] + flags + ["-o", execName, fName], stdin = infile, stdout = outfile, stderr = errfile, universal_newlines = True)
            errfile.close()
            outfile.close()
            while proc.poll() is None:  
                if time.time() - startTime >= 2:  #wait for process to finish 2 seconds for now
                    proc.kill()     #kill process if it is still running
                    msg = "\nExecutable could NOT be generated: Compile - Time Out.\n"
                    break
             
            retCode = proc.poll()
            if retCode is not None and retCode != 0:
                errfile = open ("errfile", "r")
                msg = "Executable could NOT be generated.\n" + "\n".join(errfile.readlines()) + "\n" #Show only 3 lines, error msg. might be too long
                errfile.close() #close error file
            else:
                outfile = open("com_" + str(qNum), 'r')
                msg = "\nExecutable generated successfully.\n" + "\n".join(outfile.readlines()) + "\n"
                outfile.close()
            os.remove("errfile") #errfile deleted...may be kept as a log if required
            os.remove("com_" + str(qNum))
        else:
            msg = "\nNot authorised!\n"
            tkMessageBox.showinfo("Compiler", msg)
            return False
        
        # display msg in pop-up box
        fileWin = Toplevel(self.parent)
        text = Text(fileWin)
        text.insert(END,msg)
        text.pack()

        return True
    
    # inserts the current contents of the question box into the answer
    # box
    def copyQtoA(self):
       qNum = self.curqNum
       currq = self.QuestionsArr[qNum].getQuestion()
       self.QuestionsArr[qNum]. \
               setAnswer(currq.encode('utf-8'))
       self.updateAnswerBox('cpyqtoa')
        
    def runProgram(self, qNum = None):       
        runCmd = ""
        msg = ""  #records messages
        
        if not qNum:
            qNum = self.curqNum

        runProg = self.QuestionsArr[qNum].getRunProgram()

        if runProg == 'y':
        #check if this program can be "run"
            fType = self.QuestionsArr[qNum].getFiletype()  #file type
            #name of the file to be compiled
            fName = "omsi_answer{0}{1}". \
               format(qNum, self.QuestionsArr[qNum].getFiletype()) 
            compileProg = self.QuestionsArr[qNum].getCompileProgram()
            
            if compileProg == 'y':
            #check if executable exists (if required)
                execName = "omsi_answer" + str(qNum)  #name of the executable    
                if not os.path.isfile(execName):   #check if file exists
                    msg = "Executable not found!\nPlease make sure you have compiled the program."
                    tkMessageBox.showinfo("Run", msg)
                    return False
            else:
            #check if file exists
                if not os.path.isfile(fName):   #check if file exists
                    msg = "File not found! Please make sure you have saved the file."
                    tkMessageBox.showinfo("Run", msg)
                    return False 

            infile = None  #for proc
            outfile = open("o_" + str(qNum), 'w') #for proc
            errfile = open("errfile", 'w')  #for proc

            runCmd = self.QuestionsArr[qNum].getRunCmd() #get the runCmd - in instructor questions.txt
            print runCmd
            startTime = time.time()  #start time
            proc = subprocess.Popen(runCmd, stdin = infile, stdout = outfile, stderr = errfile, universal_newlines = True)
            errfile.close()
            while proc.poll() is None:  
                if time.time() - startTime >= 2:  #wait for process to finish 2 seconds for now
                    proc.kill()     #kill process if it is still running
                    msg = "\nRun unsuccessful. Time Out.\n"
                    break
            outfile.close() 
            retCode = proc.poll()
            if retCode is not None and retCode != 0:
                errfile = open ("errfile", "r")
                msg = "Run unsuccessful.\n" + "\n".join(errfile.readlines()) + "\n" #Show only 3 lines, error msg. might be too long
                errfile.close() #close error file
            else:
            #output was created...display
                outfile = open("o_" + str(qNum), 'r')
                msg = "\nRun successful.\nOutput:\n" + "\n".join(outfile.readlines()) + "\n"
                outfile.close()
            os.remove("errfile") #errfile deleted...may be kept as a log if required
            os.remove("o_" + str(qNum)) #outputfile deleted...may be kept as a record if required
        else:
        # this question does not allow run
            msg = "\nNot authorised!\n"
            tkMessageBox.showinfo("Run", msg)
            return False

        # display msg in pop-up box
        fileWin = Toplevel(self.parent)
        text = Text(fileWin)
        text.insert(END,msg)
        text.pack()

        return True

    def submitAnswer(self, qNum=None):
        if not qNum:
            qNum = self.curqNum

        if qNum == 0:
            return

        if qNum == self.curqNum:
            self.QuestionsArr[qNum]. \
               setAnswer(self.txt.get("1.0",END).encode('utf-8'))
        self.saveAnswer(qNum)
        filename = "omsi_answer{0}{1}". \
           format(qNum,self.QuestionsArr[qNum].getFiletype())

        try:
            lServerResponse = self.OmsiClient.sendFileToServer(filename)
            print 'server response seen from submitAnswer():', lServerResponse
            tkMessageBox.showinfo("Submission Results", str(lServerResponse))
            self.OmsiClient.omsiSocket.close()
        except ValueError as e:
            tkMessageBox.showwarning("Error!", e)
            return

    def submitAllAnswers(self):
        for i in range(1, len(self.QuestionsArr)):
            self.submitAnswer(i)

    # makes a dialog window pop up asking for host port and email; makes
    # the connection; downloads and processes the exam questions
    def getConnectionInfo(self):

        # most of the code is making the connection; note, though, that
        # the actual connection is made getQuestionsFromServer(), called
        # hear the end here

        self.dBox = Toplevel(self.parent)
        self.dBox.transient(self.parent)

        body = Frame(self.dBox)
        self.hostEntry = Entry(body)
        self.portEntry = Entry(body)
        self.emailEntry = Entry(body)

        connected = "Not connected"
        if self.OmsiClient:
            connected = "Connected"

        if self.host:
            self.hostEntry.insert(0,self.host)
        if self.port:
            self.portEntry.insert(0,self.port)
        if self.email:
            self.emailEntry.insert(0,self.email)

        Label(body,text=connected).grid(row=0)
        Label(body, text="Host:").grid(row=1)
        Label(body, text="Port:").grid(row=2)
        Label(body, text="Student email:").grid(row=3)

        self.hostEntry.grid(row=1, column=1)
        self.portEntry.grid(row=2, column=1)
        self.emailEntry.grid(row=3, column=1)

        self.hostEntry.focus_set()
        body.pack()

        buttonBox = Frame(self.dBox)
        if not self.OmsiClient:
            ok = Button(buttonBox, text="Enter", 
               width=10, command=self.enteredServerInfo, default=ACTIVE)
            ok.pack(side=LEFT, padx=5, pady=5)
            cancel = Button(buttonBox, text="Cancel", 
               width=10, command=self.cancel)
            cancel.pack(side=RIGHT, padx=5, pady=5)

            # Bind enter and escape to respective methods
            self.dBox.bind("<Return>", self.enteredServerInfo)
            
        else:
            disconn = Button(buttonBox,text="Disconnect",
               width=10,command=self.disconnectFromServer)
            disconn.pack(padx=5,pady=5)

        self.dBox.bind("<Escape>", self.cancel)
        buttonBox.pack()

        self.dBox.grab_set()

        # Makes the X button call the cancel method
        self.dBox.protocol("WM_DELETE_WINDOW", self.cancel)

        # This blocks until the dialog box is closed
        self.dBox.wait_window(self.dBox)

        # If there was an error creating a client don't try
        # to get the questions.
        if not self.OmsiClient:
            return

        # now the exam questions etc.
        self.getVersion()
        self.getQuestionsFromServer()  # includes connect op
        self.loadQuestionsFromFile()

    def getVersion(self):
       v = open('VERSION')
       tmp = v.readline()
       print 'Version', tmp

    # downloads the exam questions from the server
    def getQuestionsFromServer(self):
        print 'downloading the exam questions'
        try:
            socket = self.OmsiClient.configureSocket()
            self.OmsiClient.getExamQuestionsFile(socket)
            print "closing socket"
            socket.close()
        except ValueError as e:
            tkMessageBox.showwarning("Error in downloading questions", e)
        return True

    # Ensures the info entered in the for the server is valid.
    def validate(self):
        try:
            self.host = self.hostEntry.get()
            self.port = int(self.portEntry.get())
            self.email = self.emailEntry.get()
            if not self.host or not self.port or not self.email:
                raise ValueError
            return 1
        except ValueError:
            tkMessageBox.showwarning(
                "Bad input", "Enter host, post and email!"
            )
            return 0

    # Parses the question file to separate questions.
    def loadQuestionsFromFile(self):
        import OmsiUtility
        self.QuestionsArr = OmsiUtility.ParseQuestions("ExamQuestions.txt")
        self.lb.delete(0, END)
        self.lb.insert(END, "Description")
        for i in range(1, len(self.QuestionsArr)):
            self.lb.insert(END, "Question {0}".format(i))
            filename = "omsi_answer{0}{1}". \
               format(i,self.QuestionsArr[i].getFiletype())
            if (os.path.isfile(filename)):
                with open(filename) as f:
                    st = ""
                    for line in f.readlines():
                        st += line
                    self.QuestionsArr[i].setAnswer(st)
            else:
                self.QuestionsArr[i]. \
                   setAnswer("Put your answer for question {0} here.".format(i))

        self.autoSave()

    def widgets(self):
        self.parent.title("Online Measurement of Student Insight")
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_columnconfigure(1, weight=6)
        self.parent.grid_rowconfigure(0, weight=1)
        menubar = Menu(self.parent)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=self.donothing)
        # filemenu.add_command(label="Open", command = self.onOpen)
        filemenu.add_command(label="Connect", command=self.getConnectionInfo)
        filemenu.add_command(label="Save", command=self.saveAnswer)
        filemenu.add_command(label="Save All", command=self.saveAllAnswers)
        filemenu.add_command(label="Submit", command=self.submitAnswer)
        filemenu.add_command(label="Submit All", command=self.submitAllAnswers)
        # filemenu.add_command(label="Close", command=self.donothing)
        filemenu.add_command(label="Compile", command=self.compileProgram)
        filemenu.add_command(label="Run", command=self.runProgram)
        filemenu.add_command(label="CopyQtoA", command=self.copyQtoA)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.parent.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=self.donothing)

        editmenu.add_separator()

        editmenu.add_command(label="Cut", command=self.donothing)
        editmenu.add_command(label="Copy", command=self.donothing)
        editmenu.add_command(label="Paste", command=self.donothing)
        editmenu.add_command(label="Delete", command=self.donothing)
        editmenu.add_command(label="Select All", command=self.donothing)

        menubar.add_cascade(label="Edit", menu=editmenu)

        self.parent.config(menu=menubar)

        self.questionFrame = Frame(self.parent, bg="ghost white")
        self.questionFrame.grid(row=0, column=0, sticky="nswe")

        self.lb = Listbox(self.questionFrame, width=20, bg="lavender")
        self.lb.insert(1, "Click on File to connect to server...")
        self.lb.bind('<<ListboxSelect>>', self.listboxSelected)

        self.lb.pack(fill=BOTH, expand=1, padx=5, pady=5)

        # Frame for the question and answer text boxes
        self.textFrame = Frame(self.parent, bg="azure")
        pWindow = PanedWindow(self.textFrame, orient=VERTICAL, bg="LightBlue1")

        self.textFrame.grid(row=0, column=1, sticky="nswe")
        # self.textFrame.grid_rowconfigure(0, weight=2)
        # self.textFrame.grid_rowconfigure(1, weight=2)
        # self.textFrame.grid_columnconfigure(0, weight=1)

        # Question frame (for question text and scrollbar widgets)
        qframe = Frame(pWindow, bd=0)
        # Question text box
        self.question = Text(qframe, bg="pale turquoise", font=("sans-serif", 20),wrap=WORD)
        self.question.config(state=DISABLED)
        # self.question.grid(row=0,sticky="nswe",padx=5,pady =5)
        qvscroll = Scrollbar(qframe, orient=VERTICAL, command=self.question.yview)
        self.question['yscroll'] = qvscroll.set
        qvscroll.pack(side="right", fill="y")
        self.question.pack(side="left", fill="both", expand=True)
        pWindow.add(qframe,sticky = "nwe")

        # Answer frame (for answer text and scrollbar widgets)
        aframe = Frame(pWindow, bd=0)
        # Answer text box
        self.txt = Text(aframe, bg="LightBlue2", font=("sans-serif", 16),wrap=WORD)
        avscroll = Scrollbar(aframe, orient=VERTICAL, command=self.txt.yview)
        self.txt['yscroll'] = avscroll.set
        avscroll.pack(side="right", fill="y")
        self.txt.pack(side="left", fill="both", expand=True)
        pWindow.add(aframe,sticky = "swe")
        # self.txt.grid(row=1,sticky="nswe",pa dx=5,pady=5)

        pWindow.pack(fill=BOTH, expand=1, pady=5)
        # self.loadQuestionsFromFile()


def main():
    top = Tk()
    top.geometry("{0}x{1}". \
       format(top.winfo_screenwidth(), top.winfo_screenheight()))
    top.update()
    # top.minsize(top.winfo_width(),top.winfo_height())
    app = OmsiGui(top)
    narg = len(sys.argv)
    if narg > 1:
       app.host = sys.argv[1]
       if narg >= 3:
          app.port = sys.argv[2]
          if narg == 4:
             app.email = sys.argv[3]

    top.mainloop()


if __name__ == '__main__':
    main()

# Had trouble downloading tkinter fixed by doing 
# brew install homebrew/dupes/tcl-tk
# brew uninstall python
# brew install python --with-brewed-tk
# 
#
