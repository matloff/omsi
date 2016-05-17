# Testing tkinter
import ClientGlobals
import ClientRoutines
from Tkinter import *
from threading import Timer
import tkMessageBox
import tkFileDialog
import tkSimpleDialog
import pdb
import os
import stat
import OMSIQuestion
import sys, subprocess
import filecmp
import time


class Example(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.parent = master
        self.QuestionsArr = []
        self.curqNum = -1
        self.widgets()
        self.host = None
        self.port = None
        self.email = None

    def donothing(self):
        filewin = Toplevel(self.parent)
        button = Button(filewin, text="Do nothing button")
        button.pack()

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
        # pdb.set_trace()
        if not self.QuestionsArr:
            return

        if self.curqNum == qNum:
            return
        self.question.delete("1.0", END)
        self.question.insert(END, self.QuestionsArr[qNum].getQuestion())

    # Updates the answer box when the question is clicked
    # in the listbox
    def updateAnswerBox(self, qNum=None):
        # qNum 0 refers to the description
        if not self.QuestionsArr:
            return

        if qNum == self.curqNum:
            return

        if self.curqNum > 0:
            self.QuestionsArr[self.curqNum].setAnswer(self.txt.get("1.0", END).encode('utf-8'))

        self.txt.delete("1.0", END)
        if not qNum == None and qNum > 0:
            self.txt.insert(END, self.QuestionsArr[qNum].getAnswer())
        self.curqNum = qNum

    def listboxSelected(self, evt):
        w = evt.widget
        index = int(w.curselection()[0])
        value = w.get(index)
        self.updateQuestionBox(index)
        self.updateAnswerBox(index)

    def disconnectFromServer(self):
        self.host = None
        self.port = None
        self.email = None
        self.cancel()

    def enteredServerInfo(self):
        if not self.validate():
            self.hostEntry.focus_set()
            return

        self.dBox.withdraw()
        self.dBox.update_idletasks()

        self.cancel()

    def cancel(self, event=None):
        self.parent.focus_set()
        self.dBox.destroy()

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

        #Make sure what is in the array is the most up to date
        if qNum == self.curqNum:
            self.QuestionsArr[qNum].setAnswer( self.txt.get("1.0", END).encode('utf-8'))

        filename = "omsi_answer{0}{1}".format(qNum, self.QuestionsArr[qNum].getFiletype())
        with open(filename, 'w') as f:
            st = os.stat(filename)
            os.chmod(filename,st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
            f.write(self.QuestionsArr[qNum].getAnswer())

#function compile Program
#compiles the program file with given flags
#Shows result as a pop-up box
    def compileProgram(self, qNum = None):
        compiler = ""
        msg = ""  #records messeges
        
        if not qNum:
            qNum = self.curqNum

        fType = self.QuestionsArr[qNum].getFiletype()  #file type
        fName = "omsi_answer{0}{1}".format(qNum, self.QuestionsArr[qNum].getFiletype()) #name of the file to be compiled
        flags = self.QuestionsArr[qNum].getFlags() #get flags
        flags = ["-"+x for x in flags] #adding "-" before flags

        #selecting compiler
        if fType == ".c":
            compiler = "gcc"
        elif fType == ".cpp":
            compiler = "g++"

        execName = "omsi_answer" + str(qNum)  #name of the executable

        if not os.path.isfile(fName):   #check if file exists
            msg = "File not found!"
            tkMessageBox.showinfo("Error", msg)
            return False 

        
        infile = None  #for proc
        outfile = None #for proc
        errfile = open("errfile", 'w')  #for proc

        print [compiler] + flags + ["-o", execName, fName]
        #generating executable...
        startTime = time.time()  #start time
        proc = subprocess.Popen([compiler] + flags + ["-o", execName, fName], stdin = infile, stdout = outfile, stderr = errfile, universal_newlines = True)
        errfile.close()
        while proc.poll() is None:  
            if time.time() - startTime >= 2:  #wait for process to finish 2 seconds for now
                proc.kill()     #kill process if it is still running
                msg = "\nExecutable could NOT be genarated: Compile - Time Out.\n"
                break
         
        retCode = proc.poll()
        if retCode is not None and retCode != 0:
            errfile = open ("errfile", "r")
            msg = "Executable could NOT be genarated.\n" + "\n".join(errfile.readlines()[:3]) + "\n" #Show only 3 lines, error msg. might be too long
            errfile.close() #close error file
            os.remove("errfile") #errfile deleted...may be kept as a log if required
        else:
            msg = "\nExecutable generated successfully.\n"
        
        tkMessageBox.showinfo("Compiler", msg)
        return True


    def submitAnswer(self, qNum=None):
        if not qNum:
            qNum = self.curqNum

        if qNum == 0:
            return

        if qNum == self.curqNum:
            # self.answersArr[qNum - 1] = self.txt.get("1.0", END).encode('utf-8')
            self.QuestionsArr[qNum].setAnswer(self.txt.get("1.0",END).encode('utf-8'))

        self.saveAnswer(qNum)

        filename = "omsi_answer{0}{1}".format(qNum,self.QuestionsArr[qNum].getFiletype())

        lServerResponse = ClientRoutines.sendFileToServer(filename)

        tkMessageBox.showinfo("Submission Results", str(lServerResponse))

    def submitAllAnswers(self):
        for i in range(1, self.QuestionsArr):
            self.submitAnswer(i)

    # Makes a dialog window pop up asking for host port and email
    def getConnectionInfo(self):
        self.dBox = Toplevel(self.parent)
        self.dBox.transient(self.parent)

        body = Frame(self.dBox)
        self.hostEntry = Entry(body)
        self.portEntry = Entry(body)
        self.emailEntry = Entry(body)


        connected = "Not connected"
        if self.host:
            connected = "Connected"
            self.hostEntry.insert(0,self.host)
            self.portEntry.insert(0,self.port)
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
        if not self.host:
            ok = Button(buttonBox, text="Enter", width=10, command=self.enteredServerInfo, default=ACTIVE)
            ok.pack(side=LEFT, padx=5, pady=5)
            cancel = Button(buttonBox, text="Cancel", width=10, command=self.cancel)
            cancel.pack(side=RIGHT, padx=5, pady=5)

            # Bind enter and escape to respective methods
            self.dBox.bind("<Return>", self.enteredServerInfo)
            
        else:
            disconn = Button(buttonBox,text="Disconnect",width=10,command=self.disconnectFromServer)
            disconn.pack(padx=5,pady=5)

        self.dBox.bind("<Escape>", self.cancel)
        buttonBox.pack()

        self.dBox.grab_set()

        # Makes the X button call the cancel method
        self.dBox.protocol("WM_DELETE_WINDOW", self.cancel)

        # This blocks until the dialog box is closed
        self.dBox.wait_window(self.dBox)
        if not self.connectToServer():
        	return
        self.getQuestions()

    def connectToServer(self):
        ClientGlobals.gHost = self.host
        ClientGlobals.gPort = self.port
        ClientGlobals.gStudentEmail = self.email

        # prepare socket to connect to server
        result = ClientRoutines.configureSocket()

        if not result[0]:
            tkMessageBox.showwarning("Error",result[1])
            return False

        lSocket = result[1]

        # store exam questions file from server on local machine
        result = ClientRoutines.receiveExamQuestionsFile(lSocket)
        if not result[0]:
            tkMessageBox.showinfo("Error", result[1])
            return False

        return True

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

    def getQuestions(self):
        import utility
        self.QuestionsArr = utility.ParseQuestions("ExamQuestions.txt")
        self.lb.delete(0, END)
        self.lb.insert(END, "Description")
        for i in range(1, len(self.QuestionsArr)):
            self.lb.insert(END, "Question {0}".format(i))
            filename = "omsi_answer{0}{1}".format(i,self.QuestionsArr[i].getFiletype())
            if (os.path.isfile(filename)):
                with open(filename) as f:
                    st = ""
                    for line in f.readlines():
                        st += line
                    self.QuestionsArr[i].setAnswer(st)
            else:
                self.QuestionsArr[i].setAnswer("Put your answer for question {0} here.".format(i))

        self.autoSave()

    def widgets(self):
        self.parent.title("GUI Testing")
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

        # btn = Button(self.questionFrame,text="hi",command=self.helloCalself.lback)
        # btn.pack()
        self.lb = Listbox(self.questionFrame, width=20, bg="lavender")
        self.lb.insert(1, "Connect to server to get quesions...")
        self.lb.bind('<<ListboxSelect>>', self.listboxSelected)

        self.lb.pack(fill=BOTH, expand=1, padx=5, pady=5)
        # pdb.set_trace()

        # Frame for the question and answer text boxes
        self.textFrame = Frame(self.parent, bg="azure")
        pWindow = PanedWindow(self.textFrame, orient=VERTICAL, bg="LightBlue1")


        self.textFrame.grid(row=0, column=1, sticky="nswe")
        # self.textFrame.grid_rowconfigure(0, weight=2)
        # self.textFrame.grid_rowconfigure(1, weight=2)
        # self.textFrame.grid_columnconfigure(0, weight=1)

        # Question text box
        self.question = Text(pWindow, bg="pale turquoise", font=("sans-serif", 20))
        pWindow.add(self.question,sticky = "nwe")
        self.question.config(state=DISABLED)
        # self.question.grid(row=0,sticky="nswe",padx=5,pady =5)

        # Answer text box
        self.txt = Text(pWindow, bg="LightBlue2", font=("sans-serif", 16))
        pWindow.add(self.txt,sticky = "swe")
        # self.txt.grid(row=1,sticky="nswe",pa dx=5,pady=5)
        pWindow.pack(fill=BOTH, expand=1, pady=5)


def main():
    top = Tk()
    top.geometry("{0}x{1}".format(top.winfo_screenwidth(), top.winfo_screenheight()))
    top.update()
    # top.minsize(top.winfo_width(),top.winfo_height())
    app = Example(top)

    top.mainloop()


if __name__ == '__main__':
    main()
