#AutoGradeQuiz.py
#Auto-grading program based on Norm Matloff's AutoGradeQuiz.R
#program.  Translated into Python by Kiran Bhadury.
#
#Update 11/2/15: Files are now expected to be stored in a hierarchical
#	directory format.  Each student has their own directory with their
#	answer file and any other files inside.
#
#Update 11/4/15: Now supports multi-line answers.  Assumes that any
#	line starting with a '#' is the question header, and any other
#	line is part of the corresponding answer.
#
#TODO:
#	How do we get/use the teacher's global variables?
#	Can't run R code (more details in the grade_student_ans function)
#	Doesn't currently support complex code evaluation.
#		I definitely feel like we can use Prof. Chen's GradeBot to
#		do this.  However, if Prof. Matloff is against it, Python's
#		subprocess module allows us to run external programs.
#	Doesn't set letter grades.
#		I held off on this one because I want us to find a good
#		way to display class results (maybe a graph? or maybe
#		just show avg and median?).  In any case, it will be easy
#		to add code allowing the teacher to input letter grade
#		cutoffs.
#	Doesn't email results.
#		There's a few examples in the Python docs on how to use
#		the smtplib and the email packages to send emails.  I'm
#		not sure how to set up the local server or if it requires
#		passwords, so I'm holding off on this.  Also, this isn't
#		essential to the core prototype right now (we can add code to 
#		email the results later on.)
#
#About the program
#	This program allows for semi-automated grading by parsing students'
#	answers and parsing a master answer file, and then displaying
#	both sets of answers to the teacher.  The teacher then decides how
#	many points to award and applies any late penalties.  All results are
#	stored in an output file.
#
#Conditions:
#	The students' answer directories, the master answer file, and this program
#	must all be in the same directory.  The master answer file must be
#	named Answersx, where x is the test ID.  The students' files must be
#	in directories that are named according to their email address:
#		emailname, where email name is the email address without
#		the @ucdavis.edu (i.e. jsmith@ucdavis.edu -> jsmith)
#	Their answers must be stored in a file called answers.txt within
#	their student directory.
#
#	The files must be in a certain format (more on this is explained
#	in the methods below).
#
#	The program also alerts the teacher if there are any formatting errors, 
#	and the teacher must manually fix or grade those files.
#
#Detailed information about each method precedes the method declaration

__author__ = 'Kiran'

import os

#Set up the default global variables
test_id = None 				   #Example: test_id=3 for Quiz3
test_value = -1				   #Total number of possible points
output = [] 				   #Contains one output line per student
student_anslist = [[],[]]	   #The student's answers
#More of student_anslist:
#Initialized to two empty sublists in the following format:
#	[[question #s],[answers]]
#...so let's set up some constants to refer to student_anslist indices
SNUM_INDEX = 0
SANS_INDEX = 1
#Same idea with master_anslist:
master_anslist = [[],[],[],[]] #Data from the answer key
QNUM_INDEX = 0
QTYPE_INDEX = 1
QVAL_INDEX = 2
QANS_INDEX = 3

#Function get_true_answers
#Input: none
#Output: none
#Extract problem info and the correct answers from the master answer file
#Master answer file must be named Answersx, x=test_id
#Master answer file must be in the following format:
#
# 	#1 N 10 (the question header, w/number, type, and value)
# 	2*(7/4) (the correct answer)
# 	#2 S 15 
# 	Christopher Columbus
# 
#The resulting master_anslist is in the following format:
#	[[#1,#2],['N','S'],[10,15],[2*(7/4),'Christopher Columbus']]
#
#Note that the answer may span multiple lines of the answer file
def get_true_answers():
	filename = 'Answers' + test_id
	try:
		answer_file = open(filename,'r')
	except IOError:
		print 'Error: The answer file %s does not exist' % filename
		exit() #Without the answer file, the program must close
	file_contents = list(answer_file)
	answer_file.close()
	
	ansindex = -1
	for line in file_contents:
		#Question header
		if line[0] == '#':
			vals = line.split(' ')
			if len(vals) != 3:
				print_ansfile_format()
				exit()
			master_anslist[QNUM_INDEX].append(vals[0])
			master_anslist[QTYPE_INDEX].append(vals[1])
			master_anslist[QVAL_INDEX].append(float(vals[2][:-1])) #Remove \n
			master_anslist[QANS_INDEX].append("") #Anticipate answer
			ansindex += 1
		#Answer (may be multi-line)
		else:
			master_anslist[QANS_INDEX][ansindex] += (line + '\t\t\t') #Fancy formatting
	
	#Calculate how much the test is worth
	global test_value
	test_value = sum(master_anslist[QVAL_INDEX])
			

#Function print_ansfile_format
#Input: none
#Output: prints proper file format
#Method to print out the proper file formatting in case of error
def print_ansfile_format():
	print 'Error!  Please make sure the answer file is in the following format:'
	print """
#<question number> <question type> <point value>
<correct answer>\n
Examples:
#1 N 10
2*(7/4)
#2 S 15
Christopher Columbus
		  """

#Function read_student_file
#Input: string name of the file to be graded
#Output: Boolean for successful read (True) or not (False)
#Read in the student's file
#Student's answer file must be in the following format:
#	#1
#	2*(7/4)
#	#2
#	Leonardo da Vinci
#Resulting student_anslist is in the following format:
#	[[#1, #2],[2*7/4,Leonardo da Vinci]]
#
#Note that the answer may span multiple lines of the answer file
def read_student_file(filename):
	try:
		student_file = open(filename,'r')
	except IOError:
		print '^^^Error: The student file %s does not exist^^^' % filename
		return False
	file_contents = list(student_file)
	student_file.close()
	
	#Clear out current contents
	global student_anslist
	student_anslist = [[],[]]
	
	ansindex = -1
	for line in file_contents:
		if line[0]=='#':
			student_anslist[SNUM_INDEX].append(line[:-1]) #Remove\n
			ansindex+=1
			student_anslist[SANS_INDEX].append("")
		else:
			student_anslist[SANS_INDEX][ansindex] += (line+'\t\t\t')
			
	return True

#Function is_student_format_bad
#Input: none
#Output: boolean indicating if student's answer file format is incorrect
#Checks to make sure the student has the same number of questions in
#their file as the answer key
def is_student_format_bad():
	return len(student_anslist[SNUM_INDEX]) != len(master_anslist[QNUM_INDEX])

#Function grade_student_ans
#Input: int of the index in master_anslist of the question to be scored
#Output: tuple with floats: (points the student received, points possible)
#Evaluates the student's answer (if necessary) and displays to
#the teacher the student's answer and the answer key's answer.
#The teacher then decides how many points to award.
def grade_student_ans(qnum_index):
	#Set up variables with relevant question/answer info
	student_ans = student_anslist[SANS_INDEX][qnum_index][:-4] #Remove \n\t\t\t
	real_ans = master_anslist[QANS_INDEX][qnum_index][:-4] #Remove \n\t\t\t
	qvalue = master_anslist[QVAL_INDEX][qnum_index]
	qnum = master_anslist[QNUM_INDEX][qnum_index]
	
	#Handling an unanswered problem
	if student_ans=='00':
		print 'Problem %s was left unanswered\n' % qnum
		return (0,qvalue)
	
	#Print out problem/answer information and let teacher determine
	#if problem is correct or not.  Evaluate numerical answers
	print '**Question %s, %s points**' % (qnum, qvalue)
	print 'Student answered \t%s' % student_ans
	
	#Note: this only evaluates python expressions
	if master_anslist[QTYPE_INDEX][qnum_index] == 'N':
		print 'Ans evaluated to \t%s' % str(eval(student_ans))
		if '/' in student_ans: print 'WARNING: this problem contains division.'
		
	print '\nAnswer key shows \t%s' % real_ans
	points_received = raw_input("\nHow many points to award?  Leave blank for full credit >> ")
	if points_received == '':
		points_received = qvalue
	else:
		points_received = float(points_received)
	
	print '\n' #Readability
	return (points_received, qvalue)

#Function grader
#Input: string name of the output file, boolean for verbose output
#	If verbose is true, output prints each problem and its score
#	If verbose is false (default), only a summary of results is printed
#Output: a file with the given file name
#This function goes through the current directory and pulls each student's
#answers file.  It also reads in the master answer file.  It then uses
#the grade_student_ans function to step through each student's answers
#and assign points, eventually calculating a total score for the student.
#Result data is saved in a file, with the name specified by the teacher.
#
#Output for each student is written to a list called output_line
#The format of output_line is as follows:
#	[email,prob1,score1,prob2,score2....,penalty,total]
#After grading each student's answer, the current output_line is appended
#to the output file and the main output list, which we defined globally.

def grader(outfile, verbose = False):
	global test_id
	test_id = raw_input('Please enter test ID >> ')
	get_true_answers()
	print 'Exam %s, %.2f points' % (test_id, test_value)
	
	#Apply late penalty, if desired
	late_penalty = 0 #Default
	is_late = (raw_input('Are all submissions in this group late? y/n >> ') == 'y')
	if(is_late):
		late_penalty = raw_input('Enter late penalty amount (leave blank for none) >> ')
		if late_penalty != '':
			late_penalty = float(late_penalty)
	else:
		print 'If only some submissions are late, you must grade those separately.'
		if raw_input('Exit? y/n >> ') == 'y': exit()
	
	#Create a new output file to write to and add basic test info
	f = open(outfile, 'a')
	f.write('Exam ' + test_id + ' ' + str(test_value) + ' points\n')
	
	all_student_dirs = os.listdir('.');
	count_files = 0
	bad_files = 0
	not_found = ''
	for dir in all_student_dirs:
		if not (os.path.isdir(dir)):
			continue #Skip past anything that isn't a directory
		fl = os.path.join(dir, 'answers.txt') #Look for student's answer file
		count_files+=1
		output_line = []
		email = dir
		output_line.append(email)
		
		print '\n### Grading next file... ###\n'
		
		#Check to see if the file exists.  If not, skip it
		if not read_student_file(fl):
			not_found += (email + '\n')
			continue
		#If format is bad, don't bother grading.  Just set score to -1 and alert teacher
		if is_student_format_bad():
			bad_files+=1
			output_line.append('-1')
			output.append(output_line)
			f.write(str(output_line) + '\n')
			print 'WARNING: submission %s has a formatting error.' % email
			print 'Setting total score to -1'
			continue
		
		#Begin grading the student's answers
		total = 0
		verbose_str = ''
		num_of_qs = len(master_anslist[QNUM_INDEX])
		for i in range(num_of_qs):
			(score,possible) = grade_student_ans(i)
			total += score
			qstr = master_anslist[QNUM_INDEX][i]
			score_str = str(score) + "/" + str(possible)
			
			output_line.append(qstr)
			output_line.append(score_str)
			if verbose:
				verbose_str += qstr + ': ' + score_str + '\n'
		
		#Deduct any penalties
		total -= late_penalty
		
		#Add the last few things to our output line...
		output_line.append(str(late_penalty))
		output_line.append(str(total))
		#...write the line to the output file...
		f.write(str(output_line) + '\n')
		#...and add the whole line to our output list
		output.append(output_line)
		
		#Print a summary of the grading
		print '[[Summary for %s]]' % email
		print 'Points received/total possible: %.2f/%.2f' % (total, test_value)
		print 'Late penalty applied: %s' % is_late
		if verbose:
			print verbose_str
		
	print '\nFinished grading %d files (%d with format errors)' % (count_files,bad_files)
	print 'Couldn\'t locate the following students\' answer files:\n%s' % not_found
	print 'Results stored in %s\n' % outfile
	f.close()

#Function: print_from_output
#Input: name of the file to read from, boolean Verbose
#Output: prints contents in readable format
#Convenience method to parse an output file and print its data in
#readable format.  Verbose option prints out every question and
#score, non-verbose just prints students' result summaries
def print_from_output(out_file, verbose=False):
	f = open(out_file)
	output_lines = list(f)
	
	#Print basic test info
	print '\n%s' % output_lines[0]
	
	for line in output_lines[1:]: #Skip the first line (basic info)
		word_list = line.split(',')
		
		#Skip student files with format issues
		if len(word_list) == 2:
			print word_list[0][2:-1] + ' had a formatting error!'
			continue
		
		print word_list[0][2:-1] #Student's name
		
		if verbose:
			for word in word_list[1:-2]:
				print word[2:-1] #Slice to remove leading & trailing ' marks
		
		print 'Late penalty: ' + word_list[-2][2:-1] #Remove ' marks
		print 'Total: ' + word_list[-1][2:-3] + '/' + str(test_value) + '\n' #Remove '] marks
		
	f.close()

if __name__ == "__main__":
	print 'Please set up the grader:'
	filename = raw_input('Enter name of output file (will be created if nonexistant)>> ')
	verbose = (raw_input('Print detailed info about each student\'s results? (y/n) >> ') == 'y')
	print '\nNow running grader...'
	grader(filename,verbose)
	print 'Program completed'
	if (raw_input('View all students\' results? (y/n) >> ') == 'y'):
		verbose = (raw_input('Display detailed info? (y/n) >> ') == 'y')
		print_from_output(filename,verbose)
