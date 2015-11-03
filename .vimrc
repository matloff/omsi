set number
set showcmd
syntax on
au FileType py set autoindent
au FileType py set smartindent

function! Testing(arg)
python << endpython
import vim
anArg = vim.eval("a:arg")
print("this is python " + anArg)
vim.command("return 1")
endpython
endfunction

nmap ;s :source ~/Desktop/omsi/vimtest.vim<CR>
