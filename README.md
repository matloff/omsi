

<h2>What is OMSI?</h2>

OMSI, short for Online Measurement of Student Insight, is a Python
project for conducting and grading examinations in a manner that is both
secure and conducive to high-quality measurement of student insight. It
is suitable for small or large class exams, be they based on
essays, writing code, math analysis or multiple choice question.

Students come to the classroom at the regular class time, just as with a
traditional pencil-and-paper exam.  However, they use their laptops to
take the exam, using OMSI.  The latter downloads the exam questions, and
enables the students to upload their answers.

OMSI has two components:

<UL>

<li> <i>Exam administration.</i>  This manages the actual process of the
students taking the exam.
</li> </p>

<li> <i>Exam grading.</i> OMSI does NOT take the place of instructor
judgment in assigning points to individual exam problems, and total
grade for the exam.  But it does make things much easier, by automating
much of the drudgery. For instance, OMSI automatically records grades
assigned by the instructor, and automatically notifies students of their
grades via e-mail.

</UL>

In addition to making the job of grading much easier, OMSI has a number
of advantages for students over the traditional pencil-and-paper format:

<UL>

<li> With essay questions, students have a chance to edit their answers,
producing more coherent, readable prose.
</li> </p>

<li> With coding questions, students can compile and run their code,
giving them a chance to make corrections if their code doesn't work.
</li> </p> 

</UL>

In both of these aspects, OMSI gives the student a better chance to
demonstrate his/her insight into the course material, compared to the
traditional exam format.

<h2>
How to Use This Package
</h2>

<UL>

<li> <a href=#install"">Installation (Instructors and Students)</a> 
</li> </p>

<li> <a href=#students">Directions for Students</a> 
</li> </p>

<li> <a href=#students">Directions for Instructors</a> 
</li> </p>

</UL>

<h3>
<a name="install">Installing the package (instructors and students)</a>
</h3>

Getting up and running is simple. Just download the <b>.zip</b> file.
Unzipping it will produce a directory <b>omsi-master</b>, where all
relevant files reside.

<h3>
<a name="students">Directions for Students</a>
</h3>

<b><i>Connecting to the server:</i></b>

Download the package, though you will only use the file
<b>OmsiGui.py</b>.  Run

<pre>
python OmsiGui.py
</pre>

from a terminal window.

Then connect to the server and get the exam questions by selecting 
<b>File | Connect</b>. 

Provide your student email address and the host and port provided by the
instructor.

<b>NOTE:</b> There should be two separate windows on the right of the GUI, one
for the question and one to write the answer. The boxes are resizable
and the question box may default to occupying the entire right side of the
screen on some systems. If this is the case grab the bottom of the box
to resize.

<b><i>Saving answers:</i></b>

Click the question number on the left of the OMSI screen, and
select <b>File | Save</b>.`

<b><i>Running code:</i></b>

Save the code first, then select <b>File | Run</b>.`A new window will
pop up, displaying the results.

<b><i>Submitting answers:</i></b>

Submit the answer to a particular question by clicking on the question
number on the left side of the OMSI screen, and selecting <b>File |
Submit</b>. You can also submit all answers with <b>File | Submit
All</b>. A dialog box specifying whether submission was successful will
then be displayed. 

<h3>
<a name="students">Directions for Instructors</a>
</h3>

On the server side, a directory will be created for each student, using
the email address provided by the student, under <b>ProfessorHomeDirectory</b>.
In the directory there will be an answer file for each question. e.g.
<b>omsi_answer1.txt</b> or <b>omsi_answer2.java</b>

<b><i>Preparing the exam questions (instructor)</i></b>

Within the directory <b>omsi-master</b>, there will be a directory
<b>ProfessorHomeDirectory</b>. You place your exam questions in that
directory (sample files are included there).  The format for specifying
the questions is detailed below. 

<b><i>Starting the server (instructor)</i></b>

At the start of the exam period (not before), start the server from a
shell/command line window by issuing the command

<b>python OmsiServer.py [portNumber] [quoted exam name] </b>

from within the <b>omsi-master</b> directory, e.g.

<b>python OmsiServer.py 5000 'Fall 2014 Midterm 1'</b>

The port number must be above 1024.

The address needed for students to connect to the server will then be
printed to the terminal in the format <b>host:port</b> e.g.
<b>pc16.cs.ucdavis.edu:5000</b>. This info will need to be distributed
to the students at the start of the exam. 

<b><i>What happens after the exam? How to autograding work?</i></b>

The autograding program is semi-autograded. It goes through the students' file answers.txt in their individual directory with the name of
their emailname (e.g. jsmith@ucdavis.edu -> jsmith) to parse students' answer and a master answer file with the name Answerx, where x is
the test ID. It then displays both sets of answers to the professor. If there are any formatting errors, the program will alert the
professor. The professor needs to manually fix the files and decides how many points to award and applies any
late penalties if deemed necessary. All results are then stored in an output file.


<h2>Providing the exam questions</h2>

  The exam questions should be placed in a file called Questions.txt in the ProfessorsHomeDirectory. The file should contain a description and any questions for the exam. If there are notes the instructor would like to write to himself in the file they should be placed at the beginning. When parsing the file the parser will go through line by line and search for keywords DESCRIPTION or QUESTION. Once a keyword is found each line after it is appended together until it reaches another keyword or the end of the file. So content that is not intended to be a part of a question or description should not be below a keyword. Questions are numbered in the order they are discovered.
  
  <b><i>Specifying different file types</i></b>
  
By default all answers are saved as a .txt file. If a different filetype is desired then the -ext flag may be specified when adding the QUESTION keyword. i.e 'QUESTION -ext .py'
    
  <b><i>Specifying compile and run options</i></b>
  
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
