

function! VimCheatSheet()

:b 1

endfunction

function! HelpCheatSheet()

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
python << endpython

print("This saves the current buffer")

endpython
endfunction

function! SaveAll()
python << endpython

print("This will save all buffers")

endpython
endfunction

function! Connect()
python << endpython

print ("Attempting to connect to {0} at port {1}".format(vim.eval("g:serverName"),vim.eval("g:port")))

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


python << endpython
import vim
import sys
import os
vim.command('call inputsave()')
    

while True:
    vim.command("let g:connectedMode = input('Is this exam online?(Y/N) ')")
    response = vim.eval("g:connectedMode")
    response = response.strip().lower() 
    if response in ["n","no"]:
        vim.command("let g:qCount = input('How many questions are on the exam?')")
        c = vim.eval("g:qCount")
        
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

import Client
Client.setUpServer(vim.eval("serverName"), vim.eval("port"))

endpython
let g:questionsFileName = "questions.txt"
call GetCheatSheetBuffers()
call Connect()
call ParseQuestions()


