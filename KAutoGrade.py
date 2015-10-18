#KBAutoGradeQuiz.py
#Auto-grading program based on Norm Matloff's AutoGradeQuiz.R
#program.  Translated into Python by Kiran Bhadury.
#
#TODO:
#	How do we get/use the teacher's global variables?
#	Can't run R code (more details in the grade_student_ans function)
#	Doesn't currently support complex code evaluation.
#		However, this can easily be added by using exec and the 
#		compile() function. Then the issue would be grading the 
#		code (i.e. grading against multiple test cases).
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
#This program allows for semi-automated grading by parsing students'
#answers and parsing a master answer file, and then displaying
#both sets of answers to the teacher.  The teacher then decides how
#many points to award and applies any late penalties.  All results are
#stored in an output file.
#
#Conditions:
#The students' answer files, the master answer file, and this program
#must all be in the same directory.  The master answer file must be
#named Answersx, where x is the test ID.  The students' files must be
#named emailname.txt, where email name is the email address without
#the @ucdavis.edu (i.e. jsmith@ucdavis.edu -> jsmith)
#The files must be in a certain format (more on this is explained
#in the methods below).  The program also alerts the teacher if
#there are any formatting errors, and the teacher must manually fix
#or grade those files.
#
#Detailed information about each method precedes the method declaration

__author__ = 'Kiran'

import glob

#Set up the default global variables
test_id = None 				   #Example: test_id=3 for Quiz3
test_value = -1				   #Total number of possible points
output = [] 				   #Contains one output line per student
student_anslist = [] 		   #The student's answers
master_anslist = [[],[],[],[]] #Data from the answer key
#More on master_anslist:
#Initialized to four empty sublists
#sublists are in the following format...
#	[[question #s],[question types],[point values],[correct answers]]
#... so let's set up some constants to refer to master_anslist indices
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
def get_true_answers():
	filename = 'Answers' + test_id
	try:
		answer_file = open(filename)
	except IOError:
		print 'Error: The answer file %s does not exist' % filename
		exit()
	file_contents = list(answer_file)
	answer_file.close()
	
	#Get every even line (those containing question num, type, and value)
	for header in file_contents[::2]:
		vals = header.split(' ')
		
		#Make sure question header is in the right format
		#There should be three values, and the line should start with a #
		if (len(vals)!=3 or vals[0][0]!='#'):
			print_ansfile_format()
			exit()

		master_anslist[QNUM_INDEX].append(vals[0])
		master_anslist[QTYPE_INDEX].append(vals[1])
		master_anslist[QVAL_INDEX].append(float(vals[2][:-1])) #Remove \n 
		#Now we can calculate the test value
		global test_value
		test_value = sum(master_anslist[QVAL_INDEX])
	
	#Get every odd line (those containing the question answer)
	for ans in file_contents[1::2]:
		master_anslist[QANS_INDEX].append(ans[:-1]) #Remove \n

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
#Output: none
#Read in the student's file (no fancy parsing here, just the list() function)
#Student's answer file must be in the following format:
#	#1
#	2*(7/4)
#	#2
#	Leonardo da Vinci
def read_student_file(file_name):
	try:
		stdfile = open(file_name)
		global student_anslist
		student_anslist = list(stdfile)
		stdfile.close()
	except IOError:
		print 'Error: The student file %s does not exist' % filename
		exit()

#Function is_student_format_bad
#Input: none
#Output: boolean indicating if student's answer file format is incorrect
#Performs a quick format check on the student's answer list (i.e. whatever
#is currently stored in student_anslist)
#Checks two main things:
#	Whether it has the same number of question/answer pairs as the answer list
#	Whether it properly alternates b/w question and answer
def is_student_format_bad():
	if len(student_anslist) != 2*len(master_anslist[QNUM_INDEX]):
		return True
	for line in student_anslist[::2]:
		if line[0] != '#':
			return True
	return False

#Function grade_student_ans
#Input: int of the index in master_anslist of the question to be scored
#Output: tuple with floats: (points the student received, points possible)
#Evaluates the student's answer (if necessary) and displays to
#the teacher the student's answer and the answer key's answer.
#The teacher then decides how many points to award.
def grade_student_ans(qnum_index):
	#Set up variables with relevant question/answer info
	student_ans = student_anslist[qnum_index*2+1][:-1] #Remove \n
	ans_copy = student_ans
	real_ans = master_anslist[QANS_INDEX][qnum_index]
	qvalue = master_anslist[QVAL_INDEX][qnum_index]
	qnum = master_anslist[QNUM_INDEX][qnum_index]
	
	#Handling an unanswered problem
	if student_ans=='00':
		print 'Problem %s was left unanswered' % qnum
		return 0
	
	#If we have a numerical problem, evaluate it
	#NOTE: currently only evaluates Python expressions
	#It looks like there are packages to evaluate R
	#expressions, but this may require extra installation
	#on the user's part
	if master_anslist[QTYPE_INDEX][qnum_index] == 'N':
		if '/' in student_ans:
			print 'WARNING: Integer division may cause evaluation issues.'  
			print 'Check original student answer.'
		student_ans = str(eval(student_ans))
	
	#Print out problem/answer information and let teacher determine
	#if problem is correct or not
	print '**Question %s, %s points**' % (qnum, qvalue)
	print 'Student answered \t%s' % ans_copy
	print 'Ans evaluated to \t%s' % student_ans
	print 'Answer key shows \t%s' % real_ans
	points_received = raw_input("How many points to award?  Leave blank for full credit >> ")
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
	
	all_student_files = glob.glob('*.txt') #Assuming this program is in the same dir
	count_files = 0
	bad_files = 0
	for fl in all_student_files:
		count_files+=1
		output_line = []
		email = fl[:-4]
		output_line.append(email)
		read_student_file(fl)
		
		print '\n### Grading next file... ###\n'
		
		#If format is bad, don't bother grading.  Just set score to -1
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
		print 'Summary for %s' % email
		print 'Points received/total possible: %.2f/%.2f' % (total, test_value)
		print 'Late penalty applied: %s' % is_late
		if verbose:
			print verbose_str
		
	print 'Finished grading %d files (%d with format errors)' % (count_files,bad_files)
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
