
# script to semi-automate quiz grading; see HOW TO RUN below for an
# overview, then see IMPORTANT DIRECTIONS for details

# 4.  HOW TO RUN:

#    put the student files and the Answers file in a directory (with no
#       other .txt files)
#    start R in that directory
#    set any global variables that might be needed for some of the N problems
#    call grader() to compute the total scores for the students
#    for each student, the script will:
#       check for format errors, giving the grader a chance to correct
#          them and/or impose a penalty
#       go through the problems, enabling the grader to grade each one
#    after all students are graded, the script will:
#       offer the grader a chance to make corrections
#       display the results for all students on the screen
#       write those results to a file "outfile"
#    the latter file can be moved to another machine and the process
#       continued there
#    call calcltrgrades() to compute the letter grades; it will:
#       display the student grades from outfile
#       display a table of score frequencies
#       prompt the grader to input the cutoff values for the letter grades
#       calculate the letter grades
#       rewrite outfile, with letter grades now added
#       write the results to the file Quizn
#    call emailresults() to mail out the results; it inputs from outfile

#    important note: after each of the calls to grader() and
#    calcltrgrades(), the R variable output is saved to the file outfile
#    (in R object format); the latter can be copied to another machine
#    before calling emailresults()

# IMPORTANT DIRECTIONS:

# 1.  All student files must be named in the format studentemail.txt (where
# the e-mail address is written minus the "@ucdavis.edu").  Have all of
# the files in the current directory, with no other .txt files present.

# 2.  The format of a student file is required to be as follows:  HOW WILL WE ENSURE THIS??

# The file alternates between one line of problem number and a SINGLE
# line of answer.  The problem number line of problem n must be #n, with
# a suffix of a, b etc. for parts, if any.  The answer line for a
# numeric problem (of type N below) must be executable R code.  (It may
# involve global variables set by the grader, and could have statements
# separated by semicolons.)

# There must be an answer for EVERY problem and subpart.  If a student
# does not answer a problem or subpart, he/she must write an answer of
# 00 (two zeros) in the file.  CAN WE AUTOMATICALLY REPLACE NON-ANSWERS??

# For example, say Problem 1 has the answer 3 times (2/17), Problem 2(a)
# and 2(b) have the answers 8 and 88, and Problem 3 consists of filling
# in two blanks in code, with answers "x*y" and "if".  Say Problem 4 is
# a multiple-choice problem, with answer (b), but anyway the student did
# not answer it.  The student answers file would then consist of

#  #1
#  3 * (2/17)
#  #2a
#  8
#  #2b
#  88
#  #3a
#  x*y
#  #3b
#  if
#  #4
#  00

# Note that there are NO blank lines.

# 3.  The grader's Answers file, the solutions file in this same
# directory, also alternates problem number lines with answer lines.  In
# the former, the problem number is followed by the problem type (N for
# numeric, S otherwise) and the point total for the problem.  In the N
# case, the answer is an R expression, which the script evaluates and
# displays, along with the grader's answer.  The name of the Answers
# file is Answersn, for Quiz n.

# The Answersn file for the above example would look like this: 

#  #1 N 10
#  3 * (2/17)
#  #2a N 20
#  8
#  #2b N 20
#  88
#  #3a C 15
#  x*y
#  #3b C 15
#  if
#  #4 S
#  (b)

# 5.  DETAILS OF grader():

# (a) Operation on each problem:

# During the call to grader(), for each problem the script will display
# the original student line, and the following:
#
#    N problem:  the R evaluations of the student's answer and the
#    grader's
#
#    S problem:  the student's answer and the grader's
#
# The grader then assigns points.

# pre-October 16, 2014:  
# (a) Actions if student file has format errors:

# If the student file has format errors, the program opens the file
# in vim, and the user may attempt to fix it.  In any case, the grader
# must save the file, after which it will be reread.  If the file is
# unfixable, then the user will still be prompted for grades on each
# problem; the user can simply enter 0s, and assign scores during the
# edit stage.

# after October 16, 2014:
# any format error simply results in the student temporarily getting
# 0s on all problems, and a total score of -1, signifying format
# errors

# (b) Action in case of severe format errors:

# If an "innovative" student file crashes the script, the grader need
# not restart the grading from scratch, as checkpointing is performed by
# the script.  This is done via writing the results SO FAR to the file
# named "outfile", which is a saved version of the global variable named
# "output".  If this occurs rename outfile; move the already-graded
# student files to another directory; grade the rest, producing a new
# "output"; rename the latter, say to "output1"; load the old "outfile",
# producing "output"; do output <- c(output,output1); do
# save(output,"outfile").  You are now ready to call calcltrgrades().

# GLOBALS
#
#    testid:  quiz number (Quiz 1, Quiz 2 etc.)
#    answerslist:  all data derived from the official Answers file
#    studentlines:  contents of the student answers file
#    output:  quiz results minus letter grades (latter are not yet determined) 

# read grader's Answers file, set answerslist


#KIRAN'S NOTES
#
#Must convert student's answer file into correct format
#Who handles submission format?
#I could possibly use Python to parse data and put into correct format
#
#Make more user friendly?
#

gettrueans <- function() {

   answerslist <<- list() #GLOBAL
   answersfile <- paste("Answers",testid,sep="") #Filename is"Answers#"
   lines <- scan(file=answersfile,what="",sep="\n",quiet=T) #Read in "Answers#"
   nproblems <- length(lines) / 2 #Calc num probs based on input format
   
   #Set up our global answerslist to contain info about answers file
   answerslist$nproblems <<- nproblems
   answerslist$probnum <<- vector(mode="character",length=nproblems)
   answerslist$ans <<- vector(mode="character",length=nproblems)
   answerslist$probtype <<- vector(mode="character",length=nproblems)
   answerslist$points <<- vector(mode="integer",length=nproblems)
   
   #Extract data from when we read file, place in correct arrays
   for (i in 1:answerslist$nproblems) {
      l <- lines[2*i-1]
      answerslist$ans[i] <<- lines[2*i]
      answerslist$probnum[i] <<- strsplit(l," ")[[1]][1]
      answerslist$probtype[i] <<- strsplit(l," ")[[1]][2]
      answerslist$points[i] <<- strsplit(l," ")[[1]][3]
   }
}

#Just read in the student's file
readstudentfile <- function(sfl) {
   studentlines <<- scan(file=sfl,what="",sep="\n",quiet=T)
}

# grade the i-th problem (counting subparts separately), using line
# from the student answer file
gradestudentans <- function(i) {
   studentans <- studentlines[2*i]
   if (studentans == "00") return(0) #Maybe print "Problem## not answered" or something??
   studentanscopy <- studentans
   realans <- answerslist$ans[i]
   fullpts <- answerslist$points[i]
   #If numeric answer, calculate value
   if (answerslist$probtype[i] == "N") {
      studentans <- evalrstring(studentans)  #How will Python evaluate R answers??  Maybe include NumPy/SciPy plugin??
      realans <- evalrstring(realans)
   }
   probnum <- answerslist$probnum[i]
   
   #Print results and let teacher enter number of points
   cat(probnum,"  student original:",studentanscopy,"\n")
   cat(probnum,"  student evaluated:",studentans,"\n")
   cat(probnum,"  true evaluated:",realans,"\n")
   fullpts <- answerslist$points[i]
   resp <- readline(paste("pts out of ",fullpts, "? [empty means full pts] "))
   if (resp == "") pts <- fullpts else pts <- resp
   pts #Returns the number of points
}

# check studentlines lines for format errors, returning 1 if OK, 0 else
studentfileok <- function() {
   # correct number of lines?
   nslines <- length(studentlines)
   if (nslines != 2 * answerslist$nproblems) {
      print("wrong line count")
      return(0)
   }
   # do problem numbers and answers alternate, one each at a time?
   
   # ??does this account for blank lines??
   for (i in 1:nslines) {
      tmp <- strsplit(studentlines[i]," ")[[1]][1]
      firstchar <- substr(tmp,1,1)
      if (i %% 2 == 1 && firstchar != "#") { 
          print("number, answer lines don't alternate correctly")
          return(0)
      }
   }
   return(1)
}

# October 16, 2014:  as of now, this function is not used
#
# this function is called if a format error is discovered in the
# student's file; the grader can optionally fix the error(s) and ask the
# script to re-read the file; in any case, the grader is asked hom much
# penalty to impose
# tryfix <- function(sfl) {
   # open student file for possible fix
   # xcmd <- paste("xterm -e vi ",sfl," &")
   # cmd <- paste("vim ","'",sfl,"'",sep="")
   # system(cmd)
   # resp <- readline("re-read student file? ")
   # if (resp == "y") {
      # stillbad <- F
      # readstudentfile(sfl) 
   # } else stillbad <- T
   # pen <- as.integer(readline("penalty amount:  "))
   # list(stillbad=stillbad,pen=pen)
}

#The main grading function
grader <- function() {

   # is this a batch of late submissions?
   late <- readline("late grading? ") == "y" 
   if (late) {
      latepenalty <- as.integer(readline("penalty amount (Enter for 0):  "))
      if (is.na(latepenalty)) latepenalty <- 0
   } else latepenalty <- 0
   
   # test ID, e.g. 3, 3Tues, Midterm
   testid <<- readline("enter test ID: ") 
   if (file.exists("Globals.R")) source("Globals.R") #Otherwise...?
   # set up R list that will contain the true answers
   gettrueans()  
   output <<- vector(mode="character")
   # loop across all student files
   for (sfl in list.files(pattern="*.txt")) {  
      emailaddr <- substr(sfl,1,(nchar(sfl)-4))
      cat("\n\n","  now grading",emailaddr,"\n")
      # start to build the output line for this student; it will consist
      # of e-mail address, the student's score for each problem, etc.
      outputline <- emailaddr
      readstudentfile(sfl)
      # student's file format OK?
      fmterr <- !studentfileok()
      penalty <- latepenalty
      # removed, October 16, 2014
         #      if (sflok == 0) {
         #         tried <- tryfix(sfl)
         #         penalty <- penalty + tried$pen
         #      } else tried <- list(stillbad=F,pen=0)
      # start grading the problems
      total <- 0
      for (i in 1:answerslist$nproblems) {
         # if (!tried$stillbad) {  removed, 10/16/14
         if (!fmterr) {
            score <- gradestudentans(i)
         } else score <- 0
         outputline <- paste(outputline," ", score,"/",answerslist$points[i],sep="")
         total <- total + as.integer(score)
      }
      if (fmterr) {
         total <- -1
      } else total <- total - penalty
      outputline <- paste(outputline,"penalty =",penalty)
      outputline <- paste(outputline,"total =",total)
      print(outputline)
      output <<- c(output,outputline)
      # save output after each student, so as to not have to start all
      # over again if the script crashes; then can do the rest
      # separately
      save(output,file="outfile")
   }
   # the grader now has a chance to make corrections to the
   # scores/grades
   repeat {
      resp <- readline("need to edit? ")
      if (resp  == "y" || resp == 'n') break
   }
   if (resp  == "y") {
      output <<- edit(output)
      save(output,file="outfile")
   } 
   # print the results (still no letter grade) to screen and the file
   # "outfile"
   cat("\n","results:","\n")
   for (i in 1:length(output)) {
      cat(output[i],"\n")
   }
}

# inputs a character vector svec, each element of which has the same 
# number of blanks, and then forms a data frame from the nonblank fields
splittodf <- function(svec) {
   nr <- length(svec)
   rslt <- strsplit(svec[1],split=" ")[[1]]
   for (i in 2:nr) {
       sp <- strsplit(svec[i],split=" ")[[1]]
       rslt <- rbind(rslt,sp)
   }
   rslt <- data.frame(rslt)
   rownames(rslt) <- 1:nr
   rslt
}

calcltrgrades <- function() {
   load("outfile")
   # may be on another machine, so ask again
   testid <<- readline("enter test ID: ") 
   gdf <- splittodf(output)
   print(gdf)
   print(table(gdf[,ncol(gdf)]))
   tmp <- readline("enter cutoffs (none for F), e.g. 95 A+ 85 A 70 B...: ")
   tmp <- strsplit(tmp," ")[[1]]
   inds <- 1:length(tmp)
   evens <- inds[inds %% 2 == 0]
   odds <- inds[inds %% 2 == 1]
   ltrgrades <- tmp[evens]
   cutoffs <- as.integer(tmp[odds])
   totcol <- length(strsplit(output[1]," ")[[1]]) 
   for (i in 1:length(output)) {
      total <- strsplit(output[i]," ")[[1]][totcol]
      total <- as.integer(total)
      ltrgrd <- num2ltr(total,cutoffs,ltrgrades)
      output[i] <- paste(output[i],ltrgrd)
   }
   # save to file for records
   save(output,file="outfile")
   write(output,file=paste("Quiz",testid,"Grades",sep=""))
   cat("\n","  letter grade results:","\n")
   for (i in 1:length(output)) {
      cat(output[i],"\n")
   }
   print("if not in office, upload outfile, QuiznGrades, Answersn, .tex")
}

emailresults <- function(coursename) {
   # if sending mail requires a password, remind the user
   # readline("set password externally (if any), then hit Enter")
   load("outfile")
   for (l in output) {
      tmp <- strsplit(l," ")[[1]]
      emailaddr <- tmp[1]
      emailaddr <- paste(emailaddr,"@ucdavis.edu",sep="")
      cat(l,file="onestudent")
      subject <- paste(coursename,'Quiz',testid,'results',sep=" ")
      # tosend <- paste("mutt",emailaddr,"-s 'quiz results' < onestudent")
      tosend <- paste("mutt",emailaddr,"-s '", subject, "' < onestudent")
      # tosend <- paste('mail -s "quiz results" ',emailaddr, ' < onestudent')
      system(tosend)
      print(tosend)
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

# evaluate the given R expression; note: set any needed globals,
# including functions, in Globals.R before calling grader(); also
# note: in principle, a student can put multiple R statements within one
# line, separated by semicolons, but it is not recommended to have them
# write full code, e.g. full functions--it almost always has syntax
# errors etc.
evalrstring <- function(toexec) {
   cat(toexec,file="tmpexec")
   sourceresult <- try(source("tmpexec"))
   if (class(sourceresult) == "try-error" || 
      !is.numeric(sourceresult$value)) {
      print("R parse error at:")
      print(toexec)
      return(NA)
   } else return(sourceresult$value)
}
