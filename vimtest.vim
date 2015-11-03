
"How to map ;;b n?

function! VimCheatSheet()
python << endpython

print("This is a vim cheat sheet")
vim.command("return 1")

endpython
endfunction

function! HelpCheatSheet()
python << endpython

print("This is the help cheat sheet")
vim.command("return 1")

endpython
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

:nmap ;;vim :call VimCheatSheet()<CR>
:nmap ;;help :call HelpCheatSheet()<CR>
:nmap ;;rn :call CompileRun()<CR>
:nmap ;;eval :call Evaluate()<CR>
:nmap ;;sv :call Save()<CR>
:nmap ;;sva :call SaveAll()<CR>



call inputsave()
let g:serverName = input('Enter the server name: ')
let g:port = input('Enter the port: ')
call inputrestore()
python << endpython
import vim
print (vim.eval("serverName")+ "is the server name!")
print (vim.eval("port") + " is the port number!")
print ("Vimscript has been imported")

endpython

call Connect()



