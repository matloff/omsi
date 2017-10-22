

# OMSI: Online Measurement of Student Insight 

## Original development by:

<blockquote>

[Kiran Bhadury](mailto:kbhadury@ucdavis.edu),
[Vishal Chakraborty](mailto:vch@ucdavis.edu),
[Francois Demoullin](mailto:f.demoullin@gmail.com),
[Norm Matloff](mailto:matloff@cs.ucdavis.edu),
[Monte Misa](mailto:montemisa@gmail.com), 
[Rylan Schaeffer](mailto:ryschaeffer@ucdavis.edu),
[Tiffany Ching L Yuen](mailto:tyuen@ucdavis.edu)

</blockquote>

## Later contributors::

<blockquote>

[Sachin Kumawat](mailto:skumawat@ucdavis.edu),  
[Thong Le](mailto:thmle@ucdavis.edu), 
[Darya Semyonova](mailto:dsemyonova@ucdavis.edu)

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

<li> 
<a href="#grading">Software tools for grading</a> 
</li> </p> 

<li> 
<a href="#future">Future enhancements</a> 
</li> </p> 

</UL>


<h2>
<a name="what"> What is OMSI?</a> 
</h2>

OMSI, short for Online Measurement of Student Insight, is a software
tool for conducting and grading examinations in a manner that is both
secure and conducive to high-quality measurement of student insight. It
is suitable for small or large class exams, be they based on
**essays, writing code, math analysis or multiple choice questions**.

Students come to the classroom at the regular class time, just as with a
traditional pencil-and-paper exam.  However, they use their laptop
computers to take the exam, using OMSI.  The latter downloads the exam
questions, and enables the students to upload their answers.  

Moreover, in the case of questions which require writing code, **OMSI
enables the students to compile and run their code, thus giving them an
opportunity to discover and fix errors**.

As detailed below, this arrangement has significant benefits for both
students and instructors.  The system is easy to install and use, and
can be run on Macs, Windows and Linux.

Here is a screenshot of an example screen from the student's point of
view:

![alt text](Screenshot.png)  

<h2>
<a name="benstudent"> 
Benefits for students
</a> 
</h2>

Dear students:

__OMSI will often result in your getting a higher grade in an exam than
you would have in the traditional pencil-and-paper format:__

<UL>

<li> With essay questions, you have a chance to edit your answers,
producing more coherent, readable prose.  No cross-outs, arrows, words
squeezed in above a line, no points off for unreadable handwriting. :-)
</li> </p>

<li> With coding questions, you can compile and run your code,
giving you a chance to make corrections if your code doesn't work.
</li> </p> 

</UL>

In both of these aspects, OMSI gives you a better opportunity to
demonstrate your insight into the course material, compared to the
traditional exam format.

<h2>
<a name="benteacher"> 
Benefits for instructors
</a> 
</h2>

Dear instructors:

<b>
OMSI will make your life easier. :-) 
</b>

OMSI facilitates exam administration and grading.  It 
has two components:

<UL>

<li> <i>Exam administration.</i>  This manages the actual process of the
students taking the exam.  You get electronic copies of the students'
exams, eliminating the need for collecting and carrying out out a large
number of papers, and making work sharing much easier among multiple 
graders.  As noted in "Benefits for students" above, **OMSI enables the
student to turn in a better product, and this benefits the instructor as
well:  Better exam performance by students is both more gratifying to
the instructor and also makes for easier, less frustrating grading**.
</li> </p>

<li> <i>Exam grading.</i> OMSI does NOT take the place of instructor
judgment in assigning points to exam problems. 
But it does make things much easier, by automating
much of the drudgery. For instance, OMSI automatically records grades
assigned by the instructor, and automatically notifies students of their
grades via e-mail.  Gone are the days in which the instructor must
alphabetize the papers, enter the grades by hand, carry an armload (or
boxload) of papers to give back to students in class, retaining the
stragglers not picked up by the students, and so on.

</UL>


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

The Linux term *directory* is synonymous with *folder* for Mac and
Windows.

The term *terminal window* from Mac and Linux is synonymous with *Command
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
python
```

into a terminal window.  Python should start, displaying the >>> prompt.
(Exit via ctrl-d.)

To install OMSI, download the <b>.zip</b> file.
Unzipping it will produce a directory/folder <b>omsi-master</b>, where all
relevant files reside.

<h3>
<a name="students">Directions for students</a>
</h3>

<b><i>Connect to the server, at the start of the exam:</i></b>

Download and install the package as above. Then open a terminal window,
change to the __omni-master__ directory, and run

```
python OmsiGui.py
```


Then connect to the server and get the exam questions by selecting
<b>File | Connect</b>.  State the host and port provided by the
instructor, and   your student e-mail address.  (You can also type them
as command-line arguments in running **OmsiGui**.)

After you connect to the server, the exam questions will be downloaded
to your machine.

<b>NOTE:</b> There should be two separate windows on the right of the
GUI, one on top for the question prompt and one below to write the
answer. The boxes are resizable and the question box may default to
occupying the entire right side of the screen on some systems. If this
is the case grab and drag the bottom of the box to resize the bottom
window.

<b><i>Copy-and-paste:</i></b>

In programming classes, the instructor may wish to place a template,
i.e. an outline of the answer, in the question, with students filling in
the gaps in the code.  Copy-and-paste operations using a mouse may
depend on the type of machine used.  Instead, OMSI offers a **CopyQtoA**
selection in the menu, which completely copies the contents of the
question box to the answer box.  Students then edit.

<b><i>Saving answers:</i></b>

Click the question number on the left of the OMSI screen, and
select <b>File | Save</b>.` Note that **saving is NOT submitting.**
Saving your file does NOT upload your answer to the instructor's server;
the save operation merely saves to a file on your local machine.
See "Submitting your answers" below for uploading to the instructor.

<b><i>Compiling/running code:</i></b>

Save the code first.  Then, if the problem involves a compiled language
such as C, select <b>File | Compile</b>. A new window will pop up,
displaying the results.  Then select <b>File | Run</b> (or for an
interpreted language like R or Python, go to this step directly). A new
window will pop up, displaying the results.

<b><i>Submitting answers:</i></b>

Submit the answer to a particular question by clicking on the question
number on the left side of the OMSI screen, and selecting <b>File |
Submit</b>. This will upload your answer to the instructor.  You can
also submit all answers with <b>File | Submit All</b>. A dialog box
specifying whether submission was successful will then be displayed. 

**IMPORTANT NOTE:**  If the network is busy, there may be a delay, of
say, 10 or 15 seconds, before the submit operation completes and the
dialog box comes up.

<b><i>Tips:</i></b>

**Be sure to try OMSI in an actual session before your first OMSI-based
exam.**  Start up the server, playing the role of the instructor (see
"Directions for instructors" below), and then start the client, playing
the role of the student as above.

Make sure your laptop is fully charged before the exam.  

Again, remember that saving an answer does NOT submit it.  You must do
that separately.

When you begin the exam, your very first action should be to click on
**Description**.  The instructor may have directions there that will make a
night-and-day difference to your grade!  So first take a few seconds to
read this.

If your exam tests you on Python or R, remember that they won't be
running in interactive mode here, so you must write explicit **print**
operations.  Graphical displays will not work, for the same reason.

Keep in mind that you should get confirmation of these operations.  When
you submit an answer, for instance, the Success! window then pops up to
confirm receipt, though as mentioned, this may not occur instantly.

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

During the exam, a subdirectory of __InstructorDirectory__ will be
created for each student, using the e-mail address provided by the
student.  In a student's subdirectory there will be an answer file for
each question. e.g.  <b>omsi_answer1.txt</b> or <b>omsi_answer2.java</b>

<h3>
Starting the server
</h3>

At the start of the exam period (not before), start the server from a
terminal window by issuing the command

<b>python OmsiServer.py [portNumber] [quoted exam name] </b>

from within the <b>omsi-master</b> directory, e.g.

<b>python OmsiServer.py 5000 'Fall 2019 Midterm 1'</b>

The port number must be above 1024.

The server Internet address and port number will need to be distributed
to the students at the start of the exam. 

<h3>
Closing the server
</h3>

At present, this is simply done via ctrl-C.

<h3>Providing the exam questions</h3>

Before the exam, the exam questions must be placed in a file called
**Questions.txt** in the <strong>InstructorDirectory</strong>. The file
should contain a description and the questions for the exam. If there
are notes the instructor would like to write to him/herself in the file
they can be placed at the beginning, in the section labeled **NEW**.  

When parsing the file, OMSI will go through line by line and search for
keywords **NEW**, **DESCRIPTION** or **QUESTION**.  The roles are as follows:

  * **NEW**:  Optional. The lines that follow will  contain private 
  notes for the instructor.  
  * **DESCRIPTION**:  Required. The lines that follow will contain instructions 
    to students, which would normally go on the front page of a 
    printed exam, say "You will have 50 minutes for this exam."
 .  The students will be able to view it by clicking Description in the menu.  
  * **QUESTION**:  Have one of these lines for each exam problem.  For 
  problems involving code, directions for compiling or running the 
  code go on this same line.  The lines that follow this line contain 
  the question, to be viewed by the students.

Example **Questions.txt** file:

```
DESCRIPTION

You will have 50 minutes for this exam.

QUESTION -ext .py -run "python omsi_answer1.py"

Write a function half() that will return x/2, and 
freestanding code will print half(3).

QUESTION 

What does 'D' stand for in "UCD"?

```

In this example, two exam questions are defined, one requiring Python
code and one requiring an essay.  When a student writes and submits the
answers, they will be saved in files **omsi_answer1.py** and
**omsi_answer2.txt** in <strong>InstructorDirectory</strong>, in that
student's subdirectory (indexed by e-mail address).  

The suffix in that first file name arises from the specification **-ext
.py** in the QUESTION line; otherwise the default suffix is **.txt**,

<b><i>Specifying compile and run options</i></b>
 
There are various **QUESTION** line options for the case of compiled
code, e.g.

```
QUESTION -ext .c -com gcc -flags "-Wall -g" -run ./omsi_answer1
```

for Question 1.

Here is one for R, for a Question 3:

```
QUESTION -ext .R -run 'Rscript ./omsi_answer3.R'
```
Note that fields with embedded spaces must be quoted.



<b><i>Tips:</i></b>

OMSI should greatly improve the examination process for both instructors
and students.  However, as with any automated system, some care is
needed to insure that things run smoothly.

It's hard for a student to write full code within an exam period.  What
I like to do is give the students partial code, and have them fill in
the missing lines.  Clicking the **CopyQtoA** button will copy the contents
of the question window to the answer window, so students need not type
in the provided partial code.

It is crucial that the instructor, before the first OMSI-based exam,
require the students to go through a dry run.  The instructor may wish
to incentivize this.  Note that the server will record the logins by the
students, so the instructor can nudge the laggards who haven't gone
through the dry run.

"Stuff happens."  What if, say, there is a sudden power failure or the
local WiFi access point suddenly goes out?  What if some students do not
go through the dry run, even with major incentives/disincentives, and
have trouble using OMSI in the first exam?  The following are worth
considering:

  * Paper copies of the exam prompt should be distributed at the start
    of the exam, and students should have the option of turning in their
    answers on paper.  Some students may not even have laptops.  (See
    note on tablets below.)

  * Students should be told to click the **Submit** option "early and
    often."  (Each submission would overwrite the last.)  This is
    especially important if there is concern that the local WiFi access
    point might be flooded with traffic at the end of the exam period,
    as many students turn in last-minute work.

  * Students should bring a USB key (thumb drive, memory stick).  In an
    emergency, they can copy their local copies of their **omsi_answer***
    files to the key, then turn in the key.

And what about cheating and other forms of academic dishonesty?  In my
experience, the vast majority of students are honest, and they resent
the cheaters.  What can be done about the latter?

  * The OMSI window is designed to fill the student's entire screen.
    This prevents a student from communicating with others during the
    exam.  The students must be given strict instructions not to move,
    iconify or resize OMSI window during the exam.  This is easily
    monitored by proctors.

  * As usual, there is the problem of a student looking at his/her
    neighbor's work, in this case a laptop screen rather than a piece of
    paper.  A common technique for dealing with this in the paper exam
    case is to require students to sit in specific seats that are
    randomly assigned to them.  This can be done with OMSI as well.

  * If you are on a Unix system (Mac or Linux), you may find it useful
    to run the server within the **script** command, so as to have a
    record of connections and their times.

<h2>
<a name="grading">Software tools for grading</a> 
</h2>

The answers submitted by the students and collected by the server may be
graded by hand as usual.  However, tools to facilitate electronic
grading are available in this package.  As noted earlier in this
document:

<blockquote>

OMSI does NOT take the place of instructor judgment in assigning points
to individual exam problems.  But it does make things much easier, by
automating much of the drudgery. For instance, OMSI automatically
records grades assigned by the instructor, and automatically notifies
students of their grades via e-mail.  Gone are the days in which the
instructor must alphabetize the papers, enter the grades by hand, carry
an armload (or boxload) of papers to give back to students in class,
retaining the stragglers not picked up by the students, and so on.

</blockquote>

The basic idea is that the software will display on the screen, for each
student and each exam problem, the student's answer.  In the case of
coding questions, the software will also run the code and display the
result.  In each case, the instructor then inputs the number of points
he/she wishes to assign:

```
for each student:
   for each exam problem:
      if problem involves coding:
         compile and/or run code according to the
            QUESTION line of Questions.txt, displaying result
      display student answer
      instructor inputs number of points 
   record grade for this student (individual problems and total)
```

The main tool is **Grading/AutoGradeOMSI.R**.  This code is in R, as it
is an adaptation from an earlier system I (NM) had developed; also, its
statistical and graphic capabilities facilitate analysis of the exam
grades.  (There is also a file **AutoGrade.py** in that directory, but
it is under development.)

Detailed directions are given in the comments at the top of the file.

<h2>
<a name="future">Future enhancements</a> 
</h2>

Much improvement is possible.  **Contributors of new code are welcome!**

Here are some points of improvement:

  * Tablet-friendly version of OMSI.

  * Code to check a student's e-mail address against a class list upon
    connection, with passwords being required.  
  
  * Code to confirm the integrity of the OMSI client code
    (i.e. verify that the source code hasn't been changed), and to
    upload each student Run operation to the server, to guard against
    the student running surreptitious communication code.

