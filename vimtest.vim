

function! VimCheatSheet()

if winnr('$') > 1
    hide
endif

:b 1

endfunction

function! HelpCheatSheet()

if winnr('$') > 1
    hide
endif

:b 2

endfunction

function! CompileRun()
python << endpython

print("This will compile and run the code")

endpython
endfunction

function! Evaluate()

python << endpython

print (vim.eval("g:serverName"))
print("This will evaluate the function?")

endpython
endfunction

function! Save()
w
python << endpython
import ClientRoutines
fName = vim.eval("bufname('%')")
ClientRoutines.sendFileToServer(fName)
print("Saving file {0}...".format(fName) )

endpython
endfunction

function! SaveAll()
wa
python << endpython
import ClientRoutines
import re

count = int(vim.eval("bufnr('$')"))

for i in range(2,count+1):
    name = "bufname({0})".format(i)
    if re.match(r"answer\d+\.[a-zA-Z]+$", vim.eval(name)):
        ClientRoutines.sendFileToServer(vim.eval(name))


print("This will save all buffers")

endpython
endfunction

function! Connect()
python << endpython

print ("Attempting to connect to {0} at port {1}".format(vim.eval("g:serverName"),vim.eval("g:port")))

import Client
import ClientGlobals
ClientGlobals.gHost = vim.eval("g:serverName")
ClientGlobals.gPort = int(vim.eval("g:port"))
ClientGlobals.gStudentEmail = vim.eval("g:studentEmail")
Client.main()

endpython
endfunction

function! GetCheatSheetBuffers()
edit vimCheatSheet.txt
badd examCheatSheet.txt
ls

endfunction

function! ParseQuestions()
python << endpython

fileName = vim.eval("g:questionsFileName")

f = open(fileName,'r')
firstQuestion = False
question = ""
questions = []
for line in f:
    if 'QUESTION' in line:
        if firstQuestion:
            questions.append(question)
        else:
            firstQuestion = True
        question = ""
    else:
        question += line +"\n"

questions.append(question)
count = 1
for q in questions:
    fName = "question{0}.txt".format(count)
    f = open(fName,'w')
    f.write(q)
    f.close()
    answerFile = "answer{0}.txt".format(count)
    f = open(answerFile,'w')
    f.close()
    command = "execute 'nmap ;;q{0} :call ChangeQuestions({1})<CR>'".format(count,count)
    vim.command(command)
    count+=1


endpython
endfunction

function! HideQuestion()
    wincmd k
    hide
endfunction

function! ShowQuestion()
python  << endpython
import re
fName = vim.eval("bufname('%')")
print fName
match = re.match("[a-zA-Z]+(\d+)\.", fName)
num = 1
if match:
    num = int(match.group(1))
command = ":call ChangeQuestions({0})".format(num)
vim.command(command)

endpython
endfunction

function! ChangeQuestions(number)
let a:fName =  "answer".a:number.".txt"
let a:qName = "question".a:number.".txt"
if winnr('$') > 1
    hide
endif
execute 'edit' a:fName
execute 'split' a:qName
wincmd j

endfunction


:nmap ;;vim :call VimCheatSheet()<CR>
:nmap ;;help :call HelpCheatSheet()<CR>
:nmap ;;rn :call CompileRun()<CR>
:nmap ;;eval :call Evaluate()<CR>
:nmap ;;sv :call Save()<CR>
:nmap ;;sva :call SaveAll()<CR>
:nmap ;;hide :call HideQuestion()<CR>
:nmap ;;show :call ShowQuestion()<CR>

edit intro.txt
python << endpython
import vim
import sys
import os


intro = """Welcome to 

         _______                   _____                    _____                    _____          
        /::\    \                 /\    \                  /\    \                  /\    \         
       /::::\    \               /::\____\                /::\    \                /::\    \        
      /::::::\    \             /::::|   |               /::::\    \               \:::\    \       
     /::::::::\    \           /:::::|   |              /::::::\    \               \:::\    \      
    /:::/~~\:::\    \         /::::::|   |             /:::/\:::\    \               \:::\    \     
   /:::/    \:::\    \       /:::/|::|   |            /:::/__\:::\    \               \:::\    \    
  /:::/    / \:::\    \     /:::/ |::|   |            \:::\   \:::\    \              /::::\    \   
 /:::/____/   \:::\____\   /:::/  |::|___|______    ___\:::\   \:::\    \    ____    /::::::\    \  
|:::|    |     |:::|    | /:::/   |::::::::\    \  /\   \:::\   \:::\    \  /\   \  /:::/\:::\    \ 
|:::|____|     |:::|    |/:::/    |:::::::::\____\/::\   \:::\   \:::\____\/::\   \/:::/  \:::\____\  \n
\ \:::\    \   /:::/    / \::/    / ~~~~~/:::/    /\:::\   \:::\   \::/    /\:::\  /:::/    \::/    /\n
\  \:::\    \ /:::/    /   \/____/      /:::/    /  \:::\   \:::\   \/____/  \:::\/:::/    / \/____/  \n
\   \:::\    /:::/    /                /:::/    /    \:::\   \:::\    \       \::::::/    /           \n
\    \:::\__/:::/    /                /:::/    /      \:::\   \:::\____\       \::::/____/            \n
\     \::::::::/    /                /:::/    /        \:::\  /:::/    /        \:::\    \            \n
\      \::::::/    /                /:::/    /          \:::\/:::/    /          \:::\    \           \n
\       \::::/    /                /:::/    /            \::::::/    /            \:::\    \          \n
\        \::/____/                /:::/    /              \::::/    /              \:::\____\         \n
\         ~~                      \::/    /                \::/    /                \::/    /         \n
\                                  \/____/                  \/____/                  \/____/         
                                                                                                    

                                        

The best online testing suite youll ever see broham mc bo!!"""

vim.command("let g:dummy = input('Press enter to continue...\n')")



vim.command('call inputsave()')
while True:
    vim.command("let g:studentEmail = input('Enter your student email: ')")
    s = "'You entered \"" + vim.eval('g:studentEmail') + "\" is that correct? (Y/N) '"
    vim.command("let g:correctEmail = input("+s+")")
    resp = vim.eval("g:correctEmail")
    resp = resp.strip().lower()
    if resp in ["y","yes"]:
        break

while True:
    
    vim.command("let g:connectedMode = input('Is this exam online?(Y/N) ')")
    response = vim.eval("g:connectedMode")
    response = response.strip().lower() 
    if response in ["n","no"]:
        vim.command("let g:qCount = input('How many questions are on the exam? ')")
        c = int(vim.eval("g:qCount"))
        
        for count in range(1,c+1):
            print "The count is {0}".format(count)
            answerFile = "answer{0}.txt".format(count)
            f = open(answerFile,'w')
            f.close()
            command = "execute 'nmap ;;q{0} :call ChangeQuestions({1})<CR>'".format(count,count)
            vim.command(command)
        
	break
    elif response in ["y","yes"]:
        vim.command("let g:serverName = input('Enter the server name: ')")
        vim.command("let g:port = input('Enter the port: ')")
        vim.command("echo \"\n\"")
        
 
        break
    else:
        print response + " is an invalid response. Please enter Y or N"

vim.command("call inputrestore()")

#Add current directory to path to be able to import Client
p = os.getcwd()
sys.path.insert(0,p)


endpython
let g:questionsFileName = "ExamQuestions.txt"




call GetCheatSheetBuffers()
call Connect()
call ParseQuestions()

