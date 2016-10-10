
<h2>What is OMSI?</h2>

OMSI, short for Online Measurement of Student Insight, is a Python project made for conducting and grading examinations in a manner that is
both secure and conducive to high-quality measurement of student insight. It is suitable for small or large class quizz, test or exam:
be it essay, programming, math or multiple choice question.

<b>How to use this project package?</b>

<b><i>Starting the server</i></b>

Getting up and running is simple. Just download the files. In the directory where your files are located created a directory called ProfessorHomeDirectory. The exam questions should be placed in the ProfessorHomeDirectory. The format of how to specify questions is detailed below. 

Now just run OmsiServer.py [portNumber] [exam name] e.g python OmsiServer.py 5000 'Fall 2014 Midterm 1'

The address needed for students to connect to the server will then be printed to the terminal in the format host:port. e.g. pc16.cs.ucdavis.edu:5000. This info will need to be distributed to the students at the start of the exam. 

<b><i>Connecting to the Server</i></b>

All students must download the files as well. Once they have the files all they need to do is run OmsiGui.py. They can connect to the server and get the exam questions by clicking File->Connect and providing their student email and the host and port provided by the professor.

<b>NOTE:</b> There should be two separate on the right of the gui. One for the question and one to write the answer. The boxes are resizable and the question box may default to take up the whole right side of the screen on some systems. If this is the case grab the bottom of the box to resize.

<b>What happen after the test end? How does to autograding work?</b>

The autograding program is semi-autograded. It goes through the students' file answers.txt in their individual directory with the name of
their emailname (e.g. jsmith@ucdavis.edu -> jsmith) to parse students' answer and a master answer file with the name Answerx, where x is
the test ID. It then displays both sets of answers to the professor. If there are any formatting errors, the program will alert the
professor. The professor needs to manually fix the files and decides how many points to award and applies any
late penalties if deemed necessary. All results are then stored in an output file.


<h2>Providing the exam questions</h2>

  The exam questions should be placed in a file called Questions.txt in the ProfessorsHomeDirectory. The file should contain a description and any questions for the exam. If there are notes the instructor would like to write to himself in the file they should be placed at the beginning. When parsing the file the parser will go through line by line and search for keywords DESCRIPTION or QUESTION. Once a keyword is found each line after it is appended together until it reaches another keyword or the end of the file. So content that is not intended to be a part of a question or description should not be below a keyword. Questions are numbered in the order they are discovered.
  
  <i>Specifying different file types</i>
    By default all answers are saved as a .txt file. If a different filetype is desired then the -ext flag may be specified when 
    adding the QUESTION keyword. i.e 'QUESTION -ext .py'
    
  <i>Specifying compile and run options</i>
    The compile and run functionalities are by default disabled. If any question requires compile and run then the -com and -run flags may be specified in a simillar manner as the -ext file while adding the QUESTION keyword, e.g. 'QUESTION -com gcc -flags "-Wall -g" -run .\a.out', 'QUESTION -com python -run "python omsi_answer1.py" '
    
    
<b>Summary of each file on this site (in alphabetical order)</b>

AutoGrade.py
A program to grade the students' answer electronically and automatically (translated from Prof. N. Matloff's AutoGrade.R, included in this site).

Checksum.py
A program to convert content of students' answer to hexadecimal for grading.

Client.py
Main function Client side. This function connect to the server, it allows students to cache username and email for easy submission of files to the server.

ClientGlobals.py
Global variables client side.

ClientRoutines.py
A set of routines relevant to the client. The routines include file transfer from Client to Server, file transfer from Server to Client,
a "log in"/authentication system requiring students to input their email addresses for authentication.

ExampleScriptClientSide.py
A sample script on how to use Client interface.

ExampleScriptServerSide.py
A sample script on how grading scripts can be run on Server.

NetworkMonitor.py
A program to store network traffic of students' machines while students are taking the examination.

ProcessMonitor.py
A program to store the start time of the examination and process attributes e.g. name, record number, process id.

Server.py
Main function server side. This routine runs during the entire duration of the exam. This routine allows for
students to connect to the server and it delegates requests on the Server.

ServerGlobals.py
Global variables server side.

ServerRoutines.py
Routines that can be called via Server.py. Routines include file transfer from Server to Client, file transfer from Client to Server, file storage Server side
as well as routines for setting up the Server and terminating it.
