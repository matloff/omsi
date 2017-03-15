
# script to semi-automate grading of OMSI files

# IMPORTANT DIRECTIONS:

# This script will be invoked in a directory (referred to as the "top"
# directory here).  It is assume that there is a different such
# directory for each exam.  The top directory has one subdirectory for
# each student, which is the form created by OMSI.  That subdirectory
# will contain the student's answers to the exam problems, with file
# names of the form omsi_answersk.suffix  Here k is the exam problem
# number, and suffix is determined by the instructor in
# ProfessorHomeDirectory/Questions.txt

# The script will descend into each one, grading the student there.  The
# directory name is the student's full e-mail address, input by the
# student to OMSI during the exam.

# The instructor places a file Answersn, for Quiz n, in the top
# directory, with format, for Question i

#   %i point_total-_for_Quest_i problem_type
#   one or more answer lines
#   optional command line, beginning with $

# Here problem_type is either T (text), N (numerical evaluation) or C
# (code compile/run)

# Example:
#    %3 N
#    def sq(x): return x*x
#    print sq(3)
#    $ python omsi_answers3.py

# Without a command line, the default is to read and display plain ASCII text

# Start by calling grader() in the top directory.  The script will
# descend into each student subdirectory, and then display the student's
# answers one by one, asking the grader to assign points.  

# global variables:

#    topdir: name of top directory
#    quiznum: quiz number
#    answers:  R list containing
#       nprobs: number of problems
#       posspts: possible points for each problems
#       probtypes:  'T', 'N' or 'C', as above
#       cmnds: commands to run for each problem
#    output: character vector showing the results, one element per
#            student

# input files:

#    Answersn (see above)

#    student answer files (see above)

# output files:

#    outfile;

#       After each of the calls to grader() and
#       calcltrgrades(), the R variable output is saved to the file outfile
#       (in R object format); the latter can be copied to another machine
#       before calling emailresults().

#    ExamnResults:

#       The results will be placed in a file ExamnResults, where n is 
#       the exam number, supplied by the instructor when queried by grader().

# usage order:  
#
#    call grader() to grade the problems
#    call calcltrgrades() to compute the letter grades
#    call emailresults() to mail out the results


# uses strsplit() to separate a single string s into substrings, defined
# by fields of one OR MORE blanks, including leading and trailing
# blanks; e.g. " abc  de f" is broken into c("abc","de","f"), with no ""
# components
blanksplit <- function(s) {
   tmp <- strsplit(s," ")[[1]]
   tmp[tmp != ""]
}

# displays a character vector on the screen; e.g.
# display(c('abc','de','f') will show

#    abc
#    de
#    f

# on the screen (without the '#'s)
display <- function(charvec) {
   for (s in charvec) cat(s,'\n')
}

# read students' source file for Problem i
openstudentsrcfile <- function(i) {
   src <- problemlist$src[i]
   srccmd <- paste("source('",src,"')",sep="")
   tmp <- try(docmd(srccmd))
   if (class(tmp) == "try-error") {
      print(paste("can't open ",src,"; note penalty"))
   }
}

# close students' source files for Problem i
# closestudentfiles <- function(i) {
#    for (src in problemlist$src[[i]]) {
#       xcmd <- paste("pkill -f ",src)
#       system(xcmd)
#    }
# }

# grade the i-th problem (counting subparts separately), using lines
# from the student answer file
gradestudentans <- function(i) {
   # read students' source file for Problem i
   openstudentsrcfile(i)  
   # try to run their code
   print("running student code")
   runcmd <- problemlist$run[i]
   print(paste("trying: ",runcmd))
   try(docmd(runcmd))
   # view student file
   readline(paste("hit Enter when ready to go to text editor"))
   src <- problemlist$src[i]
   cmd <- paste("vi ",src)
   system(cmd)
   # closestudentfiles(i)
   # assign score for this problem
   fullpts <- problemlist$points[i]
   resp <- readline(paste("pts out of ",fullpts, "? [empty means full pts] "))
   if (resp == "") fullpts else resp
}

# find the subdirectories, one for each student group
getgdirs <- function() {
   gdirs <- list.dirs(recursive=F)
   gdirs[gdirs != "."]
}

# unpack .tar file, find student name, check for proper structure, open
# PDF file
unpack <- function(pdf) {
   tmp <- list.files(pattern=".tar")
   # should be just one tar file, no further subdirectories
   if (length(tmp) != 1) {
      print(paste("problem in subdirectory",getwd())) 
      return(NULL)
   }
   # unpack .tar
   tarname <- tmp[1]
   cmd <- paste('system("tar xf ',tarname,'")',sep='')
   docmd(cmd)
   # get student name
   sname <- strsplit(tarname,'.',fixed=TRUE)[[1]][1]
   # open PDF
   pdfname <- list.files(pattern=".pdf")[1]
   pdfcmd <- paste(pdf,pdfname)
   cmd <- paste('system("',pdfcmd,'")')
   docmd(cmd)
   # return student e-mail address
   sname
}

# clean up the student's variables etc. so that the next student is not
# affected
cleanup <- function(i) {
   cmd <- problemlist$cleanup[i]
   if (length(cmd > 0)) docmd(cmd)
}

# reads in Answersn file, sets various globals
readanswersn <- function() {
   answers <<- list()
   # read Answersn file
   fn <- paste('Answers',quiznum,sep='')
   answersn <- readLines(fn,n=-1)
   # which lines are the problem lines, i.e. start with %?
   firstchars <- unlist(Map(function(s) substr(s,1,1),answersn))
   problinenums <- which(firstchars == '%') 
   answers$nprobs <<- length(problinenums)
   # get point totals
   getpts <- function(probline) blanksplit(probline)[2]
   answers$posspts <<- 
      as.numeric(unlist(Map(getpts,answersn[problinenums])))
   getprobtype <- function(probline) blanksplit(probline)[3]
   answers$probtypes <<- 
      as.character(unlist(Map(getprobtype,answersn[problinenums])))
   # determine the line numbers at which there may be commands
   extproblinenums <- 
      c(problinenums,length(answersn)+1)  # phantom problem line at end
   cmdlines <- (extproblinenums - 1)[-1]
   answers$cmnds <<- vector(length=answers$nprobs)
   for (i in 1:answers$nprobs) { 
      cmdlinei <- cmdlines[i]
      if (answers$probtypes[i] != 'T') 
         answers$cmnds[i] <<- 
            if (firstchars[cmdlinei] == '$') {
               tmp <- answersn[cmdlinei]
               substr(tmp,3,nchar(tmp))
            } else stop('missing script command')
   }
}

# find student answer file name
getsfname <- function(i) {
   sprintf('omsi_answer%d.txt',i)
}

backtotop <- function() {
   setwd(topdir)
}

evalr <- function(cmd) 
   eval(parse(text=cmd))

grader <- function() {
   on.exit(exp=backtotop())
   quiznum <<- readline("enter quiz number: ") 
   readanswersn()  # read Answersn file, setting posspts, cmnds etc.
   topdir <<- getwd()  # save name of top directory
   gdirs <- getgdirs()  # get student subdirectory names
   output <<- NULL
   # go through all subdirectories, one per student
   for (gdir in gdirs) {  
      cat('\n\n')
      print(paste("entering directory", gdir))
      setwd(gdir)
      cat("\n\n","  now grading",gdir,"\n")
      gdr <- substr(gdir,3,nchar(gdir))
      outputline <- gdr
      scores <- NULL
      for (prob in 1:answers$nprobs) {
         cat('Problem ',prob,'\n')
         sfname <- getsfname(prob)
         if (!(sfname %in% list.files())) {
            score <- 0 
         } else {
            studentanswer <- readLines(sfname,n=-1)
            fullpts <- answers$posspts[prob]
            if (answers$probtypes[prob] == 'T') display(studentanswer)
            ### code for non-T cases will go here
            readcmd <- paste('score, out of ',fullpts,
               '; empty means full points: ',sep='')
            score <- readline(readcmd)
            if (score == "") {
               score <- fullpts 
            } else score <- as.numeric(score)
            scores <- c(scores,score)
         }
         outputline <- 
            paste(outputline,' ',score,'/',answers$posspts[prob],sep='')
         cat('\n\n')
      }
      outputline <- paste(outputline,' total ',sum(scores),sep='')
      print(outputline)
      output <- c(output,outputline)
      backtotop()
      save(output,file='outfile')
   }
   repeat {
      if (readline("need to edit? ") == "y") {
         output <<- edit(output)
      } else break
   }
   cat("\n","results:","\n")
   save(output,file="outfile")
   for (i in 1:length(output)) {
      cat(output[i],"\n")
   }
}

calcltrgrades <- function() {
   load("outfile")  # load file named 'output', one line per student
   tmp <- readline("enter cutoffs (none for F), e.g. 95 A+ 85 A 70 B...: ")
   tmp <- strsplit(tmp," ")[[1]]
   inds <- 1:length(tmp)
   evens <- inds[inds %% 2 == 0]
   odds <- inds[inds %% 2 == 1]
   ltrgrades <- tmp[evens]
   cutoffs <- as.integer(tmp[odds])
   totcol <- length(blanksplit(output[1])) 
   # now go through all the students, assigning letters grades to each,
   # and appending the letter grade for a student to the student's line
   for (i in 1:length(output)) {
      total <- blanksplit(output[i])[totcol]
      total <- as.integer(total)
      ltrgrd <- num2ltr(total,cutoffs,ltrgrades)
      output[i] <- paste(output[i],ltrgrd)
   }
   # save to file for records
   save(output,file="outfile")
   write(output,file="QuizGrades")
   cat("\n","  letter grade results:","\n")
   for (i in 1:length(output)) {
      cat(output[i],"\n")
   }
   print("if not in office, upload outfile, GroupQuizGrades, RunCmdsGrpQuiz, .tex")
}

emailresults <- function() {
   load("outfile")
   for (l in output) {
      tmp <- strsplit(l," ")[[1]]
      emailaddr <- tmp[1]
      # emailaddr <- paste(emailaddr,"@ucdavis.edu",sep="")
      cat(l,file="onestudent")
      tosend <- paste("mutt",emailaddr,"-s 'quiz results' < onestudent")
      system(tosend)
      # print(tosend)
      print(l)
      system("sleep 10")
      system("/bin/rm onestudent")
   }
}

# determines the letter gradeoff, based on the cutoffs cuts,lgs
num2ltr <- function(tot,cuts,lgs) {
   for (i in 1:length(cuts)) {
      if (tot >= cuts[i]) return(lgs[i])
   }
   return("F")
}

# do quoted command cmd
docmd <- function(cmd) {
   eval(parse(text=cmd))
}

