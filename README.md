
# OMSI: Online Measurement of Student Insight 

## Developed by:

<blockquote>

Kiran Bhadury,
Vishal Chakraborty,
Francois Demoullin,
Thong Le,
Norm Matloff,
Monte Musa,
Rylan Schaeffer,
Tiffany Yuen

</blockquote>

## Maintained by:

<a href="http://heather.cs.ucdavis.edu/matloff.html">
Norm Matloff 
 </a> 

## Table of contents:

<UL>

<li> 
<a href="#what">What is OMSI?</a> 
</li> </p> 

<li> 
<a href="#benstudent">Benefits for students</a> 
</li> </p> 

<li> 
<a href="#benteacher">Benefits for instructors</a> 
</li> </p> 

<li> 
<a href="#howuse">How to use this package</a> 
</li> </p> 

</UL>


<h2>
<a name="what"> What is OMSI?</a> 
</h2>

OMSI, short for Online Measurement of Student Insight, is a software
tool for conducting and grading examinations in a manner that is both
secure and conducive to high-quality measurement of student insight. It
is suitable for small or large class exams, be they based on
essays, writing code, math analysis or multiple choice questions.

Students come to the classroom at the regular class time, just as with a
traditional pencil-and-paper exam.  However, they use their laptops to
take the exam, using OMSI.  The latter downloads the exam questions, and
enables the students to upload their answers.

As detailed below, this arrangement has significant benefits for both
students and instructors.  The system is easy to install and use.

Here is a screenshot of an example screen from the student's point of
view:

![alt text](Screenshot.png)  

<h2>
<a name="benteacher"> 
Benefits for instructors
</a> 
</h2>

OMSI facilitates exam administration and grading.  It 
has two components:

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

<h2>
<a name="benstudent"> 
Benefits for students
</a> 
</h2>

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
<a name="howuse"> 
How to use this package
</a> 
</h2>

Contents:

<UL>

<li> <a href="#term">Terminology</a> 
</li> </p>

<li> <a href="#install">Installation (instructors and students)</a> 
</li> </p>

<li> <a href="#students">Directions for students</a> 
</li> </p>

<li> <a href="#instructors">Directions for instructors</a> 
</li> </p>

</UL>

<h3>
<a name="term">Terminology</a>
</h3>

The term *directory* from Linux is synonymous with *folder* for Mac and
Windows.

The term *terminal window* from Mac and Linux is synonymous with *Comand
Prompt* for  Windows (**cmd**).

<h3>
<a name="install">Installing the package (instructors and students)</a>
</h3>

You will need Python installed on your machine. For Mac and Linux
systems, it should already be there, but it is easily downloadable for
Windows.

You must have Python in your executable search path.  To check this,
open a terminal window and type

```
Python
```

into a terminal window.  Python should start.

To install OMSI, download the <b>.zip</b> file.
Unzipping it will produce a directory/folder <b>omsi-master</b>, where all
relevant files reside.

<h3>
<a name="students">Directions for students</a>
</h3>

<b><i>Connecting to the server:</i></b>

Download and install the package as above, though you will only use the file
<b>OmsiGui.py</b>.  Run

<pre>
python OmsiGui.py
</pre>

from a terminal window.

Then connect to the server and get the exam questions by selecting 
<b>File | Connect</b>. 
State your student e-mail address and the host and port provided by the
instructor.

After you connect to the server, the exam questions will be downloaded
to your machine.

<b>NOTE:</b> There should be two separate windows on the right of the
GUI, one on top for the question prompt and one below to write the
answer. The boxes are resizable and the question box may default to
occupying the entire right side of the screen on some systems. If this
is the case grab and drag the bottom of the box to resize the bottom
window.

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

<h2>
<a name="instructors">Directions for instructors</a>
</h2>

<h3>
InstructorDirectory
</h3>

Within the directory <b>omsi-master</b>, there will be a directory
<b>InstructorDirectory</b>. You place your exam questions in that
directory (sample files are included there).  The format for specifying
the questions is detailed below. 

Within this directory, a subdirectory will be created for each student,
using the e-mail address provided by the student.  In a student's 
subdirectory there will be an answer file for each question. e.g. 
 <b>omsi_answer1.txt</b> or <b>omsi_answer2.java</b>

<h3>
Starting the server
</h3>

At the start of the exam period (not before), start the server from a
shell/command line window by issuing the command

<b>python OmsiServer.py [portNumber] [quoted exam name] </b>

from within the <b>omsi-master</b> directory, e.g.

<b>python OmsiServer.py 5000 'Fall 2014 Midterm 1'</b>

The port number must be above 1024.

The server Internet address and port number will need to be distributed
to the students at the start of the exam. 

<h3>
Closing the server
</h3>

At present, this is simply done via ctrl-C.

<h3>Providing the exam questions</h3>

The exam questions should be placed in a file called **Questions.txt** in
the <strong>InstructorDirectory</strong>. The file should contain a
description and the questions for the exam. If there are notes the
instructor would like to write to him/herself in the file they should be
placed at the beginning.  

When parsing the file, OMSI will go through line by line and search for
keywords NEW, DESCRIPTION or QUESTION.  The latter delineates the start
of a question for the exam, so that for a 3-problem exam there would be
3 QUESTION lines in the file  **Questions.txt**.

The lines following a keyword all are associated with that keyword,
until another keyword is encountered. 

Once a keyword is found each line
after it is appended together until it reaches another keyword or the
end of the file. So content that is not intended to be a part of a
question or description should not be below a keyword. Questions are
numbered in the order they are discovered.

  <b><i>Specifying different file types</i></b>
  
By default all answers are saved as a .txt file. If a different filetype
is desired then the -ext flag may be specified when adding the QUESTION
keyword. i.e 'QUESTION -ext .py'
    
  <b><i>Specifying compile and run options</i></b>
  
The compile and run functionalities are by default disabled. If any
question requires compile and run then the -com and -run flags may be
specified in a simillar manner as the -ext file while adding the
QUESTION keyword, e.g. 'QUESTION -com gcc -flags "-Wall -g" -run
.\a.out', 'QUESTION -com python -run "python omsi_answer1.py" '

<h2>
Summary of each file on this site (in alphabetical order)
</h2> 

AutoGrade.py
A program to grade the students' answer electronically and automatically (translated from Prof. N. Matloff's AutoGrade.R, included in this site).

Checksum.py
A program to convert content of students' answer to hexadecimal for grading.

Client.py
Main function Client side. This function connect to the server, it allows students to cache username and e-mail for easy submission of files to the server.

ClientGlobals.py
Global variables client side.

ClientRoutines.py
A set of routines relevant to the client. The routines include file transfer from Client to Server, file transfer from Server to Client,
a "log in"/authentication system requiring students to input their e-mail addresses for authentication.

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
