
<b>What is OMSI?</b>

OMSI, short for Online Measurement of Student Insight, is a Python project made for conducting and grading examinations in a manner that is
both secure and conducive to high-quality measurement of student insight. It is suitable for small or large class quizz, test or exam:
be it essay, programming, math or multiple choice question.

<b>How to use this project package?</b>

<i>Step 1a: Coding a script</i>

To use this project package to code a script that is supposed to be triggered by a certain command from the client, use Server.py.
Server.py is the main method on the professor's machine. It will be running for the entire duration of the exam. Server.py accpets request
from clients, allowing students to dump files and start the grading system.

<i>(Or) Step 1b: Coding a class/module</i>

To use this project package to code a class/module that is suppsed to be run upon a client request, write code in yout class and link it
to Server.py via an import. Add
import MyClassName
to the top of Server.py, do not put your functions or any code into Server.py.

<i>Calling your function from client's machine</i>

Add the function to the function dictionary in Server.py (function dictionary is a list of all function objects that is mapped to be a
string representative for the function, usually the function name). Find the variable
gFunctionDictionary = { ... a bunch of functions ...}
and add your function to the table above as follow:
"nameOfMyFunctionUNIQUE": MyClassWhichIImported.nameOfMyFunction
Note that yout function should not accept any parameters, as the actual function will be called without passing in any parameters.
Please also note that it is important that the first string "NameOfMyFunctionUNIQUE" is indeed unique. It is ideal to keep the function
name as close to the actual name of the function as possible, but still different from the other functions in the table.

<i>Step 2: Running Server.py</i>

Run Server.py to set up a server to listen to the Clients. Do not run any client script before running Server.py. After checking that both
the import and the functions are added to the function table, call your function
Client.callFunctionOnServer("nameOfMyFunctionUNIQUE")

<i>Step 3: Confirguing Client.py</i>

Write code in your class and module, do not modify Client unless you clearly now what you are doing. Import ServerInteractor in the class/
module that requires the server interaction like the following:
import Client
As of right now, you have two functions available: Client.setUpServer(pPort, pHost) and Client.callFunctionOnServer(functionName). Call
Client.setUpServer(pPort, pHost) by passing in the port and IP address provided by the professor to pPort and pHost respectively. If you
are just doing a test run, simply call the function by Client.setUpServer(0, 0).

<i>Step 4: Linking Server.py to Client.py</i>

Make sure the function you are trying to execute exists on the server side and is ready to be called by the client. If everything is
properly set up, call
Client.callFunctionOnServer("myFunctionName")
The return value of the function is either True or False, depending on whether the execution of the function on the server is successful
or not.
If unfortunately the return value is False, please which whether the server is set up properly. If it is, the issue might be more
complicated, which you are free to contact Francios to fix the problem.

<i>Step 5: Running Client.py</i>

Execute the Client script, but do not execute Client, for it is not supposed to be executed by itself.

<b>What does the program do when executing Server.py and Client.py?</b>

After everything is properly connected, students will connect to their server on their machines start by typing in their email addresses.
When sussecssful, the server will calculate and display the number of current connections and total connections to the professor, so that
it is detectable how many students are taking the exam, and is detectable when students face connection problem. Server.py then creates
directories for each individual student under the professor's home directory,if the student individual directory does not exist. Server.py
then uses the directory to store students' answer file. The program will then send the test questions to the students. Once the students
receive their test questions, the internal clock will start to count down the time remaining for the students to do the test. Once the time
is up, the program will automatically save the students' answer. During the time from students' first connection to the server till the end
of the test, their activities on their laptops are being monitored by an external program PyShark, the data is stored in the file specially
created for inidivual students along with their test answers.

<b>What happen after the test end? How does to autograding work?</b>

The autograding program is semi-autograded. It goes through the students' file answers.txt in their individual directory with the name of
their emailname (e.g. jsmith@ucdavis.edu -> jsmith) to parse students' answer and a master answer file with the name Answerx, where x is
the test ID. It then displays both sets of answers to the professor. If there are any formatting errors, the program will alert the
professor. The professor needs to manually fix the files and decides how many points to award and applies any
late penalties if deemed necessary. All results are then stored in an output file.


<b>Providing the exam questions</b>
  The exam questions should be placed in a file called Questions.txt in the ProfessorsHomeDirectory. The file should contain a description and any questions for the exam. If there are notes the instructor would like to write to himself in the file they should be placed at the beginning. When parsing the file the parser will go through line by line and search for keywords DESCRIPTION or QUESTION. Once a keyword is found each line after it is appended together until it reaches another keyword or the end of the file. So content that is not intended to be a part of a question or description should not be below a keyword. Questions are numbered in the order they are discovered.
  
  <i>Specifying different file types</i>
    By default all answers are saved as a .txt file. If a different filetype is desired then the -ext flag may be specified when 
    adding the QUESTION keyword. i.e 'QUESTION -ext .py'
    
  
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
