

library(gtools)

# cmds(): lists recent commands
# arguments:
#    wild: character string for indicating wild card 
#          to be matched at start of command
#    exc: exclude commands with containing this string
#    keep: return a vector of found commands
#    ask: prompt the user for the number of a command 
#         to execute (Enter means none); 'ask' and 
#    'keep' should not both be set to TRUE
# return value: character vector of the commands, 
#               or if ask = TRUE, the selection number 

cmds <- function(wild=NULL,exc=NULL,keep=FALSE,ask=TRUE) {
   savehistory("cmdshistory")
   allcmds <- scan("cmdshistory",what="",sep="\n",
      quiet=TRUE)
   foundcmds <- NULL
   for (i in 1:length(allcmds)) {
      ci <- allcmds[i]
      if (!is.null(exc)) {
         gy <- grepyes(exc,ci)
         if (gy) next
      }
      if (!is.null(wild)) {
         gy <- grepyes(wild,ci)
         if (!gy) next
         if (wild != substr(ci,1,nchar(wild))) next
      }
      cat(i,ci,"\n")
      foundcmds <- c(foundcmds,ci)
   }
   if (ask) {
      resp <- readline("enter command numberi:  ")
      if (resp == "") return()
      return(resp)
   }
   if (keep) foundcmds
}

# cmdn(), "command number"; executes the command of 
# the given number, like Unix shell '!n'
cmdn <- defmacro(cmdnum,expr={
      allcmds <- scan("cmdshistory",what="",sep="\n")
      # allcmds <- invisible(cmds(keep=TRUE))
      wishcmd <- allcmds[cmdnum]
      cat(">>",wishcmd,"\n")
      print(docmdmac(wishcmd))
   }
)

# cmdw(), "command wild card":  execute latest 
# wild match, if any
cmdw <- defmacro(wld,expr={
      tmp <- cmds(wild=wld,keep=TRUE,ask=FALSE)
      wishcmd <- tmp[length(tmp)]
      cat(">>",wishcmd,"\n")  # fake special prompt
      if (!grepyes("cmdw",wishcmd))
         print(docmdmac(wishcmd))
   }
)

# cmde(), "command execute":  execute command number 
# specified by user after he/she views commands list
cmde <- defmacro(dummy,expr={
      wishcmd <- cmds(ask=TRUE)
      if (wishcmd != "") {
         cmdn(as.integer(wishcmd))
      }
   }
)
 
# executes specified command at the caller's level
docmdmac <- defmacro(strcmd,
   expr={eval(parse(text=strcmd))})

# return TRUE if patt is found in s
grepyes <- function(patt,s) length(grep(patt,s)) > 0

