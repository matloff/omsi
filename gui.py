#Testing tkinter
from Tkinter import *
import tkMessageBox
import tkFileDialog
import pdb




class Example(Frame):

	def __init__(self,master):
		Frame.__init__(self,master)
		self.parent = master
		self.widgets()

	def donothing(self):
		filewin = Toplevel(self.parent)
		button = Button(filewin, text = "Do nothing button")
		button.pack()

	def onOpen(self):
		ftypes = [('Python files','*.py'),('All files','*')]
		dlg = tkFileDialog.Open(self,filetypes=ftypes)
		fl = dlg.show()
		if fl != '':
			f = open(fl,"r")
			text = f.read()
			self.txt.insert(END,text)

	def helloCallBack(self):
		s = "This size is {0}".format(self.parent.winfo_height())
		tkMessageBox.showinfo("Hello Python", s)

	def listboxSelected(self,evt):
		w = evt.widget
		index = int(w.curselection()[0])
		value = w.get(index)
		p= "You selected item {0}: {1}".format(index,value)
		print p

	def widgets(self):
		self.pack(fill=BOTH,expand=1)
		self.parent.title("GUI Testing")
		menubar = Menu(self.parent)
		filemenu = Menu(menubar, tearoff = 0)
		filemenu.add_command(label="New",command = self.donothing)
		filemenu.add_command(label="Open", command = self.onOpen)
		filemenu.add_command(label="Save", command=self.donothing)
		filemenu.add_command(label="Save as...", command=self.donothing)
		filemenu.add_command(label="Close", command=self.donothing)

		filemenu.add_separator()

		filemenu.add_command(label="Exit",command = self.parent.quit)
		menubar.add_cascade(label="File",menu=filemenu)

		editmenu = Menu(menubar, tearoff=0)
		editmenu.add_command(label="Undo", command = self.donothing)

		editmenu.add_separator()

		editmenu.add_command(label="Cut", command=self.donothing)
		editmenu.add_command(label="Copy", command=self.donothing)
		editmenu.add_command(label="Paste", command=self.donothing)
		editmenu.add_command(label="Delete", command=self.donothing)
		editmenu.add_command(label="Select All", command=self.donothing)

		menubar.add_cascade(label="Edit",menu=editmenu)

		self.parent.config(menu=menubar)
		
		

		questionFrame = Frame(self.parent,bg="red")
		questionFrame.pack(side=LEFT,fill=Y)

		btn = Button(questionFrame,text="hi",command=self.helloCallBack)
		btn.pack()
		lb = Listbox(questionFrame,bg="blue",width=20,height=30)
		lb.insert(1,"Question 1")
		lb.insert(2,"Question 2")
		lb.insert(3,"Question 3")
		lb.insert(4,"Question 4")
		lb.bind('<<ListboxSelect>>',self.listboxSelected)

		lb.pack(side=LEFT)

		textFrame = Frame(self.parent,bg="blue")
		textFrame.pack(side=RIGHT,fill=BOTH)
		self.txt = Text(textFrame)
		self.txt.pack(fill=BOTH,expand=1)

def main():
	top = Tk()
	app  =  Example(top)
	top.geometry("400x600")
	top.mainloop()

if __name__ == '__main__':
	main()